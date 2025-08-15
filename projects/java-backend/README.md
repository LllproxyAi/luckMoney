# 🎯 Java后端服务

## 项目简介
彩票数据分析与预测系统的Java后端服务，基于Spring Boot框架构建。

## 🚀 技术栈
- **框架**: Spring Boot 2.7.x
- **数据库**: MySQL + JPA/Hibernate
- **安全**: Spring Security + JWT
- **工具**: Lombok, Jackson
- **构建**: Maven

## 📁 项目结构
```
java-backend/
├── src/main/java/com/moneyluck/lottery/
│   ├── controller/     # REST控制器
│   ├── service/        # 业务逻辑层
│   ├── repository/     # 数据访问层
│   ├── entity/         # JPA实体
│   ├── dto/           # 数据传输对象
│   ├── config/        # 配置类
│   ├── exception/     # 异常处理
│   └── scheduler/     # 定时任务
├── src/main/resources/
│   └── application.yml # 配置文件
└── pom.xml            # Maven配置
```

## 🛠️ 快速开始

### 环境要求
- JDK 11+
- Maven 3.6+
- MySQL 8.0+

### 本地开发
```bash
# 1. 进入项目目录
cd projects/java-backend

# 2. 安装依赖
mvn clean install

# 3. 启动服务
mvn spring-boot:run
```

### Docker部署
```bash
# 1. 构建镜像
docker build -t lottery-java-backend .

# 2. 运行容器
docker run -d -p 8080:8080 --name lottery-java-backend lottery-java-backend
```

## 📡 API接口

### 彩票类型管理
- `GET /api/lottery/types` - 获取所有彩票类型
- `GET /api/lottery/types/{id}` - 根据ID获取彩票类型

### 开奖结果管理
- `GET /api/lottery/results` - 分页获取开奖结果
- `GET /api/lottery/results/{id}` - 根据ID获取开奖结果
- `POST /api/lottery/results` - 添加开奖结果
- `PUT /api/lottery/results/{id}` - 更新开奖结果
- `DELETE /api/lottery/results/{id}` - 删除开奖结果

### 预测模型
- `GET /api/prediction/models` - 获取预测模型列表
- `POST /api/prediction/generate` - 生成预测结果
- `GET /api/prediction/evaluation/{modelId}` - 获取模型评估

## ⚙️ 配置说明

### 数据库配置
```yaml
spring:
  datasource:
    url: jdbc:mysql://192.168.1.34:3306/luck_money
    username: lbc
    password: 19940314
    driver-class-name: com.mysql.cj.jdbc.Driver
```

### 服务配置
```yaml
server:
  port: 8080
  servlet:
    context-path: /api

lottery:
  python-crawler:
    base-url: http://localhost:8000
```

## 🔧 开发指南

### 添加新的API接口
1. 在`controller`包中创建控制器类
2. 在`service`包中实现业务逻辑
3. 在`repository`包中添加数据访问方法
4. 在`entity`包中定义数据模型

### 数据库迁移
1. 修改实体类
2. 更新数据库表结构
3. 运行测试验证

## 📊 监控与日志

### 健康检查
- 端点: `/actuator/health`
- 状态: 应用状态、数据库连接状态

### 日志配置
- 级别: INFO
- 输出: 控制台 + 文件
- 格式: JSON格式，便于ELK分析

## 🚀 部署说明

### 生产环境
1. 修改`application-prod.yml`配置
2. 设置JVM参数
3. 配置日志轮转
4. 设置监控告警

### 性能优化
- JVM调优
- 数据库连接池配置
- 缓存策略
- 异步处理

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 基础CRUD功能
- 预测模型接口
- 定时任务支持
