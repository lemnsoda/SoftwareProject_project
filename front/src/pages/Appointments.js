import React, { useEffect, useState } from 'react';
import { Table, Button, message } from 'antd';
import axios from 'axios';

const Appointments = () => {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = () => {
    const userId = localStorage.getItem('user_id');
    axios.get(`http://127.0.0.1:5000/teacher/appointments/${userId}`)
      .then(response => {
        setAppointments(response.data);
      })
      .catch(error => {
        message.error('获取预约请求失败');
      });
  };

  const handleApprove = (id) => {
    axios.put(`http://127.0.0.1:5000/teacher/appointments/${id}`, { status: 'approved' })
      .then(response => {
        message.success('预约已批准');
        fetchAppointments(); // 重新获取预约请求数据
      })
      .catch(error => {
        message.error('批准预约失败');
      });
  };

  const handleReject = (id) => {
    axios.put(`http://127.0.0.1:5000/teacher/appointments/${id}`, { status: 'rejected' })
      .then(response => {
        message.success('预约已拒绝');
        fetchAppointments(); // 重新获取预约请求数据
      })
      .catch(error => {
        message.error('拒绝预约失败');
      });
  };

  const columns = [
    {
      title: '学生',
      dataIndex: 'student_name',
      key: 'student_name',
    },
    {
      title: '日期',
      dataIndex: 'date',
      key: 'date',
    },
    {
      title: '开始时间',
      dataIndex: 'start_time',
      key: 'start_time',
    },
    {
      title: '结束时间',
      dataIndex: 'end_time',
      key: 'end_time',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: '操作',
      key: 'action',
      render: (text, record) => (
        <div>
          <Button type="link" onClick={() => handleApprove(record.id)}>批准</Button>
          <Button type="link" onClick={() => handleReject(record.id)}>拒绝</Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <h2>学生预约</h2>
      <Table columns={columns} dataSource={appointments} rowKey="id" />
    </div>
  );
};

export default Appointments;
