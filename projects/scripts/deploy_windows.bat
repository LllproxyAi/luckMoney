@echo off
chcp 65001 >nul
echo 🎯 彩票数据分析系统 - Windows部署脚本
echo ================================================

REM 检查Docker是否安装
echo 🔍 检查Docker环境...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker未安装，请先安装Docker Desktop
    echo 📥 下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✅ Docker已安装

REM 检查Docker是否运行
echo 🔍 检查Docker服务状态...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker服务未启动，请启动Docker Desktop
    pause
    exit /b 1
)
echo ✅ Docker服务运行正常

REM 创建必要的目录
echo 📁 创建必要的目录...
if not exist "python-crawler\logs" mkdir "python-crawler\logs"
if not exist "python-crawler\charts" mkdir "python-crawler\charts"
if not exist "backend\logs" mkdir "backend\logs"
if not exist "frontend\logs" mkdir "frontend\logs"
echo ✅ 目录创建完成

REM 启动MySQL服务
echo 🗄️  启动MySQL服务...
docker run --name lottery-mysql ^
  -e MYSQL_ROOT_PASSWORD=password ^
  -e MYSQL_DATABASE=lottery_analysis ^
  -e MYSQL_USER=lottery_user ^
  -e MYSQL_PASSWORD=lottery_pass ^
  -p 3306:3306 ^
  -d mysql:8.0

REM 等待MySQL启动
echo ⏳ 等待MySQL服务启动...
timeout /t 30 /nobreak >nul

REM 执行数据库脚本
echo 📊 初始化数据库...
docker exec -i lottery-mysql mysql -uroot -ppassword lottery_analysis < database/schema.sql
echo ✅ 数据库初始化完成

REM 启动Python爬虫服务
echo 🕷️  启动Python爬虫服务...
cd python-crawler
start "Python爬虫服务" cmd /k "python main.py"
cd ..

REM 等待服务启动
echo ⏳ 等待Python爬虫服务启动...
timeout /t 10 /nobreak >nul

REM 启动Java后端服务
echo ☕ 启动Java后端服务...
cd backend
start "Java后端服务" cmd /k "mvn spring-boot:run"
cd ..

REM 等待服务启动
echo ⏳ 等待Java后端服务启动...
timeout /t 30 /nobreak >nul

REM 启动React前端服务
echo ⚛️  启动React前端服务...
cd frontend
start "React前端服务" cmd /k "npm start"
cd ..

echo.
echo 🎉 部署完成！
echo ================================================
echo 📊 服务访问地址:
echo    前端界面: http://localhost:3000
echo    后端API: http://localhost:8080/api
echo    Python爬虫: http://localhost:8000
echo    数据库: localhost:3306
echo.
echo 🔧 管理命令:
echo    查看Docker容器: docker ps
echo    查看服务日志: docker logs lottery-mysql
echo    停止服务: docker stop lottery-mysql
echo.
echo 📝 注意事项:
echo    - 确保端口3000, 8080, 8000, 3306未被占用
echo    - 如需修改配置，请编辑相应配置文件
echo    - 关闭命令行窗口会停止对应服务
echo.
pause 