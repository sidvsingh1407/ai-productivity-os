import React from 'react';
import { NavLink } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import {
  LayoutDashboard,
  BarChart2,
  Users,
  Building,
  Settings,
  CreditCard,
  LogOut,
} from 'lucide-react';
import { cn } from '@/lib/utils';

export function Sidebar() {
  const { user, clearAuth } = useAuthStore();

  const handleLogout = () => {
    clearAuth();
    window.location.href = '/login';
  };

  return (
    <div className="flex h-screen w-64 flex-col border-r bg-white">
      <div className="flex h-14 items-center border-b px-4">
        <span className="text-lg font-bold text-slate-800">AI Productivity OS</span>
      </div>

      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-2">
          <NavLink
            to="/dashboard"
            className={({ isActive }) =>
              cn(
                'group flex items-center rounded-md px-2 py-2 text-sm font-medium',
                isActive
                  ? 'bg-slate-100 text-slate-900'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              )
            }
          >
            <LayoutDashboard className="mr-3 h-5 w-5 flex-shrink-0" />
            Dashboard
          </NavLink>

          <NavLink
            to="/analytics"
            className={({ isActive }) =>
              cn(
                'group flex items-center rounded-md px-2 py-2 text-sm font-medium',
                isActive
                  ? 'bg-slate-100 text-slate-900'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              )
            }
          >
            <BarChart2 className="mr-3 h-5 w-5 flex-shrink-0" />
            Analytics
          </NavLink>
        </nav>

        {user?.is_superadmin && (
          <div className="mt-8">
            <h3 className="px-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
              Admin
            </h3>
            <nav className="mt-2 space-y-1 px-2">
              <NavLink
                to="/admin/users"
                className={({ isActive }) =>
                  cn(
                    'group flex items-center rounded-md px-2 py-2 text-sm font-medium',
                    isActive
                      ? 'bg-slate-100 text-slate-900'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  )
                }
              >
                <Users className="mr-3 h-5 w-5 flex-shrink-0" />
                Users
              </NavLink>
              <NavLink
                to="/admin/orgs"
                className={({ isActive }) =>
                  cn(
                    'group flex items-center rounded-md px-2 py-2 text-sm font-medium',
                    isActive
                      ? 'bg-slate-100 text-slate-900'
                      : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                  )
                }
              >
                <Building className="mr-3 h-5 w-5 flex-shrink-0" />
                Organizations
              </NavLink>
            </nav>
          </div>
        )}

        <div className="mt-8">
          <h3 className="px-3 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Settings
          </h3>
          <nav className="mt-2 space-y-1 px-2">
            <NavLink
              to="/settings/org"
              className={({ isActive }) =>
                cn(
                  'group flex items-center rounded-md px-2 py-2 text-sm font-medium',
                  isActive
                    ? 'bg-slate-100 text-slate-900'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                )
              }
            >
              <Settings className="mr-3 h-5 w-5 flex-shrink-0" />
              Organization
            </NavLink>
            <NavLink
              to="/settings/billing"
              className={({ isActive }) =>
                cn(
                  'group flex items-center rounded-md px-2 py-2 text-sm font-medium',
                  isActive
                    ? 'bg-slate-100 text-slate-900'
                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                )
              }
            >
              <CreditCard className="mr-3 h-5 w-5 flex-shrink-0" />
              Billing
            </NavLink>
          </nav>
        </div>
      </div>

      <div className="border-t p-4">
        <button
          onClick={handleLogout}
          className="group flex w-full items-center rounded-md px-2 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50 hover:text-slate-900"
        >
          <LogOut className="mr-3 h-5 w-5 flex-shrink-0 text-slate-400 group-hover:text-slate-500" />
          Logout
        </button>
      </div>
    </div>
  );
}
