import React from 'react';
import StatsGrid from '../components/dashboard/StatsGrid';
import SystemStatus from '../components/dashboard/SystemStatus';
import RecentActivities from '../components/dashboard/RecentActivities';

/**
 * OverviewPage Component
 * Trang tổng quan hệ thống
 * 
 * @param {object} systemOverview - Dữ liệu tổng quan
 * @param {array} recentActivities - Hoạt động gần đây
 */
const OverviewPage = ({ systemOverview, recentActivities }) => {
  return (
    <div className="space-y-6">
      {/* Stats Grid */}
      <StatsGrid data={systemOverview} />

      {/* Overview Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* System Status */}
        <SystemStatus data={systemOverview} />

        {/* Recent Activities */}
        <RecentActivities activities={recentActivities} />
      </div>
    </div>
  );
};

export default OverviewPage;