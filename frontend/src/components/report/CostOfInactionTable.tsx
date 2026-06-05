import React from 'react';

interface COIItem {
  risk_category: string;
  risk_level: string;
  potential_consequence: string;
  business_impact: string;
  related_recommendation: string;
}

interface CostOfInactionTableProps {
  coiData: COIItem[];
}

export function CostOfInactionTable({ coiData }: CostOfInactionTableProps) {
  if (!coiData || coiData.length === 0) return null;

  return (
    <div className="mb-12">
      <h2 className="text-h2 font-semibold text-text-primary mb-6 border-b border-border-light pb-4">Cost of Inaction</h2>
      <p className="text-body text-text-secondary mb-6 max-w-3xl">
        A boardroom-level projection of business impact if the current operational trajectory remains unchanged.
      </p>

      <div className="border border-border-strong overflow-hidden bg-bg-primary">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-bg-secondary border-b border-border-strong">
              <th className="py-4 px-6 text-label text-text-secondary uppercase tracking-wider font-medium w-1/4">Risk Area</th>
              <th className="py-4 px-6 text-label text-text-secondary uppercase tracking-wider font-medium w-1/3">Consequence</th>
              <th className="py-4 px-6 text-label text-text-secondary uppercase tracking-wider font-medium w-5/12">Business Impact</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border-light">
            {coiData.map((item, idx) => (
              <tr key={idx} className="hover:bg-bg-secondary/50 transition-colors">
                <td className="py-4 px-6">
                  <div className="flex flex-col gap-1">
                    <span className="text-body font-semibold text-text-primary">{item.risk_category}</span>
                    <span className={`text-sm ${item.risk_level === 'Critical' || item.risk_level === 'High' ? 'text-accent-red' : 'text-text-secondary'}`}>
                      {item.risk_level} Exposure
                    </span>
                  </div>
                </td>
                <td className="py-4 px-6">
                  <span className="text-body text-text-primary">{item.potential_consequence}</span>
                </td>
                <td className="py-4 px-6">
                  <span className="text-body font-medium text-text-primary">{item.business_impact}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
