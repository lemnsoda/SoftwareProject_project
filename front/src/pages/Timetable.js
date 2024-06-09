import React, { useEffect, useState } from 'react';
import { Calendar, Badge, Button, Modal, Form, DatePicker, TimePicker, message, List } from 'antd';
import axios from 'axios';
import moment from 'moment';

const Timetable = () => {
  const [timetable, setTimetable] = useState([]);
  const [isAddModalVisible, setIsAddModalVisible] = useState(false);
  const [isDetailModalVisible, setIsDetailModalVisible] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchTimetable();
  }, []);

  const fetchTimetable = () => {
    const userId = localStorage.getItem('user_id');
    axios.get(`http://127.0.0.1:5000/teacher/timetable/${userId}`)
      .then(response => {
        console.log('Fetched timetable:', response.data); // 打印获取的数据
        setTimetable(response.data);
      })
      .catch(error => {
        message.error('获取时间表失败');
      });
  };

  const handleAdd = (values) => {
    const userId = localStorage.getItem('user_id');
    const newSlot = {
      teacher_id: userId,
      date: values.date.format('YYYY-MM-DD'),
      start_time: values.start_time.format('HH:mm'),
      end_time: values.end_time.format('HH:mm')
    };

    axios.post(`http://127.0.0.1:5000/teacher/timetable`, newSlot)
      .then(response => {
        message.success('新增时间成功');
        fetchTimetable();
        setIsAddModalVisible(false);
        form.resetFields();
      })
      .catch(error => {
        message.error('新增时间失败');
      });
  };

  const handleDelete = (id) => {
    axios.delete(`http://127.0.0.1:5000/teacher/timetable/${id}`)
      .then(response => {
        message.success('删除时间成功');
        fetchTimetable(); // 重新获取时间表数据
      })
      .catch(error => {
        message.error('删除时间失败');
      });
  };

  const getListData = (value) => {
    const date = value.format('YYYY-MM-DD');
    return timetable
      .filter(item => item.date === date)
      .map(item => ({
        type: 'success',
        content: `${item.start_time} - ${item.end_time}`
      }));
  };

  const dateCellRender = (value) => {
    const listData = getListData(value);
    return (
      <ul className="events">
        {listData.map((item, index) => (
          <li key={index}>
            <Badge status={item.type} text={item.content} />
          </li>
        ))}
      </ul>
    );
  };

  const handleDateSelect = (value) => {
    setSelectedDate(value);
    setIsDetailModalVisible(true);
  };

  const showAddModal = () => {
    setIsAddModalVisible(true);
  };

  const handleAddCancel = () => {
    setIsAddModalVisible(false);
    form.resetFields();
  };

  const handleDetailCancel = () => {
    setIsDetailModalVisible(false);
  };

  const getSelectedDateTimetable = () => {
    if (!selectedDate) return [];
    const date = selectedDate.format('YYYY-MM-DD');
    return timetable.filter(item => item.date === date);
  };

  return (
    <div>
      <h2>我的时间表</h2>
      <Button type="primary" onClick={showAddModal}>新增空闲时间</Button>
      <Calendar dateCellRender={dateCellRender} onSelect={handleDateSelect} />
      <Modal
        title="新增空闲时间"
        visible={isAddModalVisible}
        onCancel={handleAddCancel}
        footer={null}
      >
        <Form
          form={form}
          onFinish={handleAdd}
        >
          <Form.Item
            name="date"
            label="日期"
            rules={[{ required: true, message: '请选择日期' }]}
          >
            <DatePicker />
          </Form.Item>
          <Form.Item
            name="start_time"
            label="开始时间"
            rules={[{ required: true, message: '请选择开始时间' }]}
          >
            <TimePicker format="HH:mm" />
          </Form.Item>
          <Form.Item
            name="end_time"
            label="结束时间"
            rules={[{ required: true, message: '请选择结束时间' }]}
          >
            <TimePicker format="HH:mm" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit">保存</Button>
          </Form.Item>
        </Form>
      </Modal>
      <Modal
        title={`空闲时间 - ${selectedDate ? selectedDate.format('YYYY-MM-DD') : ''}`}
        visible={isDetailModalVisible}
        onCancel={handleDetailCancel}
        footer={null}
      >
        <List
          dataSource={getSelectedDateTimetable()}
          renderItem={item => (
            <List.Item actions={[<Button type="link" onClick={() => handleDelete(item.id)}>删除</Button>]}>
              {item.start_time} - {item.end_time}
            </List.Item>
          )}
        />
      </Modal>
    </div>
  );
};

export default Timetable;
