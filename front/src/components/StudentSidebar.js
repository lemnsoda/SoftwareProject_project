import React from 'react';
import { Layout, Menu } from 'antd';
import { BookOutlined, CalendarOutlined } from '@ant-design/icons';
import './Sidebar.css';

const { Sider } = Layout;

const StudentSidebar = () => {
  return (
    <Sider width={200} className="site-layout-background">
      <Menu
        mode="inline"
        defaultSelectedKeys={['1']}
        style={{ height: '100%', borderRight: 0 }}
      >
        <Menu.Item key="1" icon={<CalendarOutlined />}>
          预约时间
        </Menu.Item>
        <Menu.Item key="2" icon={<BookOutlined />}>
          我的课程
        </Menu.Item>
      </Menu>
    </Sider>
  );
};

export default StudentSidebar;
