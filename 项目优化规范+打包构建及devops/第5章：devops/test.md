version: '3.8'

services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    container_name: gitlab
    hostname: 124.221.166.48
    restart: always
    ports:
      - "8081:80"
      - "2222:22"
    volumes:
      - ./gitlab/config:/etc/gitlab
      - ./gitlab/logs:/var/log/gitlab
      - ./gitlab/data:/var/opt/gitlab
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'http://124.221.166.48:8081'
        gitlab_rails['gitlab_shell_ssh_port'] = 2222

  gitlab-runner:
    image: gitlab/gitlab-runner:latest
      container_name: gitlab-runner
      restart: always
      volumes:
        - ./gitlab-runner/config:/etc/gitlab-runner
        - /var/run/docker.sock:/var/run/docker.sock
      depends_on:
        - gitlab

  jenkins:
    image: jenkins/jenkins:lts-jdk21
    container_name: jenkins
    restart: always
    ports:
      - "9090:8080"
      - "50000:50000"
    volumes:
      - ./jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
      - web-data:/var/jenkins_home/workspace/deploy
      - ./known_hosts:/var/jenkins_home/.ssh/known_hosts
    user: root

  nginx:
    image: nginx:alpine
    container_name: nginx
    restart: always
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
      - web-data:/usr/share/nginx/html
    depends_on:
      - jenkins
volumes:
   web-data:  # Docker 管理，实际路径 /var/lib/docker/volumes/项目名_web-data/_data