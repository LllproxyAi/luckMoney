# 🎯 彩票数据分析与预测系统

## 🏗️ 项目架构

这是一个基于微服务架构的彩票数据爬取、分析和预测系统，采用前后端分离设计，支持多种编程语言和技术栈。

```
MoneyLuck/
├── projects/                    # 项目源码目录
│   ├── java-backend/           # Java后端服务 (Spring Boot)
│   ├── python-crawler/         # Python爬虫服务 (FastAPI)
│   ├── react-frontend/         # React前端应用 (TypeScript)
│   ├── database/               # 数据库脚本和配置
│   ├── docker/                 # Docker配置文件
│   ├── scripts/                # 部署和管理脚本
│   └── docs/                   # 项目文档
├── docker/                     # Docker相关文件
├── README.md                   # 项目总览
└── test_mysql_connection.py    # 数据库连接测试
```

## 🚀 技术栈概览

| 服务 | 技术栈 | 端口 | 说明 |
|------|--------|------|------|
| **Java后端** | Spring Boot + MySQL + JPA | 8080 | 核心业务逻辑、数据管理 |
| **Python爬虫** | FastAPI + PyMySQL + ML | 8000 | 数据爬取、分析、预测 |
| **React前端** | React 18 + TypeScript + Ant Design | 3000 | 用户界面、数据展示 |
| **数据库** | MySQL 8.0 | 3306 | 数据存储 |
| **Nginx** | Nginx | 80 | 反向代理、静态文件服务 |

## 📋 系统功能

### 🔍 数据爬取
- 支持大乐透、福彩3D、双色球等彩票类型
- 自动定时爬取最新开奖数据
- 智能重试和错误处理机制

### 📊 数据分析
- 频率统计分析
- 冷热号码分析
- 和值分布分析
- 遗漏值分析
- 趋势图表生成

### 🎯 预测模型
- 频率分析模型
- 马尔可夫链模型
- 神经网络模型
- 时间序列模型
- 模型准确率评估

### 🎨 用户界面
- 响应式设计，支持多设备
- 交互式图表展示
- 实时数据更新
- 多主题支持

## 🛠️ 快速开始

### 1. 环境准备
```bash
# 检查Docker环境
docker --version
docker-compose --version

# 检查Java环境
java -version
mvn --version

# 检查Python环境
python3 --version
pip3 --version

# 检查Node.js环境
node --version
npm --version
```

### 2. 数据库初始化
```bash
# 进入数据库目录
cd projects/database

# 执行初始化脚本
mysql -h 192.168.1.34 -P 3306 -u lbc -p19940314 < schema.sql
```

### 3. 启动服务

#### 方式一：Docker Compose (推荐)
```bash
# 进入Docker目录
cd projects/docker

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

#### 方式二：分别启动
```bash
# 启动Python爬虫
cd projects/python-crawler
docker build -t lottery-crawler .
docker run -d -p 8000:8000 lottery-crawler

# 启动Java后端
cd projects/java-backend
mvn spring-boot:run

# 启动React前端
cd projects/react-frontend
npm install
npm run dev
```

## 📡 服务访问

| 服务 | 地址 | 说明 |
|------|------|------|
| **前端界面** | http://localhost:3000 | 用户操作界面 |
| **Java API** | http://localhost:8080/api | 后端接口 |
| **Python API** | http://localhost:8000 | 爬虫和分析接口 |
| **健康检查** | http://localhost:8000/health | 服务状态 |

## 🔧 开发指南

### 添加新功能
1. **后端功能**: 在`java-backend`中添加Controller、Service、Repository
2. **爬虫功能**: 在`python-crawler`中添加爬取逻辑和分析模型
3. **前端功能**: 在`react-frontend`中添加页面和组件

### 数据库变更
1. 修改`projects/database/schema.sql`
2. 更新对应的JPA实体类
3. 执行数据库迁移脚本

### API接口
- Java后端: RESTful API，支持CRUD操作
- Python爬虫: FastAPI接口，提供数据分析和预测
- 前端: 通过Axios调用后端API

## 📊 监控和维护

### 日志查看
```bash
# Java后端日志
docker logs lottery-java-backend

# Python爬虫日志
docker logs lottery-python-crawler

# 前端日志
docker logs lottery-react-frontend
```

### 健康检查
```bash
# 检查所有服务状态
curl http://localhost:8080/actuator/health
curl http://localhost:8000/health
```

### 性能监控
- 使用JVM监控工具
- 数据库性能分析
- 前端性能指标

## 🚀 部署说明

### 开发环境
- 使用Docker Compose快速启动
- 支持热重载和调试
- 本地数据库连接

### 生产环境
- 使用Docker Swarm或Kubernetes
- 配置负载均衡和高可用
- 设置监控和告警
- 数据备份和恢复

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 基础功能实现
- Docker容器化支持
- 多语言架构设计

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交代码变更
4. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 📞 联系方式

- 项目维护者: MoneyLuck Team
- 邮箱: support@moneyluck.com
- 项目地址: https://github.com/moneyluck/lottery-analysis
