import React from 'react';
import { TrendingUp } from 'lucide-react';

/**
 * MonthlyReport Component
 * Hiển thị báo cáo phê duyệt theo tháng
 */
const MonthlyReport = () => {
  const monthlyData = [
    { month: 'Tháng 1/2025', approved: 28, rejected: 2 },
    { month: 'Tháng 2/2025', approved: 23, rejected: 3 },
    { month: 'Tháng 3/2025', approved: 18, rejected: 4 }
  ];

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
        <TrendingUp className="w-5 h-5 mr-2 text-indigo-600" />
        Báo cáo phê duyệt theo tháng
      </h3>
      
      <div className="space-y-3">
        {monthlyData.map((data, idx) => (
          <div 
            key={idx} 
            className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
          >
            <span className="text-gray-700 font-medium">{data.month}</span>
            <div className="flex items-center space-x-4">
              <span className="text-green-600 font-semibold">
                {data.approved} phê duyệt
              </span>
              <span className="text-red-600 font-semibold">
                {data.rejected} từ chối
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Summary */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-green-50 rounded-lg p-4 text-center">
            <p className="text-green-600 text-sm font-medium mb-1">Tổng phê duyệt</p>
            <p className="text-3xl font-bold text-green-700">
              {monthlyData.reduce((sum, d) => sum + d.approved, 0)}
            </p>
          </div>
          <div className="bg-red-50 rounded-lg p-4 text-center">
            <p className="text-red-600 text-sm font-medium mb-1">Tổng từ chối</p>
            <p className="text-3xl font-bold text-red-700">
              {monthlyData.reduce((sum, d) => sum + d.rejected, 0)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MonthlyReport;