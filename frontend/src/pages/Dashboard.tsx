import { useNavigate } from 'react-router-dom';
import { useOperationalNotice } from '@/hooks/useOperationalNotice';
import { OperationalNoticeModal } from '@/components/modals/OperationalNoticeModal';
import { Button } from '@/components/ui/button';

export default function Dashboard() {
  const navigate = useNavigate();
  const {
    isModalOpen,
    pendingRedirect,
    hasAcknowledgedNotice,
    acknowledgeNotice,
    openModal,
    closeModal,
  } = useOperationalNotice();

  const handleCTA = (redirectPath: string) => {
    if (hasAcknowledgedNotice()) {
      navigate(redirectPath);
    } else {
      openModal(redirectPath);
    }
  };

  const handleModalContinue = () => {
    acknowledgeNotice();
    if (pendingRedirect) {
      navigate(pendingRedirect);
    }
  };

  return (
    <div>
      <h1 className="mb-4 text-3xl font-bold tracking-tight">Dashboard</h1>
      <p className="text-muted-foreground mb-8">Welcome to AI Productivity OS.</p>

      <div className="flex flex-col gap-4 sm:flex-row">
        {/* Temporary placeholders for actual CTA buttons */}
        <Button onClick={() => handleCTA('/audits/new')} className="w-full sm:w-auto">
          Run AI Audit
        </Button>
        <Button onClick={() => handleCTA('/workflows/new')} variant="outline" className="w-full sm:w-auto">
          Explore Workflow Diagnosis
        </Button>
      </div>

      <OperationalNoticeModal
        isOpen={isModalOpen}
        onContinue={handleModalContinue}
        onClose={closeModal}
      />
    </div>
  );
}
