import React from 'react';
import { Layout, Menu } from 'antd';
import { CalendarOutlined, BookOutlined } from '@ant-design/icons';
import './Sidebar.css';

const { Sider } = Layout;

const TeacherSidebar = ({ setSelectedMenuItem }) => {
  return (
    <Sider width={200} className="site-layout-background">
      <Menu
        mode="inline"
        defaultSelectedKeys={['timetable']}
        style={{ height: '100%', borderRight: 0 }}
        onClick={({ key }) => setSelectedMenuItem(key)}
      >
        <Menu.Item key="timetable" icon={<CalendarOutlined />}>
          我的时间表
        </Menu.Item>
        <Menu.Item key="appointments" icon={<BookOutlined />}>
          学生预约
        </Menu.Item>
      </Menu>
    </Sider>
  );
};

export default TeacherSidebar;
