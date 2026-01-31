import React from 'react';
import { Eye } from 'lucide-react';
import { PRIORITY_LABELS, PRIORITY_COLORS } from '../../constants/config';

/**
 * SyllabusCard Component
 * Hiển thị thẻ thông tin đề cương
 * 
 * @param {object} syllabus - Thông tin đề cương
 * @param {function} onReview - Callback khi click xem xét
 * @param {function} onViewDetail - Callback khi xem chi tiết
 */
const SyllabusCard = ({ syllabus, onReview, onViewDetail }) => {
  return (
    <div className="border border-gray-200 rounded-lg p-5 hover:shadow-md transition bg-gradient-to-r from-white to-gray-50">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          {/* Badges */}
          <div className="flex items-center space-x-3 mb-2">
            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${PRIORITY_COLORS[syllabus.priority]}`}>
              {PRIORITY_LABELS[syllabus.priority]}
            </span>
            <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold">
              {syllabus.type}
            </span>
          </div>

          {/* Course Name */}
          <h3 className="text-lg font-bold text-gray-800 mb-1">
            {syllabus.courseName} ({syllabus.courseCode})
          </h3>

          {/* Details Grid */}
          <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-3">
            <div>
              <span className="font-medium">Khoa:</span> {syllabus.faculty}
            </div>
            <div>
              <span className="font-medium">Người nộp:</span> {syllabus.submittedBy}
            </div>
            <div>
              <span className="font-medium">Ngày nộp:</span> {syllabus.submittedDate}
            </div>
            <div>
              <span className="font-medium">Mã:</span> {syllabus.id}
            </div>
          </div>

          {/* Reviewed By */}
          <div className="flex items-center space-x-2 mb-3">
            <span className="text-sm text-gray-600">Đã được duyệt bởi:</span>
            {syllabus.reviewedBy.map((reviewer, idx) => (
              <span 
                key={idx} 
                className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium"
              >
                ✓ {reviewer}
              </span>
            ))}
          </div>
        </div>

        {/* Action Button */}
        <div className="flex flex-col space-y-2 ml-4">
          {onViewDetail && (
            <button 
              onClick={() => onViewDetail(syllabus)}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition font-medium flex items-center space-x-2"
            >
              <Eye className="w-4 h-4" />
              <span>Chi tiết</span>
            </button>
          )}
          <button 
            onClick={() => onReview(syllabus)}
            className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition font-medium flex items-center space-x-2 shadow-md"
          >
            <Eye className="w-4 h-4" />
            <span>Xem xét</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SyllabusCard;