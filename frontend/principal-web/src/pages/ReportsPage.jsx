import React, { useState } from 'react';
import MonthlyReport from '../components/reports/MonthlyReport';
import FacultyStats from '../components/reports/FacultyStats';
import CLOPLOMappingReport from '../components/reports/CLOPLOMappingReport';
import ImpactAnalysisReport from '../components/reports/ImpactAnalysisReport';
import CurriculumCoverageReport from '../components/reports/CurriculumCoverageReport';
import AuditKPIReport from '../components/reports/AuditKPIReport';

/**
 * ReportsPage Component
 * Trang báo cáo strategically cho Principal
 * 
 * Chứa:
 * - CLO-PLO Mapping Report
 * - Impact Analysis Report
 * - Curriculum Coverage Report
 * - Audit & KPI Report
 */
const ReportsPage = () => {
  const [activeReport, setActiveReport] = useState('overview');

  const reportTabs = [
    { id: 'overview', label: 'Tổng quan', icon: '📊' },
    { id: 'mapping', label: 'CLO-PLO Mapping', icon: '📚' },
    { id: 'impact', label: 'Impact Analysis', icon: '⚡' },
    { id: 'coverage', label: 'Curriculum Coverage', icon: '📋' },
    { id: 'audit', label: 'Audit & KPI', icon: '📈' }
  ];

  return (
    <div className="space-y-6">
      {/* Report Tabs */}
      <div className="bg-white rounded-lg shadow-md p-4">
        <div className="flex items-center justify-between border-b border-gray-200 pb-4 mb-4">
          <h2 className="text-xl font-bold text-gray-800">Strategic Reports</h2>
        </div>
        <div className="flex flex-wrap gap-2">
          {reportTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveReport(tab.id)}
              className={`px-4 py-2 rounded-lg font-medium transition text-sm ${
                activeReport === tab.id
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <span className="mr-1">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Report Content */}
      <div>
        {activeReport === 'overview' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <MonthlyReport />
            <FacultyStats />
          </div>
        )}

        {activeReport === 'mapping' && <CLOPLOMappingReport />}

        {activeReport === 'impact' && <ImpactAnalysisReport />}

        {activeReport === 'coverage' && <CurriculumCoverageReport />}

        {activeReport === 'audit' && <AuditKPIReport />}
      </div>
    </div>
  );
};

export default ReportsPage;