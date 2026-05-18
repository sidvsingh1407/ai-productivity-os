import { useState, useCallback } from 'react';

const ACKNOWLEDGMENT_KEY = 'tarkhax_operational_notice_acknowledged';

export function useOperationalNotice() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [pendingRedirect, setPendingRedirect] = useState<string | null>(null);

  const hasAcknowledgedNotice = useCallback(() => {
    return localStorage.getItem(ACKNOWLEDGMENT_KEY) === 'true';
  }, []);

  const acknowledgeNotice = useCallback(() => {
    localStorage.setItem(ACKNOWLEDGMENT_KEY, 'true');
    setIsModalOpen(false);
  }, []);

  const openModal = useCallback((redirectUrl?: string) => {
    if (redirectUrl) {
      setPendingRedirect(redirectUrl);
    }
    setIsModalOpen(true);
  }, []);

  const closeModal = useCallback(() => {
    setIsModalOpen(false);
    setPendingRedirect(null);
  }, []);

  return {
    isModalOpen,
    pendingRedirect,
    hasAcknowledgedNotice,
    acknowledgeNotice,
    openModal,
    closeModal,
  };
}
