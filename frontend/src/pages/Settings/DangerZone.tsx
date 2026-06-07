import { useState } from 'react';
import { toast } from 'sonner';
import { useNavigate } from 'react-router-dom';
import { Modal } from '@/components/ui/modal';
import apiClient from '@/lib/api';
import { useAuthStore } from '@/store/authStore';

export default function DangerZone() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const navigate = useNavigate();
  const { clearAuth } = useAuthStore();
  const [deleteConfirmation, setDeleteConfirmation] = useState('');
  const [hasAcknowledged, setHasAcknowledged] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const isFormValid = deleteConfirmation === 'DELETE' && hasAcknowledged;

  const handleDeleteAccount = async () => {
    if (!isFormValid) return;

    setIsDeleting(true);

    try {
      await apiClient.delete('/api/account/delete');

      toast.success('Account successfully deleted.');
      setIsModalOpen(false);
      clearAuth();
      navigate('/');
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail?.message || error.response?.data?.detail || 'Failed to submit deletion request. Please try again.';
      toast.error(typeof errorMessage === 'string' ? errorMessage : 'Failed to submit deletion request.');
    } finally {
      setIsDeleting(false);
    }
  };

  const handleOpenModal = () => {
    setIsModalOpen(true);
    setDeleteConfirmation('');
    setHasAcknowledged(false);
  };

  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-4">
          <h2 className="text-lg font-medium text-slate-900">Danger Zone</h2>
          <p className="mt-1 text-sm text-slate-500">
            Destructive actions for your account.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-md border border-slate-200 p-4 bg-slate-50">
          <div>
            <h3 className="text-sm font-medium text-slate-900">Delete Account</h3>
            <p className="mt-1 text-sm text-slate-500">
              Permanently remove your account and associated access to TarkaX. This action cannot be undone.
            </p>
          </div>
          <button
            onClick={handleOpenModal}
            className="inline-flex items-center justify-center rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-red-600 shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:ring-offset-2 whitespace-nowrap"
          >
            Delete Account
          </button>
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={() => !isDeleting && setIsModalOpen(false)}
        title="Delete Your Account?"
      >
        <div className="space-y-6">
          <div className="text-sm text-slate-600 space-y-4">
            <p>
              Are you sure you want to delete your account? This action will permanently remove your account access.
            </p>

            <div className="rounded-md bg-slate-50 p-4 border border-slate-200">
              <h4 className="font-medium text-slate-900 mb-2">What happens next?</h4>
              <ul className="list-disc pl-5 space-y-1">
                <li>Account access removed</li>
                <li>Sessions terminated</li>
                <li>API keys revoked</li>
                <li>Organization membership removed</li>
                <li>Historical records may be anonymized</li>
              </ul>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label htmlFor="confirm-text" className="block text-sm font-medium text-slate-700 mb-1">
                To verify, type <strong>DELETE</strong> below:
              </label>
              <input
                id="confirm-text"
                type="text"
                disabled={isDeleting}
                value={deleteConfirmation}
                onChange={(e) => setDeleteConfirmation(e.target.value)}
                className="block w-full rounded-md border border-slate-300 px-3 py-2 shadow-sm focus:border-slate-900 focus:outline-none focus:ring-1 focus:ring-slate-900 sm:text-sm disabled:opacity-50"
                placeholder="DELETE"
              />
            </div>

            <div className="flex items-start">
              <div className="flex h-5 items-center">
                <input
                  id="acknowledge-checkbox"
                  type="checkbox"
                  disabled={isDeleting}
                  checked={hasAcknowledged}
                  onChange={(e) => setHasAcknowledged(e.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-900"
                />
              </div>
              <div className="ml-3 text-sm">
                <label htmlFor="acknowledge-checkbox" className="font-medium text-slate-700">
                  I understand this action may be permanent.
                </label>
              </div>
            </div>
          </div>

          <div className="mt-6 flex justify-end gap-3 border-t border-slate-200 pt-4">
            <button
              onClick={() => setIsModalOpen(false)}
              disabled={isDeleting}
              className="inline-flex justify-center rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:ring-offset-2 disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              onClick={handleDeleteAccount}
              disabled={!isFormValid || isDeleting}
              className="inline-flex justify-center rounded-md border border-transparent bg-slate-900 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isDeleting ? 'Submitting...' : 'Delete Account'}
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
