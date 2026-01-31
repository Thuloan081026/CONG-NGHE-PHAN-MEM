import React, { useState } from 'react';
import { FileText, CheckCircle, XCircle, AlertCircle, Zap, GitCompare, BookOpen, Eye } from 'lucide-react';

/**
 * ApprovalModal Component
 * Modal để phê duyệt hoặc từ chối đề cương
 * Hỗ trợ: Approve, Request Revision, AI Summary, Semantic Diff, CLO-PLO Mapping
 * 
 * @param {object} syllabus - Thông tin đề cương
 * @param {function} onApprove - Callback khi phê duyệt
 * @param {function} onReject - Callback khi từ chối
 * @param {function} onRequestRevision - Callback khi yêu cầu chỉnh sửa
 * @param {function} onClose - Callback khi đóng modal
 */
const ApprovalModal = ({ syllabus, onApprove, onReject, onRequestRevision, onClose }) => {
  const [approvalComment, setApprovalComment] = useState('');
  const [revisionReason, setRevisionReason] = useState('');
  const [activeTab, setActiveTab] = useState('summary'); // summary, diff, mapping, details

  const handleApprove = () => {
    onApprove(syllabus.id, approvalComment);
  };

  const handleRequestRevision = () => {
    if (!revisionReason.trim()) {
      alert('Vui lòng nhập lý do yêu cầu chỉnh sửa');
      return;
    }
    if (onRequestRevision) {
      onRequestRevision(syllabus.id, revisionReason);
    } else {
      onReject(syllabus.id, revisionReason);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[95vh] overflow-hidden flex flex-col">
        {/* Header */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 rounded-t-xl">
          <h2 className="text-2xl font-bold text-white flex items-center">
            <FileText className="w-6 h-6 mr-2" />
            Chi tiết đề cương - Phê duyệt cuối cùng
          </h2>
          <p className="text-indigo-100 text-sm mt-1">Principal Decision</p>
        </div>
        
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {/* Course Info Header */}
          <div className="bg-gray-50 rounded-lg p-4 space-y-2 border-l-4 border-indigo-500">
            <h3 className="text-xl font-bold text-gray-800">{syllabus.courseName}</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
              <div><span className="font-medium text-gray-600">Mã học phần:</span> <span className="font-semibold">{syllabus.courseCode}</span></div>
              <div><span className="font-medium text-gray-600">Mã đề cương:</span> <span className="font-semibold">{syllabus.id}</span></div>
              <div><span className="font-medium text-gray-600">Khoa:</span> <span className="font-semibold">{syllabus.faculty}</span></div>
              <div><span className="font-medium text-gray-600">Người nộp:</span> <span className="font-semibold">{syllabus.submittedBy}</span></div>
              <div><span className="font-medium text-gray-600">Ngày nộp:</span> <span className="font-semibold">{syllabus.submittedDate}</span></div>
              <div><span className="font-medium text-gray-600">Loại:</span> <span className="font-semibold">{syllabus.type}</span></div>
            </div>
          </div>

          {/* Review Status - Approval Chain */}
          <div className="border-l-4 border-green-500 bg-green-50 p-4 rounded">
            <p className="font-semibold text-green-800 mb-3">✓ Đã được phê duyệt bởi:</p>
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
            <p className="text-sm text-green-700 mt-2">Bây giờ chờ phê duyệt cuối cùng từ Principal</p>
          </div>

          {/* Tabs */}
          <div className="border-b border-gray-200 flex space-x-1 bg-gray-50 rounded-lg p-1">
            <button
              onClick={() => setActiveTab('summary')}
              className={`flex-1 py-2 px-3 rounded text-sm font-medium transition ${
                activeTab === 'summary'
                  ? 'bg-white text-indigo-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              <Zap className="w-4 h-4 inline mr-1" /> AI Summary
            </button>
            <button
              onClick={() => setActiveTab('diff')}
              className={`flex-1 py-2 px-3 rounded text-sm font-medium transition ${
                activeTab === 'diff'
                  ? 'bg-white text-indigo-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              <GitCompare className="w-4 h-4 inline mr-1" /> Semantic Diff
            </button>
            <button
              onClick={() => setActiveTab('mapping')}
              className={`flex-1 py-2 px-3 rounded text-sm font-medium transition ${
                activeTab === 'mapping'
                  ? 'bg-white text-indigo-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              <BookOpen className="w-4 h-4 inline mr-1" /> CLO-PLO Map
            </button>
            <button
              onClick={() => setActiveTab('details')}
              className={`flex-1 py-2 px-3 rounded text-sm font-medium transition ${
                activeTab === 'details'
                  ? 'bg-white text-indigo-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              <Eye className="w-4 h-4 inline mr-1" /> Chi tiết
            </button>
          </div>

          {/* Tab Content */}
          <div className="bg-gray-50 rounded-lg p-4 min-h-[250px]">
            {/* AI Summary Tab */}
            {activeTab === 'summary' && (
              <div className="space-y-4">
                <div className="bg-white rounded p-4 border border-indigo-200">
                  <h4 className="font-bold text-indigo-900 mb-2 flex items-center">
                    <Zap className="w-5 h-5 mr-2 text-yellow-500" />
                    Tóm tắt AI - Đề xuất quyết định
                  </h4>
                  <div className="space-y-3 text-sm">
                    <div className="bg-blue-50 border-l-4 border-blue-500 p-3 rounded">
                      <p className="font-semibold text-blue-900">Chất lượng nội dung</p>
                      <p className="text-blue-800">Đề cương được kiểm tra CLO-PLO mapping, đảm bảo phù hợp với chuẩn đầu ra chương trình. Nội dung được cập nhật phù hợp với xu hướng công nghệ mới nhất.</p>
                      <p className="text-xs text-blue-700 mt-1">✓ Tất cả CLO được map đúng với PLO</p>
                    </div>
                    <div className="bg-green-50 border-l-4 border-green-500 p-3 rounded">
                      <p className="font-semibold text-green-900">Ảnh hưởng học thuật</p>
                      <p className="text-green-800">Không có xung đột với các môn học liên quan. Tín chỉ và thời lượng hợp lý.</p>
                      <p className="text-xs text-green-700 mt-1">✓ Không ảnh hưởng đến chương trình khác</p>
                    </div>
                    <div className="bg-purple-50 border-l-4 border-purple-500 p-3 rounded">
                      <p className="font-semibold text-purple-900">Khuyến nghị</p>
                      <p className="text-purple-800"><strong>Phê duyệt:</strong> Đề cương sẵn sàng để triển khai từ học kỳ tới.</p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Semantic Diff Tab */}
            {activeTab === 'diff' && (
              <div className="space-y-3">
                <div className="bg-white rounded p-4 border border-yellow-200">
                  <h4 className="font-bold text-yellow-900 mb-3 flex items-center">
                    <GitCompare className="w-5 h-5 mr-2" />
                    So sánh với phiên bản trước
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between items-start border-b pb-2">
                      <span className="font-medium">Nội dung chương trình</span>
                      <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs">20% thay đổi</span>
                    </div>
                    <div className="flex justify-between items-start border-b pb-2">
                      <span className="font-medium">Phương pháp giảng dạy</span>
                      <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">5% thay đổi</span>
                    </div>
                    <div className="flex justify-between items-start">
                      <span className="font-medium">Đánh giá kết quả học</span>
                      <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">Không thay đổi</span>
                    </div>
                  </div>
                  <p className="text-xs text-gray-600 mt-3">Các thay đổi đều nằm trong phạm vi chấp nhận và không ảnh hưởng tới PLO.</p>
                </div>
              </div>
            )}

            {/* CLO-PLO Mapping Tab */}
            {activeTab === 'mapping' && (
              <div className="space-y-3">
                <div className="bg-white rounded p-4 border border-emerald-200">
                  <h4 className="font-bold text-emerald-900 mb-3">CLO-PLO Mapping Validation</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center justify-between">
                      <span>CLO 1: Hiểu khái niệm cơ bản</span>
                      <span className="text-xs">→ PLO 1 ✓</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>CLO 2: Áp dụng vào thực tiễn</span>
                      <span className="text-xs">→ PLO 2, PLO 3 ✓</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>CLO 3: Phân tích vấn đề</span>
                      <span className="text-xs">→ PLO 4 ✓</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>CLO 4: Sáng tạo giải pháp</span>
                      <span className="text-xs">→ PLO 5 ✓</span>
                    </div>
                  </div>
                  <p className="text-xs text-emerald-700 mt-3 font-semibold">✓ Tất cả CLO được map chính xác với PLO</p>
                </div>
              </div>
            )}

            {/* Details Tab */}
            {activeTab === 'details' && (
              <div className="space-y-3">
                <div className="bg-white rounded p-4 border border-gray-200">
                  <h4 className="font-bold text-gray-900 mb-3">Thông tin chi tiết</h4>
                  <div className="space-y-2 text-sm grid grid-cols-2 gap-4">
                    <div>
                      <p className="font-medium text-gray-600">Tín chỉ:</p>
                      <p className="text-gray-800">{syllabus.credits || '3'}</p>
                    </div>
                    <div>
                      <p className="font-medium text-gray-600">Tiền quyết:</p>
                      <p className="text-gray-800">{syllabus.prerequisite || 'Không'}</p>
                    </div>
                    <div>
                      <p className="font-medium text-gray-600">Phương pháp đánh giá:</p>
                      <p className="text-gray-800">{syllabus.assessment || 'Kiểm tra + Bài tập + Thi cuối kỳ'}</p>
                    </div>
                    <div>
                      <p className="font-medium text-gray-600">Mục tiêu chương trình (PLO):</p>
                      <p className="text-gray-800">{syllabus.ploCount || '4'} PLO</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Decision Section */}
          <div className="border-t pt-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Approval Comment */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  💬 Nhận xét (khi phê duyệt)
                </label>
                <textarea
                  value={approvalComment}
                  onChange={(e) => setApprovalComment(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm"
                  rows="3"
                  placeholder="Nhập nhận xét của bạn..."
                />
              </div>

              {/* Revision Reason */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  📝 Lý do yêu cầu chỉnh sửa
                </label>
                <textarea
                  value={revisionReason}
                  onChange={(e) => setRevisionReason(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent text-sm"
                  rows="3"
                  placeholder="Nhập lý do chỉnh sửa..."
                />
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons - Fixed at bottom */}
        <div className="border-t bg-gray-50 p-4 rounded-b-xl flex gap-3 justify-end">
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition font-semibold text-sm"
          >
            Hủy
          </button>
          
          <button
            onClick={handleRequestRevision}
            className="px-6 py-2 bg-gradient-to-r from-yellow-500 to-yellow-600 text-white rounded-lg hover:from-yellow-600 hover:to-yellow-700 transition font-semibold flex items-center space-x-2 shadow-lg text-sm"
          >
            <AlertCircle className="w-4 h-4" />
            <span>Yêu cầu chỉnh sửa</span>
          </button>
          
          <button
            onClick={handleApprove}
            className="px-6 py-2 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-green-600 hover:to-green-700 transition font-semibold flex items-center space-x-2 shadow-lg text-sm"
          >
            <CheckCircle className="w-4 h-4" />
            <span>Phê duyệt</span>
          </button>
        </div>
      </div>
    </div>
  );
};
};

export default ApprovalModal;