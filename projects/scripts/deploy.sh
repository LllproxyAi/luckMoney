#!/bin/bash

# 彩票数据分析系统部署脚本
# 作者: MoneyLuck Team
# 版本: 1.0.0

set -e

echo "🎯 彩票数据分析系统部署开始..."

# 检查Docker和Docker Compose是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p python-crawler/logs
mkdir -p python-crawler/charts
mkdir -p backend/logs
mkdir -p frontend/logs
mkdir -p nginx/ssl

# 设置环境变量
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=lottery_user
export DB_PASSWORD=lottery_pass
export DB_NAME=lottery_analysis

# 创建.env文件
echo "🔧 创建环境配置文件..."
cat > .env << EOF
# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_USER=lottery_user
DB_PASSWORD=lottery_pass
DB_NAME=lottery_analysis

# Python爬虫服务配置
PYTHON_CRAWLER_BASE_URL=http://localhost:8000
PYTHON_CRAWLER_TIMEOUT=30000

# Java后端服务配置
SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/lottery_analysis?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
SPRING_DATASOURCE_USERNAME=lottery_user
SPRING_DATASOURCE_PASSWORD=lottery_pass

# 前端配置
REACT_APP_API_URL=http://localhost:8080/api
EOF

echo "✅ 环境配置文件创建完成"

# 构建Java后端
echo "🔨 构建Java后端服务..."
cd backend
if [ -f "pom.xml" ]; then
    echo "📦 使用Maven构建..."
    mvn clean package -DskipTests
    echo "✅ Java后端构建完成"
else
    echo "⚠️  未找到pom.xml，跳过Java后端构建"
fi
cd ..

# 构建前端
echo "🔨 构建React前端应用..."
cd frontend
if [ -f "package.json" ]; then
    echo "📦 安装依赖..."
    npm install
    echo "📦 构建应用..."
    npm run build
    echo "✅ React前端构建完成"
else
    echo "⚠️  未找到package.json，跳过前端构建"
fi
cd ..

# 启动服务
echo "🚀 启动Docker服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 30

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 检查服务健康状态
echo "🏥 检查服务健康状态..."
if curl -f http://localhost:8080/api/health > /dev/null 2>&1; then
    echo "✅ Java后端服务运行正常"
else
    echo "❌ Java后端服务异常"
fi

if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Python爬虫服务运行正常"
else
    echo "❌ Python爬虫服务异常"
fi

if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ React前端服务运行正常"
else
    echo "❌ React前端服务异常"
fi

echo ""
echo "🎉 部署完成！"
echo ""
echo "📊 服务访问地址:"
echo "   - 前端界面: http://localhost:3000"
echo "   - 后端API: http://localhost:8080/api"
echo "   - Python爬虫: http://localhost:8000"
echo "   - 数据库: localhost:3306"
echo ""
echo "🔧 管理命令:"
echo "   - 查看服务状态: docker-compose ps"
echo "   - 查看服务日志: docker-compose logs -f [服务名]"
echo "   - 停止服务: docker-compose down"
echo "   - 重启服务: docker-compose restart"
echo ""
echo "📝 注意事项:"
echo "   - 首次启动需要等待数据库初始化完成"
echo "   - 确保端口3000, 8080, 8000, 3306未被占用"
echo "   - 如需修改配置，请编辑.env文件后重启服务" 