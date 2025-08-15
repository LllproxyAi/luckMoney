import React, { useState } from 'react';
import { Layout as AntLayout, Menu, theme } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  BarChartOutlined,
  LineChartOutlined,
  SettingOutlined,
  TrophyOutlined,
} from '@ant-design/icons';

const { Header, Sider, Content } = AntLayout;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: '仪表盘',
    },
    {
      key: '/results',
      icon: <TrophyOutlined />,
      label: '开奖结果',
    },
    {
      key: '/analysis',
      icon: <BarChartOutlined />,
      label: '数据分析',
    },
    {
      key: '/prediction',
      icon: <LineChartOutlined />,
      label: '预测分析',
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: '系统设置',
    },
  ];

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key);
  };

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ 
          height: 32, 
          margin: 16, 
          background: 'rgba(255, 255, 255, 0.2)',
          borderRadius: 6,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
          fontSize: collapsed ? 12 : 16,
          fontWeight: 'bold'
        }}>
          {collapsed ? '🎯' : '彩票分析系统'}
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Sider>
      <AntLayout>
        <Header style={{ padding: 0, background: colorBgContainer }}>
          <div style={{ 
            padding: '0 24px', 
            fontSize: 18, 
            fontWeight: 'bold',
            color: '#1890ff'
          }}>
            🎯 彩票数据分析系统
          </div>
        </Header>
        <Content style={{ margin: '24px 16px', padding: 24, background: colorBgContainer, borderRadius: borderRadiusLG }}>
          {children}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout; 