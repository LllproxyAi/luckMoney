"""
彩票数据爬虫主程序 - 彩票数据分析系统
"""
import os
import sys
import time
import schedule
from datetime import datetime
from loguru import logger
from fastapi import FastAPI, HTTPException
from uvicorn import run
import uvicorn

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import LOG_CONFIG
from crawler import LotteryCrawler
from data_analysis import LotteryDataAnalyzer
from prediction_models import PredictionModelFactory
from database import DatabaseManager

# 配置日志
logger.add(LOG_CONFIG['file'], 
          level=LOG_CONFIG['level'], 
          format=LOG_CONFIG['format'],
          rotation="1 day",
          retention="30 days")

# 创建FastAPI应用
app = FastAPI(
    title="彩票数据分析系统",
    description="彩票数据爬取、分析和预测的综合系统",
    version="1.0.0"
)

# 全局变量
crawler = None
analyzer = None
db = None

@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    global crawler, analyzer, db
    
    try:
        # 初始化组件
        crawler = LotteryCrawler()
        analyzer = LotteryDataAnalyzer()
        db = DatabaseManager()
        
        logger.info("彩票数据分析系统启动成功")
        
        # 启动定时任务
        schedule.every().day.at("09:00").do(daily_crawl_task)
        schedule.every().day.at("21:00").do(daily_analysis_task)
        
    except Exception as e:
        logger.error(f"系统启动失败: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    global crawler, analyzer, db
    
    try:
        if crawler:
            crawler.close()
        if analyzer:
            analyzer.close()
        if db:
            db.close()
        
        logger.info("彩票数据分析系统已关闭")
        
    except Exception as e:
        logger.error(f"系统关闭失败: {e}")

@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "彩票数据分析系统",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        # 检查数据库连接
        if db and db.connection and db.connection.open:
            db_status = "healthy"
        else:
            db_status = "unhealthy"
        
        return {
            "status": "healthy",
            "database": db_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"健康检查失败: {e}")

@app.post("/crawl/start")
async def start_crawling():
    """开始数据爬取"""
    try:
        if not crawler:
            raise HTTPException(status_code=500, detail="爬虫未初始化")
        
        logger.info("开始执行数据爬取任务")
        results = crawler.crawl_all_data()
        
        return {
            "message": "数据爬取完成",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"数据爬取失败: {e}")
        raise HTTPException(status_code=500, detail=f"数据爬取失败: {e}")

@app.get("/analysis/frequency/{lottery_type_id}")
async def get_frequency_analysis(lottery_type_id: int, limit: int = 100):
    """获取频率分析结果"""
    try:
        if not analyzer:
            raise HTTPException(status_code=500, detail="分析器未初始化")
        
        results = analyzer.analyze_frequency_trends(lottery_type_id, limit)
        
        return {
            "lottery_type_id": lottery_type_id,
            "analysis_type": "frequency",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"频率分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"频率分析失败: {e}")

@app.get("/analysis/hot_cold/{lottery_type_id}")
async def get_hot_cold_analysis(lottery_type_id: int, limit: int = 50):
    """获取冷热号码分析结果"""
    try:
        if not analyzer:
            raise HTTPException(status_code=500, detail="分析器未初始化")
        
        results = analyzer.analyze_hot_cold_numbers(lottery_type_id, limit)
        
        return {
            "lottery_type_id": lottery_type_id,
            "analysis_type": "hot_cold",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"冷热号码分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"冷热号码分析失败: {e}")

@app.get("/analysis/sum_distribution/{lottery_type_id}")
async def get_sum_distribution_analysis(lottery_type_id: int, limit: int = 100):
    """获取和值分布分析结果"""
    try:
        if not analyzer:
            raise HTTPException(status_code=500, detail="分析器未初始化")
        
        results = analyzer.analyze_sum_distribution(lottery_type_id, limit)
        
        return {
            "lottery_type_id": lottery_type_id,
            "analysis_type": "sum_distribution",
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"和值分布分析失败: {e}")
        raise HTTPException(status_code=500, detail=f"和值分布分析失败: {e}")

@app.post("/prediction/generate/{lottery_type_id}")
async def generate_prediction(lottery_type_id: int, model_type: str = "FREQUENCY"):
    """生成预测结果"""
    try:
        if not crawler or not analyzer:
            raise HTTPException(status_code=500, detail="系统组件未初始化")
        
        # 获取历史数据
        historical_data = db.get_lottery_results(lottery_type_id, 100)
        if not historical_data:
            raise HTTPException(status_code=400, detail="历史数据不足")
        
        # 创建预测模型
        model = PredictionModelFactory.create_model(model_type)
        
        # 训练模型
        if not model.train(historical_data):
            raise HTTPException(status_code=500, detail="模型训练失败")
        
        # 生成预测
        prediction = model.predict(historical_data)
        if not prediction:
            raise HTTPException(status_code=500, detail="预测生成失败")
        
        # 保存预测结果
        next_draw_number = str(int(historical_data[0]['draw_number']) + 1).zfill(4)
        db.insert_prediction(
            model_id=1,  # 默认模型ID
            lottery_type_id=lottery_type_id,
            draw_number=next_draw_number,
            predicted_numbers=prediction,
            confidence_score=prediction.get('confidence', 0.5)
        )
        
        return {
            "lottery_type_id": lottery_type_id,
            "model_type": model_type,
            "next_draw_number": next_draw_number,
            "prediction": prediction,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"预测生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"预测生成失败: {e}")

@app.get("/charts/frequency/{lottery_type_id}")
async def generate_frequency_chart(lottery_type_id: int, limit: int = 50):
    """生成频率分析图表"""
    try:
        if not analyzer:
            raise HTTPException(status_code=500, detail="分析器未初始化")
        
        filename = analyzer.generate_frequency_chart(lottery_type_id, limit)
        if not filename:
            raise HTTPException(status_code=500, detail="图表生成失败")
        
        return {
            "message": "图表生成成功",
            "filename": filename,
            "lottery_type_id": lottery_type_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"图表生成失败: {e}")
        raise HTTPException(status_code=500, detail=f"图表生成失败: {e}")

def daily_crawl_task():
    """每日数据爬取任务"""
    try:
        logger.info("执行每日数据爬取任务")
        if crawler:
            results = crawler.crawl_all_data()
            logger.info(f"每日爬取任务完成: {results}")
    except Exception as e:
        logger.error(f"每日爬取任务失败: {e}")

def daily_analysis_task():
    """每日数据分析任务"""
    try:
        logger.info("执行每日数据分析任务")
        if analyzer and db:
            lottery_types = db.get_lottery_types()
            for lottery_type in lottery_types:
                try:
                    # 生成各种分析图表
                    analyzer.generate_frequency_chart(lottery_type['id'])
                    analyzer.generate_hot_cold_chart(lottery_type['id'])
                    analyzer.generate_sum_distribution_chart(lottery_type['id'])
                    logger.info(f"{lottery_type['type_name']}分析任务完成")
                except Exception as e:
                    logger.error(f"{lottery_type['type_name']}分析任务失败: {e}")
    except Exception as e:
        logger.error(f"每日分析任务失败: {e}")

def run_scheduler():
    """运行定时任务调度器"""
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
        except Exception as e:
            logger.error(f"调度器运行失败: {e}")
            time.sleep(60)

if __name__ == "__main__":
    import threading
    
    # 启动定时任务调度器
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # 启动FastAPI服务
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 