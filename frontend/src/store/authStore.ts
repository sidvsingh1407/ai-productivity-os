import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: string;
  email: string;
  full_name?: string;
  name?: string;
  first_name?: string;
  last_name?: string;
  is_superadmin?: boolean;
  is_active?: boolean;
  email_verified?: boolean;
  email_verified_at?: string;
}

export interface Org {
  id: string;
  name: string;
  slug?: string;
}

export interface AuthState {
  user: User | null;
  org: Org | null;
  organization?: Org;
  access_token: string | null;
  refresh_token: string | null;
  isAuthenticated: boolean;
  setAuth: (user: User, org: Org, access_token: string, refresh_token: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      org: null,
      organization: undefined,
      access_token: null,
      refresh_token: null,
      isAuthenticated: false,
      setAuth: (user, org, access_token, refresh_token) =>
        set({ user, org, organization: org, access_token, refresh_token, isAuthenticated: true }),
      clearAuth: () =>
        set({ user: null, org: null, organization: undefined, access_token: null, refresh_token: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
