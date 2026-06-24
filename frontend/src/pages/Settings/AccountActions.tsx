import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import { useAuthStore } from '@/store/authStore';
import { authApi } from '@/api/auth';

export default function AccountActions() {
  const navigate = useNavigate();
  const { clearAuth } = useAuthStore();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);

    try {
      await authApi.logout();
      toast.success('Logged out successfully.');
    } catch (error) {
      console.error('Logout API call failed:', error);
      // We do not block logout on failure. User should still be logged out locally.
    } finally {
      clearAuth();
      setIsLoggingOut(false);
      navigate('/login');
    }
  };

  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <div className="mb-4">
          <h2 className="text-lg font-medium text-slate-900">Account Actions</h2>
          <p className="mt-1 text-sm text-slate-500">
            Routine actions for managing your session.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 rounded-md border border-slate-200 p-4 bg-slate-50">
          <div>
            <h3 className="text-sm font-medium text-slate-900">Log Out</h3>
            <p className="mt-1 text-sm text-slate-500">
              End your current session and securely log out of your account.
            </p>
          </div>
          <button
            onClick={handleLogout}
            disabled={isLoggingOut}
            className="inline-flex items-center justify-center rounded-md border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:ring-offset-2 whitespace-nowrap disabled:opacity-50"
          >
            {isLoggingOut ? 'Logging out...' : 'Log Out'}
          </button>
        </div>
      </div>
    </div>
  );
}
