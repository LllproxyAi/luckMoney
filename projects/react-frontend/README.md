# 🎨 React前端应用

## 项目简介
彩票数据分析与预测系统的前端界面，基于React 18 + TypeScript + Ant Design构建，提供直观的数据展示和交互体验。

## 🚀 技术栈
- **框架**: React 18 + TypeScript
- **UI组件**: Ant Design 5.x
- **图表库**: ECharts + React-ECharts
- **路由**: React Router 6
- **状态管理**: React Hooks + Context
- **HTTP客户端**: Axios
- **构建工具**: Vite
- **样式**: CSS Modules + Less

## 📁 项目结构
```
react-frontend/
├── public/              # 静态资源
├── src/
│   ├── components/      # 通用组件
│   │   ├── Layout.tsx   # 主布局组件
│   │   ├── Charts/      # 图表组件
│   │   └── Forms/       # 表单组件
│   ├── pages/           # 页面组件
│   │   ├── Dashboard.tsx    # 仪表板
│   │   ├── Lottery/         # 彩票管理
│   │   ├── Analysis/        # 数据分析
│   │   └── Prediction/      # 预测管理
│   ├── services/        # API服务
│   ├── hooks/           # 自定义Hooks
│   ├── utils/           # 工具函数
│   ├── types/           # TypeScript类型定义
│   ├── App.tsx          # 主应用组件
│   └── main.tsx         # 应用入口
├── package.json         # 依赖配置
├── tsconfig.json        # TypeScript配置
├── vite.config.ts       # Vite配置
└── Dockerfile          # Docker镜像构建
```

## 🛠️ 快速开始

### 环境要求
- Node.js 16+
- npm 8+ 或 yarn 1.22+

### 本地开发
```bash
# 1. 进入项目目录
cd projects/react-frontend

# 2. 安装依赖
npm install
# 或
yarn install

# 3. 启动开发服务器
npm run dev
# 或
yarn dev

# 4. 构建生产版本
npm run build
# 或
yarn build
```

### Docker部署
```bash
# 1. 构建镜像
docker build -t lottery-react-frontend .

# 2. 运行容器
docker run -d -p 3000:80 --name lottery-react-frontend lottery-react-frontend
```

## 📡 功能特性

### 数据展示
- **仪表板**: 系统概览、统计信息、最新开奖
- **彩票管理**: 类型管理、开奖结果、历史数据
- **数据分析**: 频率分析、趋势图表、分布统计
- **预测管理**: 模型列表、预测结果、准确率评估

### 交互功能
- **响应式设计**: 支持桌面和移动设备
- **实时更新**: WebSocket连接实时数据
- **图表交互**: 可缩放、可筛选的交互式图表
- **数据导出**: 支持CSV、Excel格式导出

### 用户体验
- **主题切换**: 明暗主题支持
- **多语言**: 中英文界面
- **权限控制**: 基于角色的访问控制
- **操作反馈**: 加载状态、成功提示、错误处理

## ⚙️ 配置说明

### 环境变量
```bash
# .env.local
VITE_API_BASE_URL=http://localhost:8080/api
VITE_WS_URL=ws://localhost:8080/ws
VITE_APP_TITLE=彩票数据分析系统
```

### API配置
```typescript
// src/services/api.ts
const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
}
```

### 主题配置
```typescript
// src/theme/index.ts
export const theme = {
  token: {
    colorPrimary: '#1890ff',
    borderRadius: 6,
    fontSize: 14
  }
}
```

## 🔧 开发指南

### 添加新页面
1. 在`src/pages`中创建页面组件
2. 在`src/components`中添加相关组件
3. 在路由配置中添加路由
4. 在菜单中添加导航项

### 创建新组件
1. 使用函数组件 + TypeScript
2. 遵循Ant Design设计规范
3. 添加适当的类型定义
4. 实现响应式设计

### 集成图表
1. 使用React-ECharts组件
2. 配置图表选项和样式
3. 处理数据更新和交互
4. 优化渲染性能

## 📊 组件库

### 基础组件
- **Layout**: 页面布局、导航菜单
- **Table**: 数据表格、分页、排序
- **Form**: 表单控件、验证、提交
- **Modal**: 弹窗、确认框、抽屉

### 图表组件
- **FrequencyChart**: 频率分布图
- **TrendChart**: 趋势分析图
- **HeatmapChart**: 热力图
- **DistributionChart**: 分布统计图

### 业务组件
- **LotteryCard**: 彩票信息卡片
- **PredictionForm**: 预测参数表单
- **AnalysisPanel**: 分析结果面板
- **StatusBadge**: 状态标签

## 🚀 部署说明

### 开发环境
- 使用Vite开发服务器
- 支持热重载和快速刷新
- 代理API请求到后端服务

### 生产环境
- 构建优化后的静态文件
- 使用Nginx提供静态文件服务
- 配置CDN加速和缓存策略

### 性能优化
- 代码分割和懒加载
- 图片压缩和格式优化
- 缓存策略和预加载
- 监控和分析

## 📝 更新日志

### v1.0.0 (2024-01-XX)
- 初始版本发布
- 基础页面框架
- 数据展示组件
- 图表集成
- 响应式设计

## 🔍 故障排除

### 常见问题
1. **依赖安装失败**: 清除缓存重新安装
2. **构建错误**: 检查TypeScript类型错误
3. **API请求失败**: 检查后端服务状态
4. **样式问题**: 检查CSS模块导入

### 调试工具
- React Developer Tools
- Redux DevTools
- 浏览器开发者工具
- 网络请求监控

## 📚 学习资源

- [React官方文档](https://react.dev/)
- [TypeScript手册](https://www.typescriptlang.org/docs/)
- [Ant Design组件库](https://ant.design/components/overview/)
- [ECharts图表库](https://echarts.apache.org/zh/index.html)
