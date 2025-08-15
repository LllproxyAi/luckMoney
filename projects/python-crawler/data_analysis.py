"""
数据分析模块 - 彩票数据分析系统
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from loguru import logger
from database import DatabaseManager


class LotteryDataAnalyzer:
    """彩票数据分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.db = DatabaseManager()
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
        plt.rcParams['axes.unicode_minus'] = False
    
    def analyze_frequency_trends(self, lottery_type_id: int, limit: int = 100) -> Dict[str, Any]:
        """分析号码频率趋势"""
        try:
            results = self.db.get_lottery_results(lottery_type_id, limit)
            if not results:
                return {}
            
            # 统计号码频率
            number_counts = {}
            for result in results:
                numbers = result['numbers']
                
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
            
            # 排序
            sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)
            
            return {
                'frequency_data': sorted_numbers,
                'total_draws': len(results),
                'analysis_date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            logger.error(f"频率趋势分析失败: {e}")
            return {}
    
    def analyze_hot_cold_numbers(self, lottery_type_id: int, limit: int = 50) -> Dict[str, Any]:
        """分析冷热号码"""
        try:
            results = self.db.get_lottery_results(lottery_type_id, limit)
            if not results:
                return {}
            
            # 计算冷热指数
            hot_cold_data = {}
            total_draws = len(results)
            
            for result in results:
                numbers = result['numbers']
                
                if 'front' in numbers:  # 大乐透
                    for num in numbers['front']:
                        if num not in hot_cold_data:
                            hot_cold_data[num] = {'count': 0, 'last_appear': 0}
                        hot_cold_data[num]['count'] += 1
                        hot_cold_data[num]['last_appear'] = 0
                    
                    for num in numbers['back']:
                        if num not in hot_cold_data:
                            hot_cold_data[num] = {'count': 0, 'last_appear': 0}
                        hot_cold_data[num]['count'] += 1
                        hot_cold_data[num]['last_appear'] = 0
                
                # 更新未出现号码的间隔
                for num in hot_cold_data:
                    hot_cold_data[num]['last_appear'] += 1
            
            # 计算冷热指数
            for num in hot_cold_data:
                frequency = hot_cold_data[num]['count'] / total_draws
                interval = hot_cold_data[num]['last_appear']
                
                # 冷热指数 = 频率权重 * 0.7 + 间隔权重 * 0.3
                hot_cold_data[num]['hot_cold_index'] = frequency * 0.7 + (1 / (1 + interval)) * 0.3
            
            # 排序
            sorted_hot_cold = sorted(hot_cold_data.items(), 
                                   key=lambda x: x[1]['hot_cold_index'], reverse=True)
            
            return {
                'hot_cold_data': sorted_hot_cold,
                'total_draws': total_draws,
                'analysis_date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            logger.error(f"冷热号码分析失败: {e}")
            return {}
    
    def analyze_sum_distribution(self, lottery_type_id: int, limit: int = 100) -> Dict[str, Any]:
        """分析和值分布"""
        try:
            results = self.db.get_lottery_results(lottery_type_id, limit)
            if not results:
                return {}
            
            sum_values = []
            for result in results:
                numbers = result['numbers']
                
                if 'front' in numbers:  # 大乐透
                    front_sum = sum(int(num) for num in numbers['front'])
                    back_sum = sum(int(num) for num in numbers['back'])
                    sum_values.append({'front': front_sum, 'back': back_sum, 'total': front_sum + back_sum})
                    
                elif 'red' in numbers:  # 双色球
                    red_sum = sum(int(num) for num in numbers['red'])
                    blue_sum = int(numbers['blue'])
                    sum_values.append({'red': red_sum, 'blue': blue_sum, 'total': red_sum + blue_sum})
                    
                elif 'main' in numbers:  # 福彩3D
                    total_sum = numbers['hundred'] + numbers['ten'] + numbers['unit']
                    sum_values.append({'total': total_sum})
            
            # 统计分布
            if sum_values:
                total_sums = [item['total'] for item in sum_values]
                sum_distribution = {
                    'min': min(total_sums),
                    'max': max(total_sums),
                    'mean': round(np.mean(total_sums), 2),
                    'median': round(np.median(total_sums), 2),
                    'std': round(np.std(total_sums), 2),
                    'distribution': pd.Series(total_sums).value_counts().to_dict()
                }
                
                return {
                    'sum_distribution': sum_distribution,
                    'sum_values': sum_values,
                    'total_draws': len(results),
                    'analysis_date': datetime.now().strftime('%Y-%m-%d')
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"和值分布分析失败: {e}")
            return {}
    
    def analyze_odd_even_distribution(self, lottery_type_id: int, limit: int = 100) -> Dict[str, Any]:
        """分析奇偶分布"""
        try:
            results = self.db.get_lottery_results(lottery_type_id, limit)
            if not results:
                return {}
            
            odd_even_stats = []
            for result in results:
                numbers = result['numbers']
                
                if 'front' in numbers:  # 大乐透
                    front_odd = sum(1 for num in numbers['front'] if int(num) % 2 == 1)
                    front_even = 5 - front_odd
                    back_odd = sum(1 for num in numbers['back'] if int(num) % 2 == 1)
                    back_even = 2 - back_odd
                    
                    odd_even_stats.append({
                        'front_odd': front_odd,
                        'front_even': front_even,
                        'back_odd': back_odd,
                        'back_even': back_even,
                        'total_odd': front_odd + back_odd,
                        'total_even': front_even + back_even
                    })
                    
                elif 'red' in numbers:  # 双色球
                    red_odd = sum(1 for num in numbers['red'] if int(num) % 2 == 1)
                    red_even = 6 - red_odd
                    blue_odd = 1 if int(numbers['blue']) % 2 == 1 else 0
                    blue_even = 1 - blue_odd
                    
                    odd_even_stats.append({
                        'red_odd': red_odd,
                        'red_even': red_even,
                        'blue_odd': blue_odd,
                        'blue_even': blue_even,
                        'total_odd': red_odd + blue_odd,
                        'total_even': red_even + blue_even
                    })
                    
                elif 'main' in numbers:  # 福彩3D
                    odd_count = sum(1 for digit in [numbers['hundred'], numbers['ten'], numbers['unit']] 
                                 if digit % 2 == 1)
                    even_count = 3 - odd_count
                    
                    odd_even_stats.append({
                        'odd': odd_count,
                        'even': even_count
                    })
            
            # 统计奇偶分布
            if odd_even_stats:
                distribution = {}
                for key in odd_even_stats[0].keys():
                    values = [item[key] for item in odd_even_stats]
                    distribution[key] = {
                        'counts': pd.Series(values).value_counts().to_dict(),
                        'mean': round(np.mean(values), 2)
                    }
                
                return {
                    'odd_even_distribution': distribution,
                    'odd_even_stats': odd_even_stats,
                    'total_draws': len(results),
                    'analysis_date': datetime.now().strftime('%Y-%m-%d')
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"奇偶分布分析失败: {e}")
            return {}
    
    def generate_frequency_chart(self, lottery_type_id: int, limit: int = 50) -> str:
        """生成频率分析图表"""
        try:
            frequency_data = self.analyze_frequency_trends(lottery_type_id, limit)
            if not frequency_data:
                return ""
            
            # 创建图表
            numbers, counts = zip(*frequency_data['frequency_data'][:20])  # 取前20个
            
            plt.figure(figsize=(12, 6))
            bars = plt.bar(range(len(numbers)), counts, color='skyblue', alpha=0.7)
            plt.xlabel('号码')
            plt.ylabel('出现次数')
            plt.title(f'号码出现频率分析 (最近{limit}期)')
            plt.xticks(range(len(numbers)), numbers, rotation=45)
            
            # 添加数值标签
            for bar, count in zip(bars, counts):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        str(count), ha='center', va='bottom')
            
            plt.tight_layout()
            
            # 保存图表
            filename = f"frequency_chart_{lottery_type_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
            
        except Exception as e:
            logger.error(f"生成频率图表失败: {e}")
            return ""
    
    def generate_hot_cold_chart(self, lottery_type_id: int, limit: int = 50) -> str:
        """生成冷热号码图表"""
        try:
            hot_cold_data = self.analyze_hot_cold_numbers(lottery_type_id, limit)
            if not hot_cold_data:
                return ""
            
            # 创建图表
            numbers = [item[0] for item in hot_cold_data['hot_cold_data'][:20]]
            indices = [item[1]['hot_cold_index'] for item in hot_cold_data['hot_cold_data'][:20]]
            
            plt.figure(figsize=(12, 6))
            colors = ['red' if idx > 0.5 else 'blue' if idx < 0.3 else 'orange' 
                     for idx in indices]
            
            bars = plt.bar(range(len(numbers)), indices, color=colors, alpha=0.7)
            plt.xlabel('号码')
            plt.ylabel('冷热指数')
            plt.title(f'号码冷热分析 (最近{limit}期)')
            plt.xticks(range(len(numbers)), numbers, rotation=45)
            plt.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='热号分界线')
            plt.axhline(y=0.3, color='blue', linestyle='--', alpha=0.5, label='冷号分界线')
            plt.legend()
            
            plt.tight_layout()
            
            # 保存图表
            filename = f"hot_cold_chart_{lottery_type_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
            
        except Exception as e:
            logger.error(f"生成冷热号码图表失败: {e}")
            return ""
    
    def generate_sum_distribution_chart(self, lottery_type_id: int, limit: int = 100) -> str:
        """生成和值分布图表"""
        try:
            sum_data = self.analyze_sum_distribution(lottery_type_id, limit)
            if not sum_data:
                return ""
            
            # 创建图表
            total_sums = [item['total'] for item in sum_data['sum_values']]
            
            plt.figure(figsize=(12, 6))
            plt.hist(total_sums, bins=20, color='lightgreen', alpha=0.7, edgecolor='black')
            plt.xlabel('和值')
            plt.ylabel('频次')
            plt.title(f'和值分布分析 (最近{limit}期)')
            plt.axvline(x=sum_data['sum_distribution']['mean'], color='red', 
                       linestyle='--', label=f'平均值: {sum_data["sum_distribution"]["mean"]}')
            plt.legend()
            
            plt.tight_layout()
            
            # 保存图表
            filename = f"sum_distribution_chart_{lottery_type_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filename
            
        except Exception as e:
            logger.error(f"生成和值分布图表失败: {e}")
            return ""
    
    def close(self):
        """关闭分析器"""
        self.db.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close() 