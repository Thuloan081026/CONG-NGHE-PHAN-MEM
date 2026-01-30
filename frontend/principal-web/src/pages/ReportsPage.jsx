import React from 'react';
import MonthlyReport from '../components/reports/MonthlyReport';
import FacultyStats from '../components/reports/FacultyStats';

/**
 * ReportsPage Component
 * Trang báo cáo và thống kê
 */
const ReportsPage = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Monthly Report */}
      <MonthlyReport />

      {/* Faculty Stats */}
      <FacultyStats />
    </div>
  );
};

export default ReportsPage;