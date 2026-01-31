import React, { useState } from 'react';
import { FileText, GitCompare, CheckCircle, AlertCircle, Download } from 'lucide-react';

/**
 * SyllabusDetailPanel Component
 * Hiển thị chi tiết đề cương với AI Summary, Semantic Diff, CLO-PLO Mapping
 */
const SyllabusDetailPanel = ({ syllabusId, onClose }) => {
  const [activeTab, setActiveTab] = useState('content');

  // Mock data - thay bằng real API
  const syllabusData = {
    id: syllabusId,
    courseName: 'Cơ sở dữ liệu nâng cao',
    courseCode: 'CS301',
    faculty: 'Công nghệ Thông tin',
    credits: 3,
    semester: 'Kỳ 2 - Năm 2024-2025',
    instructor: 'TS. Nguyễn Văn A',
    content: `
      # I. Mục tiêu môn học
      Sinh viên hiểu và áp dụng các kỹ thuật quản lý dữ liệu nâng cao...
      
      # II. Nội dung môn học
      1. Tối ưu hóa truy vấn SQL
      2. Xử lý giao dịch (Transaction Processing)
      3. Cơ sở dữ liệu NoSQL - MongoDB
      4. Distributed Databases
      ...
    `,
    cloMapping: [
      { id: 'CLO1', description: 'Thiết kế cơ sở dữ liệu phức tạp', status: 'complete' },
      { id: 'CLO2', description: 'Tối ưu hóa hiệu suất truy vấn', status: 'complete' },
      { id: 'CLO3', description: 'Quản lý giao dịch và bảo mật', status: 'complete' },
      { id: 'CLO4', description: 'Làm việc với NoSQL và Big Data', status: 'complete' }
    ],
    ploMapping: [
      { plo: 'PLO1', description: 'Hiểu biết chuyên sâu về cơ sở dữ liệu', coverage: 100 },
      { plo: 'PLO2', description: 'Thiết kế hệ thống phần mềm', coverage: 80 },
      { plo: 'PLO4', description: 'Giao tiếp kỹ thuật', coverage: 50 }
    ],
    aiSummary: {
      quality: 'Excellent',
      highlights: [
        'Nội dung được cập nhật với công nghệ mới nhất (NoSQL, Big Data)',
        'CLO-PLO mapping hoàn chỉnh và chính xác',
        'Phương pháp đánh giá phù hợp với mục tiêu học tập',
        'Tài liệu tham khảo đa dạng và cập nhật'
      ],
      risks: [
        'Tăng tín chỉ có thể ảnh hưởng đến course load'
      ],
      recommendations: [
        'Phê duyệt',
        'Tham khảo ý kiến từ các khoa kỹ thuật liên quan nếu cần'
      ]
    },
    semanticDiff: {
      added: [
        'Module 3: NoSQL Database Design',
        'Module 4: Distributed Database Management',
        'Project 2: NoSQL Implementation'
      ],
      modified: [
        'Learning outcomes được chi tiết hóa',
        'Assessment methods được cập nhật'
      ],
      removed: [
        'Deprecated: Legacy Database Systems'
      ]
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center mb-2">
              <FileText className="w-6 h-6 mr-2" />
              {syllabusData.courseName}
            </h2>
            <div className="text-indigo-100 text-sm space-y-1">
              <p>📍 {syllabusData.courseCode} • {syllabusData.faculty}</p>
              <p>👨‍🏫 {syllabusData.instructor} • {syllabusData.credits} tín chỉ</p>
              <p>📅 {syllabusData.semester}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-indigo-100 transition"
          >
            ✕
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 bg-gray-50 px-6">
        <div className="flex space-x-8">
          <button
            onClick={() => setActiveTab('content')}
            className={`py-4 px-2 font-medium transition border-b-2 ${
              activeTab === 'content'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-600 hover:text-gray-800'
            }`}
          >
            📝 Nội dung
          </button>
          <button
            onClick={() => setActiveTab('mapping')}
            className={`py-4 px-2 font-medium transition border-b-2 ${
              activeTab === 'mapping'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-600 hover:text-gray-800'
            }`}
          >
            📚 CLO-PLO Mapping
          </button>
          <button
            onClick={() => setActiveTab('diff')}
            className={`py-4 px-2 font-medium transition border-b-2 ${
              activeTab === 'diff'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-600 hover:text-gray-800'
            }`}
          >
            <GitCompare className="w-4 h-4 inline mr-1" />
            Semantic Diff
          </button>
          <button
            onClick={() => setActiveTab('summary')}
            className={`py-4 px-2 font-medium transition border-b-2 ${
              activeTab === 'summary'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-gray-600 hover:text-gray-800'
            }`}
          >
            🤖 AI Summary
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="p-6 max-h-[500px] overflow-y-auto space-y-4">
        {/* Content Tab */}
        {activeTab === 'content' && (
          <div className="space-y-4">
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
              <h4 className="font-bold text-blue-900 mb-2">📋 Mục tiêu môn học</h4>
              <p className="text-sm text-blue-800">
                Sinh viên hiểu và áp dụng các kỹ thuật quản lý dữ liệu nâng cao, 
                bao gồm tối ưu hóa, xử lý giao dịch, và các hệ thống dữ liệu phân tán.
              </p>
            </div>

            <div className="bg-gray-50 border border-gray-200 p-4 rounded">
              <h4 className="font-bold text-gray-900 mb-3">📚 Nội dung chính</h4>
              <ul className="space-y-2 text-sm text-gray-700">
                <li>✓ Tối ưu hóa truy vấn SQL</li>
                <li>✓ Xử lý giao dịch (Transaction Processing)</li>
                <li>✓ Cơ sở dữ liệu NoSQL - MongoDB</li>
                <li>✓ Cơ sở dữ liệu phân tán (Distributed Databases)</li>
                <li>✓ Big Data và Hadoop Ecosystem</li>
              </ul>
            </div>

            <div className="bg-purple-50 border border-purple-200 p-4 rounded">
              <h4 className="font-bold text-purple-900 mb-3">📊 Phương pháp đánh giá</h4>
              <div className="space-y-1 text-sm text-purple-800">
                <p>• Bài tập (20%)</p>
                <p>• Kiểm tra giữa kỳ (30%)</p>
                <p>• Project nhóm (20%)</p>
                <p>• Thi cuối kỳ (30%)</p>
              </div>
            </div>
          </div>
        )}

        {/* CLO-PLO Mapping Tab */}
        {activeTab === 'mapping' && (
          <div className="space-y-4">
            <div className="bg-white border border-green-200 p-4 rounded">
              <h4 className="font-bold text-green-900 mb-3">✓ CLO (Course Learning Outcomes)</h4>
              {syllabusData.cloMapping.map((clo, idx) => (
                <div key={idx} className="flex items-start space-x-3 mb-3">
                  <CheckCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{clo.id}</p>
                    <p className="text-sm text-gray-700">{clo.description}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="bg-white border border-indigo-200 p-4 rounded">
              <h4 className="font-bold text-indigo-900 mb-3">🎯 PLO (Program Learning Outcomes) Mapping</h4>
              {syllabusData.ploMapping.map((plo, idx) => (
                <div key={idx} className="mb-3">
                  <div className="flex items-center justify-between mb-2">
                    <p className="font-medium text-gray-900">{plo.plo}: {plo.description}</p>
                    <span className="text-indigo-600 font-bold">{plo.coverage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-indigo-600 h-2 rounded-full"
                      style={{ width: `${plo.coverage}%` }}
                    />
                  </div>
                </div>
              ))}
              <p className="text-xs text-green-700 mt-4 font-semibold">✓ Tất cả CLO được map chính xác với PLO</p>
            </div>
          </div>
        )}

        {/* Semantic Diff Tab */}
        {activeTab === 'diff' && (
          <div className="space-y-4">
            <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
              <h4 className="font-bold text-green-900 mb-2">➕ Thêm mới</h4>
              <ul className="space-y-1 text-sm text-green-800">
                {syllabusData.semanticDiff.added.map((item, idx) => (
                  <li key={idx}>+ {item}</li>
                ))}
              </ul>
            </div>

            <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
              <h4 className="font-bold text-yellow-900 mb-2">🔄 Sửa đổi</h4>
              <ul className="space-y-1 text-sm text-yellow-800">
                {syllabusData.semanticDiff.modified.map((item, idx) => (
                  <li key={idx}>~ {item}</li>
                ))}
              </ul>
            </div>

            <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
              <h4 className="font-bold text-red-900 mb-2">➖ Xóa</h4>
              <ul className="space-y-1 text-sm text-red-800">
                {syllabusData.semanticDiff.removed.map((item, idx) => (
                  <li key={idx}>- {item}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* AI Summary Tab */}
        {activeTab === 'summary' && (
          <div className="space-y-4">
            <div className="bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 p-4 rounded">
              <h4 className="font-bold text-indigo-900 mb-2 flex items-center">
                🤖 AI Evaluation Summary
              </h4>
              <p className="text-sm text-gray-700">
                <strong>Chất lượng:</strong> {syllabusData.aiSummary.quality}
              </p>
            </div>

            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
              <h4 className="font-bold text-blue-900 mb-2">✨ Điểm nổi bật</h4>
              <ul className="space-y-1 text-sm text-blue-800">
                {syllabusData.aiSummary.highlights.map((highlight, idx) => (
                  <li key={idx}>✓ {highlight}</li>
                ))}
              </ul>
            </div>

            <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
              <h4 className="font-bold text-yellow-900 mb-2">⚠️ Rủi ro tiềm ẩn</h4>
              <ul className="space-y-1 text-sm text-yellow-800">
                {syllabusData.aiSummary.risks.map((risk, idx) => (
                  <li key={idx}>⚠ {risk}</li>
                ))}
              </ul>
            </div>

            <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded">
              <h4 className="font-bold text-green-900 mb-2">💡 Khuyến nghị</h4>
              <ul className="space-y-1 text-sm text-green-800">
                {syllabusData.aiSummary.recommendations.map((rec, idx) => (
                  <li key={idx}>→ {rec}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-gray-200 bg-gray-50 p-4 flex justify-end gap-2">
        <button
          className="px-4 py-2 flex items-center space-x-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm"
        >
          <Download className="w-4 h-4" />
          <span>Xuất PDF</span>
        </button>
        <button
          onClick={onClose}
          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 transition text-sm"
        >
          Đóng
        </button>
      </div>
    </div>
  );
};

export default SyllabusDetailPanel;
