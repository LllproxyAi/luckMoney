"""
预测模型模块 - 彩票数据分析系统
"""
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from loguru import logger
from config import MODEL_CONFIG


class BasePredictionModel:
    """预测模型基类"""
    
    def __init__(self, model_name: str, model_type: str):
        """初始化模型"""
        self.model_name = model_name
        self.model_type = model_type
        self.is_trained = False
    
    def train(self, data: List[Dict[str, Any]]) -> bool:
        """训练模型"""
        raise NotImplementedError("子类必须实现train方法")
    
    def predict(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """预测结果"""
        raise NotImplementedError("子类必须实现predict方法")
    
    def evaluate(self, actual: Dict[str, Any], predicted: Dict[str, Any]) -> float:
        """评估模型准确率"""
        raise NotImplementedError("子类必须实现evaluate方法")


class FrequencyAnalysisModel(BasePredictionModel):
    """频率分析模型"""
    
    def __init__(self):
        """初始化频率分析模型"""
        super().__init__("频率分析模型", "FREQUENCY")
        self.frequency_data = {}
        self.config = MODEL_CONFIG['frequency_model']
    
    def train(self, data: List[Dict[str, Any]]) -> bool:
        """训练频率分析模型"""
        try:
            logger.info("开始训练频率分析模型")
            
            # 统计号码出现频率
            number_counts = {}
            total_draws = len(data)
            
            for result in data:
                numbers = result['numbers']
                
                # 处理不同类型的彩票
                if 'front' in numbers:  # 大乐透
                    for num in numbers['front']:
                        number_counts[num] = number_counts.get(num, 0) + 1
                    for num in numbers['back']:
                        number_counts[num] = number_counts.get(num, 0) + 1
                
                elif 'red' in numbers:  # 双色球
                    for num in numbers['red']:
                        number_counts[num] = number_counts.get(num, 0) + 1
                    number_counts[numbers['blue']] = number_counts.get(numbers['blue'], 0) + 1
                
                elif 'main' in numbers:  # 福彩3D
                    for digit in [numbers['hundred'], numbers['ten'], numbers['unit']]:
                        number_counts[str(digit)] = number_counts.get(str(digit), 0) + 1
            
            # 计算加权频率
            self.frequency_data = {}
            for num, count in number_counts.items():
                frequency = count / total_draws
                weighted_frequency = frequency * self.config['weight_factor']
                self.frequency_data[num] = weighted_frequency
            
            self.is_trained = True
            logger.info("频率分析模型训练完成")
            return True
            
        except Exception as e:
            logger.error(f"频率分析模型训练失败: {e}")
            return False
    
    def predict(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """基于频率预测"""
        if not self.is_trained:
            raise ValueError("模型尚未训练")
        
        try:
            # 获取最近的开奖数据来确定彩票类型
            latest_result = data[0] if data else {}
            numbers = latest_result.get('numbers', {})
            
            if 'front' in numbers:  # 大乐透
                return self._predict_dlt()
            elif 'red' in numbers:  # 双色球
                return self._predict_ssq()
            elif 'main' in numbers:  # 福彩3D
                return self._predict_fc3d()
            else:
                raise ValueError("未知的彩票类型")
                
        except Exception as e:
            logger.error(f"频率分析预测失败: {e}")
            return {}
    
    def _predict_dlt(self) -> Dict[str, Any]:
        """预测大乐透"""
        # 按频率排序选择号码
        sorted_numbers = sorted(self.frequency_data.items(), 
                              key=lambda x: x[1], reverse=True)
        
        # 前区选择5个号码
        front_numbers = [num for num, _ in sorted_numbers[:35]][:5]
        front_numbers.sort()
        
        # 后区选择2个号码
        back_numbers = [num for num, _ in sorted_numbers[:12]][:2]
        back_numbers.sort()
        
        return {
            'front': front_numbers,
            'back': back_numbers,
            'confidence': 0.75
        }
    
    def _predict_ssq(self) -> Dict[str, Any]:
        """预测双色球"""
        sorted_numbers = sorted(self.frequency_data.items(), 
                              key=lambda x: x[1], reverse=True)
        
        # 红球选择6个号码
        red_numbers = [num for num, _ in sorted_numbers[:33]][:6]
        red_numbers.sort()
        
        # 蓝球选择1个号码
        blue_number = sorted_numbers[0][0] if sorted_numbers else "01"
        
        return {
            'red': red_numbers,
            'blue': blue_number,
            'confidence': 0.70
        }
    
    def _predict_fc3d(self) -> Dict[str, Any]:
        """预测福彩3D"""
        sorted_numbers = sorted(self.frequency_data.items(), 
                              key=lambda x: x[1], reverse=True)
        
        # 选择3个数字
        selected_digits = [num for num, _ in sorted_numbers[:10]][:3]
        
        return {
            'main': ''.join(selected_digits),
            'hundred': int(selected_digits[0]),
            'ten': int(selected_digits[1]),
            'unit': int(selected_digits[2]),
            'confidence': 0.65
        }
    
    def evaluate(self, actual: Dict[str, Any], predicted: Dict[str, Any]) -> float:
        """评估准确率"""
        try:
            if 'front' in actual:  # 大乐透
                front_match = len(set(actual['front']) & set(predicted['front']))
                back_match = len(set(actual['back']) & set(predicted['back']))
                accuracy = (front_match / 5 + back_match / 2) / 2
                
            elif 'red' in actual:  # 双色球
                red_match = len(set(actual['red']) & set(predicted['red']))
                blue_match = 1 if actual['blue'] == predicted['blue'] else 0
                accuracy = (red_match / 6 + blue_match) / 2
                
            elif 'main' in actual:  # 福彩3D
                digit_matches = 0
                if actual['hundred'] == predicted['hundred']:
                    digit_matches += 1
                if actual['ten'] == predicted['ten']:
                    digit_matches += 1
                if actual['unit'] == predicted['unit']:
                    digit_matches += 1
                accuracy = digit_matches / 3
                
            else:
                accuracy = 0.0
            
            return round(accuracy, 4)
            
        except Exception as e:
            logger.error(f"准确率评估失败: {e}")
            return 0.0


class PredictionModelFactory:
    """预测模型工厂"""
    
    @staticmethod
    def create_model(model_type: str) -> BasePredictionModel:
        """创建预测模型"""
        if model_type == "FREQUENCY":
            return FrequencyAnalysisModel()
        else:
            raise ValueError(f"未知的模型类型: {model_type}") 