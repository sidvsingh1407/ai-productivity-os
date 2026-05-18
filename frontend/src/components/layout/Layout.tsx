import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';

export function Layout() {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <div className="container mx-auto py-8 px-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
