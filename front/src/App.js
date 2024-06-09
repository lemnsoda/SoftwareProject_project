import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { Layout } from 'antd';
import Login from './pages/Login';
import Register from './pages/Register';
import Topbar from './components/Topbar';
import AdminSidebar from './components/AdminSidebar';
import StudentSidebar from './components/StudentSidebar';
import TeacherSidebar from './components/TeacherSidebar';
import Welcome from './pages/Welcome';
import AccountManagement from './pages/AccountManagement';
import AccountInfo from './pages/AccountInfo';
import AppointmentManagement from './pages/AppointmentManagement';
import Timetable from './pages/Timetable';
import Appointments from './pages/Appointments';
import './App.css';

const { Content } = Layout;

function App() {
  const [isRegister, setIsRegister] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [role, setRole] = useState('');
  const [userId, setUserId] = useState(''); // 新增 userId 状态
  const [selectedMenuItem, setSelectedMenuItem] = useState('welcome');

  useEffect(() => {
    const storedUsername = localStorage.getItem('username');
    const storedRole = localStorage.getItem('role');
    const storedUserId = localStorage.getItem('user_id'); // 从 localStorage 获取 user_id
    console.log('Initial localStorage values:', { storedUsername, storedRole, storedUserId }); // 打印初始值

    if (storedUsername && storedRole && storedUserId) {
      setIsLoggedIn(true);
      setUsername(storedUsername);
      setRole(storedRole);
      setUserId(storedUserId);
    }
  }, []);

  const switchToRegister = () => {
    setIsRegister(true);
  };

  const switchToLogin = () => {
    setIsRegister(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    localStorage.removeItem('user_id'); // 移除 user_id
    console.log('Logged out. localStorage cleared.'); // 打印退出日志
    setIsLoggedIn(false);
    setUsername('');
    setRole('');
    setUserId(''); // 清空 userId 状态
    setSelectedMenuItem('welcome');
  };

  const renderContent = () => {
    if (role === 'admin') {
      switch (selectedMenuItem) {
        case 'account-management':
          return <AccountManagement />;
        case 'appointment-management':
          return <AppointmentManagement />;
        default:
          return <Welcome username={username} />;
      }
    } else if (role === 'teacher') {
      switch (selectedMenuItem) {
        case 'timetable':
          return <Timetable />;
        case 'appointments':
          return <Appointments />;
        default:
          return <Welcome username={username} />;
      }
    } else {
      return <Welcome username={username} />;
    }
  };

  if (isLoggedIn) {
    let SidebarComponent;
    switch (role) {
      case 'admin':
        SidebarComponent = () => (
          <AdminSidebar setSelectedMenuItem={setSelectedMenuItem} />
        );
        break;
      case 'teacher':
        SidebarComponent = () => (
          <TeacherSidebar setSelectedMenuItem={setSelectedMenuItem} />
        );
        break;
      case 'student':
        SidebarComponent = StudentSidebar;
        break;
      default:
        SidebarComponent = null;
    }

    return (
      <Router>
        <Layout style={{ minHeight: '100vh' }}>
          <Topbar handleLogout={handleLogout} />
          <Layout>
            {SidebarComponent && <SidebarComponent />}
            <Layout style={{ padding: '0 24px 24px' }}>
              <Content style={{ padding: 24, margin: 0, minHeight: 280 }}>
                <Switch>
                  <Route path="/account-management" component={AccountManagement} />
                  <Route path="/account-info/:user_id" component={AccountInfo} />
                  <Route path="/timetable" component={Timetable} />
                  <Route path="/appointments" component={Appointments} />
                  <Route path="/" render={() => renderContent()} />
                </Switch>
              </Content>
            </Layout>
          </Layout>
        </Layout>
      </Router>
    );
  }

  return (
    <div className="App">
      {isRegister ? (
        <Register switchToLogin={switchToLogin} />
      ) : (
        <Login
          switchToRegister={switchToRegister}
          setIsLoggedIn={setIsLoggedIn}
          setUsername={setUsername}
          setRole={setRole}
          setUserId={setUserId} // 传递 setUserId 方法
        />
      )}
    </div>
  );
}

export default App;
