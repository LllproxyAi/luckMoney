package com.moneyluck.lottery.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalTime;

/**
 * 开奖结果数据传输对象
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class LotteryResultDTO {
    
    @NotNull(message = "彩票类型ID不能为空")
    private Long lotteryTypeId;
    
    @NotBlank(message = "期号不能为空")
    @Pattern(regexp = "^\\d{4,8}$", message = "期号格式不正确")
    private String drawNumber;
    
    @NotNull(message = "开奖日期不能为空")
    private LocalDate drawDate;
    
    private LocalTime drawTime;
    
    @NotBlank(message = "开奖号码不能为空")
    private String numbers;
    
    private BigDecimal salesAmount;
    
    private BigDecimal prizePool;
} 