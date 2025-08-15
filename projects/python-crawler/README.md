# 🕷️ Python爬虫服务

## 项目简介
彩票数据爬取、分析和预测的Python服务，基于FastAPI框架构建，提供RESTful API接口。

## 🚀 技术栈
- **框架**: FastAPI + Uvicorn
- **爬虫**: Requests + BeautifulSoup4 + LXML
- **数据分析**: Pandas + NumPy + Scikit-learn
- **可视化**: Matplotlib + Seaborn + Plotly
- **数据库**: PyMySQL + SQLAlchemy
- **任务调度**: Schedule + APScheduler

## 📁 项目结构
```
python-crawler/
├── main.py              # FastAPI主应用
├── crawler.py           # 爬虫核心逻辑
├── database.py          # 数据库操作
├── data_analysis.py     # 数据分析模块
├── prediction_models.py # 预测模型
├── config.py            # 配置文件
├── config_docker.py     # Docker环境配置
├── requirements.txt     # Python依赖
├── Dockerfile          # Docker镜像构建
├── logs/               # 日志目录
└── charts/             # 图表输出目录
```

## 🛠️ 快速开始

### 环境要求
- Python 3.9+
- pip 20.0+
- MySQL 8.0+

### 本地开发
```bash
# 1. 进入项目目录
cd projects/python-crawler

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
python main.py
```

### Docker部署
```bash
# 1. 构建镜像
docker build -t lottery-python-crawler .

# 2. 运行容器
docker run -d -p 8000:8000 --name lottery-python-crawler lottery-python-crawler
```

## 📡 API接口

### 爬虫管理
- `POST /crawl/start` - 启动数据爬取
- `GET /crawl/status` - 获取爬取状态

### 数据分析
- `GET /analysis/frequency/{lottery_type_id}` - 频率分析
- `GET /analysis/hot_cold/{lottery_type_id}` - 冷热分析
- `GET /analysis/sum_distribution/{lottery_type_id}` - 和值分布

### 预测模型
- `POST /prediction/generate` - 生成预测结果
- `GET /prediction/models` - 获取模型列表
- `GET /prediction/evaluation/{model_id}` - 模型评估

### 图表生成
- `GET /charts/frequency/{lottery_type_id}` - 频率图表
- `GET /charts/trend/{lottery_type_id}` - 趋势图表

## ⚙️ 配置说明

### 数据库配置
```python
DATABASE_CONFIG = {
    'host': '192.168.1.34',
    'port': 3306,
    'user': 'lbc',
    'password': '19940314',
    'database': 'luck_money',
    'charset': 'utf8mb4'
}
```

### 爬虫配置
```python
CRAWLER_CONFIG = {
    'request_delay': 2,      # 请求间隔(秒)
    'max_retries': 3,        # 最大重试次数
    'timeout': 30,           # 请求超时(秒)
    'user_agent': '...'      # 用户代理
}
```

## 🔧 开发指南

### 添加新的彩票类型
1. 在`crawler.py`中添加爬取方法
2. 在`data_analysis.py`中添加分析逻辑
3. 在`prediction_models.py`中添加预测模型
4. 更新API接口

### 自定义预测模型
1. 继承`BasePredictionModel`类
2. 实现`predict`方法
3. 在`PredictionModelFactory`中注册
4. 添加模型评估逻辑

### 数据源扩展
1. 在`DATA_SOURCES`中添加新源
2. 实现对应的解析器
3. 添加错误处理和重试机制

## 📊 功能特性

### 数据爬取
- 多彩票类型支持(大乐透、福彩3D、双色球)
- 智能重试和错误处理
- 请求频率控制
- 数据验证和清洗

### 数据分析
- 频率统计分析
- 冷热号码分析
- 和值分布分析
- 遗漏值分析

### 预测模型
- 频率分析模型
- 马尔可夫链模型
- 神经网络模型
- 时间序列模型

### 可视化
- 频率分布图
- 趋势分析图
- 热力图
- 交互式图表

## 🚀 部署说明

### 生产环境
1. 使用Gunicorn + Uvicorn
2. 配置Nginx反向代理
3. 设置日志轮转
4. 配置监控告警

### 性能优化
- 异步爬取
- 连接池管理
- 缓存策略
- 任务队列

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 基础爬虫功能
- 数据分析模块
- 预测模型框架
- FastAPI接口
- Docker支持

## 🔍 故障排除

### 常见问题
1. **数据库连接失败**: 检查网络和认证信息
2. **爬取失败**: 检查目标网站可访问性
3. **内存不足**: 调整批处理大小
4. **依赖冲突**: 使用虚拟环境

### 日志查看
```bash
# 查看实时日志
tail -f logs/crawler.log

# 查看错误日志
grep ERROR logs/crawler.log
```
