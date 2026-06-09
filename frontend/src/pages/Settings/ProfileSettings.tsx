import React, { useState } from 'react';
import { useAuthStore } from '../../store/authStore';
import { authApi } from '@/api/auth';

export default function ProfileSettings() {
  const { user } = useAuthStore();
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setStatus('error');
      setErrorMessage('New passwords do not match.');
      return;
    }
    if (newPassword.length < 8) {
      setStatus('error');
      setErrorMessage('New password must be at least 8 characters long.');
      return;
    }

    setStatus('loading');
    setErrorMessage('');

    try {
      await authApi.changePassword({
        current_password: currentPassword,
        new_password: newPassword
      });
      setStatus('success');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => setStatus('idle'), 3000);
    } catch (error: any) {
      setStatus('error');
      setErrorMessage(error.response?.data?.detail || error.message || 'Failed to change password.');
    }
  };

  return (
    <div className="bg-white shadow sm:rounded-lg mb-8" style={{ background: 'var(--tx-bg-card)', borderColor: 'var(--tx-border)' }}>
      <div className="px-4 py-5 sm:p-6">
        <h3 className="text-lg leading-6 font-medium text-gray-900" style={{ color: 'var(--tx-text-primary)' }}>
          Profile Settings
        </h3>

        <div className="mt-5 border-t pt-5">
          <dl className="divide-y divide-gray-200">
            <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt className="text-sm font-medium text-gray-500" style={{ color: 'var(--tx-text-secondary)' }}>Full name</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2" style={{ color: 'var(--tx-text-primary)' }}>{user?.full_name}</dd>
            </div>
            <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4">
              <dt className="text-sm font-medium text-gray-500" style={{ color: 'var(--tx-text-secondary)' }}>Email address</dt>
              <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2" style={{ color: 'var(--tx-text-primary)' }}>
                {user?.email}
                {user?.email_verified === false && (
                  <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                    Unverified
                  </span>
                )}
                {user?.email_verified && (
                  <span className="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Verified
                  </span>
                )}
              </dd>
            </div>
          </dl>
        </div>

        <div className="mt-8 border-t pt-8">
          <h4 className="text-md leading-6 font-medium text-gray-900 mb-4" style={{ color: 'var(--tx-text-primary)' }}>
            Change Password
          </h4>

          <form onSubmit={handleChangePassword} className="space-y-4 max-w-md">
            {status === 'success' && (
              <div className="rounded-md bg-green-50 p-4 mb-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-green-800">Password changed successfully</h3>
                  </div>
                </div>
              </div>
            )}

            {status === 'error' && (
              <div className="rounded-md bg-red-50 p-4 mb-4">
                <div className="flex">
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">{errorMessage}</h3>
                  </div>
                </div>
              </div>
            )}

            <div>
              <label htmlFor="current-password" className="block text-sm font-medium text-gray-700" style={{ color: 'var(--tx-text-secondary)' }}>Current Password</label>
              <input
                type="password"
                name="current-password"
                id="current-password"
                required
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className="mt-1 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
              />
            </div>

            <div>
              <label htmlFor="new-password" className="block text-sm font-medium text-gray-700" style={{ color: 'var(--tx-text-secondary)' }}>New Password</label>
              <input
                type="password"
                name="new-password"
                id="new-password"
                required
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="mt-1 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
              />
            </div>

            <div>
              <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-700" style={{ color: 'var(--tx-text-secondary)' }}>Confirm New Password</label>
              <input
                type="password"
                name="confirm-password"
                id="confirm-password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="mt-1 shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
              />
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={status === 'loading'}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                style={{ background: 'var(--tx-button-primary)', color: 'var(--tx-button-primary-text)' }}
              >
                {status === 'loading' ? 'Saving...' : 'Update Password'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
