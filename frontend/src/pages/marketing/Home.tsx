import { Link } from 'react-router-dom';
import { ArrowRight, AlertTriangle, CheckCircle2, Clock, Zap, Target } from 'lucide-react';
import { SeoHead } from '../../components/geo/SeoHead';
import { FAQSection, generateFAQSchema } from '../../components/geo/FAQSection';
import ConstellationMap from '../../components/ConstellationMap';

export default function Home() {
  const faqItems = [
    {
      question: "How is TarkaX different from an AI consulting firm?",
      answer: "We focus on uncovering hidden operational realities through structured diagnostic analysis, not selling you expensive transformation projects or unneeded tools. We provide the truth about where your business is slowing down so you can make informed decisions."
    },
    {
      question: "Does TarkaX help with automation?",
      answer: "We help you determine *what* to automate. By revealing manual handoffs, repetitive tasks, and workflow bottlenecks, we ensure your automation investments target the actual root causes of operational friction."
    },
    {
      question: "How long does a diagnostic take?",
      answer: "Our assessments are designed to be fast and self-serve. You can establish a baseline for your team or organization's friction points in days, not the months typical of traditional discovery processes."
    },
    {
      question: "Who typically uses TarkaX?",
      answer: "Founders, COOs, Operations Leaders, and executives who suspect their business is moving slower than it should and want empirical evidence of the bottlenecks before investing in new headcount or software."
    }
  ];

  const organizationSchema = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "TarkaX",
    "url": "https://tarkax.com",
    "logo": "https://tarkax.com/logo.png",
    "contactPoint": {
      "@type": "ContactPoint",
      "contactType": "Customer Service",
      "url": "https://tarkax.com/contact"
    }
  };

  const websiteSchema = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "TarkaX",
    "url": "https://tarkax.com"
  };

  const faqSchema = generateFAQSchema(faqItems);

  return (
    <div className="bg-bg-primary">
      <SeoHead
        title="TarkaX | Business Clarity for the AI Era"
        description="The fastest way to discover what's really holding your business back. TarkaX reveals hidden bottlenecks, manual work, and wasted AI investments."
        canonical="https://tarkax.com/"
        schema={[organizationSchema, websiteSchema, faqSchema]}
      />

      {/* 1. Hero Section */}
      <section className="border-b border-border-strong bg-bg-primary overflow-hidden">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-20 lg:py-32">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

            {/* Left Content */}
            <div className="flex flex-col items-start text-left">
              <h1 className="text-display text-text-primary mb-6 leading-tight">
                Find What's Really Holding Your Business Back
              </h1>
              <div className="text-h3 font-normal text-text-secondary mb-10 space-y-4">
                <p>Most businesses don't have an AI problem.</p>
                <p>They have a visibility problem.</p>
                <p className="text-body mt-4 text-text-secondary/80">TarkaX reveals where time, money, operational effort, and AI investments are being wasted so you know exactly what to fix next.</p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
                <Link
                  to="/register"
                  className="px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium transition-colors hover:bg-accent-blue/90 inline-flex items-center justify-center rounded-md shadow-sm"
                >
                  Start Free Analysis
                </Link>
                <Link
                  to="/example-findings"
                  className="px-8 py-4 bg-bg-secondary text-text-primary border border-border-strong text-body font-medium transition-colors hover:bg-bg-tertiary inline-flex items-center justify-center rounded-md shadow-sm"
                >
                  See Example Findings
                </Link>
              </div>
            </div>

            {/* Right Visual: Business Reality Dashboard with Constellation Background */}
            <div className="relative h-[480px] rounded-xl overflow-hidden border border-border-strong shadow-lg bg-bg-dark">
              {/* Background Map */}
              <div className="absolute inset-0 z-0 opacity-60">
                <ConstellationMap variant="hero" height={480} />
              </div>

              {/* Foreground Dashboard Overlay */}
              <div className="absolute inset-0 z-10 flex items-end justify-center p-6 bg-gradient-to-t from-bg-dark via-transparent to-transparent">
                <div className="w-full bg-bg-primary border border-border-strong rounded-xl p-6 shadow-xl relative mt-32">
                  <div className="flex items-center justify-between mb-4 border-b border-border-light pb-4">
                    <h3 className="font-semibold text-text-primary">Business Reality Dashboard</h3>
                    <span className="text-xs font-mono text-accent-blue px-2 py-1 bg-accent-blue/10 rounded">LIVE SCAN</span>
                  </div>

                <div className="space-y-6">
                  {/* Metric Row 1 */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-4 bg-bg-secondary rounded-lg border border-border-light">
                      <div className="text-xs text-text-secondary mb-1">AI Adoption Gaps</div>
                      <div className="text-2xl font-bold text-text-primary">42%</div>
                      <div className="text-xs text-accent-amber mt-1 flex items-center gap-1"><AlertTriangle className="w-3 h-3"/> High Risk</div>
                    </div>
                    <div className="p-4 bg-bg-secondary rounded-lg border border-border-light">
                      <div className="text-xs text-text-secondary mb-1">Workflow Bottlenecks</div>
                      <div className="text-2xl font-bold text-text-primary">4</div>
                      <div className="text-xs text-accent-red mt-1 flex items-center gap-1"><AlertTriangle className="w-3 h-3"/> Critical</div>
                    </div>
                  </div>

                  {/* List Items */}
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 border border-border-light rounded bg-bg-primary">
                      <div className="flex items-center gap-3">
                        <Clock className="w-4 h-4 text-text-secondary" />
                        <span className="text-sm font-medium">Process Delays</span>
                      </div>
                      <span className="text-sm text-accent-red font-medium">Elevated</span>
                    </div>
                    <div className="flex items-center justify-between p-3 border border-border-light rounded bg-bg-primary">
                      <div className="flex items-center gap-3">
                        <AlertTriangle className="w-4 h-4 text-text-secondary" />
                        <span className="text-sm font-medium">Manual Tasks Identified</span>
                      </div>
                      <span className="text-sm text-text-primary font-medium">17</span>
                    </div>
                    <div className="flex items-center justify-between p-3 border border-border-light rounded bg-bg-primary">
                      <div className="flex items-center gap-3">
                        <Zap className="w-4 h-4 text-text-secondary" />
                        <span className="text-sm font-medium">Recommended Priority</span>
                      </div>
                      <span className="text-sm text-accent-blue font-medium">Workflow Handoff</span>
                    </div>
                  </div>
                </div>
              </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* 2. Reality Gap Section */}
      <section className="py-24 bg-bg-secondary border-b border-border-strong">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <h2 className="text-h2 text-text-primary mb-16">
            Everyone Sees a Different Version of the Business
          </h2>

          <div className="space-y-4 max-w-2xl mx-auto">
            {/* The Hierarchy Flow */}
            <div className="bg-bg-primary border border-border-strong p-6 rounded-lg shadow-sm transform transition-all hover:scale-[1.02]">
              <div className="text-sm font-semibold text-accent-blue uppercase tracking-wider mb-2">Executives See</div>
              <div className="text-h3 text-text-primary">"Green Dashboards"</div>
            </div>

            <div className="flex justify-center"><ArrowRight className="w-6 h-6 text-text-secondary rotate-90" /></div>

            <div className="bg-bg-primary border border-border-strong p-6 rounded-lg shadow-sm transform transition-all hover:scale-[1.02]">
              <div className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Managers See</div>
              <div className="text-h3 text-text-primary">"Delayed Reports"</div>
            </div>

            <div className="flex justify-center"><ArrowRight className="w-6 h-6 text-text-secondary rotate-90" /></div>

            <div className="bg-bg-primary border border-border-strong p-6 rounded-lg shadow-sm transform transition-all hover:scale-[1.02]">
              <div className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Employees See</div>
              <div className="text-h3 text-text-primary">"Manual Workarounds"</div>
            </div>

            <div className="flex justify-center"><ArrowRight className="w-6 h-6 text-text-secondary rotate-90" /></div>

            <div className="bg-bg-primary border border-accent-red/30 bg-accent-red/5 p-6 rounded-lg shadow-sm transform transition-all hover:scale-[1.02]">
              <div className="text-sm font-semibold text-accent-red uppercase tracking-wider mb-2">Customers See</div>
              <div className="text-h3 text-text-primary">"Slow Delivery"</div>
            </div>
          </div>

          <div className="mt-16 text-xl font-medium text-text-primary">
            Nobody sees the full picture. <span className="text-accent-blue">TarkaX connects the dots.</span>
          </div>
        </div>
      </section>

      {/* 3. What We Help You Discover (Problem Cards) */}
      <section className="py-24 bg-bg-primary border-b border-border-strong">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-h2 text-text-primary mb-4">Discover What's Broken</h2>
            <p className="text-body text-text-secondary max-w-2xl mx-auto">We look past the symptoms to find the hidden causes dragging down your operational efficiency.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Card 1 */}
            <Link to="/problems/ai-roi" className="group block bg-bg-secondary border border-border-strong p-6 rounded-lg hover:border-accent-blue transition-colors">
              <h3 className="text-lg font-bold text-text-primary mb-4 group-hover:text-accent-blue transition-colors">AI Investments Not Delivering ROI</h3>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Unused licenses</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Low adoption rates</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Workflow disconnects</li>
              </ul>
            </Link>

            {/* Card 2 */}
            <Link to="/solutions/discover-bottlenecks" className="group block bg-bg-secondary border border-border-strong p-6 rounded-lg hover:border-accent-blue transition-colors">
              <h3 className="text-lg font-bold text-text-primary mb-4 group-hover:text-accent-blue transition-colors">Hidden Operational Bottlenecks</h3>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Approval delays</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Manual handoffs</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Process friction</li>
              </ul>
            </Link>

            {/* Card 3 */}
            <Link to="/problems/inconsistent-ai" className="group block bg-bg-secondary border border-border-strong p-6 rounded-lg hover:border-accent-blue transition-colors">
              <h3 className="text-lg font-bold text-text-primary mb-4 group-hover:text-accent-blue transition-colors">Inconsistent AI Outputs</h3>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Off-brand responses</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Poor prompt structures</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Unpredictable results</li>
              </ul>
            </Link>

            {/* Card 4 */}
            <Link to="/solutions/reduce-manual-work" className="group block bg-bg-secondary border border-border-strong p-6 rounded-lg hover:border-accent-blue transition-colors">
              <h3 className="text-lg font-bold text-text-primary mb-4 group-hover:text-accent-blue transition-colors">Manual Work Holding You Back</h3>
              <ul className="space-y-2 text-sm text-text-secondary">
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Repetitive tasks</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Duplicate data entry</li>
                <li className="flex items-center gap-2"><CheckCircle2 className="w-4 h-4 text-border-strong" /> Spreadsheet dependency</li>
              </ul>
            </Link>
          </div>
        </div>
      </section>

      {/* 4. How TarkaX Works (Journey) */}
      <section className="py-24 bg-bg-dark text-text-inverse border-b border-border-strong">
        <div className="max-w-5xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-h2 text-text-inverse mb-4">How We Find the Truth</h2>
            <p className="text-body text-text-inverse/70">A structured process to move from symptom to solution.</p>
          </div>

          <div className="relative border-l border-text-inverse/20 ml-6 md:ml-0 md:border-none">
            <div className="md:grid md:grid-cols-5 md:gap-4 md:items-start text-center hidden mb-4">
              <div className="col-span-1"><div className="w-8 h-8 rounded-full bg-accent-blue text-text-inverse flex items-center justify-center mx-auto mb-2 font-bold">1</div><div className="text-sm font-semibold">Identify Symptom</div></div>
              <div className="col-span-1"><div className="w-8 h-8 rounded-full bg-accent-blue text-text-inverse flex items-center justify-center mx-auto mb-2 font-bold">2</div><div className="text-sm font-semibold">Run Analysis</div></div>
              <div className="col-span-1"><div className="w-8 h-8 rounded-full bg-accent-blue text-text-inverse flex items-center justify-center mx-auto mb-2 font-bold">3</div><div className="text-sm font-semibold">Reveal Causes</div></div>
              <div className="col-span-1"><div className="w-8 h-8 rounded-full bg-accent-blue text-text-inverse flex items-center justify-center mx-auto mb-2 font-bold">4</div><div className="text-sm font-semibold">Prioritize Actions</div></div>
              <div className="col-span-1"><div className="w-8 h-8 rounded-full bg-accent-blue text-text-inverse flex items-center justify-center mx-auto mb-2 font-bold">5</div><div className="text-sm font-semibold">Implement</div></div>
            </div>

            <div className="md:grid md:grid-cols-5 md:gap-4 hidden text-sm text-text-inverse/70 text-center">
               <div className="col-span-1 p-2 bg-text-inverse/5 rounded border border-text-inverse/10">e.g., "Team is slow"</div>
               <div className="col-span-1 p-2 bg-text-inverse/5 rounded border border-text-inverse/10">Deploy diagnostic survey</div>
               <div className="col-span-1 p-2 bg-text-inverse/5 rounded border border-text-inverse/10">Find workflow bottlenecks</div>
               <div className="col-span-1 p-2 bg-text-inverse/5 rounded border border-text-inverse/10">Rank by cost/impact</div>
               <div className="col-span-1 p-2 bg-text-inverse/5 rounded border border-text-inverse/10">Fix structural issues</div>
            </div>

            {/* Mobile View */}
            <div className="md:hidden space-y-8 pl-8 relative">
              {[
                { step: 1, title: 'Identify the symptom.', desc: 'Examples: AI isn\'t working, Team is slow, Operations are chaotic.' },
                { step: 2, title: 'Run analysis.', desc: 'Deploy targeted diagnostic instruments across your team.' },
                { step: 3, title: 'Reveal root causes.', desc: 'Uncover the hidden structural reality behind the symptom.' },
                { step: 4, title: 'Receive prioritized recommendations.', desc: 'Get actionable findings based on business impact.' },
                { step: 5, title: 'Implement improvements.', desc: 'Fix what is actually broken, instead of guessing.' },
              ].map((item) => (
                <div key={item.step} className="relative">
                  <div className="absolute -left-[44px] w-8 h-8 rounded-full bg-accent-blue text-text-inverse flex items-center justify-center font-bold">{item.step}</div>
                  <h4 className="text-lg font-semibold text-text-inverse mb-1">{item.title}</h4>
                  <p className="text-sm text-text-inverse/70">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* 5. Example Findings */}
      <section className="py-24 bg-bg-primary border-b border-border-strong">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-h2 text-text-primary mb-4">Stop Guessing. Start Knowing.</h2>
            <p className="text-body text-text-secondary">We sell clarity and evidence, not tools.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="border border-border-strong bg-bg-secondary p-8 rounded-lg">
              <div className="text-xs font-mono text-accent-red mb-4">FINDING 01</div>
              <h3 className="text-xl font-bold text-text-primary mb-2">73% of AI licenses unused.</h3>
              <p className="text-sm text-text-secondary mb-6 border-b border-border-light pb-6">Licenses were purchased for 100 employees, but only 27 use them weekly.</p>
              <div className="space-y-4">
                <div>
                  <div className="text-xs text-text-secondary uppercase">Impact</div>
                  <div className="font-medium text-text-primary">$18,000 annual waste.</div>
                </div>
                <div>
                  <div className="text-xs text-text-secondary uppercase">Recommendation</div>
                  <div className="font-medium text-text-primary">Focus onboarding on 3 high-impact workflows instead of general rollout.</div>
                </div>
              </div>
            </div>

            <div className="border border-border-strong bg-bg-secondary p-8 rounded-lg">
              <div className="text-xs font-mono text-accent-red mb-4">FINDING 02</div>
              <h3 className="text-xl font-bold text-text-primary mb-2">14 hour delay in approval loop.</h3>
              <p className="text-sm text-text-secondary mb-6 border-b border-border-light pb-6">Client onboarding is bottlenecked because of a manual PDF handoff.</p>
              <div className="space-y-4">
                <div>
                  <div className="text-xs text-text-secondary uppercase">Impact</div>
                  <div className="font-medium text-text-primary">Reduced client satisfaction, slow revenue recognition.</div>
                </div>
                <div>
                  <div className="text-xs text-text-secondary uppercase">Recommendation</div>
                  <div className="font-medium text-text-primary">Automate PDF data extraction and route directly to compliance system.</div>
                </div>
              </div>
            </div>

            <div className="border border-border-strong bg-bg-secondary p-8 rounded-lg">
              <div className="text-xs font-mono text-accent-red mb-4">FINDING 03</div>
              <h3 className="text-xl font-bold text-text-primary mb-2">Inconsistent Prompt Quality.</h3>
              <p className="text-sm text-text-secondary mb-6 border-b border-border-light pb-6">Support team is generating answers using varied, unstandardized prompts.</p>
              <div className="space-y-4">
                <div>
                  <div className="text-xs text-text-secondary uppercase">Impact</div>
                  <div className="font-medium text-text-primary">Off-brand responses, compliance risk, and rework.</div>
                </div>
                <div>
                  <div className="text-xs text-text-secondary uppercase">Recommendation</div>
                  <div className="font-medium text-text-primary">Implement global prompt templates and operational guidelines.</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 6. Product Lenses (Investigations) */}
      <section className="py-24 bg-bg-secondary border-b border-border-strong">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="mb-16">
            <h2 className="text-h2 text-text-primary mb-4">Investigate Your Business</h2>
            <p className="text-body text-text-secondary">Choose an area to analyze.</p>
          </div>

          <div className="space-y-6">
            <Link to="/problems/ai-roi" className="flex flex-col md:flex-row md:items-center justify-between p-8 bg-bg-primary border border-border-strong rounded-lg hover:border-accent-blue transition-all group">
              <div>
                <h3 className="text-2xl font-bold text-text-primary mb-2 group-hover:text-accent-blue transition-colors">Why Isn't AI Working?</h3>
                <p className="text-text-secondary">Discover where your AI investments are breaking down across awareness, adoption, and governance.</p>
              </div>
              <div className="mt-6 md:mt-0 flex items-center gap-2 text-accent-blue font-medium">
                Start Investigation <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

            <Link to="/problems/team-productivity" className="flex flex-col md:flex-row md:items-center justify-between p-8 bg-bg-primary border border-border-strong rounded-lg hover:border-accent-blue transition-all group">
              <div>
                <h3 className="text-2xl font-bold text-text-primary mb-2 group-hover:text-accent-blue transition-colors">What's Slowing Your Team Down?</h3>
                <p className="text-text-secondary">Identify the hidden bottlenecks, tool bloat, and manual tasks dragging down productivity.</p>
              </div>
              <div className="mt-6 md:mt-0 flex items-center gap-2 text-accent-blue font-medium">
                Start Investigation <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>

            <Link to="/problems/inconsistent-ai" className="flex flex-col md:flex-row md:items-center justify-between p-8 bg-bg-primary border border-border-strong rounded-lg hover:border-accent-blue transition-all group">
              <div>
                <h3 className="text-2xl font-bold text-text-primary mb-2 group-hover:text-accent-blue transition-colors">Why Are AI Outputs Inconsistent?</h3>
                <p className="text-text-secondary">Diagnose and standardize the prompt structures being used by your team.</p>
              </div>
              <div className="mt-6 md:mt-0 flex items-center gap-2 text-accent-blue font-medium">
                Start Investigation <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </div>
            </Link>
          </div>
        </div>
      </section>

      {/* 8. FAQ Section */}
      <FAQSection
        title="Frequently Asked Questions"
        faqItems={faqItems}
      />

      {/* 9. Final CTA */}
      <section className="py-32 bg-bg-primary text-center">
        <div className="max-w-3xl mx-auto px-6 lg:px-8">
          <h2 className="text-display text-text-primary mb-6">
            Stop Guessing. Start Knowing.
          </h2>
          <p className="text-h3 font-normal text-text-secondary mb-12">
            Discover what's actually slowing growth before you spend more money on tools, consultants, or hiring.
          </p>
          <Link
            to="/register"
            className="inline-flex items-center justify-center px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium transition-colors hover:bg-accent-blue/90 rounded-md shadow-sm gap-2"
          >
            Start Free Analysis
          </Link>
        </div>
      </section>
    </div>
  );
}
