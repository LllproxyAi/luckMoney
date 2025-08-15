package com.moneyluck.lottery.repository;

import com.moneyluck.lottery.entity.LotteryType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

/**
 * 彩票类型数据访问接口
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@Repository
public interface LotteryTypeRepository extends JpaRepository<LotteryType, Long> {
    
    /**
     * 根据类型代码查找彩票类型
     */
    Optional<LotteryType> findByTypeCode(String typeCode);
    
    /**
     * 查找所有启用的彩票类型
     */
    @Query("SELECT lt FROM LotteryType lt WHERE lt.id IN (SELECT DISTINCT lr.lotteryType.id FROM LotteryResult lr)")
    List<LotteryType> findActiveTypes();
    
    /**
     * 根据类型名称查找彩票类型
     */
    Optional<LotteryType> findByTypeName(String typeName);
    
    /**
     * 检查类型代码是否存在
     */
    boolean existsByTypeCode(String typeCode);
} 