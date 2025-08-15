#!/usr/bin/env python3
"""
数据库连接测试脚本
用于验证MySQL连接和数据库表结构
"""
import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DATABASE_CONFIG
from database import DatabaseManager
from loguru import logger

def test_database_connection():
    """测试数据库连接"""
    print("🔍 开始测试数据库连接...")
    print(f"📊 连接配置: {DATABASE_CONFIG}")
    
    try:
        # 测试连接
        with DatabaseManager() as db:
            print("✅ 数据库连接成功!")
            
            # 测试查询彩票类型
            print("\n📋 测试查询彩票类型...")
            lottery_types = db.get_lottery_types()
            if lottery_types:
                print(f"✅ 找到 {len(lottery_types)} 个彩票类型:")
                for lt in lottery_types:
                    print(f"   - {lt['type_code']}: {lt['type_name']}")
            else:
                print("⚠️  未找到彩票类型数据")
            
            # 测试查询预测模型
            print("\n🤖 测试查询预测模型...")
            models = db.get_prediction_models()
            if models:
                print(f"✅ 找到 {len(models)} 个预测模型:")
                for model in models:
                    print(f"   - {model['model_name']}: {model['model_type']}")
            else:
                print("⚠️  未找到预测模型数据")
                
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False
    
    return True

def test_crawler_functionality():
    """测试爬虫功能"""
    print("\n🕷️  开始测试爬虫功能...")
    
    try:
        from crawler import LotteryCrawler
        
        # 创建爬虫实例
        crawler = LotteryCrawler()
        print("✅ 爬虫实例创建成功")
        
        # 测试获取彩票类型
        lottery_types = crawler.db.get_lottery_types()
        if lottery_types:
            print(f"✅ 获取到 {len(lottery_types)} 个彩票类型")
            
            # 测试爬取大乐透数据（模拟）
            print("\n🎯 测试爬取大乐透数据...")
            dlt_data = crawler.crawl_dlt_data(pages=1)  # 只爬取1页
            if dlt_data:
                print(f"✅ 成功爬取 {len(dlt_data)} 条大乐透数据")
                print(f"   示例数据: {dlt_data[0] if dlt_data else '无'}")
            else:
                print("⚠️  大乐透数据爬取失败")
        
        crawler.close()
        
    except Exception as e:
        print(f"❌ 爬虫功能测试失败: {e}")
        return False
    
    return True

def test_prediction_models():
    """测试预测模型"""
    print("\n🔮 开始测试预测模型...")
    
    try:
        from prediction_models import PredictionModelFactory
        
        # 测试创建频率分析模型
        model = PredictionModelFactory.create_model("FREQUENCY")
        print("✅ 频率分析模型创建成功")
        
        # 测试模型训练（使用模拟数据）
        test_data = [
            {
                'numbers': {
                    'front': ['01', '05', '12', '23', '35'],
                    'back': ['03', '08']
                }
            },
            {
                'numbers': {
                    'front': ['02', '08', '15', '28', '33'],
                    'back': ['05', '11']
                }
            }
        ]
        
        if model.train(test_data):
            print("✅ 模型训练成功")
            
            # 测试预测
            prediction = model.predict(test_data)
            if prediction:
                print(f"✅ 预测成功: {prediction}")
            else:
                print("⚠️  预测失败")
        else:
            print("⚠️  模型训练失败")
            
    except Exception as e:
        print(f"❌ 预测模型测试失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("🎯 彩票数据分析系统 - Python爬虫服务测试")
    print("=" * 50)
    
    # 测试数据库连接
    db_ok = test_database_connection()
    
    if db_ok:
        # 测试爬虫功能
        crawler_ok = test_crawler_functionality()
        
        # 测试预测模型
        model_ok = test_prediction_models()
        
        print("\n" + "=" * 50)
        print("📊 测试结果总结:")
        print(f"   数据库连接: {'✅ 成功' if db_ok else '❌ 失败'}")
        print(f"   爬虫功能: {'✅ 成功' if crawler_ok else '❌ 失败'}")
        print(f"   预测模型: {'✅ 成功' if model_ok else '❌ 失败'}")
        
        if all([db_ok, crawler_ok, model_ok]):
            print("\n🎉 所有测试通过！爬虫服务可以正常使用。")
        else:
            print("\n⚠️  部分测试失败，请检查相关配置。")
    else:
        print("\n❌ 数据库连接失败，无法进行其他测试。")
        print("请检查MySQL配置和连接信息。")

if __name__ == "__main__":
    main() 