import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: string;
  email: string;
  full_name: string;
}

export interface Org {
  id: string;
  name: string;
}

export interface AuthState {
  user: User | null;
  org: Org | null;
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
      access_token: null,
      refresh_token: null,
      isAuthenticated: false,
      setAuth: (user, org, access_token, refresh_token) =>
        set({ user, org, access_token, refresh_token, isAuthenticated: true }),
      clearAuth: () =>
        set({ user: null, org: null, access_token: null, refresh_token: null, isAuthenticated: false }),
    }),
    {
      name: 'auth-storage',
    }
  )
);
