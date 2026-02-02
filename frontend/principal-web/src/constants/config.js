// Cấu hình hệ thống và các hằng số

export const APP_CONFIG = {
  APP_NAME: 'SMD System - Principal',
  APP_DESCRIPTION: 'Hệ thống Quản lý Đề cương - Hiệu trưởng',
  VERSION: '1.0.0',
  API_TIMEOUT: 30000, // 30 seconds
};

export const USER_INFO = {
  name: 'PGS. TS. Nguyễn Xuân Phương',
  role: 'Principal',
  title: 'Hiệu trưởng',
  avatar: 'P'
};

export const TABS = [
  { id: 'overview', label: 'Tổng quan', icon: 'Activity' },
  { id: 'approvals', label: 'Phê duyệt', icon: 'CheckCircle' },
  { id: 'reports', label: 'Báo cáo', icon: 'TrendingUp' }
];

export const PRIORITY_LEVELS = {
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low'
};

export const PRIORITY_LABELS = {
  high: 'Ưu tiên cao',
  medium: 'Ưu tiên trung bình',
  low: 'Ưu tiên thấp'
};

export const PRIORITY_COLORS = {
  high: 'bg-red-100 text-red-700',
  medium: 'bg-yellow-100 text-yellow-700',
  low: 'bg-blue-100 text-blue-700'
};

export const APPROVAL_STATUS = {
  DRAFT: 'Draft',
  PENDING_REVIEW: 'Pending Review',
  PENDING_APPROVAL: 'Pending Approval',
  PENDING_FINAL: 'Pending Final Approval',
  APPROVED: 'Approved',
  PUBLISHED: 'Published',
  REJECTED: 'Rejected'
};

export const STAT_CARD_COLORS = {
  blue: 'from-blue-500 to-blue-600',
  yellow: 'from-yellow-500 to-yellow-600',
  green: 'from-green-500 to-green-600',
  purple: 'from-purple-500 to-purple-600',
  indigo: 'from-indigo-500 to-indigo-600',
  red: 'from-red-500 to-red-600'
};

export const NOTIFICATION_TYPES = {
  SUCCESS: 'success',
  ERROR: 'error',
  WARNING: 'warning',
  INFO: 'info'
};

export const MONTH_LABELS = [
  'Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4', 
  'Tháng 5', 'Tháng 6', 'Tháng 7', 'Tháng 8',
  'Tháng 9', 'Tháng 10', 'Tháng 11', 'Tháng 12'
];

export const FACULTIES = [
  'Công nghệ Thông tin',
  'Quản trị Kinh doanh',
  'Kỹ thuật',
  'Khoa học Xã hội',
  'Ngoại ngữ',
  'Khoa học Tự nhiên',
  'Y Dược',
  'Luật'
];