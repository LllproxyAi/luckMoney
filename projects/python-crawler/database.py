"""
数据库操作模块 - 彩票数据分析系统
"""
import json
import pymysql
from typing import List, Dict, Any, Optional
from loguru import logger
from config import DATABASE_CONFIG


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.connection = None
        self.connect()
    
    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(**DATABASE_CONFIG)
            logger.info("数据库连接成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询语句"""
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            logger.error(f"查询执行失败: {e}")
            self.connect()  # 重新连接
            raise
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """执行更新语句"""
        try:
            if not self.connection or not self.connection.open:
                self.connect()
            
            with self.connection.cursor() as cursor:
                affected_rows = cursor.execute(query, params)
                self.connection.commit()
                return affected_rows
        except Exception as e:
            logger.error(f"更新执行失败: {e}")
            self.connection.rollback()
            self.connect()  # 重新连接
            raise
    
    def insert_lottery_result(self, lottery_type_id: int, draw_number: str, 
                            draw_date: str, numbers: Dict[str, Any], 
                            sales_amount: float = None, prize_pool: float = None) -> bool:
        """插入开奖结果"""
        query = """
        INSERT INTO lottery_results 
        (lottery_type_id, draw_number, draw_date, numbers, sales_amount, prize_pool)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        numbers = VALUES(numbers),
        sales_amount = VALUES(sales_amount),
        prize_pool = VALUES(prize_pool)
        """
        
        try:
            numbers_json = json.dumps(numbers, ensure_ascii=False)
            self.execute_update(query, (lottery_type_id, draw_number, draw_date, 
                                      numbers_json, sales_amount, prize_pool))
            logger.info(f"开奖结果插入成功: {draw_number}")
            return True
        except Exception as e:
            logger.error(f"开奖结果插入失败: {e}")
            return False
    
    def get_lottery_results(self, lottery_type_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """获取开奖结果"""
        query = """
        SELECT * FROM lottery_results 
        WHERE lottery_type_id = %s 
        ORDER BY draw_date DESC 
        LIMIT %s
        """
        
        try:
            results = self.execute_query(query, (lottery_type_id, limit))
            # 解析JSON字段
            for result in results:
                if result.get('numbers'):
                    result['numbers'] = json.loads(result['numbers'])
            return results
        except Exception as e:
            logger.error(f"获取开奖结果失败: {e}")
            return []
    
    def get_lottery_types(self) -> List[Dict[str, Any]]:
        """获取彩票类型列表"""
        query = "SELECT * FROM lottery_types"
        
        try:
            return self.execute_query(query)
        except Exception as e:
            logger.error(f"获取彩票类型失败: {e}")
            return []
    
    def insert_prediction(self, model_id: int, lottery_type_id: int, 
                         draw_number: str, predicted_numbers: Dict[str, Any], 
                         confidence_score: float = None) -> bool:
        """插入预测结果"""
        query = """
        INSERT INTO predictions 
        (model_id, lottery_type_id, draw_number, predicted_numbers, confidence_score)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            numbers_json = json.dumps(predicted_numbers, ensure_ascii=False)
            self.execute_update(query, (model_id, lottery_type_id, draw_number, 
                                      numbers_json, confidence_score))
            logger.info(f"预测结果插入成功: {draw_number}")
            return True
        except Exception as e:
            logger.error(f"预测结果插入失败: {e}")
            return False
    
    def insert_model_evaluation(self, model_id: int, lottery_type_id: int, 
                              draw_number: str, actual_numbers: Dict[str, Any], 
                              predicted_numbers: Dict[str, Any], accuracy_score: float) -> bool:
        """插入模型评估结果"""
        query = """
        INSERT INTO model_evaluations 
        (model_id, lottery_type_id, draw_number, actual_numbers, predicted_numbers, accuracy_score)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        try:
            actual_json = json.dumps(actual_numbers, ensure_ascii=False)
            predicted_json = json.dumps(predicted_numbers, ensure_ascii=False)
            self.execute_update(query, (model_id, lottery_type_id, draw_number, 
                                      actual_json, predicted_json, accuracy_score))
            logger.info(f"模型评估结果插入成功: {draw_number}")
            return True
        except Exception as e:
            logger.error(f"模型评估结果插入失败: {e}")
            return False
    
    def get_prediction_models(self) -> List[Dict[str, Any]]:
        """获取预测模型列表"""
        query = "SELECT * FROM prediction_models WHERE is_active = 1"
        
        try:
            results = self.execute_query(query)
            # 解析JSON字段
            for result in results:
                if result.get('parameters'):
                    result['parameters'] = json.loads(result['parameters'])
            return results
        except Exception as e:
            logger.error(f"获取预测模型失败: {e}")
            return []
    
    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()
            logger.info("数据库连接已关闭")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 