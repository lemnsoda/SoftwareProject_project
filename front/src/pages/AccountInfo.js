import React, { useEffect, useState } from 'react';
import { Form, Input, Button, message, Select } from 'antd';
import axios from 'axios';
import { useParams, useHistory } from 'react-router-dom';

const { Option } = Select;

const AccountInfo = () => {
  const { user_id } = useParams();
  const [userInfo, setUserInfo] = useState({});
  const [isTeacher, setIsTeacher] = useState(false);
  const [form] = Form.useForm();
  const history = useHistory();

  useEffect(() => {
    fetchUserInfo();
  }, []);

  const fetchUserInfo = () => {
    axios.get(`http://127.0.0.1:5000/user/${user_id}`)
      .then(response => {
        setUserInfo(response.data);
        setIsTeacher(response.data.role === 'teacher');
        form.setFieldsValue(response.data); // 设置表单初始值
      })
      .catch(error => {
        message.error('获取用户信息失败');
      });
  };

  const handleUpdate = (values) => {
    console.log("Sending data to backend:", values); // 打印发送的数据
    axios.put(`http://127.0.0.1:5000/user/${user_id}`, values)
      .then(response => {
        message.success('用户信息更新成功');
        history.push('/account-management');
      })
      .catch(error => {
        message.error('用户信息更新失败');
      });
  };

  return (
    <div>
      <h2>用户信息</h2>
      <Form
        form={form} // 使用 form 实例
        initialValues={userInfo}
        onFinish={handleUpdate}
      >
        <Form.Item
          label="用户名"
          name="username"
          rules={[{ required: true, message: '请输入用户名' }]}
        >
          <Input />
        </Form.Item>
        <Form.Item
          label="角色"
          name="role"
          rules={[{ required: true, message: '请选择角色' }]}
        >
          <Select
            onChange={(value) => setIsTeacher(value === 'teacher')}
          >
            <Option value="admin">管理员</Option>
            <Option value="teacher">教师</Option>
            <Option value="student">学生</Option>
          </Select>
        </Form.Item>
        {isTeacher ? (
          <>
            <Form.Item
              label="姓名"
              name="name"
              rules={[{ required: true, message: '请输入姓名' }]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="性别"
              name="gender"
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="职称"
              name="title"
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="部门"
              name="department"
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="办公室号码"
              name="office_number"
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="电话"
              name="phone"
            >
              <Input />
            </Form.Item>
          </>
        ) : (
          <>
            <Form.Item
              label="姓名"
              name="name"
              rules={[{ required: true, message: '请输入姓名' }]}
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="性别"
              name="gender"
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="学号"
              name="student_number"
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="班级"
              name="class"
            >
              <Input />
            </Form.Item>
            <Form.Item
              label="电话"
              name="phone"
            >
              <Input />
            </Form.Item>
          </>
        )}
        <Form.Item>
          <Button type="primary" htmlType="submit">
            更新
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default AccountInfo;
