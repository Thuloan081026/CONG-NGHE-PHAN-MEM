import React from 'react';
import { Activity } from 'lucide-react';

/**
 * SystemStatus Component
 * Hiển thị tình trạng hệ thống
 * 
 * @param {object} data - Dữ liệu hệ thống
 */
const SystemStatus = ({ data }) => {
  if (!data) return null;

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
        <Activity className="w-5 h-5 mr-2 text-indigo-600" />
        Tình trạng hệ thống
      </h3>
      
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Khoa/Viện</span>
          <span className="font-bold text-gray-800">{data.faculties}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Giảng viên</span>
          <span className="font-bold text-gray-800">{data.activeLecturers}</span>
        </div>
        
        <div className="flex justify-between items-center">
          <span className="text-gray-600">Sinh viên</span>
          <span className="font-bold text-gray-800">{data.students.toLocaleString()}</span>
        </div>
        
        <div className="pt-4 border-t border-gray-200">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-gray-600">Hiệu suất hệ thống</span>
            <span className="text-sm font-semibold text-green-600">{data.systemHealth}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-green-400 to-green-600 h-2 rounded-full" 
              style={{ width: `${data.systemHealth}%` }}
            ></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemStatus;