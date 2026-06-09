import React from 'react';
import { AlertTriangle, Clock, Target, Zap } from 'lucide-react';

export function KeyFindings() {
  return (
    <section className="py-24 bg-bg-primary border-b border-border-strong relative">
      <div className="max-w-7xl mx-auto px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-h2 text-text-primary mb-4">Key Findings Businesses Miss</h2>
          <p className="text-body text-text-secondary">Most problems are symptoms. These are the signals behind them.</p>
        </div>

        <div className="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex items-center justify-between p-6 border border-border-light rounded-lg bg-bg-secondary hover:border-accent-blue/50 transition-colors">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-accent-amber/10 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5 text-accent-amber" />
              </div>
              <span className="text-lg font-medium text-text-secondary">AI Adoption Gaps</span>
            </div>
            <span className="text-2xl text-text-primary font-bold">42%</span>
          </div>

          <div className="flex items-center justify-between p-6 border border-border-light rounded-lg bg-bg-secondary hover:border-accent-blue/50 transition-colors">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-accent-red/10 flex items-center justify-center">
                <Clock className="w-5 h-5 text-accent-red" />
              </div>
              <span className="text-lg font-medium text-text-secondary">Workflow Bottlenecks</span>
            </div>
            <span className="text-2xl text-text-primary font-bold">4</span>
          </div>

          <div className="flex items-center justify-between p-6 border border-border-light rounded-lg bg-bg-secondary hover:border-accent-blue/50 transition-colors">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-text-secondary/10 flex items-center justify-center">
                <Target className="w-5 h-5 text-text-secondary" />
              </div>
              <span className="text-lg font-medium text-text-secondary">Manual Tasks Identified</span>
            </div>
            <span className="text-2xl text-text-primary font-bold">17</span>
          </div>

          <div className="flex items-center justify-between p-6 border border-accent-blue/30 rounded-lg bg-accent-blue/5 hover:border-accent-blue transition-colors">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 rounded-full bg-accent-blue/20 flex items-center justify-center">
                <Zap className="w-5 h-5 text-accent-blue" />
              </div>
              <span className="text-lg font-medium text-accent-blue">Recommended Priority</span>
            </div>
            <span className="text-xl text-accent-blue font-bold text-right">Workflow<br className="sm:hidden" /> Handoff</span>
          </div>
        </div>
      </div>
    </section>
  );
}
