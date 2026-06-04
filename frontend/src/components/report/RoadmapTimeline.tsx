interface RoadmapAction {
  action: string;
  reason: string;
  priority: string;
}

interface RoadmapTimelineProps {
  roadmap: {
    day_30: RoadmapAction[];
    day_60: RoadmapAction[];
    day_90: RoadmapAction[];
  };
}

export function RoadmapTimeline({ roadmap }: RoadmapTimelineProps) {
  if (!roadmap) {
    return null;
  }

  const renderTimelineSection = (title: string, actions: RoadmapAction[]) => (
    <div className="relative pl-8 md:pl-0">
      {/* Mobile timeline line */}
      <div className="absolute left-[11px] top-2 bottom-0 w-px bg-border-light md:hidden"></div>

      <div className="md:grid md:grid-cols-[120px_1fr] md:gap-8 relative">
        <div className="mb-4 md:mb-0">
          <h3 className="text-h3 font-medium text-text-primary bg-bg-primary relative z-10 inline-block pr-4 md:pr-0">
            {/* Mobile timeline dot */}
            <span className="absolute left-[-29px] top-1.5 w-3 h-3 rounded-full border-2 border-text-primary bg-bg-primary md:hidden"></span>
            {title}
          </h3>
        </div>

        <div className="flex flex-col gap-4 pb-12 md:border-l md:border-border-light md:pl-8 relative">
          {/* Desktop timeline dot */}
          <span className="hidden md:block absolute left-[-6px] top-1.5 w-3 h-3 rounded-full border-2 border-text-primary bg-bg-primary"></span>

          {actions.map((actionItem, idx) => (
            <div key={idx} className="border border-border-strong bg-bg-primary p-5 hover:border-text-primary/30 transition-colors">
              <div className="flex items-start justify-between gap-4 mb-2">
                <h4 className="text-body font-medium text-text-primary">{actionItem.action}</h4>
                <span className="text-xs uppercase tracking-wider text-text-secondary font-medium shrink-0">
                  {actionItem.priority}
                </span>
              </div>
              <p className="text-sm text-text-secondary">{actionItem.reason}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="mb-12">
      <h2 className="text-h2 font-semibold text-text-primary mb-8 border-b border-border-light pb-4">30/60/90 Day Implementation Roadmap</h2>

      <div className="flex flex-col">
        {renderTimelineSection('30 Days', roadmap.day_30 || [])}
        {renderTimelineSection('60 Days', roadmap.day_60 || [])}
        {renderTimelineSection('90 Days', roadmap.day_90 || [])}
      </div>
    </div>
  );
}
