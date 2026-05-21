
import { useState } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Activity, ShieldCheck, Database, BarChart3, Fingerprint, Lock } from 'lucide-react';
import { DisclaimerModal } from '@/components/DisclaimerModal';
import { useAppStore } from '@/store/appStore';
import { useNavigate } from 'react-router-dom';

export default function LandingPage() {
  const [isDisclaimerOpen, setIsDisclaimerOpen] = useState(false);
  const [targetAction, setTargetAction] = useState<string | null>(null);
  const { disclaimerAcknowledged } = useAppStore();
  const navigate = useNavigate();

  const handleActionClick = (path: string) => {
    if (disclaimerAcknowledged) {
      navigate(path);
    } else {
      setTargetAction(path);
      setIsDisclaimerOpen(true);
    }
  };

  return (
    <div className="min-h-screen bg-background font-sans selection:bg-accent-gold/20">

      {/* 1. Hero Section (Dark Cinematic) */}
      <section className="relative w-full bg-dark min-h-[90vh] flex items-center justify-center overflow-hidden">
        {/* Background Atmosphere */}
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-noise opacity-30 mix-blend-overlay"></div>
          <div className="absolute top-1/4 left-1/4 w-[500px] h-[500px] bg-accent-teal/10 rounded-full blur-[120px] mix-blend-screen"></div>
          <div className="absolute bottom-1/4 right-1/4 w-[600px] h-[600px] bg-accent-gold/5 rounded-full blur-[150px] mix-blend-screen"></div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-8 flex flex-col items-center text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 backdrop-blur-sm mb-8"
          >
            <span className="w-2 h-2 rounded-full bg-accent-gold animate-pulse"></span>
            <span className="text-sm font-medium text-white/80 tracking-wide uppercase">TarkhaX Intelligence System</span>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.1, ease: "easeOut" }}
            className="text-5xl md:text-7xl font-light text-white tracking-tight leading-[1.1] max-w-4xl"
          >
            Strategic Systems Optimization & <span className="text-white/60">Workflow Observability</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            className="mt-8 text-lg md:text-xl text-dark-zinc-400 font-light max-w-2xl leading-relaxed"
          >
            Executive-grade analytical intelligence. Diagnose process friction, assess automation maturity, and govern AI integration securely.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3, ease: "easeOut" }}
            className="mt-12 flex flex-col sm:flex-row items-center gap-4"
          >
            <button
              onClick={() => handleActionClick('/audits/new')}
              className="px-8 py-4 bg-accent-gold text-dark font-medium rounded-lg hover:bg-accent-gold/90 transition-all flex items-center gap-2 shadow-[0_0_30px_rgba(212,183,106,0.15)] group w-full sm:w-auto justify-center"
            >
              Run AI Audit
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
            <button
              onClick={() => handleActionClick('/workflows/new')}
              className="px-8 py-4 bg-white/5 text-white font-medium rounded-lg hover:bg-white/10 border border-white/10 transition-all backdrop-blur-sm w-full sm:w-auto justify-center"
            >
              Explore Workflow Diagnosis
            </button>
          </motion.div>
        </div>

        {/* Subtle bottom fade to transition to light section */}
        <div className="absolute bottom-0 left-0 w-full h-32 bg-gradient-to-t from-background to-transparent z-10"></div>
      </section>

      {/* 2. Product Positioning (Light Editorial) */}
      <section className="py-24 bg-background relative z-20">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="max-w-3xl">
            <h2 className="text-4xl font-light text-foreground tracking-tight leading-tight">
              Operational intelligence requires clarity, not complexity.
            </h2>
            <div className="w-20 h-[1px] bg-accent-gold mt-8 mb-8"></div>
            <p className="text-xl text-gray-500 font-light leading-relaxed">
              TarkhaX unifies process analysis with AI maturity scoring to deliver actionable, executive-ready insights. We replace fragmented tooling with a singular, cinematic observability layer.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mt-24">
            <div>
              <div className="w-12 h-12 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center mb-6">
                <BarChart3 className="w-6 h-6 text-foreground" />
              </div>
              <h3 className="text-xl font-medium text-foreground mb-3 tracking-tight">Audit Engine</h3>
              <p className="text-gray-500 font-light leading-relaxed">Comprehensive maturity scoring across awareness, adoption, integration, governance, and ROI.</p>
            </div>
            <div>
              <div className="w-12 h-12 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center mb-6">
                <Activity className="w-6 h-6 text-foreground" />
              </div>
              <h3 className="text-xl font-medium text-foreground mb-3 tracking-tight">Workflow Diagnosis</h3>
              <p className="text-gray-500 font-light leading-relaxed">Identify friction points and generate exact automation blueprints for immediate operational impact.</p>
            </div>
            <div>
              <div className="w-12 h-12 rounded-lg bg-gray-50 border border-gray-100 flex items-center justify-center mb-6">
                <Database className="w-6 h-6 text-foreground" />
              </div>
              <h3 className="text-xl font-medium text-foreground mb-3 tracking-tight">Integration Intelligence</h3>
              <p className="text-gray-500 font-light leading-relaxed">Map the correlation between audit metrics and actionable workflow states securely.</p>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Optimization Audit Engine */}
      <section className="py-24 bg-muted border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-sm font-medium text-accent-gold tracking-widest uppercase mb-4">Module 01</h2>
              <h3 className="text-4xl font-light text-foreground tracking-tight mb-6">Optimization Audit Engine</h3>
              <p className="text-lg text-gray-500 font-light leading-relaxed mb-8">
                Establish a quantitative baseline for AI integration. Our engine evaluates your operational readiness across five key dimensions, generating executive reports instantly.
              </p>
              <ul className="space-y-4">
                {[
                  'Dimensional Maturity Scoring',
                  'Compliance Risk Flagging',
                  'Executive Report Generation',
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-gray-600 font-light">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent-gold"></div>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            {/* Visual representation placeholder for Radar Chart */}
            <div className="bg-white p-8 rounded-2xl border border-gray-100 shadow-sm relative overflow-hidden h-[400px] flex items-center justify-center">
              <div className="absolute inset-0 bg-noise opacity-10"></div>
              <div className="text-center relative z-10">
                <div className="w-48 h-48 rounded-full border border-gray-200 mx-auto flex items-center justify-center relative">
                  <div className="w-32 h-32 rounded-full border border-gray-100 absolute"></div>
                  <div className="w-16 h-16 rounded-full border border-gray-50 absolute"></div>
                  <div className="absolute w-full h-[1px] bg-gray-100"></div>
                  <div className="absolute h-full w-[1px] bg-gray-100"></div>
                  <svg className="w-full h-full absolute inset-0 text-accent-teal/20 fill-current" viewBox="0 0 100 100">
                    <polygon points="50,10 85,35 75,80 25,80 15,35" />
                  </svg>
                  <svg className="w-full h-full absolute inset-0 text-accent-gold/40 fill-transparent stroke-current stroke-2" viewBox="0 0 100 100">
                    <polygon points="50,20 75,40 65,75 35,75 25,40" />
                  </svg>
                </div>
                <p className="mt-6 text-sm font-medium text-gray-400 tracking-widest uppercase">Maturity Radar</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Workflow Diagnosis Engine */}
      <section className="py-24 bg-background">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center flex-row-reverse lg:flex-row">
            <div className="order-2 lg:order-1">
               {/* Visual representation placeholder for Process Mapping */}
               <div className="bg-muted p-8 rounded-2xl border border-gray-100 shadow-sm h-[400px] flex flex-col items-center justify-center gap-6 relative">
                 <div className="w-full max-w-sm bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
                    <span className="text-sm font-medium text-foreground">Data Ingestion</span>
                    <span className="text-xs text-gray-400">Step 1</span>
                 </div>
                 <div className="w-[1px] h-8 bg-gray-300"></div>
                 <div className="w-full max-w-sm bg-white p-4 rounded-xl border border-accent-gold/30 shadow-sm flex items-center justify-between relative overflow-hidden">
                    <div className="absolute left-0 top-0 bottom-0 w-1 bg-accent-gold"></div>
                    <span className="text-sm font-medium text-foreground">AI Analysis Node</span>
                    <span className="text-xs text-accent-gold font-medium">Optimization Found</span>
                 </div>
                 <div className="w-[1px] h-8 bg-gray-300"></div>
                 <div className="w-full max-w-sm bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
                    <span className="text-sm font-medium text-foreground">Report Generation</span>
                    <span className="text-xs text-accent-emerald font-medium">Automated</span>
                 </div>
               </div>
            </div>
            <div className="order-1 lg:order-2">
              <h2 className="text-sm font-medium text-accent-teal tracking-widest uppercase mb-4">Module 02</h2>
              <h3 className="text-4xl font-light text-foreground tracking-tight mb-6">Workflow Diagnosis</h3>
              <p className="text-lg text-gray-500 font-light leading-relaxed mb-8">
                Map operational processes with high-fidelity observability. Discover friction, assess time cost, and deploy structured automation blueprints.
              </p>
              <ul className="space-y-4">
                {[
                  'Visual Process Orchestration',
                  'Friction Identification',
                  'Actionable Blueprint Cards',
                ].map((item, i) => (
                  <li key={i} className="flex items-center gap-3 text-gray-600 font-light">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent-teal"></div>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* 5 & 6. Intelligence Layer & Dashboard Preview (Dark Intelligence) */}
      <section className="py-32 bg-dark relative border-t border-white/5 overflow-hidden">
        <div className="absolute inset-0 bg-noise opacity-20 mix-blend-overlay"></div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-20">
            <h2 className="text-4xl font-light text-white tracking-tight mb-6">
              Integration Intelligence
            </h2>
            <p className="text-xl text-dark-zinc-400 font-light leading-relaxed">
              The dashboard unifies audit scores with workflow recommendations, delivering a secure, executive command center.
            </p>
          </div>

          {/* Premium Dashboard Preview */}
          <div className="w-full bg-dark-surface rounded-2xl border border-white/10 shadow-2xl overflow-hidden backdrop-blur-md">
            {/* Window Controls Header */}
            <div className="h-12 border-b border-white/10 bg-white/5 flex items-center px-6 gap-2">
              <div className="w-3 h-3 rounded-full bg-white/20"></div>
              <div className="w-3 h-3 rounded-full bg-white/20"></div>
              <div className="w-3 h-3 rounded-full bg-white/20"></div>
              <div className="ml-4 px-3 py-1 rounded bg-white/5 text-[10px] text-white/40 tracking-widest uppercase font-medium">
                TarkhaX Overview
              </div>
            </div>

            <div className="p-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left Column */}
              <div className="col-span-1 space-y-6">
                <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
                  <p className="text-sm text-dark-zinc-400 mb-1">Overall System Score</p>
                  <p className="text-5xl font-light text-white">84</p>
                  <div className="mt-4 h-1 w-full bg-white/10 rounded-full overflow-hidden">
                    <div className="h-full bg-accent-gold w-[84%]"></div>
                  </div>
                </div>
                <div className="p-6 rounded-xl bg-white/[0.02] border border-white/5">
                  <div className="flex items-center justify-between mb-4">
                    <p className="text-sm text-dark-zinc-400">Risk Assessment</p>
                    <ShieldCheck className="w-4 h-4 text-accent-emerald" />
                  </div>
                  <p className="text-lg text-white font-light">Governance Compliant</p>
                  <p className="text-sm text-dark-zinc-500 mt-2">All controls validated across 12 active workflows.</p>
                </div>
              </div>

              {/* Right Column - Mock Chart */}
              <div className="col-span-1 lg:col-span-2 p-6 rounded-xl bg-white/[0.02] border border-white/5 flex flex-col">
                <p className="text-sm text-dark-zinc-400 mb-6">Maturity Over Time</p>
                <div className="flex-1 flex items-end gap-2 h-48">
                  {[40, 45, 55, 50, 65, 75, 84].map((val, i) => (
                    <div key={i} className="flex-1 bg-white/5 rounded-t-sm relative group">
                      <div
                        className="absolute bottom-0 w-full bg-gradient-to-t from-accent-teal/20 to-accent-teal/60 rounded-t-sm transition-all duration-500 group-hover:to-accent-gold/60"
                        style={{ height: `${val}%` }}
                      ></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Compliance & Governance (Mixed Contrast) */}
      <section className="py-24 bg-background">
        <div className="max-w-4xl mx-auto px-6 lg:px-8 text-center">
          <div className="w-16 h-16 mx-auto bg-accent-red/10 rounded-full flex items-center justify-center mb-8">
            <Lock className="w-8 h-8 text-accent-red" />
          </div>
          <h2 className="text-3xl font-light text-foreground tracking-tight mb-6">
            Governance-First Architecture
          </h2>
          <p className="text-lg text-gray-500 font-light leading-relaxed mb-12 max-w-2xl mx-auto">
            Operational intelligence must be paired with strict control. TarkhaX highlights compliance risks natively, ensuring optimization recommendations align with internal security policies.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-8">
            <div className="flex items-center gap-3">
               <Fingerprint className="w-5 h-5 text-gray-400" />
               <span className="text-sm text-gray-600 font-medium">Stateless Execution</span>
            </div>
            <div className="flex items-center gap-3">
               <ShieldCheck className="w-5 h-5 text-gray-400" />
               <span className="text-sm text-gray-600 font-medium">Risk Flagging</span>
            </div>
          </div>
        </div>
      </section>

      {/* 8. CTA/Footer */}
      <footer className="bg-background border-t border-gray-100 py-16">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 flex flex-col items-center">
          <h2 className="text-2xl font-medium text-foreground tracking-tight mb-8">Ready to optimize your systems?</h2>
          <button
              onClick={() => handleActionClick('/dashboard')}
              className="px-8 py-3 bg-foreground text-background font-medium rounded-lg hover:bg-foreground/90 transition-all mb-16"
            >
              Access Intelligence Dashboard
          </button>

          <div className="w-full border-t border-gray-100 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-lg font-medium tracking-tight text-foreground">
                TarkhaX
              </span>
              <span className="text-sm text-gray-400">© 2024 Intelligence Systems</span>
            </div>
            <div className="flex items-center gap-6 text-sm text-gray-500">
              <button className="hover:text-foreground transition-colors">Documentation</button>
              <button className="hover:text-foreground transition-colors">Privacy</button>
              <button className="hover:text-foreground transition-colors">Terms</button>
            </div>
          </div>
        </div>
      </footer>

      {/* Disclaimer Modal */}
      <DisclaimerModal
        isOpen={isDisclaimerOpen}
        onClose={() => setIsDisclaimerOpen(false)}
        targetPath={targetAction}
      />
    </div>
  );
}