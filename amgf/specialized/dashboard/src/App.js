import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { Container } from 'react-bootstrap';
import io from 'socket.io-client';
import { toast } from 'react-toastify';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Opportunities from './pages/Opportunities';
import Allocation from './pages/Allocation';
import Performance from './pages/Performance';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';

// Services
import AuthService from './services/AuthService';
import ApiService from './services/ApiService';

// Styles
import './App.css';

const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [systemStatus, setSystemStatus] = useState({
    services: {},
    metrics: {}
  });
  const [socket, setSocket] = useState(null);
  const navigate = useNavigate();

  // Check if user is logged in
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const currentUser = await AuthService.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        console.error('Error checking authentication:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Initialize socket connection
  useEffect(() => {
    if (user) {
      const newSocket = io();
      setSocket(newSocket);

      // Socket event listeners
      newSocket.on('system:status', (data) => {
        setSystemStatus(data);
      });

      newSocket.on('events:opportunity_scan_complete', (data) => {
        toast.info(`Opportunity scan complete: ${data.opportunities_found} opportunities found`);
      });

      newSocket.on('events:allocation_updated', (data) => {
        toast.info(`Resource allocation updated: ${data.opportunity_count} opportunities allocated`);
      });

      newSocket.on('events:profits_reinvested', (data) => {
        toast.success(`Profits reinvested: $${data.profits.toFixed(2)}`);
      });

      // Fetch initial system status
      const fetchSystemStatus = async () => {
        try {
          const response = await ApiService.getSystemStatus();
          setSystemStatus(response.data);
        } catch (error) {
          console.error('Error fetching system status:', error);
        }
      };

      fetchSystemStatus();

      // Clean up on unmount
      return () => {
        newSocket.disconnect();
      };
    }
  }, [user]);

  // Handle logout
  const handleLogout = () => {
    AuthService.logout();
    setUser(null);
    navigate('/login');
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="app">
      {user ? (
        <>
          <Navbar user={user} onLogout={handleLogout} />
          <div className="content-wrapper">
            <Sidebar systemStatus={systemStatus} />
            <main className="main-content">
              <Container fluid>
                <Routes>
                  <Route path="/" element={<Dashboard systemStatus={systemStatus} />} />
                  <Route path="/opportunities" element={<Opportunities />} />
                  <Route path="/allocation" element={<Allocation />} />
                  <Route path="/performance" element={<Performance />} />
                  <Route path="/settings" element={<Settings user={user} />} />
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </Container>
            </main>
          </div>
        </>
      ) : (
        <Routes>
          <Route path="/login" element={<Login onLogin={setUser} />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      )}
    </div>
  );
};

export default App;