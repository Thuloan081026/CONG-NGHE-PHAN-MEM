import React from 'react';
import { AlertTriangle, Zap, TrendingUp, Download } from 'lucide-react';

/**
 * ImpactAnalysisReport Component
 * Báo cáo phân tích ảnh hưởng của các thay đổi syllabus
 */
const ImpactAnalysisReport = () => {
  const impacts = [
    {
      syllabusId: 'SYL-2025-001',
      courseName: 'Cơ sở dữ liệu nâng cao',
      courseCode: 'CS301',
      faculty: 'Công nghệ Thông tin',
      changeType: 'Content Update',
      severity: 'low',
      affectedCourses: 2,
      affectedStudents: 145,
      description: 'Cập nhật nội dung để bao gồm công nghệ NoSQL mới nhất',
      risks: [
        'Sinh viên cần cập nhật kiến thức về NoSQL',
        'Tài liệu tham khảo cần được bổ sung'
      ],
      recommendations: [
        'Cung cấp tài liệu bổ sung cho sinh viên',
        'Tổ chức workshop giới thiệu NoSQL'
      ],
      status: 'approved'
    },
    {
      syllabusId: 'SYL-2025-002',
      courseName: 'Trí tuệ nhân tạo',
      courseCode: 'CS401',
      faculty: 'Công nghệ Thông tin',
      changeType: 'Credit Change',
      severity: 'medium',
      affectedCourses: 1,
      affectedStudents: 0,
      description: 'Tăng tín chỉ từ 2 lên 3 để phù hợp với chương trình quốc tế',
      risks: [
        'Ảnh hưởng đến tổng số tín chỉ của chương trình',
        'Sinh viên cũ có thể theo học phiên bản cũ hoặc mới'
      ],
      recommendations: [
        'Rà soát tổng tín chỉ của chương trình',
        'Cộng tác với các khoa khác nếu cần'
      ],
      status: 'pending'
    },
    {
      syllabusId: 'SYL-2025-003',
      courseName: 'Quản trị chiến lược',
      courseCode: 'BA301',
      faculty: 'Quản trị Kinh doanh',
      changeType: 'PLO Update',
      severity: 'high',
      affectedCourses: 5,
      affectedStudents: 320,
      description: 'Thay đổi mục tiêu học tập liên quan đến 2 PLO chính',
      risks: [
        'Ảnh hưởng trực tiếp đến chất lượng đạo tạo',
        'Cần xem xét lại các môn học liên quan',
        'Có thể ảnh hưởng đến chứng chỉ accreditation'
      ],
      recommendations: [
        'Kiểm tra tương thích với PLO của chương trình',
        'Rà soát lại các môn học tiên quyết',
        'Cập nhật curriculum map'
      ],
      status: 'needs_review'
    }
  ];

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'low':
        return 'bg-green-50 border-l-4 border-green-500';
      case 'medium':
        return 'bg-yellow-50 border-l-4 border-yellow-500';
      case 'high':
        return 'bg-red-50 border-l-4 border-red-500';
      default:
        return 'bg-gray-50';
    }
  };

  const getSeverityLabel = (severity) => {
    switch (severity) {
      case 'low':
        return '🟢 Thấp';
      case 'medium':
        return '🟡 Trung bình';
      case 'high':
        return '🔴 Cao';
      default:
        return 'Không xác định';
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Zap className="w-6 h-6 text-orange-600" />
            <h3 className="text-xl font-bold text-gray-800">Impact Analysis Report</h3>
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm">
            <Download className="w-4 h-4" />
            <span>Xuất báo cáo</span>
          </button>
        </div>

        {/* Summary */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-red-50 rounded-lg p-4 border-l-4 border-red-500">
            <p className="text-sm font-medium text-gray-600">Ảnh hưởng cao</p>
            <p className="text-2xl font-bold text-red-600">1</p>
          </div>
          <div className="bg-yellow-50 rounded-lg p-4 border-l-4 border-yellow-500">
            <p className="text-sm font-medium text-gray-600">Ảnh hưởng trung bình</p>
            <p className="text-2xl font-bold text-yellow-600">1</p>
          </div>
          <div className="bg-green-50 rounded-lg p-4 border-l-4 border-green-500">
            <p className="text-sm font-medium text-gray-600">Ảnh hưởng thấp</p>
            <p className="text-2xl font-bold text-green-600">1</p>
          </div>
          <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500">
            <p className="text-sm font-medium text-gray-600">Sinh viên bị ảnh hưởng</p>
            <p className="text-2xl font-bold text-blue-600">465</p>
          </div>
        </div>

        {/* Impact Details */}
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-800 flex items-center space-x-2">
            <TrendingUp className="w-5 h-5" />
            <span>Chi tiết ảnh hưởng</span>
          </h4>
          {impacts.map((impact, idx) => (
            <div key={idx} className={`rounded-lg p-5 ${getSeverityColor(impact.severity)}`}>
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <p className="text-lg font-bold text-gray-800">{impact.courseName}</p>
                  <p className="text-sm text-gray-600">{impact.courseCode} • {impact.faculty}</p>
                </div>
                <div className="text-right">
                  <span className={`px-3 py-1 rounded text-sm font-semibold ${
                    impact.severity === 'low'
                      ? 'bg-green-100 text-green-800'
                      : impact.severity === 'medium'
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-red-100 text-red-800'
                  }`}>
                    {getSeverityLabel(impact.severity)}
                  </span>
                </div>
              </div>

              <div className="bg-white bg-opacity-50 rounded p-3 mb-3">
                <p className="text-sm font-medium text-gray-700 mb-2">📋 Loại thay đổi</p>
                <p className="text-sm text-gray-700">{impact.description}</p>
              </div>

              <div className="grid grid-cols-2 gap-3 mb-3">
                <div className="bg-white bg-opacity-50 rounded p-3">
                  <p className="text-xs font-medium text-gray-600">Học phần liên quan</p>
                  <p className="text-xl font-bold text-gray-800">{impact.affectedCourses}</p>
                </div>
                <div className="bg-white bg-opacity-50 rounded p-3">
                  <p className="text-xs font-medium text-gray-600">Sinh viên bị ảnh hưởng</p>
                  <p className="text-xl font-bold text-gray-800">{impact.affectedStudents}</p>
                </div>
              </div>

              {/* Risks */}
              <div className="mb-3">
                <p className="text-sm font-semibold text-gray-700 mb-2 flex items-center space-x-1">
                  <AlertTriangle className="w-4 h-4" />
                  <span>Rủi ro tiềm ẩn:</span>
                </p>
                <ul className="space-y-1 text-sm">
                  {impact.risks.map((risk, i) => (
                    <li key={i} className="text-gray-700">• {risk}</li>
                  ))}
                </ul>
              </div>

              {/* Recommendations */}
              <div>
                <p className="text-sm font-semibold text-gray-700 mb-2">💡 Khuyến nghị:</p>
                <ul className="space-y-1 text-sm">
                  {impact.recommendations.map((rec, i) => (
                    <li key={i} className="text-gray-700">✓ {rec}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ImpactAnalysisReport;
