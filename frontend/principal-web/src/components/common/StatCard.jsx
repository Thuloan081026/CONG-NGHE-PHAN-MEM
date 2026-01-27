import React from 'react';
import { STAT_CARD_COLORS } from '../../constants/config';

/**
 * StatCard Component
 * Hiển thị thẻ thống kê với icon, tiêu đề và giá trị
 * 
 * @param {string} title - Tiêu đề của thẻ
 * @param {string|number} value - Giá trị hiển thị
 * @param {Component} icon - Icon component từ lucide-react
 * @param {string} color - Màu sắc (blue, yellow, green, purple)
 * @param {string} badge - Badge hiển thị (ví dụ: 'urgent')
 */
const StatCard = ({ title, value, icon: Icon, color, badge }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200 hover:shadow-xl transition">
      <div className="flex items-start justify-between mb-4">
        <div className={`p-3 rounded-lg bg-gradient-to-br ${STAT_CARD_COLORS[color]} shadow-md`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        {badge === 'urgent' && value > 0 && (
          <span className="px-2 py-1 bg-red-100 text-red-600 text-xs font-bold rounded-full">
            Khẩn
          </span>
        )}
      </div>
      <h3 className="text-gray-500 text-sm font-medium mb-1">{title}</h3>
      <p className="text-3xl font-bold text-gray-800">{value}</p>
    </div>
  );
};

export default StatCard;