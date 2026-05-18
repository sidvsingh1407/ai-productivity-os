
import { Link } from 'react-router-dom';
import { LayoutDashboard, Activity, Settings, BarChart2 } from 'lucide-react';

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-muted flex">
      {/* Sidebar Navigation */}
      <aside className="w-64 bg-background border-r border-gray-200 flex flex-col">
        <div className="p-6">
          <Link to="/" className="text-xl font-medium tracking-tight text-foreground">
            TarkhaX <span className="text-accent-gold">OS</span>
          </Link>
        </div>
        <nav className="flex-1 px-4 space-y-2">
          <Link to="/dashboard" className="flex items-center gap-3 px-3 py-2 bg-gray-100 text-foreground rounded-md font-medium">
            <LayoutDashboard className="w-4 h-4 text-accent-gold" />
            Overview
          </Link>
          <Link to="/audits/new" className="flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-md font-medium transition-colors">
            <BarChart2 className="w-4 h-4" />
            Audits
          </Link>
          <Link to="/workflows/new" className="flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-md font-medium transition-colors">
            <Activity className="w-4 h-4" />
            Workflows
          </Link>
        </nav>
        <div className="p-4 border-t border-gray-200">
          <button className="flex items-center gap-3 px-3 py-2 text-gray-600 hover:bg-gray-50 rounded-md font-medium transition-colors w-full text-left">
            <Settings className="w-4 h-4" />
            Settings
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-light tracking-tight text-foreground">Operational Overview</h1>
            <p className="text-gray-500 mt-1">Executive intelligence and system metrics.</p>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Metric Cards */}
          <div className="bg-background p-6 border border-gray-200 rounded-xl">
            <p className="text-sm text-gray-500 font-medium">System Maturity</p>
            <p className="text-3xl font-light mt-2 text-foreground">84<span className="text-lg text-gray-400">/100</span></p>
            <div className="mt-4 flex items-center gap-2 text-sm text-accent-emerald">
              <span className="w-2 h-2 rounded-full bg-accent-emerald"></span>
              Optimized
            </div>
          </div>
          <div className="bg-background p-6 border border-gray-200 rounded-xl">
            <p className="text-sm text-gray-500 font-medium">Active Workflows</p>
            <p className="text-3xl font-light mt-2 text-foreground">12</p>
            <div className="mt-4 flex items-center gap-2 text-sm text-accent-teal">
              <span className="w-2 h-2 rounded-full bg-accent-teal"></span>
              Healthy
            </div>
          </div>
          <div className="bg-background p-6 border border-gray-200 rounded-xl">
            <p className="text-sm text-gray-500 font-medium">Compliance Risks</p>
            <p className="text-3xl font-light mt-2 text-foreground">2</p>
            <div className="mt-4 flex items-center gap-2 text-sm text-accent-red">
              <span className="w-2 h-2 rounded-full bg-accent-red"></span>
              Attention Required
            </div>
          </div>
        </div>

        <div className="bg-background p-8 border border-gray-200 rounded-xl min-h-[400px] flex items-center justify-center">
            <p className="text-gray-400 font-light">Detailed analytics and reports will appear here.</p>
        </div>
      </main>
    </div>
  );
}