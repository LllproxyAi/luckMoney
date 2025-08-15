#!/bin/bash

# 启动Python爬虫Docker服务
echo "🚀 启动Python爬虫Docker服务..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker服务未启动，请先启动Docker"
    exit 1
fi

# 检查配置文件
if [ ! -f "docker-compose-crawler.yml" ]; then
    echo "❌ 未找到docker-compose-crawler.yml配置文件"
    exit 1
fi

# 停止并删除现有容器
echo "🔄 清理现有容器..."
docker-compose -f docker-compose-crawler.yml down

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose -f docker-compose-crawler.yml up --build -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose -f docker-compose-crawler.yml ps

# 检查服务健康状态
echo "🏥 检查服务健康状态..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Python爬虫服务启动成功！"
    echo "🌐 访问地址: http://localhost:8000"
    echo "📊 健康检查: http://localhost:8000/health"
else
    echo "❌ 服务启动异常，查看日志:"
    docker-compose -f docker-compose-crawler.yml logs lottery-crawler
fi
