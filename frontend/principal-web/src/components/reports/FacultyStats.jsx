import React from 'react';
import { Users } from 'lucide-react';

/**
 * FacultyStats Component
 * Hiển thị thống kê theo khoa
 */
const FacultyStats = () => {
  const facultyData = [
    { name: 'Công nghệ Thông tin', count: 45, color: 'from-blue-400 to-blue-600' },
    { name: 'Quản trị Kinh doanh', count: 38, color: 'from-green-400 to-green-600' },
    { name: 'Kỹ thuật', count: 32, color: 'from-purple-400 to-purple-600' },
    { name: 'Khoa học Xã hội', count: 28, color: 'from-yellow-400 to-yellow-600' },
    { name: 'Ngoại ngữ', count: 25, color: 'from-pink-400 to-pink-600' }
  ];

  const maxCount = Math.max(...facultyData.map(f => f.count));

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
      <h3 className="text-lg font-bold text-gray-800 mb-4 flex items-center">
        <Users className="w-5 h-5 mr-2 text-indigo-600" />
        Thống kê theo Khoa
      </h3>
      
      <div className="space-y-4">
        {facultyData.map((faculty, idx) => (
          <div key={idx} className="p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-700 font-medium">{faculty.name}</span>
              <span className="text-indigo-600 font-bold">{faculty.count}</span>
            </div>
            
            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className={`bg-gradient-to-r ${faculty.color} h-2 rounded-full transition-all duration-500`}
                style={{ width: `${(faculty.count / maxCount) * 100}%` }}
              ></div>
            </div>
          </div>
        ))}
      </div>

      {/* Total */}
      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="flex justify-between items-center">
          <span className="text-gray-600 font-medium">Tổng cộng</span>
          <span className="text-2xl font-bold text-indigo-600">
            {facultyData.reduce((sum, f) => sum + f.count, 0)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default FacultyStats;