import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Table, Button, Space, Tag } from 'antd';
import { TrophyOutlined, BarChartOutlined, LineChartOutlined, ReloadOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';

interface LotteryResult {
  id: number;
  drawNumber: string;
  drawDate: string;
  lotteryTypeName: string;
  numbers: string;
  salesAmount: number;
  prizePool: number;
}

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [latestResults, setLatestResults] = useState<LotteryResult[]>([]);
  const [statistics, setStatistics] = useState({
    totalDraws: 0,
    totalSales: 0,
    totalPrizePool: 0,
    activeTypes: 0
  });

  const columns: ColumnsType<LotteryResult> = [
    {
      title: '期号',
      dataIndex: 'drawNumber',
      key: 'drawNumber',
      render: (text) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: '彩票类型',
      dataIndex: 'lotteryTypeName',
      key: 'lotteryTypeName',
    },
    {
      title: '开奖日期',
      dataIndex: 'drawDate',
      key: 'drawDate',
    },
    {
      title: '开奖号码',
      dataIndex: 'numbers',
      key: 'numbers',
      render: (text) => <span style={{ fontFamily: 'monospace' }}>{text}</span>,
    },
    {
      title: '销售额',
      dataIndex: 'salesAmount',
      key: 'salesAmount',
      render: (value) => `¥${(value / 10000).toFixed(2)}万`,
    },
    {
      title: '奖池金额',
      dataIndex: 'prizePool',
      key: 'prizePool',
      render: (value) => `¥${(value / 10000).toFixed(2)}万`,
    },
  ];

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // 这里应该调用实际的API
      // const response = await api.getDashboardData();
      // setLatestResults(response.data.latestResults);
      // setStatistics(response.data.statistics);
      
      // 模拟数据
      setLatestResults([
        {
          id: 1,
          drawNumber: '2024001',
          drawDate: '2024-01-01',
          lotteryTypeName: '大乐透',
          numbers: '01,05,12,23,35 + 03,08',
          salesAmount: 15000000,
          prizePool: 50000000
        },
        {
          id: 2,
          drawNumber: '2024002',
          drawDate: '2024-01-03',
          lotteryTypeName: '双色球',
          numbers: '03,08,15,22,28,33 + 12',
          salesAmount: 12000000,
          prizePool: 45000000
        }
      ]);
      
      setStatistics({
        totalDraws: 1250,
        totalSales: 1500000000,
        totalPrizePool: 500000000,
        activeTypes: 3
      });
    } catch (error) {
      console.error('获取仪表盘数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h1>🎯 系统仪表盘</h1>
        <p>欢迎使用彩票数据分析系统，这里展示了系统的整体运行状况和最新数据。</p>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总开奖期数"
              value={statistics.totalDraws}
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总销售额"
              value={statistics.totalSales / 100000000}
              suffix="亿元"
              prefix={<BarChartOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="总奖池金额"
              value={statistics.totalPrizePool / 100000000}
              suffix="亿元"
              prefix={<LineChartOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="活跃彩票类型"
              value={statistics.activeTypes}
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 最新开奖结果 */}
      <Card
        title="📊 最新开奖结果"
        extra={
          <Space>
            <Button 
              type="primary" 
              icon={<ReloadOutlined />}
              onClick={fetchDashboardData}
              loading={loading}
            >
              刷新数据
            </Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={latestResults}
          rowKey="id"
          loading={loading}
          pagination={false}
          size="small"
        />
      </Card>

      {/* 系统状态 */}
      <Row gutter={16} style={{ marginTop: 24 }}>
        <Col span={12}>
          <Card title="🔄 系统状态" size="small">
            <p>✅ 数据爬虫服务: 运行中</p>
            <p>✅ 数据分析服务: 运行中</p>
            <p>✅ 预测模型服务: 运行中</p>
            <p>✅ 数据库连接: 正常</p>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="📈 今日任务" size="small">
            <p>🕐 09:00 - 数据爬取任务</p>
            <p>🕐 21:00 - 数据分析任务</p>
            <p>🕐 实时 - 预测模型训练</p>
            <p>🕐 每日 - 系统健康检查</p>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard; 