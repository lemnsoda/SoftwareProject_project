import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import axios from 'axios';
import './Login.css';

const Login = ({ switchToRegister, setIsLoggedIn, setUsername, setRole }) => {
  const [loading, setLoading] = useState(false);
  console.log('Login page loaded');

  const onFinish = (values) => {
    setLoading(true);
    console.log('Received values of form:', values);
    axios.post('http://127.0.0.1:5000/login', values, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        const { username, role, user_id } = response.data;
        localStorage.setItem('username', username);
        localStorage.setItem('role', role);
        localStorage.setItem('user_id', user_id); // 存储 user_id
        console.log('Logged in. localStorage values:', { username, role, user_id }); // 打印登录后的 localStorage 值
        setIsLoggedIn(true);
        setUsername(username);
        setRole(role);
        message.success('登录成功');
        setLoading(false);
      })
      .catch(error => {
        if (error.response) {
          message.error(error.response.data.message);
        } else {
          console.error(error);
          message.error('登录失败，请稍后再试');
        }
        setLoading(false);
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
          rules={[{ required: true, message: '请输入用户名' }]}
        >
          <Input placeholder="用户名" />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[{ required: true, message: '请输入密码' }]}
        >
          <Input.Password placeholder="密码" />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            登录
          </Button>
          <br />
          或 <a href="#" onClick={switchToRegister}>注册</a>
        </Form.Item>
      </Form>
      </div>
     
    </div>
  );
};

export default Login;
