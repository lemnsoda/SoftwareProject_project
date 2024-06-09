import React from 'react';
import { Layout, Menu } from 'antd';
import './Topbar.css';

const { Header } = Layout;

const Topbar = ({ handleLogout }) => {
  return (
    <Header className="topbar">
      <div className="logo">学校管理系统</div>
      <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
        <Menu.Item key="1">主页</Menu.Item>
        <Menu.Item key="2">关于</Menu.Item>
        <Menu.Item key="3">帮助</Menu.Item>
        <Menu.Item key="4" onClick={handleLogout}>登出</Menu.Item>
      </Menu>
    </Header>
  );
};

export default Topbar;
