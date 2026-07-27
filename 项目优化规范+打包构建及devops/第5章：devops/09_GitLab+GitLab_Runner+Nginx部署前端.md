# GitLab + GitLab Runner + Nginx 同一台服务器部署前端（无 Docker）

---

## 架构总览

```
┌──────────── 服务器 124.221.166.48 ────--────────┐
│                                                 │
│  ┌──────────┐  ┌───────────────┐               │
│  │  GitLab  │  │ GitLab Runner │               │
│  │  :80     │  │ (shell exec)  │               │
│  └──────────┘  └───────┬───────┘               │
│                        │                        │
│                        │ CI Job：cp dist/* → /srv/frontend
│                        ▼                        │
│              ┌──────────────────────┐          │
│              │  /srv/frontend       │          │
│              │  (前端静态文件)       │          │
│              └──────────┬───────────┘          │
│                         │                       │
│                    ┌────▼────┐                  │
│                    │  Nginx  │                  │
│                    │  :8080  │ ← 用户访问入口    │
│                    └─────────┘                  │
└────────────────────────────────────────────────┘
```

**核心思路**：GitLab Runner 使用 **Shell Executor**，CI Job 直接在宿主机执行脚本，构建产物写入 `/srv/frontend`，Nginx 读取同一目录。无需任何 Docker 容器或卷挂载。

---

## 端口规划

| 服务 | 端口 | 说明 |
|------|------|------|
| GitLab Web | 80 | GitLab 管理界面 + Git HTTP 推送 |
| GitLab SSH | 22（或自定义） | Git SSH 推送 |
| Nginx（前端） | 8080 | 用户访问前端页面 |

> 如果 80 端口被占用，GitLab 可以用其他端口如 8081。

---

## 步骤一：安装 GitLab CE

> 操作系统：Ubuntu 20.04+ / CentOS 7+ / Debian 11+

### Ubuntu / Debian

```bash
# 1. 安装依赖
sudo apt update
sudo apt install -y curl openssh-server ca-certificates tzdata perl

# 2. 添加 GitLab 仓库
curl -fsSL https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash

# 3. 安装 GitLab CE
sudo EXTERNAL_URL="http://124.221.166.48" apt install -y gitlab-ce
```

### CentOS / Rocky Linux

```bash
# 1. 安装依赖
sudo yum install -y curl openssh-server ca-certificates tzdata perl policycoreutils-python-utils

# 2. 添加 GitLab 仓库
curl -fsSL https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh | sudo bash

# 3. 安装 GitLab CE
sudo EXTERNAL_URL="http://124.221.166.48" yum install -y gitlab-ce
```

> **注意**：首次安装需要 5-10 分钟。`EXTERNAL_URL` 替换为你的服务器 IP 或域名。
> GitLab 默认监听 80 端口，如果 80 被占用，修改 `/etc/gitlab/gitlab.rb` 中的 `external_url` 并 `sudo gitlab-ctl reconfigure`。

### 获取 root 密码

```bash
# GitLab 15.x+ 密码在以下文件中（24小时内有效）
sudo cat /etc/gitlab/initial_root_password
```

### 常用管理命令

```bash
sudo gitlab-ctl status           # 查看服务状态
sudo gitlab-ctl reconfigure      # 重新配置
sudo gitlab-ctl restart          # 重启
sudo gitlab-ctl tail             # 查看日志
```

---

## 步骤二：安装 Node.js

Runner 使用 Shell Executor，需要在服务器上预装 Node.js 用于前端构建。

```bash
# 方法一：使用 NodeSource 官方仓库安装 LTS 版本
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# 方法二：使用 nvm（推荐，便于多版本管理）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20
nvm alias default 20

# 验证安装
node -v   # 应输出 v20.x.x
npm -v    # 应输出 10.x.x
```

---

## 步骤三：安装 GitLab Runner

```bash
# Ubuntu / Debian
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt install -y gitlab-runner

# CentOS / Rocky
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.rpm.sh" | sudo bash
sudo yum install -y gitlab-runner
```

### 注册 Runner（使用 Shell Executor）

```bash
sudo gitlab-runner register
```

交互式填写：

| 提示 | 输入值 |
|------|--------|
| GitLab instance URL | `http://124.221.166.48` |
| Registration token | 从 GitLab 项目 Settings → CI/CD → Runners 获取 |
| Description | `shell-runner` |
| Tags | `shell,linux` |
| Executor | **`shell`** ← 关键：选 shell，不要选 docker |
| Maintenance note | 留空回车 |

### 验证注册结果

```bash
# 查看 Runner 配置
sudo cat /etc/gitlab-runner/config.toml
```

确认内容类似：

```toml
concurrent = 2
check_interval = 0

[[runners]]
  name = "shell-runner"
  url = "http://124.221.166.48"
  token = "xxx..."
  executor = "shell"
  shell = "bash"
```

### 给 gitlab-runner 用户授权

Runner 以 `gitlab-runner` 用户身份执行 CI Job，需要给它写入部署目录和安装 npm 包的权限。

```bash
# 创建部署目录
cd /usr/share/nginx/html/
# srv/frontend
sudo mkdir everyday_doc

# 将 gitlab-runner 用户加入当前用户组（方便共享权限）
sudo usermod -aG $(whoami) gitlab-runner

# 设置目录权限
sudo chown -R gitlab-runner:gitlab-runner /srv/frontend
sudo chmod -R 755 /srv/frontend

# 确保 gitlab-runner 可以使用 node 和 npm
# （如果用的 nvm，需要把 nvm 路径加到 gitlab-runner 的环境变量）
sudo chown -R gitlab-runner:gitlab-runner /home/gitlab-runner
```

> **nvm 用户特别注意**：gitlab-runner 运行时不会自动加载 `.bashrc`。可在 CI 脚本中手动 source nvm，或直接用 apt 安装的 Node.js。

---

## 步骤四：安装并配置 Nginx

```bash
# Ubuntu / Debian
sudo apt install -y nginx

# CentOS / Rocky
sudo yum install -y nginx
```

### 创建 Nginx 站点配置

```bash
sudo nano /etc/nginx/conf.d/frontend.conf
```

粘贴以下内容：

```nginx
server {
    listen 8080;                         # 前端访问端口（避免与 GitLab 的 80 冲突）
    server_name 124.221.166.48;          # 改为你的域名或 IP

    root /srv/frontend;
    index index.html;

    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript
               text/xml application/xml application/xml+rss text/javascript image/svg+xml;

    # SPA 路由回退（Vue Router / React Router 需要）
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 静态资源强缓存
    location /assets {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    access_log /var/log/nginx/frontend_access.log;
    error_log  /var/log/nginx/frontend_error.log;
}
```

### 启动 Nginx

```bash
# 测试配置
sudo nginx -t

# 启动
sudo systemctl start nginx
sudo systemctl enable nginx   # 开机自启

# 验证
sudo systemctl status nginx
```

### 创建测试页面验证

```bash
echo "<h1>部署成功！Nginx 正常运行</h1>" | sudo tee /srv/frontend/index.html
# 浏览器访问 http://124.221.166.48:8080
```

---

## 步骤五：在 GitLab 创建项目并推送代码

### 5.1 登录 GitLab

浏览器打开 **http://124.221.166.48**

- 用户名：`root`
- 密码：步骤一获取的初始密码

### 5.2 创建项目

1. **Create a project** → **Create blank project**
2. Project name：`my-frontend`
3. Visibility Level：Private
4. 点击 **Create project**

### 5.3 推送前端代码

```bash
# 在本地前端项目目录中
cd my-frontend-project

# 初始化 Git
git init
git remote add origin http://124.221.166.48/root/my-frontend.git

# 将 gitlab-ci.yml 放入项目中
cp /path/to/gitlab-ci.yml .gitlab-ci.yml

# 提交并推送
git add .
git commit -m "init: frontend project with CI/CD"
git push -u origin main
```

### 5.4 确认 Runner 在线

GitLab 项目 → **Settings** → **CI/CD** → **Runners**，应看到绿色圆点的 `shell-runner`。

---

## 步骤六：触发 CI/CD 流水线

推送代码后，GitLab 自动触发 Pipeline：

```
install → lint → test → build → deploy-prod
```

- `install`、`lint`、`test`、`build` 自动执行
- `deploy-prod` 需手动点击 ▶ 触发（已设置 `when: manual`）

部署完成后访问 **http://124.221.166.48:8080** 查看前端页面。

---

## 步骤七：日常开发流程

```bash
# 1. 修改代码
# 2. 提交推送
git add .
git commit -m "feat: 新增功能"
git push origin main

# 3. 去 GitLab → CI/CD → Pipelines 查看进度
# 4. Pipeline 跑完 install → lint → test → build 后
#    手动点击 deploy-prod 部署
# 5. 访问 http://124.221.166.48:8080 验证
```

### 自动部署（跳过手动确认）

编辑 `.gitlab-ci.yml`，删除 `deploy-prod` 中的这行：

```yaml
  when: manual    # ← 删除这行
```

---

## 目录结构总览

```
服务器上：

/etc/gitlab/                          # GitLab 配置
/etc/gitlab-runner/
│   └── config.toml                   # Runner 配置（shell executor）
/etc/nginx/conf.d/
│   └── frontend.conf                 # 前端站点 Nginx 配置
/var/log/nginx/                       # Nginx 日志
/srv/frontend/                        # 前端部署目录（CI 写入 + Nginx 读取）
│   ├── index.html
│   ├── assets/
│   └── ...
/var/opt/gitlab/                      # GitLab 数据目录
/home/gitlab-runner/builds/           # Runner 构建工作目录

前端项目仓库中（推送到 GitLab）：

my-frontend/
├── .gitlab-ci.yml                    # CI/CD 流水线定义
├── package.json
├── src/
├── dist/                             # 构建产物（CI 中生成）
└── ...
```

---

## 常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| Runner 离线（灰色圆点） | Runner 服务未启动 | `sudo gitlab-runner status` → `sudo gitlab-runner start` |
| Pipeline 一直 pending | Tags 不匹配 | 确认 `.gitlab-ci.yml` 中 `tags` 与 Runner 注册时一致 |
| build Job 报找不到 node/npm | gitlab-runner 用户环境变量未配置 | 在 CI 脚本中手动 `export PATH=$PATH:/usr/local/bin` 或使用绝对路径 |
| deploy Job 报 Permission denied | `/srv/frontend` 权限不足 | `sudo chown -R gitlab-runner /srv/frontend` |
| 部署后访问 404 | Nginx root 路径或 SPA 路由问题 | 确认 `root /srv/frontend` 且 `try_files` 配置正确 |
| Nginx 页面不更新 | 浏览器缓存 | Ctrl+F5 强制刷新 |
| npm install 慢 | 没有国内镜像 | `npm config set registry https://registry.npmmirror.com`（在 CI 中设置） |
| GitLab 访问很慢 | 服务器内存不足 | GitLab 至少需要 4GB RAM |
| nvm 在 CI 中不生效 | shell executor 不加载 .bashrc | CI 脚本开头加 `source ~/.bashrc` 或改用 apt 安装的 Node.js |

---

## 安全建议

1. **修改 GitLab root 密码**：首次登录后立即修改
2. **配置 HTTPS**：生产环境为 Nginx 和 GitLab 配置 SSL 证书（Let's Encrypt）
3. **防火墙**：仅开放必要端口（80/443/8080），GitLab SSH 端口按需
4. **定期备份**：GitLab 数据目录 `/var/opt/gitlab/backups/`
5. **Runner 权限最小化**：gitlab-runner 用户只给必要的目录写入权限
