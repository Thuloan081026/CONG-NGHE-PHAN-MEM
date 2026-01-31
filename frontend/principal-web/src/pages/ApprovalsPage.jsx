import React, { useState } from 'react';
import ApprovalList from '../components/approvals/ApprovalList';
import ApprovalModal from '../components/approvals/ApprovalModal';
import SyllabusDetailPanel from '../components/approvals/SyllabusDetailPanel';
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
  const [showDetailPanel, setShowDetailPanel] = useState(false);

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

  const handleRequestRevision = async (syllabusId, reason) => {
    try {
      const result = await APIService.requestRevision(syllabusId, reason);
      if (result.success) {
        alert(result.message);
        setShowModal(false);
        setSelectedSyllabus(null);
        if (onRefresh) onRefresh();
      }
    } catch (error) {
      alert('Có lỗi xảy ra khi yêu cầu chỉnh sửa');
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

  const handleViewDetail = (syllabus) => {
    setSelectedSyllabus(syllabus);
    setShowDetailPanel(true);
  };

  const handleCloseDetail = () => {
    setShowDetailPanel(false);
    setSelectedSyllabus(null);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Approval List - Left/Full */}
      <div className="lg:col-span-2">
        <ApprovalList 
          syllabi={pendingApprovals} 
          onReview={handleReview}
          onViewDetail={handleViewDetail}
        />
      </div>

      {/* Detail Panel - Right side */}
      {showDetailPanel && selectedSyllabus && (
        <div className="lg:col-span-1">
          <SyllabusDetailPanel 
            syllabusId={selectedSyllabus.id}
            onClose={handleCloseDetail}
          />
        </div>
      )}

      {showModal && selectedSyllabus && (
        <ApprovalModal
          syllabus={selectedSyllabus}
          onApprove={handleApprove}
          onRequestRevision={handleRequestRevision}
          onReject={handleReject}
          onClose={handleClose}
        />
      )}
    </div>
  );
};

export default ApprovalsPage;