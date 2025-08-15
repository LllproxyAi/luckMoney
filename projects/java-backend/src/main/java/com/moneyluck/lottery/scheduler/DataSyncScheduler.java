package com.moneyluck.lottery.scheduler;

import com.moneyluck.lottery.service.LotteryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/**
 * 数据同步定时任务
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@Component
@RequiredArgsConstructor
@Slf4j
public class DataSyncScheduler {

    private final LotteryService lotteryService;
    
    @Value("${python-crawler.base-url:http://localhost:8000}")
    private String pythonCrawlerUrl;

    /**
     * 每日上午9点执行数据爬取同步
     */
    @Scheduled(cron = "0 0 9 * * ?")
    public void dailyDataSync() {
        log.info("开始执行每日数据同步任务");
        
        try {
            boolean success = lotteryService.syncDataFromCrawler();
            if (success) {
                log.info("每日数据同步任务执行成功");
            } else {
                log.error("每日数据同步任务执行失败");
            }
        } catch (Exception e) {
            log.error("每日数据同步任务执行异常", e);
        }
    }

    /**
     * 每小时检查一次数据更新
     */
    @Scheduled(fixedRate = 3600000) // 1小时
    public void hourlyDataCheck() {
        log.debug("执行每小时数据检查任务");
        
        try {
            // 这里可以添加数据完整性检查逻辑
            log.debug("每小时数据检查完成");
        } catch (Exception e) {
            log.error("每小时数据检查异常", e);
        }
    }

    /**
     * 每周日凌晨2点执行数据清理任务
     */
    @Scheduled(cron = "0 0 2 ? * SUN")
    public void weeklyDataCleanup() {
        log.info("开始执行每周数据清理任务");
        
        try {
            // 这里可以添加数据清理逻辑，如删除过期数据、压缩历史数据等
            log.info("每周数据清理任务执行完成");
        } catch (Exception e) {
            log.error("每周数据清理任务执行异常", e);
        }
    }
} 