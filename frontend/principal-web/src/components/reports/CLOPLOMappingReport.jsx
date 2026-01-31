import React, { useState } from 'react';
import { BookOpen, CheckCircle, AlertCircle, Download } from 'lucide-react';

/**
 * CLOPLOMappingReport Component
 * Báo cáo CLO-PLO Mapping cho toàn trường
 */
const CLOPLOMappingReport = () => {
  const [expandedFaculty, setExpandedFaculty] = useState('CS');

  const faculties = [
    {
      id: 'CS',
      name: 'Công nghệ Thông tin',
      totalCourses: 45,
      mappedCourses: 45,
      percentage: 100,
      status: 'complete',
      courses: [
        { code: 'CS101', name: 'Lập trình cơ bản', clos: 4, plos: 4, status: '✓' },
        { code: 'CS201', name: 'Cơ sở dữ liệu', clos: 3, plos: 3, status: '✓' },
        { code: 'CS301', name: 'Cơ sở dữ liệu nâng cao', clos: 4, plos: 4, status: '✓' },
      ]
    },
    {
      id: 'BA',
      name: 'Quản trị Kinh doanh',
      totalCourses: 38,
      mappedCourses: 36,
      percentage: 95,
      status: 'warning',
      courses: [
        { code: 'BA101', name: 'Quản trị căn bản', clos: 3, plos: 3, status: '✓' },
        { code: 'BA201', name: 'Marketing', clos: 4, plos: 3, status: '⚠' },
      ]
    },
    {
      id: 'ENG',
      name: 'Tiếng Anh',
      totalCourses: 28,
      mappedCourses: 25,
      percentage: 89,
      status: 'danger',
      courses: [
        { code: 'ENG101', name: 'Tiếng Anh 1', clos: 2, plos: 2, status: '✓' },
        { code: 'ENG201', name: 'Tiếng Anh chuyên ngành', clos: 3, plos: 2, status: '⚠' },
      ]
    }
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <BookOpen className="w-6 h-6 text-indigo-600" />
            <h3 className="text-xl font-bold text-gray-800">CLO-PLO Mapping Report</h3>
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm">
            <Download className="w-4 h-4" />
            <span>Xuất báo cáo</span>
          </button>
        </div>

        {/* Summary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 rounded-lg p-4">
            <p className="text-sm font-medium text-gray-600">Tổng học phần</p>
            <p className="text-2xl font-bold text-blue-600">111</p>
          </div>
          <div className="bg-green-50 rounded-lg p-4">
            <p className="text-sm font-medium text-gray-600">Đã mapping</p>
            <p className="text-2xl font-bold text-green-600">106</p>
          </div>
          <div className="bg-yellow-50 rounded-lg p-4">
            <p className="text-sm font-medium text-gray-600">Cần xem xét</p>
            <p className="text-2xl font-bold text-yellow-600">3</p>
          </div>
          <div className="bg-purple-50 rounded-lg p-4">
            <p className="text-sm font-medium text-gray-600">Tỷ lệ hoàn thành</p>
            <p className="text-2xl font-bold text-purple-600">95.5%</p>
          </div>
        </div>

        {/* Faculty Breakdown */}
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-800">Phân tích theo khoa</h4>
          {faculties.map((faculty) => (
            <div key={faculty.id} className="border border-gray-200 rounded-lg overflow-hidden">
              {/* Faculty Header */}
              <div
                onClick={() => setExpandedFaculty(expandedFaculty === faculty.id ? null : faculty.id)}
                className={`p-4 cursor-pointer flex items-center justify-between ${
                  faculty.status === 'complete'
                    ? 'bg-green-50 hover:bg-green-100'
                    : faculty.status === 'warning'
                    ? 'bg-yellow-50 hover:bg-yellow-100'
                    : 'bg-orange-50 hover:bg-orange-100'
                }`}
              >
                <div className="flex items-center space-x-4 flex-1">
                  {faculty.status === 'complete' ? (
                    <CheckCircle className="w-5 h-5 text-green-600" />
                  ) : (
                    <AlertCircle className="w-5 h-5 text-yellow-600" />
                  )}
                  <div>
                    <p className="font-semibold text-gray-800">{faculty.name}</p>
                    <p className="text-sm text-gray-600">
                      {faculty.mappedCourses}/{faculty.totalCourses} học phần
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`text-lg font-bold ${
                    faculty.status === 'complete'
                      ? 'text-green-600'
                      : faculty.status === 'warning'
                      ? 'text-yellow-600'
                      : 'text-orange-600'
                  }`}>
                    {faculty.percentage}%
                  </p>
                </div>
              </div>

              {/* Expanded Content */}
              {expandedFaculty === faculty.id && (
                <div className="bg-gray-50 border-t border-gray-200 p-4">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-gray-300">
                        <th className="text-left py-2 font-semibold text-gray-700">Mã học phần</th>
                        <th className="text-left py-2 font-semibold text-gray-700">Tên học phần</th>
                        <th className="text-center py-2 font-semibold text-gray-700">CLO</th>
                        <th className="text-center py-2 font-semibold text-gray-700">PLO</th>
                        <th className="text-center py-2 font-semibold text-gray-700">Trạng thái</th>
                      </tr>
                    </thead>
                    <tbody>
                      {faculty.courses.map((course, idx) => (
                        <tr key={idx} className="border-b border-gray-200 hover:bg-white">
                          <td className="py-2 font-mono text-xs">{course.code}</td>
                          <td className="py-2">{course.name}</td>
                          <td className="text-center py-2">{course.clos}</td>
                          <td className="text-center py-2">{course.plos}</td>
                          <td className="text-center py-2">
                            <span className={course.status === '✓' ? 'text-green-600' : 'text-yellow-600'}>
                              {course.status}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CLOPLOMappingReport;
