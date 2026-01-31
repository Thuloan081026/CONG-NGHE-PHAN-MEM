import React, { useState } from 'react';
import { BarChart3, TrendingUp, Clock, CheckCircle, Download } from 'lucide-react';

/**
 * AuditKPIReport Component
 * Báo cáo kiểm toán và KPI của hệ thống phê duyệt
 */
const AuditKPIReport = () => {
  const [timeRange, setTimeRange] = useState('month');

  const kpiData = {
    week: {
      avgProcessTime: 2.5,
      approvalRate: 82,
      revisionRate: 18,
      totalProcessed: 11,
      totalApproved: 9,
      totalRevision: 2
    },
    month: {
      avgProcessTime: 3.2,
      approvalRate: 79,
      revisionRate: 21,
      totalProcessed: 42,
      totalApproved: 33,
      totalRevision: 9
    },
    quarter: {
      avgProcessTime: 3.5,
      approvalRate: 76,
      revisionRate: 24,
      totalProcessed: 125,
      totalApproved: 95,
      totalRevision: 30
    }
  };

  const currentData = kpiData[timeRange];

  const auditLog = [
    {
      date: '2025-01-24 10:30',
      action: 'Phê duyệt',
      syllabus: 'Lập trình Web (CS201)',
      approver: 'Principal',
      duration: '2 ngày',
      status: 'approved'
    },
    {
      date: '2025-01-23 15:45',
      action: 'Yêu cầu chỉnh sửa',
      syllabus: 'Marketing căn bản (MK101)',
      approver: 'Principal',
      duration: '3 ngày',
      status: 'revision'
    },
    {
      date: '2025-01-22 11:20',
      action: 'Phê duyệt',
      syllabus: 'Toán cao cấp 2 (MA102)',
      approver: 'Principal',
      duration: '1 ngày',
      status: 'approved'
    },
    {
      date: '2025-01-21 09:15',
      action: 'Phê duyệt',
      syllabus: 'Vật lý đại cương (PH101)',
      approver: 'Principal',
      duration: '2 ngày',
      status: 'approved'
    },
    {
      date: '2025-01-20 14:00',
      action: 'Yêu cầu chỉnh sửa',
      syllabus: 'Hóa học đại cương (CH101)',
      approver: 'Principal',
      duration: '4 ngày',
      status: 'revision'
    }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <BarChart3 className="w-6 h-6 text-teal-600" />
            <h3 className="text-xl font-bold text-gray-800">Audit & KPI Report</h3>
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm">
            <Download className="w-4 h-4" />
            <span>Xuất báo cáo</span>
          </button>
        </div>

        {/* Time Range Selector */}
        <div className="mb-6 flex gap-2">
          {['week', 'month', 'quarter'].map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                timeRange === range
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {range === 'week' ? 'Tuần này' : range === 'month' ? 'Tháng này' : 'Quý này'}
            </button>
          ))}
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-medium text-gray-600">Thời gian xử lý TB</p>
              <Clock className="w-4 h-4 text-blue-600" />
            </div>
            <p className="text-2xl font-bold text-blue-600">{currentData.avgProcessTime}</p>
            <p className="text-xs text-gray-600 mt-1">ngày</p>
          </div>

          <div className="bg-green-50 rounded-lg p-4 border-l-4 border-green-500">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-medium text-gray-600">Tỷ lệ phê duyệt</p>
              <CheckCircle className="w-4 h-4 text-green-600" />
            </div>
            <p className="text-2xl font-bold text-green-600">{currentData.approvalRate}%</p>
            <p className="text-xs text-gray-600 mt-1">{currentData.totalApproved} phê duyệt</p>
          </div>

          <div className="bg-yellow-50 rounded-lg p-4 border-l-4 border-yellow-500">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-medium text-gray-600">Yêu cầu chỉnh sửa</p>
              <TrendingUp className="w-4 h-4 text-yellow-600" />
            </div>
            <p className="text-2xl font-bold text-yellow-600">{currentData.revisionRate}%</p>
            <p className="text-xs text-gray-600 mt-1">{currentData.totalRevision} chỉnh sửa</p>
          </div>

          <div className="bg-purple-50 rounded-lg p-4 border-l-4 border-purple-500">
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm font-medium text-gray-600">Tổng xử lý</p>
              <BarChart3 className="w-4 h-4 text-purple-600" />
            </div>
            <p className="text-2xl font-bold text-purple-600">{currentData.totalProcessed}</p>
            <p className="text-xs text-gray-600 mt-1">đề cương</p>
          </div>
        </div>

        {/* Trend Chart Placeholder */}
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <h4 className="font-semibold text-gray-800 mb-4">Xu hướng thời gian xử lý</h4>
          <div className="h-64 flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg">
            <div className="text-center text-gray-500">
              <p className="font-medium mb-1">📊 Biểu đồ xu hướng</p>
              <p className="text-xs">Thời gian xử lý trung bình theo tuần</p>
              <div className="mt-4 flex justify-center gap-2 h-16">
                {[3.2, 3.5, 3.1, 2.8, 3.2, 2.5].map((h, i) => (
                  <div
                    key={i}
                    className="w-8 bg-indigo-500 rounded"
                    style={{ height: `${(h / 4) * 100}%` }}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Audit Log */}
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-800 flex items-center space-x-2">
            <Clock className="w-5 h-5" />
            <span>Lịch sử phê duyệt (Audit Log)</span>
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-300 bg-gray-50">
                  <th className="text-left py-3 px-3 font-semibold text-gray-700">Ngày giờ</th>
                  <th className="text-left py-3 px-3 font-semibold text-gray-700">Hành động</th>
                  <th className="text-left py-3 px-3 font-semibold text-gray-700">Học phần</th>
                  <th className="text-left py-3 px-3 font-semibold text-gray-700">Người phê duyệt</th>
                  <th className="text-left py-3 px-3 font-semibold text-gray-700">Thời gian xử lý</th>
                  <th className="text-center py-3 px-3 font-semibold text-gray-700">Trạng thái</th>
                </tr>
              </thead>
              <tbody>
                {auditLog.map((log, idx) => (
                  <tr key={idx} className="border-b border-gray-200 hover:bg-gray-50">
                    <td className="py-3 px-3 text-gray-700 text-xs font-mono">{log.date}</td>
                    <td className="py-3 px-3 text-gray-700">{log.action}</td>
                    <td className="py-3 px-3 text-gray-700">{log.syllabus}</td>
                    <td className="py-3 px-3 text-gray-700">{log.approver}</td>
                    <td className="py-3 px-3 text-gray-700">
                      <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-medium">
                        {log.duration}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-center">
                      {log.status === 'approved' ? (
                        <span className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">
                          ✓ Phê duyệt
                        </span>
                      ) : (
                        <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-xs font-medium">
                          ⚠ Chỉnh sửa
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuditKPIReport;
