import { Link } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { LayoutDashboard, LogOut } from 'lucide-react';
import { Button } from '../ui/button';

export function Sidebar() {
  const { clearAuth } = useAuthStore();

  return (
    <aside className="w-64 border-r bg-card flex flex-col justify-between">
      <div className="p-4">
        <div className="flex items-center gap-2 mb-8 px-2">
          <div className="w-8 h-8 bg-primary rounded-md flex items-center justify-center">
            <LayoutDashboard className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="font-bold text-lg">AI Productivity OS</span>
        </div>

        <nav className="space-y-1">
          <Link to="/dashboard">
            <Button variant="secondary" className="w-full justify-start gap-2">
              <LayoutDashboard className="w-4 h-4" />
              Dashboard
            </Button>
          </Link>
          {/* Add more links here later */}
        </nav>
      </div>

      <div className="p-4 border-t">
        <Button variant="ghost" className="w-full justify-start gap-2 text-muted-foreground hover:text-foreground" onClick={clearAuth}>
          <LogOut className="w-4 h-4" />
          Log out
        </Button>
      </div>
    </aside>
  );
}
