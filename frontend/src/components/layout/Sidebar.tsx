import { Link, useLocation } from 'react-router-dom';
import { Home, FileSearch, History, PlaySquare } from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { name: 'Dashboard', path: '/', icon: Home },
  { name: 'Run Audit', path: '/audits/new', icon: FileSearch },
  { name: 'Audit History', path: '/audits', icon: History },
  { name: 'Run Workflow', path: '/workflows/new', icon: PlaySquare },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <div className="flex h-screen w-64 flex-col bg-white border-r">
      <div className="flex h-16 items-center border-b px-6">
        <h1 className="text-lg font-bold text-slate-800">AI Productivity OS</h1>
      </div>
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
          return (
            <Link
              key={item.name}
              to={item.path}
              className={cn(
                'flex items-center rounded-md px-3 py-2 text-sm font-medium',
                isActive
                  ? 'bg-slate-100 text-slate-900'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              )}
            >
              <Icon className={cn('mr-3 h-5 w-5', isActive ? 'text-slate-900' : 'text-slate-400')} />
              {item.name}
            </Link>
          );
        })}
      </nav>
    </div>
  );
}
