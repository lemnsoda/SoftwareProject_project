import React, { useEffect, useState } from 'react';
import { Table, Button, message, Input } from 'antd';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

const { Search } = Input;

const AccountManagement = () => {
  const [users, setUsers] = useState([]);
  const [filteredUsers, setFilteredUsers] = useState([]);
  const [showPasswords, setShowPasswords] = useState({});
  const history = useHistory();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = () => {
    axios.get('http://127.0.0.1:5000/admin/users')
      .then(response => {
        const usersData = response.data;
        setUsers(usersData);
        setFilteredUsers(usersData);
        // 初始化所有用户的密码显示状态为隐藏
        const initialShowPasswords = usersData.reduce((acc, user) => {
          acc[user.user_id] = false;
          return acc;
        }, {});
        setShowPasswords(initialShowPasswords);
      })
      .catch(error => {
        message.error('获取用户数据失败');
      });
  };

  const deleteUser = (userId) => {
    axios.delete(`http://127.0.0.1:5000/admin/users/${userId}`)
      .then(response => {
        message.success('删除用户成功');
        fetchUsers(); // 重新获取用户数据，确保删除后列表更新
      })
      .catch(error => {
        message.error('删除用户失败');
      });
  };

  const toggleShowPassword = (userId) => {
    setShowPasswords(prevState => ({
      ...prevState,
      [userId]: !prevState[userId]
    }));
  };

  const handleSearch = (value) => {
    const filtered = users.filter(user => user.username.toLowerCase().includes(value.toLowerCase()));
    setFilteredUsers(filtered);
    message.info(`匹配到 ${filtered.length} 个账户`);
  };

  const handleRowClick = (record) => {
    console.log(`Navigating to /account-info/${record.user_id}`); // Debug log
    if (record.role !== 'admin') {
      history.push(`/account-info/${record.user_id}`);
    }
  };

  const columns = [
    {
      title: '用户名',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: '密码',
      key: 'password',
      render: (text, record) => (
        <div>
          <span>{showPasswords[record.user_id] ? record.password : '******'}</span>
          <Button type="link" onClick={() => toggleShowPassword(record.user_id)}>
            {showPasswords[record.user_id] ? '隐藏' : '显示'}
          </Button>
        </div>
      ),
    },
    {
      title: '角色',
      dataIndex: 'role',
      key: 'role',
    },
    {
      title: '操作',
      key: 'action',
      render: (text, record) => (
        <Button type="link" onClick={() => deleteUser(record.user_id)}>删除</Button>
      ),
    },
  ];

  return (
    <div>
      <h2>账号管理</h2>
      <Search
        placeholder="输入用户名搜索"
        onSearch={handleSearch}
        style={{ marginBottom: 20, width: 300 }}
      />
      <Table
        columns={columns}
        dataSource={filteredUsers}
        rowKey="user_id"
        onRow={(record) => ({
          onClick: () => handleRowClick(record),
        })}
      />
    </div>
  );
};

export default AccountManagement;
