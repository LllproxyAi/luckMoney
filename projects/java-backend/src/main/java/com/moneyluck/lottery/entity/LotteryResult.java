package com.moneyluck.lottery.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import javax.persistence.*;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.LocalDateTime;

/**
 * 开奖结果实体类
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@Entity
@Table(name = "lottery_results")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class LotteryResult {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "lottery_type_id", nullable = false)
    private LotteryType lotteryType;

    @Column(name = "draw_number", nullable = false, length = 20)
    private String drawNumber;

    @Column(name = "draw_date", nullable = false)
    @JsonFormat(pattern = "yyyy-MM-dd")
    private LocalDate drawDate;

    @Column(name = "draw_time")
    @JsonFormat(pattern = "HH:mm:ss")
    private LocalTime drawTime;

    @Column(name = "numbers", columnDefinition = "TEXT", nullable = false)
    private String numbers;

    @Column(name = "sales_amount", precision = 15, scale = 2)
    private BigDecimal salesAmount;

    @Column(name = "prize_pool", precision = 15, scale = 2)
    private BigDecimal prizePool;

    @Column(name = "created_at")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }

    /**
     * 获取彩票类型代码
     */
    @JsonProperty("lotteryTypeCode")
    public String getLotteryTypeCode() {
        return lotteryType != null ? lotteryType.getTypeCode() : null;
    }

    /**
     * 获取彩票类型名称
     */
    @JsonProperty("lotteryTypeName")
    public String getLotteryTypeName() {
        return lotteryType != null ? lotteryType.getTypeName() : null;
    }
} 