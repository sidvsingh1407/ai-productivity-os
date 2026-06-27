

interface ReportHeaderProps {
  organizationName: string;
  reportTitle: string;
  date: string;
  version?: string;
}

export function ReportHeader({ organizationName, reportTitle, date, version = '1.0' }: ReportHeaderProps) {
  return (
    <div className="border-b-2 border-border-strong pb-8 mb-12">
      <div className="flex justify-between items-start mb-16">
        <div>
          <div className="text-h2 font-bold tracking-tight text-text-primary">TarkaX</div>
          <div className="text-label text-text-secondary mt-1">AI Governance Platform</div>
        </div>
        <div className="text-right">
          <div className="text-body font-medium text-text-primary">{organizationName}</div>
          <div className="text-data text-text-secondary mt-1">{date}</div>
          <div className="text-data text-text-secondary">Version {version}</div>
        </div>
      </div>

      <div>
        <h1 className="text-display text-text-primary mb-4">{reportTitle}</h1>
      </div>
    </div>
  );
}
