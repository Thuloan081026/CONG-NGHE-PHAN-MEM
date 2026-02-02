import React from 'react';
import { CheckCircle, Filter, Download } from 'lucide-react';
import SyllabusCard from './SyllabusCard';

/**
 * ApprovalList Component
 * Hiển thị danh sách đề cương chờ phê duyệt
 * 
 * @param {array} syllabi - Danh sách đề cương
 * @param {function} onReview - Callback khi xem xét đề cương
 */
const ApprovalList = ({ syllabi, onReview }) => {
  if (!syllabi || syllabi.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <div className="text-center py-12">
          <CheckCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-gray-600 mb-2">
            Không có đề cương chờ phê duyệt
          </h3>
          <p className="text-gray-500">
            Tất cả đề cương đã được xử lý
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-800 flex items-center">
            <CheckCircle className="w-6 h-6 mr-2 text-indigo-600" />
            Đề cương chờ phê duyệt cuối cùng ({syllabi.length})
          </h2>
          
          <div className="flex space-x-2">
            <button className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition flex items-center space-x-2">
              <Filter className="w-4 h-4" />
              <span>Lọc</span>
            </button>
            <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition flex items-center space-x-2">
              <Download className="w-4 h-4" />
              <span>Xuất báo cáo</span>
            </button>
          </div>
        </div>

        {/* List */}
        <div className="space-y-4">
          {syllabi.map(syllabus => (
            <SyllabusCard 
              key={syllabus.id} 
              syllabus={syllabus} 
              onReview={onReview}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default ApprovalList;