import React from 'react';
import { SeoHead } from '../../components/geo/SeoHead';

export default function SubprocessorsPage() {
  const subprocessors = [
    {
      name: 'Supabase',
      purpose: 'Database and related backend services',
      status: 'Verified',
    },
    {
      name: 'Render',
      purpose: 'Backend application hosting',
      status: 'Verified',
    },
    {
      name: 'Vercel',
      purpose: 'Frontend hosting and deployment',
      status: 'Verified',
    },
    {
      name: 'Resend',
      purpose: 'Transactional email delivery',
      status: 'Verified',
    },
    {
      name: 'Google Gemini',
      purpose: 'AI-powered generation or analysis',
      status: 'Verified',
    }
  ];

  return (
    <div className="bg-bg-primary min-h-screen animate-fade-up">
      <SeoHead
        title="Subprocessors | TarkaX"
        description="List of subprocessors used by the TarkaX platform."
        canonical="https://tarkax.com/subprocessors"
      />
      <div className="max-w-4xl mx-auto py-24 px-6">
        <h1 className="text-h1 font-semibold mb-8 border-b border-border-light pb-4">Subprocessors</h1>

        <div className="prose text-body text-text-secondary mb-8">
          <p>
            The following table lists the current documented service providers and subprocessors used to operate the TarkaX platform.
            Note that inclusion in this list does not necessarily mean the provider processes personal data or is an active subprocessor in all contexts.
          </p>
        </div>

        <div className="overflow-x-auto bg-bg-secondary rounded-lg border border-border-light shadow-sm">
          <table className="min-w-full divide-y divide-border-light text-left">
            <thead className="bg-bg-primary">
              <tr>
                <th scope="col" className="px-6 py-4 text-sm font-semibold text-text-primary uppercase tracking-wider">Provider Name</th>
                <th scope="col" className="px-6 py-4 text-sm font-semibold text-text-primary uppercase tracking-wider">Documented Purpose</th>
                <th scope="col" className="px-6 py-4 text-sm font-semibold text-text-primary uppercase tracking-wider">Status</th>
              </tr>
            </thead>
            <tbody className="bg-bg-primary divide-y divide-border-light">
              {subprocessors.map((provider) => (
                <tr key={provider.name} className="hover:bg-bg-secondary transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-text-primary">
                    {provider.name}
                  </td>
                  <td className="px-6 py-4 text-sm text-text-secondary">
                    {provider.purpose}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-text-secondary">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 border border-green-200">
                      {provider.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
