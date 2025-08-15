FROM openjdk:11-jre-slim

# 设置工作目录
WORKDIR /app

# 安装必要的包
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制JAR文件
COPY target/lottery-analysis-backend-1.0.0.jar app.jar

# 设置环境变量
ENV JAVA_OPTS="-Xmx512m -Xms256m"

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# 启动命令
CMD ["sh", "-c", "java $JAVA_OPTS -jar app.jar"] 