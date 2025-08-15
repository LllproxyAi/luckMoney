# 彩票数据分析与预测系统

## 项目简介
这是一个彩票数据爬取、分析和预测的综合系统，支持大乐透和福彩3D等彩票类型的数据分析。

## 功能特性
- 🕷️ 自动爬取彩票开奖数据
- 📊 多维度数据分析和可视化
- 🔮 多种概率统计预测模型
- 📈 趋势分析和图表展示
- 🎯 模型准确率评估和打分
- ☁️ 云端部署支持

## 技术架构
- **后端**: Java Spring Boot + Python爬虫
- **前端**: React + TypeScript + Ant Design
- **数据库**: MySQL
- **部署**: Docker + Docker Compose

## 快速开始
```bash
# 克隆项目
git clone <repository-url>
cd MoneyLuck

# 启动服务
docker-compose up -d

# 访问前端
http://localhost:3000

# 访问后端API
http://localhost:8080
```

## 项目结构
```
MoneyLuck/
├── backend/                 # Java后端服务
├── frontend/               # React前端应用
├── python-crawler/         # Python爬虫服务
├── database/               # 数据库脚本
├── docker/                 # Docker配置文件
└── docs/                   # 项目文档
``` 