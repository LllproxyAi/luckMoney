#!/usr/bin/env python3
"""
MySQL连接测试脚本
测试局域网MySQL连接状态
"""
import pymysql
import sys
from datetime import datetime

# MySQL连接配置
MYSQL_CONFIG = {
    'host': '192.168.1.34',
    'port': 3306,
    'user': 'root',
    'password': '20210808',
    'charset': 'utf8mb4',
    'connect_timeout': 10
}

def test_mysql_connection():
    """测试MySQL连接"""
    print("🔍 开始测试MySQL连接...")
    print(f"📊 连接信息:")
    print(f"   主机: {MYSQL_CONFIG['host']}")
    print(f"   端口: {MYSQL_CONFIG['port']}")
    print(f"   用户: {MYSQL_CONFIG['user']}")
    print(f"   密码: {'*' * len(MYSQL_CONFIG['password'])}")
    print(f"   超时: {MYSQL_CONFIG['connect_timeout']}秒")
    print("-" * 50)
    
    try:
        # 尝试连接MySQL
        print("🔄 正在连接MySQL...")
        connection = pymysql.connect(**MYSQL_CONFIG)
        
        if connection:
            print("✅ MySQL连接成功!")
            
            # 获取MySQL版本信息
            with connection.cursor() as cursor:
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()
                print(f"📋 MySQL版本: {version[0]}")
            
            # 获取数据库列表
            with connection.cursor() as cursor:
                cursor.execute("SHOW DATABASES")
                databases = cursor.fetchall()
                print(f"📁 数据库列表 ({len(databases)}个):")
                for db in databases:
                    print(f"   - {db[0]}")
            
            # 检查lottery_analysis数据库是否存在
            db_names = [db[0] for db in databases]
            if 'lottery_analysis' in db_names:
                print("✅ lottery_analysis数据库存在")
                
                # 切换到lottery_analysis数据库
                connection.select_db('lottery_analysis')
                
                # 获取表列表
                with connection.cursor() as cursor:
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()
                    print(f"📋 数据表列表 ({len(tables)}个):")
                    for table in tables:
                        print(f"   - {table[0]}")
                
                # 检查关键表是否存在
                table_names = [table[0] for table in tables]
                required_tables = ['lottery_types', 'lottery_results', 'prediction_models']
                
                print("\n🔍 检查必需的数据表:")
                for table in required_tables:
                    if table in table_names:
                        print(f"   ✅ {table} - 存在")
                    else:
                        print(f"   ❌ {table} - 不存在")
                
                # 测试查询数据
                print("\n📊 测试数据查询:")
                
                # 查询彩票类型
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) FROM lottery_types")
                        count = cursor.fetchone()
                        print(f"   📈 lottery_types表记录数: {count[0]}")
                        
                        if count[0] > 0:
                            cursor.execute("SELECT type_code, type_name FROM lottery_types LIMIT 3")
                            types = cursor.fetchall()
                            print("   📋 彩票类型示例:")
                            for t in types:
                                print(f"      - {t[0]}: {t[1]}")
                except Exception as e:
                    print(f"   ⚠️  查询lottery_types失败: {e}")
                
                # 查询开奖结果
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) FROM lottery_results")
                        count = cursor.fetchone()
                        print(f"   📈 lottery_results表记录数: {count[0]}")
                except Exception as e:
                    print(f"   ⚠️  查询lottery_results失败: {e}")
                
                # 查询预测模型
                try:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT COUNT(*) FROM prediction_models")
                        count = cursor.fetchone()
                        print(f"   📈 prediction_models表记录数: {count[0]}")
                except Exception as e:
                    print(f"   ⚠️  查询prediction_models失败: {e}")
                
            else:
                print("⚠️  lottery_analysis数据库不存在")
                print("💡 建议执行数据库初始化脚本")
            
            # 测试网络延迟
            print("\n🌐 测试网络性能:")
            start_time = datetime.now()
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            
            end_time = datetime.now()
            latency = (end_time - start_time).total_seconds() * 1000
            print(f"   ⏱️  网络延迟: {latency:.2f}ms")
            
            if latency < 100:
                print("   ✅ 网络延迟正常")
            elif latency < 500:
                print("   ⚠️  网络延迟较高")
            else:
                print("   ❌ 网络延迟过高")
            
            connection.close()
            print("\n✅ MySQL连接测试完成!")
            return True
            
    except pymysql.Error as e:
        print(f"❌ MySQL连接失败: {e}")
        print(f"   错误代码: {e.args[0]}")
        print(f"   错误信息: {e.args[1]}")
        
        # 提供故障排除建议
        print("\n🔧 故障排除建议:")
        if "Can't connect to MySQL server" in str(e):
            print("   - 检查MySQL服务是否启动")
            print("   - 检查IP地址和端口是否正确")
            print("   - 检查防火墙设置")
        elif "Access denied" in str(e):
            print("   - 检查用户名和密码是否正确")
            print("   - 检查用户权限设置")
        elif "Unknown database" in str(e):
            print("   - 检查数据库是否存在")
            print("   - 执行数据库创建脚本")
        
        return False
    
    except Exception as e:
        print(f"❌ 连接测试异常: {e}")
        return False

def test_python_crawler_config():
    """测试Python爬虫配置"""
    print("\n🕷️  测试Python爬虫配置...")
    
    try:
        # 导入配置
        sys.path.append('python-crawler')
        from config import DATABASE_CONFIG
        
        print(f"📋 当前爬虫配置:")
        print(f"   主机: {DATABASE_CONFIG['host']}")
        print(f"   端口: {DATABASE_CONFIG['port']}")
        print(f"   用户: {DATABASE_CONFIG['user']}")
        print(f"   数据库: {DATABASE_CONFIG['database']}")
        
        # 检查配置是否匹配
        if (DATABASE_CONFIG['host'] == MYSQL_CONFIG['host'] and 
            DATABASE_CONFIG['port'] == MYSQL_CONFIG['port'] and
            DATABASE_CONFIG['user'] == MYSQL_CONFIG['user']):
            print("✅ 爬虫配置与测试配置匹配")
        else:
            print("⚠️  爬虫配置与测试配置不匹配")
            print("💡 建议更新python-crawler/config.py中的配置")
        
    except Exception as e:
        print(f"❌ 测试爬虫配置失败: {e}")

def main():
    """主函数"""
    print("🎯 MySQL连接测试工具")
    print("=" * 60)
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 测试MySQL连接
    connection_ok = test_mysql_connection()
    
    # 测试Python爬虫配置
    test_python_crawler_config()
    
    print("\n" + "=" * 60)
    print("📊 测试结果总结:")
    print(f"   MySQL连接: {'✅ 成功' if connection_ok else '❌ 失败'}")
    
    if connection_ok:
        print("\n🎉 MySQL连接正常！可以继续部署其他服务。")
        print("💡 下一步建议:")
        print("   1. 运行Python爬虫服务测试")
        print("   2. 启动Java后端服务")
        print("   3. 启动React前端服务")
    else:
        print("\n❌ MySQL连接失败，请检查配置后重试。")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 