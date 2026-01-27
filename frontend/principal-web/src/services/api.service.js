// API Service - Xử lý tất cả các API calls
const APIService = {
  baseURL: 'https://api.smd-system.edu.vn', // Thay đổi URL này theo backend thực tế
  
  // Headers mặc định cho mọi request
  getHeaders() {
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token') || ''}`,
    };
  },

  // Generic request handler
  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        ...options,
        headers: {
          ...this.getHeaders(),
          ...options.headers,
        },
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // Lấy danh sách đề cương chờ phê duyệt
  async getPendingApprovals() {
    // Simulate API call - thay bằng real API
    await new Promise(resolve => setTimeout(resolve, 800));
    
    return [
      {
        id: 'SYL-2025-001',
        courseName: 'Cơ sở dữ liệu nâng cao',
        courseCode: 'CS301',
        faculty: 'Công nghệ Thông tin',
        submittedBy: 'TS. Nguyễn Văn A',
        submittedDate: '2025-01-20',
        priority: 'high',
        type: 'Đề cương mới',
        reviewedBy: ['HOD', 'Academic Affairs'],
        status: 'Pending Final Approval'
      },
      {
        id: 'SYL-2025-002',
        courseName: 'Trí tuệ nhân tạo',
        courseCode: 'CS401',
        faculty: 'Công nghệ Thông tin',
        submittedBy: 'PGS.TS. Trần Thị B',
        submittedDate: '2025-01-22',
        priority: 'medium',
        type: 'Cập nhật đề cương',
        reviewedBy: ['HOD', 'Academic Affairs'],
        status: 'Pending Final Approval'
      },
      {
        id: 'SYL-2025-003',
        courseName: 'Quản trị chiến lược',
        courseCode: 'BA301',
        faculty: 'Quản trị Kinh doanh',
        submittedBy: 'TS. Lê Văn C',
        submittedDate: '2025-01-23',
        priority: 'high',
        type: 'Đề cương mới',
        reviewedBy: ['HOD', 'Academic Affairs'],
        status: 'Pending Final Approval'
      }
    ];
    
    // Real API call sẽ như này:
    // return this.request('/api/approvals/pending');
  },

  // Lấy tổng quan hệ thống
  async getSystemOverview() {
    await new Promise(resolve => setTimeout(resolve, 600));
    
    return {
      totalSyllabi: 342,
      pendingApprovals: 3,
      approvedThisMonth: 28,
      faculties: 8,
      activeLecturers: 156,
      students: 4520,
      systemHealth: 98.5
    };
    
    // Real API: return this.request('/api/system/overview');
  },

  // Lấy hoạt động gần đây
  async getRecentActivities() {
    await new Promise(resolve => setTimeout(resolve, 500));
    
    return [
      {
        id: 1,
        action: 'Phê duyệt đề cương',
        syllabus: 'Lập trình Web (CS201)',
        user: 'Principal',
        timestamp: '2025-01-24 09:30',
        result: 'approved'
      },
      {
        id: 2,
        action: 'Yêu cầu chỉnh sửa',
        syllabus: 'Marketing căn bản (MK101)',
        user: 'Principal',
        timestamp: '2025-01-23 15:45',
        result: 'rejected'
      },
      {
        id: 3,
        action: 'Phê duyệt đề cương',
        syllabus: 'Toán cao cấp 2 (MA102)',
        user: 'Principal',
        timestamp: '2025-01-23 10:20',
        result: 'approved'
      }
    ];
    
    // Real API: return this.request('/api/activities/recent');
  },

  // Phê duyệt đề cương
  async approveSyllabus(syllabusId, comment = '') {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return { 
      success: true, 
      message: 'Đề cương đã được phê duyệt thành công' 
    };
    
    // Real API:
    // return this.request(`/api/approvals/${syllabusId}/approve`, {
    //   method: 'POST',
    //   body: JSON.stringify({ comment })
    // });
  },

  // Từ chối đề cương
  async rejectSyllabus(syllabusId, reason) {
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return { 
      success: true, 
      message: 'Đề cương đã được yêu cầu chỉnh sửa' 
    };
    
    // Real API:
    // return this.request(`/api/approvals/${syllabusId}/reject`, {
    //   method: 'POST',
    //   body: JSON.stringify({ reason })
    // });
  },

  // Lấy chi tiết đề cương
  async getSyllabusDetail(syllabusId) {
    await new Promise(resolve => setTimeout(resolve, 600));
    
    return {
      id: syllabusId,
      content: '...',
      cloMapping: [],
      ploMapping: [],
      aiSummary: 'AI generated summary...'
    };
    
    // Real API: return this.request(`/api/syllabus/${syllabusId}`);
  },

  // Xuất báo cáo
  async exportReport(type, params = {}) {
    // Real API:
    // return this.request('/api/reports/export', {
    //   method: 'POST',
    //   body: JSON.stringify({ type, params })
    // });
    
    return { success: true, downloadUrl: '#' };
  }
};

export default APIService;