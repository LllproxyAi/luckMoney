package com.moneyluck.lottery;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * 彩票数据分析系统主应用类
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@SpringBootApplication
@EnableScheduling
public class LotteryAnalysisApplication {

    public static void main(String[] args) {
        SpringApplication.run(LotteryAnalysisApplication.class, args);
        System.out.println("🎯 彩票数据分析系统启动成功！");
        System.out.println("📊 访问地址: http://localhost:8080/api");
        System.out.println("📈 管理界面: http://localhost:8080/api/admin");
    }
} 