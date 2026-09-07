# 2026年各中大厂 DevOps/CI/CD 面试题汇总（100道）

> 来源：技术栈、面试鸭、SharpSkill、DevOps面试题库、知乎等  
> 涉及厂商：腾讯、阿里、字节跳动、美团、华为云、AWS、微软、Accenture、Deloitte 等  
> 时间范围：2025-2026 年真实面试真题

---

## 一、Docker 容器（25道）

### 基础与原理

**1. 容器和虚拟机到底有什么区别？你项目里怎么选的？各自的适用边界是什么？**

核心区分：虚拟机模拟完整硬件（Hypervisor 层），容器是进程隔离（共享宿主机内核）。需结合实际资源消耗说明，并理解各自的适用边界。

**2. Docker 镜像为什么要分层？有什么好处？**

分层实现共享与缓存，可大幅节省磁盘空间和构建时间。核心价值：增量存储、增量传输、增量构建。需用实例说明。

**3. Docker 的 Namespace 隔离机制有哪些？分别隔离什么资源？**

PID、NET、IPC、MNT、UTS、USER、Cgroup 七种 Namespace，每种隔离不同的系统资源。

**4. Docker 的 Cgroups 具体是怎么限制 CPU 和内存的？写出具体参数和原理。**

- CPU 通过时间片配额（`--cpus`、`--cpu-shares`）限制
- 内存通过 `--memory` 限制，超限触发 OOM Kill
- 注意 swap 配额问题

**5. overlay2 存储驱动的工作原理是什么？lowerdir、upperdir、merged 层的关系？**

使用 lowerdir（只读层）+ upperdir（可写层）+ merged（联合挂载）实现 Copy-on-Write 和文件系统快照。

**6. 容器里的进程 PID 是 1，和宿主机的 PID 1 有什么关系？为什么推荐 CMD 使用 exec 格式？**

- PID Namespace 隔离，互不影响
- 容器内 PID 1 是应用主进程
- exec 格式（`CMD ["app"]`）确保信号正确传递，shell 格式（`CMD app`）会包裹一层 sh，导致 PID 1 是 sh 而非应用

**7. Docker 的写时复制（Copy-on-Write）机制是什么？对性能有什么影响？**

镜像层只读，容器层用于写入。修改文件时会先从只读层复制到可写层再修改。大量写操作会影响性能，建议将写频繁的目录挂载为 Volume。

**8. 容器退出码 137、139、143 分别代表什么？怎么排查处理？**

- 137（SIGKILL）= OOM Killed，需检查内存限制与泄漏
- 139（SIGSEGV）= 段错误，应用 bug
- 143（SIGTERM）= 优雅终止信号，正常关闭

### Dockerfile 与镜像

**9. 写一个生产级的 Dockerfile，要求镜像尽量小、安全、能健康检查。**

关键要点：
- 多阶段构建（slim/alpine 镜像）
- 利用缓存顺序（先复制依赖文件再复制代码）
- 非 root 用户运行（`USER 1000`）
- 配置健康检查（`HEALTHCHECK`）
- `.dockerignore` 排除无关文件

**10. ENTRYPOINT 和 CMD 有什么区别？各自的使用场景？两者同时存在时如何生效？**

- `ENTRYPOINT`：容器启动时执行的命令，不可被 `docker run` 后参数覆盖（除非使用 `--entrypoint`）
- `CMD`：默认参数或命令，可被 `docker run` 后参数覆盖
- 同时存在时：`CMD` 作为 `ENTRYPOINT` 的默认参数
- 推荐：`ENTRYPOINT ["app"]` + `CMD ["--config", "default"]`

**11. 多阶段构建（Multi-stage Build）的原理和优势？如何减小最终镜像体积？**

- 在同一个 Dockerfile 中使用多个 `FROM` 指令
- 第一阶段编译，第二阶段只复制编译产物
- 最终镜像不包含编译工具链和中间文件
- 可配合 `--target` 参数构建特定阶段

**12. Docker 构建缓存机制是什么？如何优化 Dockerfile 的构建速度？为什么先 COPY 依赖文件再 COPY 源码？**

- Docker 按层缓存，指令未变则复用缓存
- 将不变层放前面（如 `COPY package.json`），频繁变动的放后面（如 `COPY .`）
- 先复制依赖文件可避免每次代码改动都重装依赖

**13. 如何给 Docker 镜像瘦身？除了 alpine/slim 镜像外还有哪些技巧？**

- 多阶段构建
- 使用 `.dockerignore`
- 清理包管理器缓存（`apt-get clean`、`rm -rf /var/lib/apt/lists/*`）
- 合并 RUN 指令减少层数
- 使用 `--squash`（实验性功能）
- 使用 distroless 镜像

**14. `.dockerignore` 文件的作用是什么？和 `.gitignore` 的区别？**

- `.dockerignore`：排除不需要发送到 Docker daemon 的文件，减小构建上下文，防止密钥泄露
- 语法类似 `.gitignore`，但作用于 docker build context 而非 git

### 网络与存储

**15. Docker 默认 bridge 网络和自定义 bridge 网络有什么区别？为什么生产环境一定要用自定义网络？**

- 默认网络不支持基于容器名的 DNS 解析，只能使用 IP
- 自定义网络自带 DNS 服务（嵌入式 DNS），支持服务名访问
- 自定义网络隔离性更好，可按项目/环境分组管理
- 可通过 `--network-alias` 设置网络别名

**16. 容器之间怎么通信？跨宿主机通信的底层原理是什么？**

- 同宿主机：通过 Network Namespace + veth pair 连接到 docker0 网桥
- 跨宿主机：overlay 网络（VXLAN 隧道）或通过宿主机的 iptables SNAT/MASQUERADE 和 DNAT

**17. 端口映射 `-p 8080:80` 底层发生了什么？iptables 规则是怎样的？**

Docker 在 iptables 的 NAT 表中添加 DNAT 规则，将宿主机 8080 端口流量转发到容器 IP 的 80 端口。同时注意云安全组/防火墙配置。

**18. Docker 的网络模式有哪些？各自使用场景？**

- **bridge**：默认模式，单机容器通信
- **host**：与宿主机共享网络，性能最好，端口冲突风险
- **none**：无网络，用于离线/安全隔离场景
- **container**：共享其他容器网络，如 sidecar 模式
- **overlay**：跨宿主机通信（Swarm）

**19. Docker 数据卷（Volume）和绑定挂载（Bind Mount）的区别？`tmpfs` 挂载的使用场景？**

- **Volume**：Docker 管理，存储在 `/var/lib/docker/volumes/`，跨平台可移植
- **Bind Mount**：依赖宿主机目录结构，灵活性高但可移植性差
- **tmpfs**：内存存储，用于临时敏感数据

**20. 容器化应用的持久化存储方案有哪些？你在项目里怎么做的？**

- Docker Volume + 卷插件（如 RexRay、Portworx）
- 云存储方案（CSI driver：EBS、Azure Disk、GCE PD）
- NFS / Ceph 共享存储
- 数据库类服务需特别关注 IO 性能和数据一致性

### 安全与生产实践

**21. 生产环境 Docker 容器有哪些安全加固措施？**

- 非 root 用户运行（`USER` 指令）
- 最小权限（`--cap-drop ALL --cap-add NET_BIND_SERVICE`）
- 只读根文件系统（`--read-only`）
- 资源限制（CPU/内存/进程数）
- 密钥不入镜像（Secrets / Vault）
- 镜像漏洞扫描（Trivy / Clair）
- 使用受信任的基础镜像
- 启用 seccomp / AppArmor / SELinux

**22. Docker Secrets 是什么？和环境变量有什么区别？**

- Secrets 以加密挂载文件形式注入（`/run/secrets/`），不暴露在 `docker inspect` 中
- 环境变量易泄露（`docker inspect` 可见、子进程继承、日志中可能打印）
- 非 Swarm 环境可用 Vault、云 KMS 或 Kubernetes Secrets 替代

**23. Harbor 镜像仓库用过吗？怎么实现镜像扫描、签名、权限控制和垃圾回收？**

- 镜像扫描：集成 Trivy/Clair，设置阻止高危漏洞镜像
- 镜像签名：Notary 实现内容信任
- 权限控制：项目级 RBAC，LDAP/OIDC 集成
- 垃圾回收：定期执行 GC 清理未引用的 Blob
- 复制：支持主从/双主复制实现异地灾备

**24. 线上容器日志撑爆磁盘了怎么办？临时方案和根治方案分别是什么？**

- 临时：`truncate -s 0 /var/lib/docker/containers/*/*.log` 或 `>logfile`
- 根治：
  - `daemon.json` 配置日志轮转（`max-size`、`max-file`）
  - 应用层合理设置日志级别
  - 接入集中式日志系统（ELK / Loki / 云日志服务）
  - 应用输出 stdout/stderr，由 Docker 日志驱动接管

**25. 线上容器突然访问不了了，完整的排查链路是什么？**

1. 检查运行状态（`docker ps -a` → 查看退出码）
2. 查看日志（`docker logs --tail 100`）
3. 进入容器测网络（`docker exec` → `curl`/`ping`）
4. 检查端口映射和 iptables 规则（`docker port`、`iptables -t nat -L`）
5. 检查防火墙/安全组规则
6. 检查宿主机资源（CPU/内存/磁盘/IO）
7. 检查依赖服务可达性和健康状态

---

## 二、Jenkins（25道）

### 基础架构

**26. Jenkins 在 CI/CD 流程中扮演什么角色？它的核心架构是怎样的？**

- 开源 CI/CD 服务器，自动化构建、测试、部署
- Master-Agent 架构：Master 负责任务调度、UI、配置管理，Agent 负责实际执行构建任务
- 通过插件体系扩展功能（1500+ 插件）

**27. Jenkins Master 磁盘满的原因有哪些？Pipeline 层面如何规避？**

原因：构建日志堆积、workspace 未清理、大量 Junk 文件、插件/JAR 膨胀

规避策略：
- 配置日志轮转和构建丢弃策略
- Pipeline 中强制 `cleanWs()`
- 定期清理旧插件和 JAR
- 监控磁盘使用率并告警

**28. Jenkins 中 Job、Pipeline、Stage、Step 之间的关系是什么？**

- **Job/Project**：一个可执行的构建任务
- **Pipeline**：定义了整个 CI/CD 流水线的 Jenkinsfile
- **Stage**：Pipeline 中的一个阶段（如 Build、Test、Deploy）
- **Step**：Stage 中的单个操作（如 `sh 'npm test'`）

**29. Jenkins 的插件体系是怎样的？推荐哪些不可或缺的插件？**

- 插件基于 Java 开发，通过 Update Center 管理
- 核心推荐：Pipeline、Git、Docker、Blue Ocean、Credentials、Kubernetes、JUnit、Mailer、Configuration as Code

**30. Jenkinsfile 是什么？它解决了传统 Freestyle Job 的哪些痛点？**

- Jenkinsfile 是 Pipeline as Code 的具体实现
- 解决痛点：配置无法版本控制、无法代码评审、难以复用、手动配置繁琐、团队协作困难

**31. 2026 年 Jenkins 要求 Java 21 以上版本，为什么需要关注运行环境依赖？**

- Jenkins 从 2026 年 1 月起要求 Java 21（2.479+）
- 版本不匹配会导致启动失败或运行时异常
- 插件也需兼容对应 Java 版本
- 面试体现对环境管理的关注

### Pipeline 语法

**32. Scripted Pipeline 与 Declarative Pipeline 的区别？为什么 2026 年优先推荐声明式语法？**

| 维度 | Scripted Pipeline | Declarative Pipeline |
|------|------------------|---------------------|
| 语言 | Groovy | 结构化 DSL |
| 灵活性 | 高，可写任意 Groovy 代码 | 受限于预定义块 |
| 可读性 | 低 | 高 |
| 错误处理 | 需手动 try-catch | 自动处理 |
| 蓝海编辑器 | 有限支持 | 原生支持 |

2026 年优先推荐声明式，除非有特殊动态逻辑需求。

**33. Declarative Pipeline 中 `agent none` 的使用场景是什么？**

- 全局不分配 agent，在 stage 级别按需分配
- 场景：不同 stage 需要在不同环境/节点执行（如 Linux 编译 + Windows 测试）
- 节省资源，避免整个 Pipeline 占用一个 agent

**34. `post` 部分的常见条件判断有哪些？**

| 条件 | 触发时机 |
|------|---------|
| `always` | 无论结果如何都执行 |
| `success` | Pipeline 成功时 |
| `failure` | Pipeline 失败时 |
| `unstable` | 测试失败但构建成功时 |
| `changed` | 当前构建结果与上次不同时 |
| `aborted` | 手动中止时 |

**35. Pipeline 中如何处理凭据？`withCredentials` 和 `credentials()` 的正确用法？**

```groovy
// 声明式：绑定为环境变量
environment {
    DOCKER_PASSWORD = credentials('docker-hub-password')
}

// 脚本式：withCredentials 包装器
withCredentials([string(credentialsId: 'token', variable: 'API_TOKEN')]) {
    sh 'curl -H "Authorization: Bearer $API_TOKEN" ...'
}
```

**36. `parallel` 指令如何实现并行构建？如何限制最大并行度？FailFast 模式是什么？**

```groovy
stage('Test') {
    failFast true  // 任一失败立即终止其他并行任务
    parallel {
        stage('Unit Test') { steps { ... } }
        stage('Integration Test') { steps { ... } }
    }
}
```

通过节点数量或 `Throttle Concurrent Builds` 插件限制并行度。

**37. `input` 手动审批如何实现？如何避免 input 步骤占用 Executor 资源？**

```groovy
stage('Deploy') {
    input {
        message "Deploy to production?"
        ok "Yes"
        submitter "admin,lead"
    }
    steps { ... }
}
```

关键：`input` 放在 `agent` 块之前，或使用 `agent none`，避免占用 executor。

**38. `when` 指令有哪些条件判断方式？如何实现按分支差异化执行？**

```groovy
when {
    branch 'main'           // 分支匹配
    environment name: 'DEPLOY_TO', value: 'production'  // 环境变量
    expression { ... }      // Groovy 表达式
    anyOf { ... }           // 或条件
    allOf { ... }           // 且条件
    not { ... }             // 取反
}
```

**39. Pipeline 中环境变量有哪些层级？`environment`、`env`、`withEnv` 的作用域区别？**

- 系统级：Jenkins 全局配置
- Pipeline 级：顶层 `environment` 块
- Stage 级：Stage 内的 `environment` 块
- `env`：Groovy 变量，脚本式操作环境变量
- `withEnv`：临时设置，仅在块内生效

### 高级实战

**40. Shared Libraries 是什么？目录结构 `vars/`、`src/`、`resources/` 各自的职责？**

```
my-shared-lib/
├── vars/          # 全局变量/步骤函数，每个 .groovy 文件自动暴露为函数
├── src/           # Java/Groovy 类，可导入使用
└── resources/     # 静态资源文件，通过 libraryResource 函数加载
```

实现 DRY 原则，代码复用，团队标准化。

**41. 如何平滑更新 Shared Library 而不影响运行中的任务？版本管理和分支策略？**

- 使用版本标签或 Commit ID 引用（`@v1.2.0` 或 `@abc123`）
- 分支策略：`main`=稳定版，`develop`=开发版
- 运行时已加载的库不受更新影响
- CI 验证：库变更触发下游测试 Pipeline

**42. Jenkinsfile 超过 1000 行如何重构？有哪些拆分策略？**

- 通用逻辑下沉到 Shared Libraries
- 拆分为多个下游 Job/Pipeline（Pipeline 调用 Pipeline）
- 使用模板化参数
- 环境配置外部化

**43. 如何实现 Docker 化的 Jenkins Pipeline？`docker.build()` 和 `docker.withRegistry()` 怎么用？**

```groovy
pipeline {
    agent { docker { image 'node:22-alpine' } }  // 容器化 agent
    stages {
        stage('Build Image') {
            steps {
                script {
                    def app = docker.build("myapp:${env.BUILD_ID}")
                    docker.withRegistry('https://registry.example.com', 'registry-cred') {
                        app.push()
                    }
                }
            }
        }
    }
}
```

**44. 如何在 K8s 环境中配置动态 Agent？（Kubernetes Plugin、Pod Template）**

```groovy
pipeline {
    agent {
        kubernetes {
            yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: node
    image: node:22-alpine
    command: ['sleep', 'infinity']
'''
        }
    }
    stages { ... }
}
```

每个构建启动独立 Pod，构建完自动销毁，实现资源隔离和弹性伸缩。

**45. 灰度/蓝绿发布在 Jenkins Pipeline 中如何实现？**

- 蓝绿：准备两套环境，通过负载均衡一次性切换流量
- 灰度：逐步增加新版本副本数，减少旧版本副本数
- Pipeline 中通过 Kubernetes API / Helm 控制副本数和流量策略
- 配合健康检查和自动回滚逻辑

**46. Pipeline 异常处理怎么做？`try-catch-finally` 和声明式 post 的各自适用场景？**

- 声明式：使用 `post { failure { ... } }` 处理失败
- 脚本式：使用 `try-catch-finally` 处理异常
- 声明式优势：自动处理，更规范
- 脚本式优势：精细控制异常类型和恢复策略

**47. 代码提交即触发构建（Webhook）的完整配置流程是什么？**

1. Jenkins 安装 Git/GitHub/GitLab 插件
2. 创建 Pipeline Job，配置 SCM 仓库地址
3. 启用 "GitHub hook trigger for GITScm polling" / "Build when a change is pushed to GitLab"
4. Git 平台配置 Webhook URL：`http://jenkins.example.com/github-webhook/` 或 `/project/<job-name>`
5. 确保 Jenkins 可从公网访问（或使用内网穿透/云 SMEE）

### 性能与故障排查

**48. Pipeline 运行太慢的优化方向有哪些？**

- 依赖缓存（Maven `.m2`、npm `node_modules`、Docker 层缓存）
- 并行化测试（split tests）
- 浅克隆（`git clone --depth 1`）
- 减少大文件传输（使用 artifacts 而非 stash）
- 选择合适的 Agent/节点
- 移除不必要的 Stage

**49. 如何保证工作空间清理？`cleanWs()` 失败怎么办？**

```groovy
post {
    always {
        cleanWs(cleanWhenNotBuilt: false,
                cleanWhenFailure: true,
                deleteDirs: true)
    }
}
```

如果 `cleanWs()` 失败：使用容器化构建规避（构建结束容器销毁），或在系统级配置强制定时清理脚本。

**50. Jenkins 高并发场景下 Shared Libraries 变量冲突如何解决？为什么不能用静态变量？**

- 所有 Pipeline 共享同一个 JVM，静态变量会跨构建污染
- 解决方案：
  - 无状态设计，避免共享可变状态
  - 使用参数传递替代全局变量
  - 必要时使用 `ThreadLocal`
  - 库代码保持纯函数风格

---

## 三、GitHub Actions（20道）

### Workflow 基础

**51. GitHub Actions 的核心概念：Workflow、Job、Step、Action、Runner 分别是什么？**

| 概念 | 说明 |
|------|------|
| Workflow | `.github/workflows/` 下的 YAML 文件，定义整个流程 |
| Job | Workflow 中的一组 Step，在同一个 Runner 上执行 |
| Step | Job 中的单个任务，可以是 Action 或 Shell 命令 |
| Action | 可复用的最小单元（JS/Docker/Composite） |
| Runner | 执行 Job 的服务器（GitHub-hosted 或 Self-hosted） |

**52. `on` 触发器有哪些类型？如何配置 push、pull_request、schedule、workflow_dispatch 等事件？**

```yaml
on:
  push:
    branches: [main, develop]
  pull_request:
    types: [opened, synchronize, reopened]
  schedule:
    - cron: '0 0 * * *'  # 每天 0 点
  workflow_dispatch:     # 手动触发
    inputs:
      environment:
        type: choice
        options: [staging, production]
  workflow_call:         # 被其他 workflow 调用
```

**53. `needs` 关键字的作用是什么？如何构建有向无环图（DAG）实现串并行混合？**

`needs` 建立 Job 间依赖关系，只有依赖的 Job 成功后当前 Job 才运行。默认所有 Job 并行，通过 `needs` 构建 DAG，实现复杂串并行混合。

**54. GitHub Actions 的 `strategy.matrix` 如何实现并行测试？写一个多 Node 版本测试的示例。**

```yaml
jobs:
  test:
    strategy:
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

**55. `if` 条件表达式如何使用？如何在特定分支或条件下跳过某些 Job？**

```yaml
jobs:
  deploy:
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    # 或使用
    if: ${{ github.ref == 'refs/heads/main' }}
```

支持：`success()`、`failure()`、`always()`、`cancelled()` 等上下文函数。

**56. GitHub Actions 中如何使用缓存？`actions/cache` 的原理和最佳实践？**

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

最佳实践：
- key 包含依赖文件的 hash
- 使用 `restore-keys` 做宽松匹配
- 注意缓存大小限制（10GB 总容量）
- setup 类 Action（如 setup-node）自带缓存支持

### 环境与安全

**57. GitHub Actions 中 Secrets 的管理方式有哪些？各自的可见范围？**

| 级别 | 范围 | 适用场景 |
|------|------|---------|
| Repository | 单个仓库 | 项目特定密钥 |
| Environment | 特定环境 | 生产环境密钥，配合审批 |
| Organization | 整个组织 | 跨仓库共享密钥 |

日志自动屏蔽 Secret 值，显示为 `***`。

**58. 2026 年 GitHub Actions 引入的"作用域 Secret"是什么？解决什么问题？**

限定 Secret 绑定到具体执行上下文（特定分支/Job/Step），实现最小权限原则，防止非授权 Job 访问敏感密钥。

**59. `environment` 关键字的作用？如何配置手动审批和部署保护规则？**

```yaml
deploy:
  needs: test
  environment:
    name: production
    url: https://example.com
  steps: ...
```

在仓库 Settings → Environments → 配置：
- Required reviewers（手动审批）
- Wait timer（延迟部署）
- Deployment branches（限制部署分支）

**60. OIDC（OpenID Connect）在 GitHub Actions 中如何实现无密钥的云平台认证？**

```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/github-actions
    aws-region: us-east-1
```

流程：GitHub 作为 OIDC Provider → 云平台验证 Token → 返回短期凭证。无需存储长期 Access Key。

**61. GitHub Actions 中的供应链安全最佳实践有哪些？**

- **固定 Action 版本为 SHA**：`uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683`
- 使用 `--recursive` 检查子模块完整性
- 启用 Dependabot 安全更新
- 审查第三方 Action 的权限（`permissions` 字段）
- 签名和验证 artifacts

### 高级用法

**62. Self-hosted Runner 和 GitHub-hosted Runner 的区别？什么时候需要使用自托管 Runner？**

| 维度 | GitHub-hosted | Self-hosted |
|------|-------------|-------------|
| 管理 | GitHub 维护 | 自行管理 |
| 硬件 | 标准配置 | 自定义 |
| 网络 | 公网出口 | 可访问内网 |
| 缓存 | 自动清理 | 持久化 |
| 安全 | GitHub 负责 | 自行加固 |

适用场景：需要访问内网资源、GPU/大内存、国内网络优化、持久化构建缓存、私有化合规要求。

**63. Self-hosted Runner 的安全风险有哪些？如何加固？**

风险：恶意 PR 代码执行、凭据提取、横向攻击

加固：
- 网络隔离（VPC / 防火墙）
- 只用于私有仓库
- 定期更新 Runner 版本
- 使用临时/ephemeral Runner
- 最小权限运行
- 不安装不必要工具

**64. Reusable Workflow 是什么？如何设计和复用？和 Composite Action 的区别？**

```yaml
# 定义（.github/workflows/reusable.yml）
on: workflow_call
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps: ...

# 调用
jobs:
  call-deploy:
    uses: org/repo/.github/workflows/reusable.yml@main
    secrets: inherit
```

| 维度 | Reusable Workflow | Composite Action |
|------|-------------------|-----------------|
| 粒度 | 完整 Job | 一组 Step |
| 运行环境 | 独立 Runner | 调用者的 Runner |
| Secret 传递 | `secrets: inherit` | 需显式 inputs |
| 适用场景 | 复杂流水线 | 通用步骤组合 |

**65. GitHub Actions 的计费模型是怎样的？如何优化 Action 的运行成本？**

- 公开仓库免费无限使用
- 私有仓库按月提供免费额度，超出按分钟计费
- 优化：合并 Workflow、最小化运行时间、使用缓存、合理设置并发、使用 Self-hosted Runner

**66. 如何在 GitHub Actions 中实现跨仓库的 CI/CD 流水线触发？**

- `repository_dispatch` 事件（需要 PAT token）
- Reusable Workflow（跨仓库调用）
- `workflow_dispatch` + REST API 触发

**67. GitHub Actions 中如何实现 Docker 镜像的构建、扫描和推送？**

```yaml
- name: Build and Push
  uses: docker/build-push-action@v6
  with:
    context: .
    push: true
    tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
- name: Scan Image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/${{ github.repository }}:${{ github.sha }}
```

**68. GitHub Actions 的运行日志如何调试？如何开启 Debug Logging？**

- 设置 Secret：`ACTIONS_STEP_DEBUG=true` 开启步骤调试日志
- 设置 Secret：`ACTIONS_RUNNER_DEBUG=true` 开启 Runner 诊断日志
- 使用 `::debug::`、`::warning::`、`::error::` 命令输出
- 查看原始日志（View raw logs）

### 实战对比

**69. GitHub Actions 和 Jenkins 的架构核心差异是什么？选型时考虑哪些因素？**

| 维度 | GitHub Actions | Jenkins |
|------|---------------|---------|
| 架构 | 云原生、事件驱动 | 服务端 + 插件 |
| 配置 | YAML, 在代码仓库 | Jenkinsfile / UI |
| 维护 | SaaS，无需运维 | 需自建和维护 |
| 灵活性 | 受限于 YAML 语法 | Groovy，灵活性高 |
| 成本 | 免费额度 + 按量 | 服务器成本 |

**70. 如何将 Jenkins Pipeline 迁移到 GitHub Actions？关键映射关系是什么？**

| Jenkins | GitHub Actions |
|---------|---------------|
| `agent` | `runs-on` |
| `stages` / `stage` | `jobs` / 串行依赖 |
| `parallel` | `matrix` / 多 Job 并行 |
| `when { branch }` | `if: github.ref` |
| `input` | `environment` 审批 |
| `post` | `if: ${{ always() }}` |
| `credentials()` | `${{ secrets.XXX }}` |
| Shared Library | Reusable Workflow / Composite Action |

---

## 四、GitLab CI（15道）

### 核心概念

**71. GitLab CI 中 stages 和 jobs 有什么区别？如何配置多阶段流水线？**

- **Stage**：流水线阶段（如 build、test、deploy），全局 `stages` 字段定义顺序
- **Job**：Stage 内的具体任务，同一 Stage 的 Job 并行执行
- 多阶段：`stages` 列表中依次执行，前一阶段全部成功才进入下一阶段

**72. GitLab Runner 在 CI/CD 流程中扮演什么角色？有哪些类型的 Runner？**

- Runner 是执行 CI Job 的代理程序
- 类型：
  - **Shared Runner**：整个 GitLab 实例共享
  - **Group Runner**：组内项目共享
  - **Specific Runner**：绑定到特定项目
- Executor 类型：Shell、Docker、Docker Machine、Kubernetes、VirtualBox、Parallels、SSH

**73. GitLab CI 的 `rules` 关键字如何使用？和 `only/except` 的区别？**

```yaml
job:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - when: never
```

- `rules`：2026 年推荐方式，支持复杂条件组合
- `only/except`：旧语法，功能简单，不再推荐使用
- `rules` 支持：`if`、`changes`、`exists`、`when`、`allow_failure`、`variables`

**74. GitLab CI 中如何使用 `cache` 加速构建过程？cache 的 key 策略如何设计？**

```yaml
job:
  cache:
    key: $CI_COMMIT_REF_SLUG
    paths:
      - node_modules/
      - .m2/repository/
    policy: pull-push  # pull | push | pull-push
```

Key 策略：
- `$CI_COMMIT_REF_SLUG`：按分支缓存
- `$CI_JOB_NAME`：按 Job 名缓存
- `files: "**/package-lock.json"`：按文件 hash
- 组合使用实现高效缓存策略

**75. GitLab CI 中的 artifacts 有什么作用？如何配置和有效期管理？**

```yaml
job:
  artifacts:
    name: "artifacts-$CI_COMMIT_SHA"
    paths:
      - dist/
      - coverage/
    reports:
      junit: coverage/junit.xml
    expire_in: 7 days
    when: always  # on_success | on_failure | always
```

artifacts 用于在 Job 间传递构建产物，reports 类 artifacts 直接集成到 MR UI。

### 高级特性

**76. GitLab CI 中的 `include` 关键字有什么作用？如何复用流水线配置？**

```yaml
include:
  - local: .gitlab/ci/build.yml
  - remote: https://gitlab.com/shared/ci-templates/main.yml
  - template: Security/SAST.gitlab-ci.yml
  - project: org/shared-ci
    file: /pipelines/deploy.yml
    ref: main
```

支持四种来源：local（同仓库）、remote（远程 URL）、template（官方模板）、project（其他 GitLab 项目）。

**77. GitLab CI 的 `environment` 关键字如何实现多环境区分和部署追踪？**

```yaml
deploy:
  environment:
    name: production
    url: https://example.com
    on_stop: stop_production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

支持：环境仪表盘、部署历史、回滚操作、审批规则。

**78. GitLab CI 中如何实现 Docker-in-Docker（DinD）构建？有哪些注意事项？**

```yaml
build:
  image: docker:27
  services:
    - docker:27-dind
  variables:
    DOCKER_TLS_CERTDIR: "/certs"
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

注意事项：
- Runner 需配置 `privileged = true`（安全风险）
- 隔离方案：使用 `kaniko` 替代 DinD（无需特权模式）
- 使用 `--cache-from` 和 `--cache-to` 优化

**79. GitLab Container Registry 如何使用？如何在 CI 中构建、推送和部署镜像？**

- GitLab 内置 Container Registry，每个项目独立空间
- 通过预定义变量：`$CI_REGISTRY_IMAGE`、`$CI_REGISTRY_USER`、`$CI_REGISTRY_PASSWORD`
- 支持分层镜像缓存和垃圾回收

**80. GitLab 18.3 的"精细化作业令牌权限"解决了什么问题？最小权限如何实践？**

限制 CI/CD 作业令牌只能访问必需的资源（特定项目/仓库），防止过度授权带来的安全隐患，实现最小权限原则。

**81. GitLab CI 组件的 SLSA 1 级证明和不可变容器标签（18.1/18.2）是什么概念？**

- SLSA 1 级证明：为组件生成来源证明，确保供应链可追溯
- 不可变容器标签：防止标签被覆盖，确保部署的一致性和可审计性
- 最终目标是实现 SLSA 3-4 级，抗篡改构建

### 对比与实战

**82. GitLab CI 与 GitHub Actions 的执行模型有哪些核心差异？**

| 维度 | GitLab CI | GitHub Actions |
|------|-----------|---------------|
| 执行模型 | stages 全局串行，同 stage 并行 | 默认并行，needs 控制依赖 |
| 矩阵 | `parallel:matrix` | `strategy.matrix` |
| 测试报告 | `artifacts:reports:junit` 原生集成 MR | 需额外配置 |
| 环境 | 环境仪表盘内置 | 环境保护规则 |
| 仓库注册表 | 内置 Container Registry | GitHub Packages |

**83. 如何将 GitHub Actions 工作流转换为 GitLab CI Pipeline？矩阵构建如何映射？**

```yaml
# GitHub Actions matrix
strategy:
  matrix:
    node: [20, 22]

# GitLab CI 等效
parallel:
  matrix:
    - NODE_VERSION: ["20", "22"]
image: node:$NODE_VERSION
```

**84. GitLab CI 与 Jenkins 的选型对比？各自适合什么规模和场景的团队？**

| 维度 | GitLab CI | Jenkins |
|------|-----------|---------|
| 平台集成 | GitLab 原生集成 | 独立部署 |
| 学习曲线 | 低，YAML 配置 | 中高，Pipeline DSL |
| 维护成本 | 低（Shared Runner） | 高（自建服务） |
| 灵活性 | 中 | 高（Groovy 脚本） |
| 适合 | 中小团队、GitLab 用户 | 大型企业、复杂场景 |

**85. GitLab CI 中如何实现安全扫描（SAST、Secret Detection、Container Scanning）的左移集成？**

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Secret-Detection.gitlab-ci.yml
  - template: Container-Scanning.gitlab-ci.yml
```

安全扫描结果直接展示在 MR 页面，阻塞合并直到修复。

---

## 五、CI/CD 通用概念与综合题（15道）

### 概念与设计

**86. 解释 CI（持续集成）、Continuous Delivery（持续交付）、Continuous Deployment（持续部署）三者的区别和演进关系？**

- **CI（持续集成）**：频繁将代码合并到主干，自动化构建和测试，快速发现集成错误
- **Continuous Delivery（持续交付）**：在 CI 基础上，确保代码随时可部署到生产，但部署操作需人工触发
- **Continuous Deployment（持续部署）**：在持续交付基础上，通过自动化测试的代码自动部署到生产，无需人工干预

演进关系：CI → Continuous Delivery → Continuous Deployment，自动化程度逐步提高。

**87. 一个完整的 CI/CD 流水线应该包含哪些阶段？画出你设计的企业级流水线架构图。**

标准阶段：
1. **Checkout**：代码检出
2. **Static Analysis**：代码规范检查、SAST 安全扫描
3. **Build**：编译构建
4. **Unit Test**：单元测试
5. **Quality Gate**：代码质量门禁（SonarQube）
6. **Container Build**：构建 Docker 镜像
7. **Image Scan**：镜像漏洞扫描
8. **Deploy to Staging**：部署到预发布环境
9. **Integration/E2E Test**：集成/端到端测试
10. **Manual Approval**：人工审批
11. **Deploy to Production**：生产部署（蓝绿/灰度）
12. **Post-Deploy Validation**：冒烟测试、监控验证

**88. 什么是 DevSecOps？如何在 CI/CD 流水线中实现"安全左移"？**

- DevSecOps：将安全实践融入 DevOps 的每个阶段，安全不再是最后一道关卡
- 安全左移实现：
  - 代码阶段：SAST、Secret Detection、依赖扫描（SCA）
  - 构建阶段：镜像漏洞扫描、IaC 安全扫描
  - 部署阶段：DAST、合规检查
  - 运行阶段：运行时安全监控

**89. 什么是 GitOps？和传统 CI/CD 的区别是什么？ArgoCD/Flux 在其中的角色？**

- GitOps：以 Git 作为单一事实源，通过声明式配置管理基础设施和应用
- 区别：
  - 传统 CI/CD：CI 推送部署变更到环境
  - GitOps：Agent（ArgoCD/Flux）拉取 Git 状态并自动同步到集群
- ArgoCD/Flux：监控 Git 仓库变化，自动将集群状态同步到期望状态

**90. 蓝绿部署、金丝雀发布（灰度）、滚动更新的区别？各自的实现要点和回滚策略？**

| 策略 | 原理 | 回滚 | 适用场景 |
|------|------|------|---------|
| 滚动更新 | 逐步替换旧实例 | 重新部署旧版本 | 无状态服务 |
| 蓝绿部署 | 两套环境瞬间切换 | 切回旧环境 | 核心服务 |
| 金丝雀发布 | 小比例流量验证后全量 | 撤销金丝雀路由 | 高风险变更 |

### 实践与优化

**91. 流水线运行太慢，你会从哪些维度进行优化？**

1. **依赖缓存**：Maven `.m2`、npm `node_modules`、Go `GOPATH/pkg`、Docker 层缓存
2. **并行执行**：拆分测试用例、Matrix 并行
3. **增量构建**：只构建变更模块（Monorepo 场景）
4. **浅克隆**：`git clone --depth 1`
5. **资源分配**：使用性能更好的 Runner/Agent
6. **条件执行**：跳过不必要的 Stage/Job
7. **构建工具优化**：使用 Gradle build cache、Webpack 增量编译

**92. CI/CD 中如何管理多环境（dev/staging/production）的差异化配置？**

- 配置文件外部化（ConfigMap、Consul、Vault）
- 环境变量注入（不同环境不同值）
- 配置模板 + 渲染
- GitLab CI 的 `environment` 变量 + GitHub Actions 的 Environment Secrets
- 12-Factor App 原则：配置与代码分离

**93. CI/CD 流水线中密钥管理的最佳实践是什么？**

1. **永远不硬编码**：不将密钥写在代码或配置文件中
2. **使用平台原生 Secret 管理**：GitHub Secrets、GitLab CI Variables、Jenkins Credentials
3. **定期轮换**：设置密钥过期策略
4. **优先使用短期令牌**：OIDC 动态凭证优于静态 AK/SK
5. **最小权限**：每个 Job 只能访问其必需的 Secret
6. **审计日志**：追踪密钥使用记录

**94. 如何处理流水线中的"雪花"问题（只在特定机器上能构建成功）？**

- 标准化构建环境（Docker 镜像）
- 基础设施即代码（IaC）管理 Runner/Agent
- 定期重建/销毁和替换 Runner
- 锁定依赖版本（lock file）
- CI 环境的一致性检查

**95. 单体仓库（Monorepo）的 CI/CD 流水线如何设计？如何只对有变更的模块触发构建？**

```yaml
# GitHub Actions 路径过滤
on:
  push:
    paths:
      - 'services/user-service/**'
      - '!docs/**'

# GitLab CI
rules:
  - changes:
      - services/user-service/**/*
```

进阶：使用工具（Nx、Turborepo、Bazel）实现基于依赖图的增量构建。

**96. 如何设计一套支持多语言、多服务的 CI/CD 标准化流水线？**

- 流水线模板化（GitLab CI `include`、GitHub Reusable Workflow、Jenkins Shared Library）
- 约定优于配置：统一目录结构、统一构建脚本入口
- 插件化构建步骤：不同语言只需替换构建/测试命令
- 统一制品格式：Docker 镜像 + Helm Chart
- 统一部署流程：标准化部署参数，差异化体现在配置层面

### 故障与面试官追问

**97. 你有没有遇到过 CI/CD 相关的线上事故？怎么处理、恢复和预防的？**

用 STAR 法则描述真实案例：
- **Situation**：场景和影响
- **Task**：需要解决什么问题
- **Action**：采取的步骤（紧急止血 → 根因分析 → 修复 → 预防）
- **Result**：结果和教训

示例：错误的镜像标签导致生产回滚、Secret 泄露应急响应、流水线配置错误批量影响部署等。

**98. CI/CD 流水线中测试失败，你如何判断是代码问题还是环境/流水线问题？**

排查思路：
1. 检查是否稳定复现（重试机制）
2. 查看失败日志中的错误类型（网络/超时 vs 断言失败）
3. 本地复现（相同依赖版本和配置）
4. 检查环境差异（Node 版本、OS、系统依赖）
5. 检查最近流水线变更（配置文件修改）
6. 对比上一次成功构建的环境差异

**99. 如何保证 CI/CD 流水线的高可用性？Master/Jenkins 挂了怎么办？**

- Jenkins：Master HA（CloudBees 方案）、定期备份 `$JENKINS_HOME`、Pipeline as Code 确保配置可重建
- GitHub Actions：平台级高可用，GitHub 负责
- GitLab CI：多 Runner 冗余、跨区域部署
- 通用：构建配置版本化管理、快速重建能力、监控告警

**100. 系统设计题：从零搭建一套容器化 CI/CD 基础设施，你会怎么做？**

参考答案框架：

1. **镜像管理**：Harbor / GitLab Container Registry → 镜像仓库、漏洞扫描、签名验证
2. **代码管理**：GitLab / GitHub → 分支策略、Code Review、Webhook
3. **CI/CD 平台**：
   - 小型团队：GitHub Actions / GitLab CI
   - 大型企业：Jenkins + K8s 动态 Agent
4. **容器编排**：Kubernetes（生产级编排、自动扩缩、服务发现）
5. **配置管理**：Helm / Kustomize（声明式部署）
6. **GitOps**：ArgoCD（自动同步、可视化、回滚）
7. **监控告警**：Prometheus + Grafana（指标）、ELK / Loki（日志）、Tempo/Jaeger（链路）
8. **安全**：Trivy 镜像扫描、SAST（SonarQube）、Secret 管理（Vault）
9. **高可用**：多节点部署、跨可用区、定期备份、灾备演练

---

## 附录：2026 年面试趋势总结

| 维度 | 趋势 |
|------|------|
| **平台对比** | 面试官不再只问单一工具，而是要求对比 GitHub Actions / GitLab CI / Jenkins 的差异和选型 |
| **安全左移** | DevSecOps 成为必考，供应链安全（SLSA、SBOM、签名验证）是高频考点 |
| **云原生集成** | 与 K8s、Helm、ArgoCD 的联动成为中高级岗位标配 |
| **AI 赋能** | GitHub Copilot Next / AI 辅助 CI/CD 编排开始出现在面试中 |
| **Java 21** | Jenkins 强制 Java 21，版本依赖成为面试细节考察点 |
| **实战导向** | 不再考"定义"，而是考"你怎么排查的""踩过什么坑""怎么优化的" |
| **GitOps** | ArgoCD/Flux 的出现频率显著上升，成为 CI/CD 面试的延伸考点 |
| **多平台迁移** | 考察跨平台迁移能力（如 Jenkins → GitHub Actions） |

---

> **备考建议**：建议按分类逐块准备，每道题都能用具体项目经验和数据来回答。面试前对照每道题口述一遍，卡壳处即为薄弱环节。记住面试原则：**不说定义，说"我用过"；带具体数据；分享踩坑经历；承认边界；主动解释"why"**。
