import { useEffect } from "react";
import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { toast } from 'sonner';

export function AdminRoute() {
  const { isAuthenticated, user } = useAuthStore();

  useEffect(() => {
    if (isAuthenticated && !user?.is_superadmin) {
      toast.error('Access Denied', {
        description: 'You do not have permission to access the admin panel.',
      });
    }
  }, [isAuthenticated, user]);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (!user?.is_superadmin) {
    return <Navigate to="/app/dashboard" replace />;
  }

  return <Outlet />;
}
