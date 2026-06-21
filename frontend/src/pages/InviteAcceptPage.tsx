import { useEffect, useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import apiClient from '@/api/client';
import { useAuthStore } from '@/store/authStore';

export default function InviteAcceptPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [errorMsg, setErrorMsg] = useState('');

  useEffect(() => {
    if (!token) {
      setStatus('error');
      setErrorMsg('No token provided');
      return;
    }

    if (!isAuthenticated) {
      // Must be logged in to accept
      // Store token in session storage and redirect to login
      sessionStorage.setItem('pending_invite_token', token);
      navigate('/login?redirect=/invite');
      return;
    }

    const acceptInvite = async () => {
      try {
        await apiClient.post('/organizations/invitations/accept', { token });
        setStatus('success');
        sessionStorage.removeItem('pending_invite_token');
        setTimeout(() => {
          navigate('/app/dashboard');
        }, 2000);
      } catch (err: any) {
        setStatus('error');
        setErrorMsg(err.response?.data?.detail || 'Failed to accept invitation');
      }
    };

    acceptInvite();
  }, [token, isAuthenticated, navigate]);

  if (status === 'loading') {
    return <div className="flex h-screen items-center justify-center">Accepting invitation...</div>;
  }

  if (status === 'error') {
    return (
      <div className="flex h-screen flex-col items-center justify-center p-4">
        <h1 className="text-2xl font-bold text-red-600 mb-4">Invitation Failed</h1>
        <p className="text-slate-600 mb-6">{errorMsg}</p>
        <Link to="/app/dashboard" className="text-blue-600 hover:underline">Return to Dashboard</Link>
      </div>
    );
  }

  return (
    <div className="flex h-screen flex-col items-center justify-center p-4">
      <h1 className="text-2xl font-bold text-green-600 mb-4">Invitation Accepted!</h1>
      <p className="text-slate-600">You have successfully joined the organization. Redirecting to dashboard...</p>
    </div>
  );
}
