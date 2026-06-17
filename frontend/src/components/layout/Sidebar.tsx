import { Link } from 'react-router-dom';
import { useAuthStore } from '@/store/authStore';
import { LayoutDashboard, Target, GitBranch, Sparkles, FileText, Settings, LogOut, Code2, Shield } from "lucide-react";
import { Button } from '../ui/button';

export function Sidebar() {
  const { clearAuth, user } = useAuthStore();

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
          <Link to="/app/dashboard">
            <Button variant="ghost" className="w-full justify-start gap-2 text-text-secondary hover:text-text-primary">
              <LayoutDashboard className="w-4 h-4" />
              Dashboard
            </Button>
          </Link>
          <Link to="/app/audits/new">
            <Button variant="ghost" className="w-full justify-start gap-2 text-text-secondary hover:text-text-primary">
              <Target className="w-4 h-4" />
              AI Audit
            </Button>
          </Link>
          <Link to="/app/workflows/new">
            <Button variant="ghost" className="w-full justify-start gap-2 text-text-secondary hover:text-text-primary">
              <GitBranch className="w-4 h-4" />
              Workflow Diagnostic
            </Button>
          </Link>
          <Link to="/app/prompt-improver">
            <Button variant="secondary" className="w-full justify-start gap-2">
              <Sparkles className="w-4 h-4 text-accent-blue" />
              Prompt Improver
            </Button>
          </Link>
          <div className="pt-4 pb-2 px-3 text-xs font-semibold text-text-secondary uppercase tracking-wider">
            Organization
          </div>
          <Link to="/app/audits">
            <Button variant="ghost" className="w-full justify-start gap-2 text-text-secondary hover:text-text-primary">
              <FileText className="w-4 h-4" />
              Reports
            </Button>
          </Link>
          {/* Developer Dashboard route kept protected but hidden from sidebar as API Platform is incomplete */}
          {/* <Link to="/app/developers">
            <Button variant="ghost" className="w-full justify-start gap-2 text-text-secondary hover:text-text-primary">
              <Code2 className="w-4 h-4" />
              API Access
            </Button>
          </Link> */}
          <Link to="/app/settings">
            <Button variant="ghost" className="w-full justify-start gap-2 text-text-secondary hover:text-text-primary">
              <Settings className="w-4 h-4" />
              Settings
            </Button>
          </Link>

          {user?.is_superadmin && (
            <>
              <div className="pt-4 pb-2 px-3 text-xs font-semibold text-text-secondary uppercase tracking-wider">
                System
              </div>
              <Link to="/app/admin">
                <Button variant="ghost" className="w-full justify-start gap-2 text-text-secondary hover:text-text-primary">
                  <Shield className="w-4 h-4" />
                  Admin Panel
                </Button>
              </Link>
            </>
          )}
        </nav>
      </div>

      <div className="p-4 border-t">
        {/* Auth is temporarily disabled */}
      </div>
    </aside>
  );
}
