import { useAuthStore } from '@/store/authStore';

export function PrivateRoute({ children }: { children: React.ReactNode }) {
  // Temporary pass-through component
  return <>{children}</>;
}
