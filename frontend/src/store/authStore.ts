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
      user: {
        id: "00000000-0000-0000-0000-000000000001",
        email: "development@tarkax.com",
        full_name: "Development Mode",
        is_superadmin: true,
        is_active: true,
        email_verified: true,
      },
      org: {
        id: "00000000-0000-0000-0000-000000000002",
        name: "Development Organization",
        slug: "development-organization",
      },
      organization: {
        id: "00000000-0000-0000-0000-000000000002",
        name: "Development Organization",
        slug: "development-organization",
      },
      access_token: "temp_access_token",
      refresh_token: "temp_refresh_token",
      isAuthenticated: true,
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
