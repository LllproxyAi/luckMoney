package com.moneyluck.lottery.repository;

import com.moneyluck.lottery.entity.LotteryResult;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

/**
 * 开奖结果数据访问接口
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@Repository
public interface LotteryResultRepository extends JpaRepository<LotteryResult, Long> {
    
    /**
     * 根据期号查找开奖结果
     */
    Optional<LotteryResult> findByDrawNumber(String drawNumber);
    
    /**
     * 根据彩票类型ID查找开奖结果
     */
    List<LotteryResult> findByLotteryTypeIdOrderByDrawDateDesc(Long lotteryTypeId);
    
    /**
     * 分页查询开奖结果
     */
    @Query("SELECT lr FROM LotteryResult lr " +
           "WHERE (:lotteryTypeId IS NULL OR lr.lotteryType.id = :lotteryTypeId) " +
           "AND (:startDate IS NULL OR lr.drawDate >= :startDate) " +
           "AND (:endDate IS NULL OR lr.drawDate <= :endDate) " +
           "ORDER BY lr.drawDate DESC, lr.drawNumber DESC")
    Page<LotteryResult> findByConditions(
        @Param("lotteryTypeId") Long lotteryTypeId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate,
        Pageable pageable
    );
    
    /**
     * 获取最新开奖结果
     */
    @Query("SELECT lr FROM LotteryResult lr ORDER BY lr.drawDate DESC, lr.drawNumber DESC")
    List<LotteryResult> findLatestResults(Pageable pageable);
    
    /**
     * 根据彩票类型ID获取最新开奖结果
     */
    @Query("SELECT lr FROM LotteryResult lr WHERE lr.lotteryType.id = :lotteryTypeId " +
           "ORDER BY lr.drawDate DESC, lr.drawNumber DESC")
    List<LotteryResult> findLatestResultsByType(@Param("lotteryTypeId") Long lotteryTypeId, Pageable pageable);
    
    /**
     * 检查期号是否存在
     */
    boolean existsByDrawNumberAndLotteryTypeId(String drawNumber, Long lotteryTypeId);
    
    /**
     * 统计指定日期范围内的开奖期数
     */
    @Query("SELECT COUNT(lr) FROM LotteryResult lr " +
           "WHERE lr.lotteryType.id = :lotteryTypeId " +
           "AND lr.drawDate BETWEEN :startDate AND :endDate")
    long countByDateRange(
        @Param("lotteryTypeId") Long lotteryTypeId,
        @Param("startDate") LocalDate startDate,
        @Param("endDate") LocalDate endDate
    );
    
    /**
     * 根据彩票类型ID统计开奖期数
     */
    long countByLotteryTypeId(Long lotteryTypeId);
    
    /**
     * 统计所有开奖期数
     */
    @Query("SELECT COUNT(lr) FROM LotteryResult lr")
    long count();
} 