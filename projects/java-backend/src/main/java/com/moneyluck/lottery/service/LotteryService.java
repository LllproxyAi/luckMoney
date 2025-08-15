package com.moneyluck.lottery.service;

import com.moneyluck.lottery.dto.LotteryResultDTO;
import com.moneyluck.lottery.entity.LotteryResult;
import com.moneyluck.lottery.entity.LotteryType;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/**
 * 彩票服务接口
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
public interface LotteryService {
    
    /**
     * 获取所有彩票类型
     */
    List<LotteryType> getAllLotteryTypes();
    
    /**
     * 根据ID获取彩票类型
     */
    LotteryType getLotteryTypeById(Long id);
    
    /**
     * 根据类型代码获取彩票类型
     */
    LotteryType getLotteryTypeByCode(String typeCode);
    
    /**
     * 分页获取开奖结果
     */
    Page<LotteryResult> getLotteryResults(Long lotteryTypeId, LocalDate startDate, 
                                         LocalDate endDate, Pageable pageable);
    
    /**
     * 根据期号获取开奖结果
     */
    LotteryResult getLotteryResultByDrawNumber(String drawNumber);
    
    /**
     * 获取最新开奖结果
     */
    List<LotteryResult> getLatestLotteryResults(int limit);
    
    /**
     * 添加开奖结果
     */
    LotteryResult addLotteryResult(LotteryResultDTO resultDTO);
    
    /**
     * 更新开奖结果
     */
    LotteryResult updateLotteryResult(Long id, LotteryResultDTO resultDTO);
    
    /**
     * 删除开奖结果
     */
    boolean deleteLotteryResult(Long id);
    
    /**
     * 获取统计数据
     */
    Map<String, Object> getStatistics(Long lotteryTypeId);
    
    /**
     * 批量导入开奖结果
     */
    List<LotteryResult> batchImportResults(List<LotteryResultDTO> results);
    
    /**
     * 数据同步（从Python爬虫服务）
     */
    boolean syncDataFromCrawler();
} 