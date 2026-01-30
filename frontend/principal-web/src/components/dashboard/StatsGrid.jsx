import React from 'react';
import { FileText, Clock, CheckCircle, Activity } from 'lucide-react';
import StatCard from '../common/StatCard';

/**
 * StatsGrid Component
 * Hiển thị lưới thống kê tổng quan
 * 
 * @param {object} data - Dữ liệu thống kê từ API
 */
const StatsGrid = ({ data }) => {
  if (!data) return null;

  const stats = [
    {
      title: 'Tổng đề cương',
      value: data.totalSyllabi,
      icon: FileText,
      color: 'blue'
    },
    {
      title: 'Chờ phê duyệt',
      value: data.pendingApprovals,
      icon: Clock,
      color: 'yellow',
      badge: 'urgent'
    },
    {
      title: 'Phê duyệt tháng này',
      value: data.approvedThisMonth,
      icon: CheckCircle,
      color: 'green'
    },
    {
      title: 'Sức khỏe hệ thống',
      value: `${data.systemHealth}%`,
      icon: Activity,
      color: 'purple'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </div>
  );
};

export default StatsGrid;