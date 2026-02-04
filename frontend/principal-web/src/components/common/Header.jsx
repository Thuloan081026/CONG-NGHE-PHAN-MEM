import React from 'react';
import { Bell, FileText } from 'lucide-react';
import { APP_CONFIG, USER_INFO } from '../../constants/config';

/**
 * Header Component
 * Hiển thị header của ứng dụng với thông tin user và notifications
 * 
 * @param {number} notifications - Số lượng thông báo chưa đọc
 */
const Header = ({ notifications = 0 }) => {
  return (
    <header className="bg-white shadow-md border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo & App Name */}
          <div className="flex items-center space-x-4">
            <div className="bg-gradient-to-br from-indigo-600 to-purple-600 p-3 rounded-xl shadow-lg">
              <FileText className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">{APP_CONFIG.APP_NAME}</h1>
              <p className="text-sm text-gray-500">{APP_CONFIG.APP_DESCRIPTION}</p>
            </div>
          </div>

          {/* User Info & Notifications */}
          <div className="flex items-center space-x-4">
            {/* Notification Bell */}
            <div className="relative">
              <Bell className="w-6 h-6 text-gray-600 cursor-pointer hover:text-indigo-600 transition" />
              {notifications > 0 && (
                <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
                  {notifications}
                </span>
              )}
            </div>

            {/* User Profile */}
            <div className="flex items-center space-x-2 bg-gray-100 rounded-lg px-4 py-2">
              <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                {USER_INFO.avatar}
              </div>
              <div className="text-sm">
                <p className="font-semibold text-gray-800">{USER_INFO.name}</p>
                <p className="text-gray-500 text-xs">{USER_INFO.title}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;