package com.moneyluck.lottery.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

import javax.persistence.*;
import java.time.LocalDateTime;

/**
 * 预测模型实体类
 * 
 * @author MoneyLuck Team
 * @version 1.0.0
 */
@Entity
@Table(name = "prediction_models")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class PredictionModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "model_name", nullable = false, length = 100)
    private String modelName;

    @Column(name = "model_type", nullable = false, length = 50)
    private String modelType;

    @Column(name = "description", columnDefinition = "TEXT")
    private String description;

    @Column(name = "parameters", columnDefinition = "TEXT")
    private String parameters;

    @Column(name = "is_active")
    private Boolean isActive;

    @Column(name = "created_at")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (isActive == null) {
            isActive = true;
        }
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
} 