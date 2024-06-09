import React from 'react';
import { Layout, Menu } from 'antd';
import { UserOutlined, ScheduleOutlined } from '@ant-design/icons';
import './Sidebar.css';

const { Sider } = Layout;

const AdminSidebar = ({ setSelectedMenuItem }) => {
  return (
    <Sider width={200} className="site-layout-background">
      <Menu
        mode="inline"
        defaultSelectedKeys={['account-management']}
        style={{ height: '100%', borderRight: 0 }}
        onClick={({ key }) => setSelectedMenuItem(key)}
      >
        <Menu.Item key="account-management" icon={<UserOutlined />}>
          账号管理
        </Menu.Item>
        <Menu.Item key="appointment-management" icon={<ScheduleOutlined />}>
          预约管理
        </Menu.Item>
      </Menu>
    </Sider>
  );
};

export default AdminSidebar;
