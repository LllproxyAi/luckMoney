-- 彩票数据分析系统数据库设计
-- 创建数据库
CREATE DATABASE IF NOT EXISTS lottery_analysis DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lottery_analysis;

-- 彩票类型表
CREATE TABLE lottery_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type_code VARCHAR(20) NOT NULL UNIQUE COMMENT '彩票类型代码',
    type_name VARCHAR(50) NOT NULL COMMENT '彩票类型名称',
    description TEXT COMMENT '描述',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 开奖记录表
CREATE TABLE lottery_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    lottery_type_id INT NOT NULL COMMENT '彩票类型ID',
    draw_number VARCHAR(20) NOT NULL COMMENT '期号',
    draw_date DATE NOT NULL COMMENT '开奖日期',
    draw_time TIME COMMENT '开奖时间',
    numbers TEXT NOT NULL COMMENT '开奖号码(JSON格式)',
    sales_amount DECIMAL(15,2) COMMENT '销售额',
    prize_pool DECIMAL(15,2) COMMENT '奖池金额',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lottery_type_id) REFERENCES lottery_types(id),
    UNIQUE KEY uk_type_draw (lottery_type_id, draw_number)
);

-- 预测模型表
CREATE TABLE prediction_models (
    id INT PRIMARY KEY AUTO_INCREMENT,
    model_name VARCHAR(100) NOT NULL COMMENT '模型名称',
    model_type VARCHAR(50) NOT NULL COMMENT '模型类型',
    description TEXT COMMENT '模型描述',
    parameters TEXT COMMENT '模型参数(JSON格式)',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 预测结果表
CREATE TABLE predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT NOT NULL COMMENT '预测模型ID',
    lottery_type_id INT NOT NULL COMMENT '彩票类型ID',
    draw_number VARCHAR(20) NOT NULL COMMENT '预测期号',
    predicted_numbers TEXT NOT NULL COMMENT '预测号码(JSON格式)',
    confidence_score DECIMAL(5,4) COMMENT '置信度分数',
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '预测时间',
    FOREIGN KEY (model_id) REFERENCES prediction_models(id),
    FOREIGN KEY (lottery_type_id) REFERENCES lottery_types(id)
);

-- 模型评估表
CREATE TABLE model_evaluations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    model_id INT NOT NULL COMMENT '预测模型ID',
    lottery_type_id INT NOT NULL COMMENT '彩票类型ID',
    draw_number VARCHAR(20) NOT NULL COMMENT '开奖期号',
    actual_numbers TEXT NOT NULL COMMENT '实际开奖号码',
    predicted_numbers TEXT NOT NULL COMMENT '预测号码',
    accuracy_score DECIMAL(5,4) COMMENT '准确率分数',
    evaluation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '评估时间',
    FOREIGN KEY (model_id) REFERENCES prediction_models(id),
    FOREIGN KEY (lottery_type_id) REFERENCES lottery_types(id)
);

-- 统计分析表
CREATE TABLE statistical_analysis (
    id INT PRIMARY KEY AUTO_INCREMENT,
    lottery_type_id INT NOT NULL COMMENT '彩票类型ID',
    analysis_type VARCHAR(50) NOT NULL COMMENT '分析类型',
    analysis_data TEXT NOT NULL COMMENT '分析数据(JSON格式)',
    analysis_date DATE NOT NULL COMMENT '分析日期',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lottery_type_id) REFERENCES lottery_types(id)
);

-- 插入初始彩票类型数据
INSERT INTO lottery_types (type_code, type_name, description) VALUES
('DLT', '大乐透', '超级大乐透，前区35选5，后区12选2'),
('FC3D', '福彩3D', '福彩3D，000-999选号'),
('SSQ', '双色球', '双色球，红球33选6，蓝球16选1');

-- 插入初始预测模型数据
INSERT INTO prediction_models (model_name, model_type, description, parameters) VALUES
('频率分析模型', 'FREQUENCY', '基于历史号码出现频率的统计分析模型', '{"window_size": 100, "weight_factor": 0.8}'),
('马尔可夫链模型', 'MARKOV', '基于马尔可夫链的序列预测模型', '{"order": 3, "smoothing": 0.1}'),
('神经网络模型', 'NEURAL_NET', '基于深度学习的神经网络预测模型', '{"layers": [64, 32, 16], "epochs": 1000}'),
('时间序列模型', 'TIME_SERIES', '基于ARIMA的时间序列预测模型', '{"p": 2, "d": 1, "q": 1}'); 