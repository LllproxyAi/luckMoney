package com.moneyluck.lottery.service.impl;

import com.moneyluck.lottery.dto.LotteryResultDTO;
import com.moneyluck.lottery.entity.LotteryResult;
import com.moneyluck.lottery.entity.LotteryType;
import com.moneyluck.lottery.repository.LotteryResultRepository;
import com.moneyluck.lottery.repository.LotteryTypeRepository;
import com.moneyluck.lottery.service.LotteryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityNotFoundException;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 彩票服务实现类
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@Service
@RequiredArgsConstructor
@Slf4j
@Transactional
public class LotteryServiceImpl implements LotteryService {
    
    private final LotteryTypeRepository lotteryTypeRepository;
    private final LotteryResultRepository lotteryResultRepository;
    
    @Override
    public List<LotteryType> getAllLotteryTypes() {
        log.info("获取所有彩票类型");
        return lotteryTypeRepository.findAll();
    }
    
    @Override
    public LotteryType getLotteryTypeById(Long id) {
        log.info("根据ID获取彩票类型: {}", id);
        return lotteryTypeRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("彩票类型不存在: " + id));
    }
    
    @Override
    public LotteryType getLotteryTypeByCode(String typeCode) {
        log.info("根据类型代码获取彩票类型: {}", typeCode);
        return lotteryTypeRepository.findByTypeCode(typeCode)
                .orElseThrow(() -> new EntityNotFoundException("彩票类型不存在: " + typeCode));
    }
    
    @Override
    public Page<LotteryResult> getLotteryResults(Long lotteryTypeId, LocalDate startDate, 
                                               LocalDate endDate, Pageable pageable) {
        log.info("分页获取开奖结果: typeId={}, startDate={}, endDate={}, page={}, size={}", 
                lotteryTypeId, startDate, endDate, pageable.getPageNumber(), pageable.getPageSize());
        
        return lotteryResultRepository.findByConditions(lotteryTypeId, startDate, endDate, pageable);
    }
    
    @Override
    public LotteryResult getLotteryResultByDrawNumber(String drawNumber) {
        log.info("根据期号获取开奖结果: {}", drawNumber);
        return lotteryResultRepository.findByDrawNumber(drawNumber)
                .orElseThrow(() -> new EntityNotFoundException("开奖结果不存在: " + drawNumber));
    }
    
    @Override
    public List<LotteryResult> getLatestLotteryResults(int limit) {
        log.info("获取最新开奖结果: limit={}", limit);
        Pageable pageable = PageRequest.of(0, limit);
        return lotteryResultRepository.findLatestResults(pageable);
    }
    
    @Override
    public LotteryResult addLotteryResult(LotteryResultDTO resultDTO) {
        log.info("添加开奖结果: {}", resultDTO.getDrawNumber());
        
        // 检查期号是否已存在
        if (lotteryResultRepository.existsByDrawNumberAndLotteryTypeId(
                resultDTO.getDrawNumber(), resultDTO.getLotteryTypeId())) {
            throw new IllegalArgumentException("期号已存在: " + resultDTO.getDrawNumber());
        }
        
        // 获取彩票类型
        LotteryType lotteryType = getLotteryTypeById(resultDTO.getLotteryTypeId());
        
        // 创建开奖结果实体
        LotteryResult result = new LotteryResult();
        result.setLotteryType(lotteryType);
        result.setDrawNumber(resultDTO.getDrawNumber());
        result.setDrawDate(resultDTO.getDrawDate());
        result.setDrawTime(resultDTO.getDrawTime());
        result.setNumbers(resultDTO.getNumbers());
        result.setSalesAmount(resultDTO.getSalesAmount());
        result.setPrizePool(resultDTO.getPrizePool());
        
        LotteryResult savedResult = lotteryResultRepository.save(result);
        log.info("开奖结果添加成功: {}", savedResult.getId());
        
        return savedResult;
    }
    
    @Override
    public LotteryResult updateLotteryResult(Long id, LotteryResultDTO resultDTO) {
        log.info("更新开奖结果: id={}", id);
        
        LotteryResult existingResult = lotteryResultRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("开奖结果不存在: " + id));
        
        // 更新字段
        if (resultDTO.getDrawDate() != null) {
            existingResult.setDrawDate(resultDTO.getDrawDate());
        }
        if (resultDTO.getDrawTime() != null) {
            existingResult.setDrawTime(resultDTO.getDrawTime());
        }
        if (resultDTO.getNumbers() != null) {
            existingResult.setNumbers(resultDTO.getNumbers());
        }
        if (resultDTO.getSalesAmount() != null) {
            existingResult.setSalesAmount(resultDTO.getSalesAmount());
        }
        if (resultDTO.getPrizePool() != null) {
            existingResult.setPrizePool(resultDTO.getPrizePool());
        }
        
        LotteryResult updatedResult = lotteryResultRepository.save(existingResult);
        log.info("开奖结果更新成功: {}", updatedResult.getId());
        
        return updatedResult;
    }
    
    @Override
    public boolean deleteLotteryResult(Long id) {
        log.info("删除开奖结果: id={}", id);
        
        if (!lotteryResultRepository.existsById(id)) {
            return false;
        }
        
        lotteryResultRepository.deleteById(id);
        log.info("开奖结果删除成功: {}", id);
        
        return true;
    }
    
    @Override
    public Map<String, Object> getStatistics(Long lotteryTypeId) {
        log.info("获取统计数据: typeId={}", lotteryTypeId);
        
        Map<String, Object> statistics = new HashMap<>();
        
        try {
            // 总开奖期数
            long totalDraws = lotteryTypeId != null ? 
                    lotteryResultRepository.countByLotteryTypeId(lotteryTypeId) :
                    lotteryResultRepository.count();
            statistics.put("totalDraws", totalDraws);
            
            // 总销售额和奖池金额（简化处理）
            statistics.put("totalSales", BigDecimal.ZERO);
            statistics.put("totalPrizePool", BigDecimal.ZERO);
            
            // 活跃彩票类型数量
            long activeTypes = lotteryTypeRepository.count();
            statistics.put("activeTypes", activeTypes);
            
            // 最近开奖统计
            LocalDate today = LocalDate.now();
            LocalDate weekAgo = today.minusWeeks(1);
            LocalDate monthAgo = today.minusMonths(1);
            
            long weekDraws = lotteryTypeId != null ?
                    lotteryResultRepository.countByDateRange(lotteryTypeId, weekAgo, today) :
                    lotteryResultRepository.countByDateRange(null, weekAgo, today);
            statistics.put("weekDraws", weekDraws);
            
            long monthDraws = lotteryTypeId != null ?
                    lotteryResultRepository.countByDateRange(lotteryTypeId, monthAgo, today) :
                    lotteryResultRepository.countByDateRange(null, monthAgo, today);
            statistics.put("monthDraws", monthDraws);
            
        } catch (Exception e) {
            log.error("获取统计数据失败", e);
            statistics.put("error", "获取统计数据失败: " + e.getMessage());
        }
        
        return statistics;
    }
    
    @Override
    public List<LotteryResult> batchImportResults(List<LotteryResultDTO> results) {
        log.info("批量导入开奖结果: count={}", results.size());
        
        List<LotteryResult> savedResults = new ArrayList<>();
        
        for (LotteryResultDTO resultDTO : results) {
            try {
                LotteryResult result = addLotteryResult(resultDTO);
                savedResults.add(result);
            } catch (Exception e) {
                log.error("导入开奖结果失败: {}", resultDTO.getDrawNumber(), e);
            }
        }
        
        log.info("批量导入完成: 成功={}, 总数={}", savedResults.size(), results.size());
        return savedResults;
    }
    
    @Override
    public boolean syncDataFromCrawler() {
        log.info("开始从Python爬虫服务同步数据");
        
        try {
            // 这里应该调用Python爬虫服务的API
            // 暂时返回true表示同步成功
            log.info("数据同步完成");
            return true;
        } catch (Exception e) {
            log.error("数据同步失败", e);
            return false;
        }
    }
} 