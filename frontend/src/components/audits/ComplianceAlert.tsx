import { AlertTriangle } from "lucide-react";

interface ComplianceAlertProps {
  reasons: string[];
}

export function ComplianceAlert({ reasons }: ComplianceAlertProps) {
  if (!reasons || reasons.length === 0) return null;

  return (
    <div className="rounded-md bg-red-50 p-4 border border-red-200 mb-6">
      <div className="flex">
        <div className="flex-shrink-0">
          <AlertTriangle className="h-5 w-5 text-red-400" aria-hidden="true" />
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-medium text-red-800">Compliance Risk Detected</h3>
          <div className="mt-2 text-sm text-red-700">
            <ul role="list" className="list-disc space-y-1 pl-5">
              {reasons.map((reason, index) => (
                <li key={index}>{reason}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
