import { useAuthStore } from '@/store/authStore';

export function Topbar() {
  const { user, org } = useAuthStore();

  return (
    <header className="h-16 border-b bg-card flex items-center justify-between px-6">
      <div className="flex items-center gap-2">
        {org && (
          <span className="text-sm font-medium text-muted-foreground border-r pr-4 mr-4">
            {org.name}
          </span>
        )}
        <h1 className="text-xl font-semibold">Dashboard</h1>
      </div>
      <div className="flex items-center gap-4">
        {user && (
          <div className="flex items-center gap-3">
            <span className="text-sm font-medium">
              {user.full_name || user.name || "User"}
            </span>
            <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-semibold text-sm">
              {(user.full_name || user.name || "U").charAt(0).toUpperCase()}
            </div>
          </div>
        )}
      </div>
    </header>
  );
}
