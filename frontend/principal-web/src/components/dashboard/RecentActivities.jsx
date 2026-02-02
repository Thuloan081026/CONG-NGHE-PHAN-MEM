import React from 'react';
import { Clock, CheckCircle, XCircle } from 'lucide-react';

/**
 * RecentActivities Component
 * Hiển thị các hoạt động gần đây
 * 
 * @param {array} activities - Danh sách hoạt động
 */
const RecentActivities = ({ activities }) => {
  if (!activities || activities.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
          <Clock className="w-5 h-5 mr-2 text-indigo-600" />
          Hoạt động gần đây
        </h3>
        <p className="text-gray-500 text-center py-8">Chưa có hoạt động nào</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
        <Clock className="w-5 h-5 mr-2 text-indigo-600" />
        Hoạt động gần đây
      </h3>
      
      <div className="space-y-3">
        {activities.map(activity => (
          <div 
            key={activity.id} 
            className="flex items-start space-x-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
          >
            {activity.result === 'approved' ? (
              <CheckCircle className="w-5 h-5 text-green-500 mt-0.5 flex-shrink-0" />
            ) : (
              <XCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
            )}
            
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-800">{activity.action}</p>
              <p className="text-sm text-gray-600 truncate">{activity.syllabus}</p>
              <p className="text-xs text-gray-400 mt-1">{activity.timestamp}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentActivities;