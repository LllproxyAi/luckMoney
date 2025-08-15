import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import 'antd/dist/reset.css';

import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import LotteryResults from './pages/LotteryResults';
import DataAnalysis from './pages/DataAnalysis';
import Prediction from './pages/Prediction';
import Settings from './pages/Settings';

import './App.css';

const App: React.FC = () => {
  return (
    <ConfigProvider locale={zhCN}>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/results" element={<LotteryResults />} />
            <Route path="/analysis" element={<DataAnalysis />} />
            <Route path="/prediction" element={<Prediction />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </Router>
    </ConfigProvider>
  );
};

export default App; 