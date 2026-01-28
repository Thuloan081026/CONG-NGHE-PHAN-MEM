import React, { useState } from 'react';
import { FileText, CheckCircle, XCircle, AlertCircle } from 'lucide-react';

/**
 * ApprovalModal Component
 * Modal để phê duyệt hoặc từ chối đề cương
 * 
 * @param {object} syllabus - Thông tin đề cương
 * @param {function} onApprove - Callback khi phê duyệt
 * @param {function} onReject - Callback khi từ chối
 * @param {function} onClose - Callback khi đóng modal
 */
const ApprovalModal = ({ syllabus, onApprove, onReject, onClose }) => {
  const [approvalComment, setApprovalComment] = useState('');
  const [rejectionReason, setRejectionReason] = useState('');

  const handleApprove = () => {
    onApprove(syllabus.id, approvalComment);
  };

  const handleReject = () => {
    if (!rejectionReason.trim()) {
      alert('Vui lòng nhập lý do yêu cầu chỉnh sửa');
      return;
    }
    onReject(syllabus.id, rejectionReason);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 rounded-t-xl">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <FileText className="w-6 h-6 mr-2" />
            Chi tiết đề cương - Phê duyệt cuối cùng
          </h2>
        </div>
        
        <div className="p-6 space-y-6">
          {/* Course Info */}
          <div className="bg-gray-50 rounded-lg p-4 space-y-2">
            <h3 className="text-xl font-bold text-gray-800">{syllabus.courseName}</h3>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div><span className="font-medium">Mã học phần:</span> {syllabus.courseCode}</div>
              <div><span className="font-medium">Mã đề cương:</span> {syllabus.id}</div>
              <div><span className="font-medium">Khoa:</span> {syllabus.faculty}</div>
              <div><span className="font-medium">Người nộp:</span> {syllabus.submittedBy}</div>
              <div><span className="font-medium">Ngày nộp:</span> {syllabus.submittedDate}</div>
              <div><span className="font-medium">Loại:</span> {syllabus.type}</div>
            </div>
          </div>

          {/* Review Status */}
          <div className="border-l-4 border-green-500 bg-green-50 p-4 rounded">
            <p className="font-semibold text-green-800 mb-2">Đã được phê duyệt bởi:</p>
            <div className="flex flex-wrap gap-2">
              {syllabus.reviewedBy.map((reviewer, idx) => (
                <span 
                  key={idx} 
                  className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium"
                >
                  ✓ {reviewer}
                </span>
              ))}
            </div>
          </div>

          {/* AI Summary */}
          <div className="border border-indigo-200 rounded-lg p-4 bg-indigo-50">
            <h4 className="font-bold text-indigo-900 mb-2 flex items-center">
              <AlertCircle className="w-4 h-4 mr-2" />
              Tóm tắt AI
            </h4>
            <p className="text-sm text-gray-700">
              Đề cương đã được kiểm tra CLO-PLO mapping, đảm bảo phù hợp với chuẩn đầu ra chương trình. 
              Nội dung được cập nhật phù hợp với xu hướng công nghệ mới nhất.
            </p>
          </div>

          {/* Approval Comment */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Nhận xét phê duyệt (không bắt buộc)
            </label>
            <textarea
              value={approvalComment}
              onChange={(e) => setApprovalComment(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              rows="3"
              placeholder="Nhập nhận xét của bạn..."
            />
          </div>

          {/* Rejection Reason */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Lý do yêu cầu chỉnh sửa (nếu từ chối)
            </label>
            <textarea
              value={rejectionReason}
              onChange={(e) => setRejectionReason(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              rows="3"
              placeholder="Nhập lý do yêu cầu chỉnh sửa..."
            />
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              onClick={handleApprove}
              className="flex-1 px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition font-semibold flex items-center justify-center space-x-2 shadow-lg"
            >
              <CheckCircle className="w-5 h-5" />
              <span>Phê duyệt</span>
            </button>
            
            <button
              onClick={handleReject}
              className="flex-1 px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 transition font-semibold flex items-center justify-center space-x-2 shadow-lg"
            >
              <XCircle className="w-5 h-5" />
              <span>Yêu cầu chỉnh sửa</span>
            </button>
            
            <button
              onClick={onClose}
              className="px-6 py-3 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition font-semibold"
            >
              Hủy
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ApprovalModal;