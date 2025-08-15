"""
Docker环境配置文件 - 彩票数据爬虫和分析系统
"""
import os

# 数据库配置 - Docker环境
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', '192.168.1.34'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'lbc'),
    'password': os.getenv('DB_PASSWORD', '19940314'),
    'database': os.getenv('DB_NAME', 'luck_money'),
    'charset': 'utf8mb4'
}

# 爬虫配置
CRAWLER_CONFIG = {
    'request_delay': int(os.getenv('REQUEST_DELAY', 2)),
    'max_retries': int(os.getenv('MAX_RETRIES', 3)),
    'timeout': int(os.getenv('TIMEOUT', 30)),
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 数据源配置
DATA_SOURCES = {
    'DLT': {
        'name': '大乐透',
        'url': 'http://www.lottery.gov.cn/historykj/history.jspx?_ltype=4',
        'parser': 'dlt_parser'
    },
    'FC3D': {
        'name': '福彩3D',
        'url': 'http://www.lottery.gov.cn/historykj/history.jspx?_ltype=1',
        'parser': 'fc3d_parser'
    },
    'SSQ': {
        'name': '双色球',
        'url': 'http://www.lottery.gov.cn/historykj/history.jspx?_ltype=1',
        'parser': 'ssq_parser'
    }
}

# 预测模型配置
MODEL_CONFIG = {
    'frequency_model': {
        'window_size': 100,
        'weight_factor': 0.8
    },
    'markov_model': {
        'order': 3,
        'smoothing': 0.1
    },
    'neural_net_model': {
        'layers': [64, 32, 16],
        'epochs': 1000,
        'learning_rate': 0.001
    },
    'time_series_model': {
        'p': 2,
        'd': 1,
        'q': 1
    }
}

# 日志配置 - Docker环境
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}',
    'file': 'logs/crawler.log'
}

# 服务配置
SERVICE_CONFIG = {
    'host': os.getenv('HOST', '0.0.0.0'),
    'port': int(os.getenv('PORT', 8000)),
    'debug': os.getenv('DEBUG', 'false').lower() == 'true'
}

# 定时任务配置
SCHEDULER_CONFIG = {
    'daily_crawl_time': os.getenv('DAILY_CRAWL_TIME', '09:00'),
    'daily_analysis_time': os.getenv('DAILY_ANALYSIS_TIME', '21:00')
}
