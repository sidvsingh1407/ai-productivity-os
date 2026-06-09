import { Link } from 'react-router-dom';
import { ArrowRight, CheckCircle2, Target } from 'lucide-react';
import { SeoHead } from '../../components/geo/SeoHead';
import { FAQSection, generateFAQSchema } from '../../components/geo/FAQSection';
import ConstellationMap from '../../components/ConstellationMap';
import { TickerStrip } from '../../components/TickerStrip';
import { KeyFindings } from '../../components/KeyFindings';

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
      <section className="border-b border-border-strong bg-bg-primary overflow-hidden w-full">
        <div className="w-full flex flex-col md:flex-row min-h-[auto] md:min-h-[70vh] xl:min-h-[80vh]">

          {/* Left Content */}
          <div className="w-full md:w-[55vw] xl:w-[50vw] flex items-center justify-center px-6 py-20 md:py-16">
            <div className="flex flex-col items-start text-left w-full max-w-[650px]">
              <h1 className="text-display text-text-primary mb-6 leading-tight">
                Find What's Really Holding Your Business Back
              </h1>
              <div className="text-h3 font-normal text-text-secondary mb-10 space-y-4">
                <p>Most businesses don't know what's actually slowing them down.</p>
                <p className="text-body mt-4 text-text-secondary/80">TarkaX helps uncover bottlenecks, workflow friction, adoption gaps, and hidden inefficiencies before you spend time or money fixing the wrong thing.</p>
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
          </div>

          {/* Right Visual: Constellation */}
          <div className="w-full md:w-[45vw] xl:w-[50vw] relative bg-[#0B1F3A] flex-shrink-0 h-[420px] md:h-auto">
            {/* Header inside the absolute map container */}
            <div className="absolute top-6 left-6 z-10 pointer-events-none">
              <h3 className="text-sm font-semibold text-text-inverse mb-1">Operational Intelligence Map</h3>
              <p className="text-xs text-text-inverse/70 max-w-[250px]">Visualizing hidden bottlenecks, workflow friction, adoption gaps, and operational risks.</p>
            </div>

            <div className="absolute inset-0 overflow-hidden bg-[#0B1F3A]">
              <ConstellationMap variant="hero" height="100%" />
            </div>
          </div>

        </div>
      </section>

      {/* 2. Ticker Strip */}
      <TickerStrip />

      {/* 3. Key Findings Businesses Miss */}
      <KeyFindings />

      {/* 4. Reality Gap Section */}
      <section className="py-24 bg-bg-secondary border-b border-border-strong">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <h2 className="text-h2 text-text-primary mb-16">
            Everyone Sees a Different Version of the Business
          </h2>

          <div className="space-y-4 max-w-2xl mx-auto">
            {/* The Hierarchy Flow */}
            <div className="bg-bg-primary border border-border-strong p-6 rounded-lg shadow-sm transform transition-all hover:scale-[1.02]">
              <div className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Executives See</div>
              <div className="text-h3 text-text-primary">Reports</div>
            </div>

            <div className="flex justify-center"><ArrowRight className="w-6 h-6 text-text-secondary rotate-90" /></div>

            <div className="bg-bg-primary border border-border-strong p-6 rounded-lg shadow-sm transform transition-all hover:scale-[1.02]">
              <div className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Managers See</div>
              <div className="text-h3 text-text-primary">Metrics</div>
            </div>

            <div className="flex justify-center"><ArrowRight className="w-6 h-6 text-text-secondary rotate-90" /></div>

            <div className="bg-bg-primary border border-border-strong p-6 rounded-lg shadow-sm transform transition-all hover:scale-[1.02]">
              <div className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-2">Employees See</div>
              <div className="text-h3 text-text-primary">Workarounds</div>
            </div>

            <div className="flex justify-center"><ArrowRight className="w-6 h-6 text-text-secondary rotate-90" /></div>

            <div className="bg-bg-primary border border-accent-red/30 bg-accent-red/5 p-6 rounded-lg shadow-sm transform transition-all hover:scale-[1.02]">
              <div className="text-sm font-semibold text-accent-red uppercase tracking-wider mb-2">Customers Experience</div>
              <div className="text-h3 text-text-primary">Delays</div>
            </div>
          </div>

          <div className="mt-16 p-8 bg-[#0B1F3A] border border-accent-blue/30 rounded-xl shadow-lg transform transition-all hover:scale-[1.02] max-w-2xl mx-auto relative overflow-hidden">
             <div className="absolute inset-0 opacity-20 pointer-events-none mix-blend-screen">
                <ConstellationMap variant="hero" height={200} />
             </div>
             <div className="relative z-10 flex flex-col items-center justify-center">
               <div className="w-12 h-12 bg-accent-blue rounded-full flex items-center justify-center mb-4 shadow-[0_0_15px_rgba(37,99,235,0.5)]">
                  <Target className="w-6 h-6 text-white" />
               </div>
               <div className="text-sm font-semibold text-accent-blue uppercase tracking-wider mb-2">TarkaX Reveals</div>
               <div className="text-h3 text-white">The Underlying Reality</div>
             </div>
          </div>
        </div>
      </section>

      {/* 5. How TarkaX Works (Journey) */}
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

      {/* 7. Example Findings */}
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
