import React, { useState } from 'react';
import { Grid, CheckCircle, AlertCircle, Download } from 'lucide-react';

/**
 * CurriculumCoverageReport Component
 * Báo cáo coverage của các PLO trong chương trình đào tạo
 */
const CurriculumCoverageReport = () => {
  const [selectedProgram, setSelectedProgram] = useState('cs_undergrad');

  const programs = [
    {
      id: 'cs_undergrad',
      name: 'Cử nhân Công nghệ Thông tin',
      plos: [
        {
          id: 'PLO1',
          name: 'Hiểu biết chuyên sâu về ngôn ngữ lập trình và cấu trúc dữ liệu',
          coverage: 100,
          courses: ['CS101', 'CS102', 'CS201', 'CS301'],
          status: 'complete'
        },
        {
          id: 'PLO2',
          name: 'Thiết kế và phát triển hệ thống phần mềm',
          coverage: 95,
          courses: ['CS201', 'CS202', 'CS301', 'CS302', 'CS401'],
          status: 'complete'
        },
        {
          id: 'PLO3',
          name: 'Quản lý cơ sở dữ liệu',
          coverage: 85,
          courses: ['CS102', 'CS201', 'CS301'],
          status: 'review'
        },
        {
          id: 'PLO4',
          name: 'Giao tiếp kỹ thuật và làm việc nhóm',
          coverage: 70,
          courses: ['CS101', 'GE101', 'CS401'],
          status: 'warning'
        },
        {
          id: 'PLO5',
          name: 'Nghiên cứu và phát triển kỹ năng tự học',
          coverage: 65,
          courses: ['CS401', 'CS402'],
          status: 'warning'
        }
      ]
    },
    {
      id: 'ba_undergrad',
      name: 'Cử nhân Quản trị Kinh doanh',
      plos: [
        {
          id: 'PLO1',
          name: 'Hiểu biết về quản lý chiến lược',
          coverage: 90,
          courses: ['BA101', 'BA301', 'BA401'],
          status: 'complete'
        },
        {
          id: 'PLO2',
          name: 'Kỹ năng phân tích dữ liệu kinh doanh',
          coverage: 75,
          courses: ['BA102', 'BA201', 'BA301'],
          status: 'review'
        },
        {
          id: 'PLO3',
          name: 'Kỹ năng lãnh đạo và quản lý nhân sự',
          coverage: 60,
          courses: ['BA201', 'BA401'],
          status: 'warning'
        }
      ]
    }
  ];

  const currentProgram = programs.find(p => p.id === selectedProgram);
  const avgCoverage = Math.round(
    currentProgram.plos.reduce((sum, plo) => sum + plo.coverage, 0) / currentProgram.plos.length
  );

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <Grid className="w-6 h-6 text-cyan-600" />
            <h3 className="text-xl font-bold text-gray-800">Curriculum Coverage Report</h3>
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition text-sm">
            <Download className="w-4 h-4" />
            <span>Xuất báo cáo</span>
          </button>
        </div>

        {/* Program Selector */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">Chọn chương trình</label>
          <div className="flex gap-2 flex-wrap">
            {programs.map((program) => (
              <button
                key={program.id}
                onClick={() => setSelectedProgram(program.id)}
                className={`px-4 py-2 rounded-lg font-medium transition ${
                  selectedProgram === program.id
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {program.name}
              </button>
            ))}
          </div>
        </div>

        {/* Coverage Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500">
            <p className="text-sm font-medium text-gray-600">Tổng PLO</p>
            <p className="text-2xl font-bold text-blue-600">{currentProgram.plos.length}</p>
          </div>
          <div className="bg-green-50 rounded-lg p-4 border-l-4 border-green-500">
            <p className="text-sm font-medium text-gray-600">Coverage trung bình</p>
            <p className="text-2xl font-bold text-green-600">{avgCoverage}%</p>
          </div>
          <div className="bg-purple-50 rounded-lg p-4 border-l-4 border-purple-500">
            <p className="text-sm font-medium text-gray-600">Cần cải thiện</p>
            <p className="text-2xl font-bold text-purple-600">
              {currentProgram.plos.filter(p => p.coverage < 80).length}
            </p>
          </div>
        </div>

        {/* PLO Coverage Details */}
        <div className="space-y-4">
          <h4 className="font-semibold text-gray-800">Chi tiết PLO Coverage</h4>
          {currentProgram.plos.map((plo, idx) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-bold text-indigo-600">{plo.id}</span>
                    {plo.status === 'complete' && <CheckCircle className="w-4 h-4 text-green-600" />}
                    {plo.status === 'review' && <AlertCircle className="w-4 h-4 text-yellow-600" />}
                    {plo.status === 'warning' && <AlertCircle className="w-4 h-4 text-red-600" />}
                  </div>
                  <p className="font-semibold text-gray-800">{plo.name}</p>
                </div>
                <div className="text-right">
                  <p className={`text-lg font-bold ${
                    plo.coverage >= 90
                      ? 'text-green-600'
                      : plo.coverage >= 80
                      ? 'text-yellow-600'
                      : 'text-red-600'
                  }`}>
                    {plo.coverage}%
                  </p>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="bg-gray-200 rounded-full h-3 mb-3 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all ${
                    plo.coverage >= 90
                      ? 'bg-green-500'
                      : plo.coverage >= 80
                      ? 'bg-yellow-500'
                      : 'bg-red-500'
                  }`}
                  style={{ width: `${plo.coverage}%` }}
                />
              </div>

              {/* Course List */}
              <div className="flex flex-wrap gap-2">
                {plo.courses.map((course, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-xs font-medium"
                  >
                    {course}
                  </span>
                ))}
              </div>

              {/* Recommendation */}
              {plo.coverage < 80 && (
                <div className="mt-3 bg-yellow-50 border-l-4 border-yellow-500 p-3 rounded">
                  <p className="text-xs font-semibold text-yellow-800">⚠️ Cần cải thiện:</p>
                  <p className="text-xs text-yellow-700 mt-1">
                    Xem xét thêm các học phần hoặc bổ sung nội dung vào các môn học hiện có để tăng coverage.
                  </p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CurriculumCoverageReport;
