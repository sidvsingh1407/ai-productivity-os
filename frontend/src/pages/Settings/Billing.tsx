import { toast } from 'sonner';
import { Check } from 'lucide-react';

export default function Billing() {
  const handleUpgradeClick = () => {
    toast.info('Billing configuration coming soon', {
      description: 'We are currently setting up our payment provider. Please check back later.',
    });
  };

  const features = [
    'Up to 5 team members',
    'Basic analytics dashboard',
    'Standard support',
    '10 audits per month',
    'Community access'
  ];

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Billing & Plans</h1>
        <p className="text-sm text-slate-500">Manage your subscription and billing details.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Current Plan */}
        <div className="relative rounded-2xl border border-slate-200 p-8 shadow-sm" style={{ background: 'var(--tx-bg-card)' }}>
          <div className="absolute top-0 right-0 -mt-3 mr-6 rounded-full px-3 py-1 text-xs font-medium text-white shadow-sm" style={{ background: 'var(--tx-bg-dark)' }}>
            Active Plan
          </div>
          <h2 className="text-xl font-bold text-slate-900">Free Plan</h2>
          <p className="mt-2 text-sm text-slate-500">Perfect for exploring the platform and early stage testing.</p>

          <div className="mt-6 flex items-baseline text-4xl font-extrabold text-slate-900">
            $0
            <span className="ml-1 text-xl font-medium text-slate-500">/mo</span>
          </div>

          <ul className="mt-8 space-y-4">
            {features.map((feature, idx) => (
              <li key={idx} className="flex items-start">
                <div className="flex-shrink-0">
                  <Check className="h-5 w-5 text-green-500" />
                </div>
                <p className="ml-3 text-sm text-slate-700">{feature}</p>
              </li>
            ))}
          </ul>
        </div>

        {/* Upgrade Prompt */}
        <div className="flex flex-col justify-center rounded-2xl border border-slate-200 border-dashed bg-slate-50 p-8 text-center">
          <h3 className="text-lg font-medium text-slate-900">Need more features?</h3>
          <p className="mt-2 text-sm text-slate-500">
            Upgrade to our Pro plan for unlimited team members, advanced analytics, priority support, and unlimited audits.
          </p>
          <div className="mt-6">
            <button
              onClick={handleUpgradeClick}
              className="inline-flex items-center justify-center rounded-md px-6 py-3 text-sm font-medium text-white shadow-sm hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-900 focus:ring-offset-2" style={{ background: 'var(--tx-bg-dark)' }}
            >
              Upgrade to Pro
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
