import React, { useState } from 'react';
import ApprovalList from '../components/approvals/ApprovalList';
import ApprovalModal from '../components/approvals/ApprovalModal';
import APIService from '../services/api.service';

/**
 * ApprovalsPage Component
 * Trang phê duyệt đề cương
 * 
 * @param {array} pendingApprovals - Danh sách đề cương chờ duyệt
 * @param {function} onRefresh - Callback để refresh data
 */
const ApprovalsPage = ({ pendingApprovals, onRefresh }) => {
  const [selectedSyllabus, setSelectedSyllabus] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleReview = (syllabus) => {
    setSelectedSyllabus(syllabus);
    setShowModal(true);
  };

  const handleApprove = async (syllabusId, comment) => {
    try {
      const result = await APIService.approveSyllabus(syllabusId, comment);
      if (result.success) {
        alert(result.message);
        setShowModal(false);
        setSelectedSyllabus(null);
        if (onRefresh) onRefresh();
      }
    } catch (error) {
      alert('Có lỗi xảy ra khi phê duyệt');
      console.error(error);
    }
  };

  const handleReject = async (syllabusId, reason) => {
    try {
      const result = await APIService.rejectSyllabus(syllabusId, reason);
      if (result.success) {
        alert(result.message);
        setShowModal(false);
        setSelectedSyllabus(null);
        if (onRefresh) onRefresh();
      }
    } catch (error) {
      alert('Có lỗi xảy ra khi từ chối');
      console.error(error);
    }
  };

  const handleClose = () => {
    setShowModal(false);
    setSelectedSyllabus(null);
  };

  return (
    <div>
      <ApprovalList 
        syllabi={pendingApprovals} 
        onReview={handleReview}
      />

      {showModal && selectedSyllabus && (
        <ApprovalModal
          syllabus={selectedSyllabus}
          onApprove={handleApprove}
          onReject={handleReject}
          onClose={handleClose}
        />
      )}
    </div>
  );
};

export default ApprovalsPage;