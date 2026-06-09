import React from 'react';

const TICKER_ITEMS = [
  "OPERATIONAL CLARITY",
  "BOTTLENECK DETECTION",
  "WORKFLOW VISIBILITY",
  "PROCESS INTELLIGENCE",
  "BUSINESS REALITY",
  "ROOT CAUSE ANALYSIS",
  "TEAM PRODUCTIVITY",
  "OPERATIONAL SIGNALS",
  "PROCESS FRICTION",
  "DECISION SUPPORT"
];

export function TickerStrip() {
  return (
    <div className="bg-bg-dark border-b border-border-strong py-4 overflow-hidden relative flex items-center">
      <div className="absolute inset-0 pointer-events-none z-10 bg-gradient-to-r from-[#060F1C] via-transparent to-[#060F1C] w-full"></div>

      {/* We duplicate the items a few times to create a seamless loop */}
      <div className="flex animate-ticker whitespace-nowrap">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="flex items-center">
            {TICKER_ITEMS.map((item, index) => (
              <React.Fragment key={`${i}-${index}`}>
                <span className="text-sm font-mono font-medium text-text-inverse mx-8 tracking-widest">
                  {item}
                </span>
                <span className="text-accent-blue text-xs font-bold">◆</span>
              </React.Fragment>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
