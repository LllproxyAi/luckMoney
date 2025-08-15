# 彩票数据分析系统部署指南

## 系统要求

### 硬件要求
- **CPU**: 2核心以上
- **内存**: 4GB以上
- **存储**: 20GB以上可用空间
- **网络**: 稳定的网络连接

### 软件要求
- **操作系统**: Linux (Ubuntu 18.04+), macOS 10.15+, Windows 10+
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Java**: 11+ (如果本地构建)
- **Node.js**: 16+ (如果本地构建)
- **Python**: 3.9+ (如果本地构建)

## 快速部署

### 1. 克隆项目
```bash
git clone <repository-url>
cd MoneyLuck
```

### 2. 运行部署脚本
```bash
chmod +x deploy.sh
./deploy.sh
```

部署脚本会自动完成以下工作：
- 检查环境依赖
- 创建必要的目录
- 构建Java后端和React前端
- 启动所有Docker服务
- 检查服务健康状态

### 3. 访问系统
部署完成后，可以通过以下地址访问系统：
- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8080/api
- **Python爬虫**: http://localhost:8000

## 手动部署

### 1. 环境准备
```bash
# 安装Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 配置环境变量
```bash
# 创建.env文件
cp .env.example .env

# 编辑配置文件
nano .env
```

### 3. 启动服务
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看服务日志
docker-compose logs -f
```

## 服务配置

### 数据库配置
```yaml
# MySQL配置
MYSQL_ROOT_PASSWORD: password
MYSQL_DATABASE: lottery_analysis
MYSQL_USER: lottery_user
MYSQL_PASSWORD: lottery_pass
```

### 端口配置
- **MySQL**: 3306
- **Python爬虫**: 8000
- **Java后端**: 8080
- **React前端**: 3000
- **Nginx**: 80, 443

### 环境变量
```bash
# 数据库连接
DB_HOST=localhost
DB_PORT=3306
DB_USER=lottery_user
DB_PASSWORD=lottery_pass
DB_NAME=lottery_analysis

# Python爬虫服务
PYTHON_CRAWLER_BASE_URL=http://localhost:8000
PYTHON_CRAWLER_TIMEOUT=30000

# Java后端服务
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/lottery_analysis
SPRING_DATASOURCE_USERNAME=lottery_user
SPRING_DATASOURCE_PASSWORD=lottery_pass
```

## 生产环境部署

### 1. 安全配置
```bash
# 修改默认密码
# 编辑.env文件，使用强密码

# 配置防火墙
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 22
sudo ufw enable
```

### 2. SSL证书配置
```bash
# 创建SSL证书目录
mkdir -p nginx/ssl

# 复制SSL证书
cp your-cert.pem nginx/ssl/
cp your-key.pem nginx/ssl/

# 配置Nginx
# 编辑nginx/nginx.conf文件
```

### 3. 数据备份
```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backup/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# 备份数据库
docker exec lottery-mysql mysqldump -u root -ppassword lottery_analysis > $BACKUP_DIR/database.sql

# 备份配置文件
cp -r .env $BACKUP_DIR/
cp -r nginx/ $BACKUP_DIR/

echo "备份完成: $BACKUP_DIR"
EOF

chmod +x backup.sh
```

## 监控和维护

### 1. 服务监控
```bash
# 查看服务状态
docker-compose ps

# 查看资源使用
docker stats

# 查看服务日志
docker-compose logs -f [服务名]
```

### 2. 日志管理
```bash
# 查看Python爬虫日志
tail -f python-crawler/logs/crawler.log

# 查看Java后端日志
docker logs lottery-java-backend

# 查看前端日志
docker logs lottery-react-frontend
```

### 3. 性能优化
```bash
# 调整Java内存配置
# 编辑backend/Dockerfile中的JAVA_OPTS

# 调整Python爬虫配置
# 编辑python-crawler/config.py

# 调整数据库配置
# 编辑docker-compose.yml中的MySQL配置
```

## 故障排除

### 常见问题

#### 1. 服务启动失败
```bash
# 检查端口占用
netstat -tulpn | grep :8080

# 检查Docker状态
docker system info

# 查看详细错误日志
docker-compose logs [服务名]
```

#### 2. 数据库连接失败
```bash
# 检查MySQL服务状态
docker exec lottery-mysql mysqladmin -u root -ppassword ping

# 检查网络连接
docker network ls
docker network inspect lottery-network
```

#### 3. 前端无法访问后端
```bash
# 检查CORS配置
# 编辑backend/src/main/java/com/moneyluck/lottery/config/CorsConfig.java

# 检查代理配置
# 编辑frontend/package.json中的proxy字段
```

### 日志分析
```bash
# 查看错误日志
docker-compose logs | grep ERROR

# 查看访问日志
docker-compose logs nginx | grep "GET\|POST"

# 查看性能日志
docker-compose logs | grep "timeout\|slow"
```

## 扩展部署

### 1. 负载均衡
```yaml
# 在docker-compose.yml中添加多个实例
services:
  java-backend-1:
    # ... 配置
  java-backend-2:
    # ... 配置
  
  nginx:
    # 配置负载均衡
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
```

### 2. 高可用部署
```bash
# 使用Docker Swarm
docker swarm init
docker stack deploy -c docker-compose.yml lottery

# 使用Kubernetes
kubectl apply -f k8s/
```

### 3. 微服务架构
```yaml
# 拆分服务
services:
  user-service:
    # 用户服务
  prediction-service:
    # 预测服务
  analysis-service:
    # 分析服务
```

## 联系支持

如果在部署过程中遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查GitHub Issues
3. 联系技术支持团队

**技术支持邮箱**: support@moneyluck.com
**技术支持电话**: 400-123-4567 