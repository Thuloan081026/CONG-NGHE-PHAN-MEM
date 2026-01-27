import React, { useState, useEffect } from 'react';
import Header from './components/common/Header';
import NavigationTabs from './components/common/NavigationTabs';
import OverviewPage from './pages/OverviewPage';
import ApprovalsPage from './pages/ApprovalsPage';
import ReportsPage from './pages/ReportsPage';
import APIService from './services/api.service';

/**
 * Quản lý state và điều hướng giữa các trang
 */
const App = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [notifications, setNotifications] = useState(3);
  
  // Data states
  const [pendingApprovals, setPendingApprovals] = useState([]);
  const [systemOverview, setSystemOverview] = useState(null);
  const [recentActivities, setRecentActivities] = useState([]);

  // Load dữ liệu ban đầu
  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [approvals, overview, activities] = await Promise.all([
        APIService.getPendingApprovals(),
        APIService.getSystemOverview(),
        APIService.getRecentActivities()
      ]);
      
      setPendingApprovals(approvals);
      setSystemOverview(overview);
      setRecentActivities(activities);
      setNotifications(approvals.length);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  // Hiển thị loading screen
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 font-medium">Đang tải dữ liệu...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <Header notifications={notifications} />

      {/* Navigation Tabs */}
      <NavigationTabs 
        activeTab={activeTab} 
        onTabChange={setActiveTab}
      />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {activeTab === 'overview' && (
          <OverviewPage 
            systemOverview={systemOverview}
            recentActivities={recentActivities}
          />
        )}

        {activeTab === 'approvals' && (
          <ApprovalsPage 
            pendingApprovals={pendingApprovals}
            onRefresh={loadDashboardData}
          />
        )}

        {activeTab === 'reports' && (
          <ReportsPage />
        )}
      </main>
    </div>
  );
};

export default App;