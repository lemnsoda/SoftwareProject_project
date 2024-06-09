import React, { useEffect, useState } from 'react';
import { Table, message } from 'antd';
import axios from 'axios';

const AppointmentManagement = () => {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    fetchAppointments();
  }, []);

  const fetchAppointments = () => {
    axios.get('http://127.0.0.1:5000/admin/appointments')
      .then(response => {
        setAppointments(response.data);
      })
      .catch(error => {
        message.error('获取预约数据失败');
      });
  };

  const columns = [
    {
      title: '学生ID',
      dataIndex: 'student_id',
      key: 'student_id',
    },
    {
      title: '教师ID',
      dataIndex: 'teacher_id',
      key: 'teacher_id',
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
  ];

  return (
    <div>
      <h2>预约管理</h2>
      <Table columns={columns} dataSource={appointments} rowKey="appointment_id" />
    </div>
  );
};

export default AppointmentManagement;
