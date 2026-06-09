import React from 'react';

const TICKER_ITEMS = [
  "OPERATIONAL CLARITY",
  "BOTTLENECK DETECTION",
  "WORKFLOW VISIBILITY",
  "PROCESS INTELLIGENCE",
  "HIDDEN INEFFICIENCIES",
  "TEAM PRODUCTIVITY",
  "OPERATIONAL SIGNALS",
  "BUSINESS REALITY",
  "ROOT CAUSE ANALYSIS",
  "ADOPTION INSIGHTS",
  "DECISION SUPPORT",
  "PROCESS FRICTION"
];

export function TickerStrip() {
  return (
    <div className="bg-bg-dark border-b border-border-strong py-4 overflow-hidden relative flex items-center">
      <div className="absolute inset-0 pointer-events-none z-10 bg-gradient-to-r from-[#060F1C] via-transparent to-[#060F1C] w-full"></div>

      {/* We duplicate the items a few times to create a seamless loop */}
      <div className="flex animate-ticker whitespace-nowrap">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="flex items-center">
            {TICKER_ITEMS.map((item, index) => (
              <React.Fragment key={`${i}-${index}`}>
                <span className="text-sm font-mono font-medium text-text-inverse/70 mx-8 tracking-wider">
                  {item}
                </span>
                <span className="text-text-inverse/20 text-xs">◆</span>
              </React.Fragment>
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
