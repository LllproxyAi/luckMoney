#!/usr/bin/env python3
"""
初始化数据库：创建表结构和初始数据
"""
import sys
import os
import pymysql

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DATABASE_CONFIG

DDL_STATEMENTS = [
    # 彩票类型表
    """
    CREATE TABLE IF NOT EXISTS lottery_types (
        id INT PRIMARY KEY AUTO_INCREMENT,
        type_code VARCHAR(20) NOT NULL UNIQUE,
        type_name VARCHAR(50) NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    # 开奖记录表
    """
    CREATE TABLE IF NOT EXISTS lottery_results (
        id INT PRIMARY KEY AUTO_INCREMENT,
        lottery_type_id INT NOT NULL,
        draw_number VARCHAR(20) NOT NULL,
        draw_date DATE NOT NULL,
        draw_time TIME NULL,
        numbers TEXT NOT NULL,
        sales_amount DECIMAL(15,2) NULL,
        prize_pool DECIMAL(15,2) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uk_type_draw (lottery_type_id, draw_number),
        CONSTRAINT fk_result_type FOREIGN KEY (lottery_type_id) REFERENCES lottery_types(id)
            ON DELETE RESTRICT ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    # 预测模型表
    """
    CREATE TABLE IF NOT EXISTS prediction_models (
        id INT PRIMARY KEY AUTO_INCREMENT,
        model_name VARCHAR(100) NOT NULL,
        model_type VARCHAR(50) NOT NULL,
        description TEXT,
        parameters TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    # 预测结果表
    """
    CREATE TABLE IF NOT EXISTS predictions (
        id INT PRIMARY KEY AUTO_INCREMENT,
        model_id INT NOT NULL,
        lottery_type_id INT NOT NULL,
        draw_number VARCHAR(20) NOT NULL,
        predicted_numbers TEXT NOT NULL,
        confidence_score DECIMAL(5,4) NULL,
        prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_pred_model FOREIGN KEY (model_id) REFERENCES prediction_models(id),
        CONSTRAINT fk_pred_type FOREIGN KEY (lottery_type_id) REFERENCES lottery_types(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """,
    # 模型评估表
    """
    CREATE TABLE IF NOT EXISTS model_evaluations (
        id INT PRIMARY KEY AUTO_INCREMENT,
        model_id INT NOT NULL,
        lottery_type_id INT NOT NULL,
        draw_number VARCHAR(20) NOT NULL,
        actual_numbers TEXT NOT NULL,
        predicted_numbers TEXT NOT NULL,
        accuracy_score DECIMAL(5,4) NOT NULL,
        evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_eval_model FOREIGN KEY (model_id) REFERENCES prediction_models(id),
        CONSTRAINT fk_eval_type FOREIGN KEY (lottery_type_id) REFERENCES lottery_types(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
]

SEED_STATEMENTS = [
    # 彩票类型
    ("INSERT IGNORE INTO lottery_types(type_code, type_name, description) VALUES(%s,%s,%s)",
     [("DLT", "大乐透", "超级大乐透，前区35选5，后区12选2"),
      ("FC3D", "福彩3D", "福彩3D，000-999选号"),
      ("SSQ", "双色球", "双色球，红球33选6，蓝球16选1")]),
    # 预测模型
    ("INSERT IGNORE INTO prediction_models(model_name, model_type, description, parameters, is_active) VALUES(%s,%s,%s,%s,1)",
     [("频率分析模型", "FREQUENCY", "基于历史号码出现频率的统计分析模型", '{"window_size":100,"weight_factor":0.8}'),
      ("马尔可夫链模型", "MARKOV", "基于马尔可夫链的序列预测模型", '{"order":3,"smoothing":0.1}'),
      ("神经网络模型", "NEURAL_NET", "基于深度学习的神经网络预测模型", '{"layers":[64,32,16],"epochs":1000}'),
      ("时间序列模型", "TIME_SERIES", "基于ARIMA的时间序列预测模型", '{"p":2,"d":1,"q":1}')])
]

def main():
    print("🔧 初始化数据库(创建表+种子数据)...")
    print(f"📍 连接: {DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']} / DB={DATABASE_CONFIG['database']}  用户={DATABASE_CONFIG['user']}")

    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        with conn.cursor() as cur:
            for ddl in DDL_STATEMENTS:
                cur.execute(ddl)
            conn.commit()
            print("✅ 表结构创建完成")
            
            for sql, params_list in SEED_STATEMENTS:
                cur.executemany(sql, params_list)
            conn.commit()
            print("✅ 初始数据插入完成")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)
    finally:
        try:
            conn.close()
        except Exception:
            pass
    print("🎉 初始化完成！")

if __name__ == '__main__':
    main()
