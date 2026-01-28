import React from 'react';
import { Activity, CheckCircle, TrendingUp } from 'lucide-react';

/**
 * NavigationTabs Component
 * Hiển thị các tab điều hướng
 * 
 * @param {string} activeTab - Tab đang active
 * @param {function} onTabChange - Callback khi đổi tab
 */
const NavigationTabs = ({ activeTab, onTabChange }) => {
  const tabs = [
    { id: 'overview', label: 'Tổng quan', icon: Activity },
    { id: 'approvals', label: 'Phê duyệt', icon: CheckCircle },
    { id: 'reports', label: 'Báo cáo', icon: TrendingUp }
  ];

  return (
    <div className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-6">
        <nav className="flex space-x-8">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex items-center space-x-2 py-4 px-2 border-b-2 font-medium transition ${
                activeTab === tab.id
                  ? 'border-indigo-600 text-indigo-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <tab.icon className="w-5 h-5" />
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default NavigationTabs;