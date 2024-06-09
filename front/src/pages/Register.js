import React from 'react';
import { Form, Input, Button, Select, message } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import axios from 'axios';
import './Register.css';

const { Option } = Select;

const Register = ({ switchToLogin }) => {
  const onFinish = (values) => {
    axios.post('http://127.0.0.1:5000/register', values)
      .then(response => {
        if (response.status === 201) {
          message.success(response.data.message);
          switchToLogin();
        }
      })
      .catch(error => {
        if (error.response) {
          message.error(error.response.data.message);
        } else {
          message.error('注册失败，请稍后再试');
        }
      });
  };

  return (
    <div className="register-container">
      <div className="register-box">
        <Form
          name="register"
          className="register-form"
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
          <Form.Item
            name="confirm"
            dependencies={['password']}
            hasFeedback
            rules={[
              {
                required: true,
                message: '请确认密码!',
              },
              ({ getFieldValue }) => ({
                validator(_, value) {
                  if (!value || getFieldValue('password') === value) {
                    return Promise.resolve();
                  }
                  return Promise.reject(new Error('两次输入的密码不匹配!'));
                },
              }),
            ]}
          >
            <Input
              prefix={<LockOutlined className="site-form-item-icon" />}
              type="password"
              placeholder="确认密码"
            />
          </Form.Item>
          <Form.Item
            name="role"
            rules={[{ required: true, message: '请选择角色!' }]}
          >
            <Select placeholder="请选择角色">
              <Option value="teacher">老师</Option>
              <Option value="student">学生</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" className="register-form-button">
              注册
            </Button>
            或 <a href="#" onClick={switchToLogin}>登录</a>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default Register;
