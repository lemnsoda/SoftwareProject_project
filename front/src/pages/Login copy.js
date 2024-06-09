import React from 'react';
import { Form, Input, Button, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import axios from 'axios';
import './Login.css';

const Login = ({ switchToRegister, setIsLoggedIn, setUsername, setRole }) => {
  const onFinish = (values) => {
    axios.post('http://127.0.0.1:5000/login', values)
      .then(response => {
        if (response.status === 200) {
          message.success(response.data.message);
          const { username, role } = response.data;
          // 保存用户信息到 localStorage
          localStorage.setItem('username', username);
          localStorage.setItem('role', role);
          // 更新状态以触发页面跳转
          setUsername(username);
          setRole(role);
          setIsLoggedIn(true);
        }
      })
      .catch(error => {
        if (error.response) {
          message.error(error.response.data.message);
        } else {
          message.error('登录失败，请稍后再试');
        }
      });
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <Form
          name="normal_login"
          className="login-form"
          initialValues={{ remember: true }}
          onFinish={onFinish}
        >
          <Form.Item
            name="username"
            rules={[{ required: true, message: '请输入用户名!' }]}
          >
            <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="请输入用户名" />
          </Form.Item>
          <Form.Item
            name="password"
            rules={[{ required: true, message: '请输入密码!' }]}
          >
            <Input
              prefix={<LockOutlined className="site-form-item-icon" />}
              type="password"
              placeholder="请输入密码"
            />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" className="login-form-button">
              登录
            </Button>
            或 <a href="#" onClick={switchToRegister}>注册</a>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default Login;
