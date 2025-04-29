import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Button, Alert, ProgressBar } from 'react-bootstrap';
import { Line, Pie, Bar } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import moment from 'moment';
import { FaRocket, FaChartLine, FaMoneyBillWave, FaExclamationTriangle } from 'react-icons/fa';

// Services
import ApiService from '../services/ApiService';

// Register Chart.js components
Chart.register(...registerables);

const Dashboard = ({ systemStatus }) => {
  const [allocation, setAllocation] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [performanceData, setPerformanceData] = useState({
    labels: [],
    datasets: []
  });

  // Fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch current allocation
        const allocationResponse = await ApiService.getAllocation();
        setAllocation(allocationResponse.data.allocation);
        
        // Fetch top opportunities
        const opportunitiesResponse = await ApiService.getTopOpportunities();
        setOpportunities(opportunitiesResponse.data.opportunities);
        
        // Fetch performance data (last 24 hours)
        const performanceResponse = await ApiService.getPerformanceData();
        
        // Format performance data for chart
        const labels = performanceResponse.data.timestamps.map(ts => 
          moment(ts).format('HH:mm')
        );
        
        setPerformanceData({
          labels,
          datasets: [
            {
              label: 'ROI',
              data: performanceResponse.data.roi,
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              tension: 0.4
            },
            {
              label: 'Allocated Resources',
              data: performanceResponse.data.allocated_resources,
              borderColor: 'rgba(153, 102, 255, 1)',
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
              tension: 0.4
            }
          ]
        });
        
        setError(null);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
        setError('Failed to load dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
    
    // Refresh data every 5 minutes
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);

  // Prepare allocation data for pie chart
  const allocationChartData = {
    labels: ['Service', 'Content', 'Marketplace'],
    datasets: [
      {
        data: [
          allocation?.category_allocation?.service || 0,
          allocation?.category_allocation?.content || 0,
          allocation?.category_allocation?.marketplace || 0
        ],
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)'
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)'
        ],
        borderWidth: 1
      }
    ]
  };

  // Handle system run
  const handleRunSystem = async () => {
    try {
      setLoading(true);
      await ApiService.runSystem();
      // Refresh data after system run
      window.location.reload();
    } catch (err) {
      console.error('Error running system:', err);
      setError('Failed to run system. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !allocation) {
    return <div className="loading">Loading dashboard data...</div>;
  }

  return (
    <div className="dashboard">
      <h1 className="page-title">Dashboard</h1>
      
      {error && (
        <Alert variant="danger">
          <FaExclamationTriangle className="me-2" />
          {error}
        </Alert>
      )}
      
      {/* System Status */}
      <Card className="mb-4">
        <Card.Header>
          <h5 className="mb-0">System Status</h5>
        </Card.Header>
        <Card.Body>
          <Row>
            <Col md={8}>
              <div className="system-services">
                <h6>Services</h6>
                {Object.entries(systemStatus.services || {}).map(([service, status]) => (
                  <div key={service} className="service-status">
                    <span className="service-name">{service.replace('_', ' ')}</span>
                    <span className={`status-badge ${status.status}`}>
                      {status.status}
                    </span>
                    {status.status === 'healthy' && (
                      <small>{status.response_time.toFixed(2)}s</small>
                    )}
                  </div>
                ))}
              </div>
            </Col>
            <Col md={4} className="text-center">
              <div className="system-actions">
                <Button 
                  variant="primary" 
                  size="lg" 
                  className="run-system-btn"
                  onClick={handleRunSystem}
                  disabled={loading}
                >
                  <FaRocket className="me-2" />
                  Run System Cycle
                </Button>
                <div className="mt-3">
                  <small>Last run: {systemStatus.metrics?.last_run || 'Never'}</small>
                </div>
              </div>
            </Col>
          </Row>
        </Card.Body>
      </Card>
      
      {/* Key Metrics */}
      <Row className="mb-4">
        <Col md={3}>
          <Card className="metric-card">
            <Card.Body>
              <div className="metric-icon">
                <FaMoneyBillWave />
              </div>
              <div className="metric-content">
                <h6>Total Allocated</h6>
                <h3>${allocation?.total_allocated.toFixed(2) || '0.00'}</h3>
                <small>of ${allocation?.max_allocation || '0.00'}</small>
              </div>
            </Card.Body>
            <div className="metric-progress">
              <ProgressBar 
                now={(allocation?.total_allocated / allocation?.max_allocation) * 100 || 0} 
                variant="success" 
              />
            </div>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="metric-card">
            <Card.Body>
              <div className="metric-icon">
                <FaChartLine />
              </div>
              <div className="metric-content">
                <h6>Current ROI</h6>
                <h3>{allocation?.current_roi?.toFixed(2) || '0.00'}%</h3>
                <small>Target: 50-100%</small>
              </div>
            </Card.Body>
            <div className="metric-progress">
              <ProgressBar 
                now={allocation?.current_roi || 0} 
                max={100}
                variant={allocation?.current_roi >= 50 ? "success" : "warning"} 
              />
            </div>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="metric-card">
            <Card.Body>
              <div className="metric-icon">
                <FaRocket />
              </div>
              <div className="metric-content">
                <h6>Opportunities</h6>
                <h3>{opportunities.length}</h3>
                <small>Active opportunities</small>
              </div>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card className="metric-card">
            <Card.Body>
              <div className="metric-icon">
                <FaMoneyBillWave />
              </div>
              <div className="metric-content">
                <h6>Reserve Funds</h6>
                <h3>${allocation?.reserve_funds.toFixed(2) || '0.00'}</h3>
                <small>{allocation?.reserve_ratio * 100 || 0}% of total</small>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      {/* Charts */}
      <Row className="mb-4">
        <Col md={8}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Performance (Last 24 Hours)</h5>
            </Card.Header>
            <Card.Body>
              <Line 
                data={performanceData} 
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true
                    }
                  }
                }}
                height={300}
              />
            </Card.Body>
          </Card>
        </Col>
        <Col md={4}>
          <Card>
            <Card.Header>
              <h5 className="mb-0">Resource Allocation</h5>
            </Card.Header>
            <Card.Body>
              <Pie 
                data={allocationChartData} 
                options={{
                  responsive: true,
                  maintainAspectRatio: false
                }}
                height={300}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>
      
      {/* Top Opportunities */}
      <Card>
        <Card.Header>
          <h5 className="mb-0">Top Opportunities</h5>
        </Card.Header>
        <Card.Body>
          <div className="table-responsive">
            <table className="table table-hover">
              <thead>
                <tr>
                  <th>Opportunity</th>
                  <th>Category</th>
                  <th>Platform</th>
                  <th>Expected ROI</th>
                  <th>Allocated</th>
                  <th>Risk Score</th>
                </tr>
              </thead>
              <tbody>
                {opportunities.slice(0, 5).map(opp => (
                  <tr key={opp.id}>
                    <td>{opp.title}</td>
                    <td>{opp.category}</td>
                    <td>{opp.platform}</td>
                    <td>{(opp.expected_roi * 100).toFixed(2)}%</td>
                    <td>${opp.allocated_amount?.toFixed(2) || '0.00'}</td>
                    <td>
                      <div className="risk-indicator">
                        <div 
                          className="risk-level" 
                          style={{
                            width: `${opp.risk_score * 100}%`,
                            backgroundColor: opp.risk_score < 0.3 ? 'green' : 
                                            opp.risk_score < 0.7 ? 'orange' : 'red'
                          }}
                        ></div>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card.Body>
      </Card>
    </div>
  );
};

export default Dashboard;