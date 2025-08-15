package com.moneyluck.lottery.controller;

import com.moneyluck.lottery.dto.ApiResponse;
import com.moneyluck.lottery.dto.LotteryResultDTO;
import com.moneyluck.lottery.entity.LotteryResult;
import com.moneyluck.lottery.entity.LotteryType;
import com.moneyluck.lottery.service.LotteryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.time.LocalDate;
import java.util.List;

/**
 * 彩票数据控制器
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@RestController
@RequestMapping("/lottery")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin(origins = "*")
public class LotteryController {

    private final LotteryService lotteryService;

    /**
     * 获取所有彩票类型
     */
    @GetMapping("/types")
    public ResponseEntity<ApiResponse<List<LotteryType>>> getAllLotteryTypes() {
        try {
            List<LotteryType> types = lotteryService.getAllLotteryTypes();
            return ResponseEntity.ok(ApiResponse.success("获取彩票类型成功", types));
        } catch (Exception e) {
            log.error("获取彩票类型失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("获取彩票类型失败: " + e.getMessage()));
        }
    }

    /**
     * 根据ID获取彩票类型
     */
    @GetMapping("/types/{id}")
    public ResponseEntity<ApiResponse<LotteryType>> getLotteryTypeById(@PathVariable Long id) {
        try {
            LotteryType type = lotteryService.getLotteryTypeById(id);
            if (type != null) {
                return ResponseEntity.ok(ApiResponse.success("获取彩票类型成功", type));
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            log.error("获取彩票类型失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("获取彩票类型失败: " + e.getMessage()));
        }
    }

    /**
     * 分页获取开奖结果
     */
    @GetMapping("/results")
    public ResponseEntity<ApiResponse<Page<LotteryResult>>> getLotteryResults(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "20") int size,
            @RequestParam(required = false) Long lotteryTypeId,
            @RequestParam(required = false) @DateTimeFormat(pattern = "yyyy-MM-dd") LocalDate startDate,
            @RequestParam(required = false) @DateTimeFormat(pattern = "yyyy-MM-dd") LocalDate endDate) {
        
        try {
            Pageable pageable = PageRequest.of(page, size);
            Page<LotteryResult> results = lotteryService.getLotteryResults(
                lotteryTypeId, startDate, endDate, pageable);
            
            return ResponseEntity.ok(ApiResponse.success("获取开奖结果成功", results));
        } catch (Exception e) {
            log.error("获取开奖结果失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("获取开奖结果失败: " + e.getMessage()));
        }
    }

    /**
     * 根据期号获取开奖结果
     */
    @GetMapping("/results/{drawNumber}")
    public ResponseEntity<ApiResponse<LotteryResult>> getLotteryResultByDrawNumber(
            @PathVariable String drawNumber) {
        try {
            LotteryResult result = lotteryService.getLotteryResultByDrawNumber(drawNumber);
            if (result != null) {
                return ResponseEntity.ok(ApiResponse.success("获取开奖结果成功", result));
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            log.error("获取开奖结果失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("获取开奖结果失败: " + e.getMessage()));
        }
    }

    /**
     * 获取最新开奖结果
     */
    @GetMapping("/results/latest")
    public ResponseEntity<ApiResponse<List<LotteryResult>>> getLatestLotteryResults(
            @RequestParam(defaultValue = "10") int limit) {
        try {
            List<LotteryResult> results = lotteryService.getLatestLotteryResults(limit);
            return ResponseEntity.ok(ApiResponse.success("获取最新开奖结果成功", results));
        } catch (Exception e) {
            log.error("获取最新开奖结果失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("获取最新开奖结果失败: " + e.getMessage()));
        }
    }

    /**
     * 手动添加开奖结果
     */
    @PostMapping("/results")
    public ResponseEntity<ApiResponse<LotteryResult>> addLotteryResult(
            @Valid @RequestBody LotteryResultDTO resultDTO) {
        try {
            LotteryResult result = lotteryService.addLotteryResult(resultDTO);
            return ResponseEntity.ok(ApiResponse.success("添加开奖结果成功", result));
        } catch (Exception e) {
            log.error("添加开奖结果失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("添加开奖结果失败: " + e.getMessage()));
        }
    }

    /**
     * 更新开奖结果
     */
    @PutMapping("/results/{id}")
    public ResponseEntity<ApiResponse<LotteryResult>> updateLotteryResult(
            @PathVariable Long id, @Valid @RequestBody LotteryResultDTO resultDTO) {
        try {
            LotteryResult result = lotteryService.updateLotteryResult(id, resultDTO);
            if (result != null) {
                return ResponseEntity.ok(ApiResponse.success("更新开奖结果成功", result));
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            log.error("更新开奖结果失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("更新开奖结果失败: " + e.getMessage()));
        }
    }

    /**
     * 删除开奖结果
     */
    @DeleteMapping("/results/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteLotteryResult(@PathVariable Long id) {
        try {
            boolean deleted = lotteryService.deleteLotteryResult(id);
            if (deleted) {
                return ResponseEntity.ok(ApiResponse.success("删除开奖结果成功", null));
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            log.error("删除开奖结果失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("删除开奖结果失败: " + e.getMessage()));
        }
    }

    /**
     * 获取统计数据
     */
    @GetMapping("/statistics")
    public ResponseEntity<ApiResponse<Object>> getStatistics(
            @RequestParam(required = false) Long lotteryTypeId) {
        try {
            Object statistics = lotteryService.getStatistics(lotteryTypeId);
            return ResponseEntity.ok(ApiResponse.success("获取统计数据成功", statistics));
        } catch (Exception e) {
            log.error("获取统计数据失败", e);
            return ResponseEntity.badRequest().body(ApiResponse.error("获取统计数据失败: " + e.getMessage()));
        }
    }
} 