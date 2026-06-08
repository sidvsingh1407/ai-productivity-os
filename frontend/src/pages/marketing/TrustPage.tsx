import React from 'react';
import { Shield, Lock, FileCheck, Eye } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function TrustPage() {
  return (
    <div style={{ background: 'var(--tx-bg-card)' }}>
      {/* Hero Section */}
      <section className="text-white py-20" style={{ background: 'var(--tx-bg-dark)' }}>
        <div className="container mx-auto px-4 max-w-4xl text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Trust & Security Center</h1>
          <p className="text-xl text-slate-300 mb-8">
            How we protect your data, ensure objective intelligence, and build verifiable trust.
          </p>
        </div>
      </section>

      {/* Core Principles */}
      <section className="py-20">
        <div className="container mx-auto px-4 max-w-5xl">
          <div className="mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-6">Our Commitment to Enterprise Security</h2>
            <p className="text-lg text-slate-600 mb-6">
              As an organizational intelligence platform, TarkaX handles sensitive operational data. We do not treat data security as an afterthought. Our architecture is designed from the ground up to ensure strict tenant isolation, data privacy, and objective analysis.
            </p>
          </div>

          {/* Key Pillars */}
          <div className="grid md:grid-cols-2 gap-8 mb-20">
            <div className="flex gap-4 p-6 bg-slate-50 rounded-lg border border-slate-100">
              <div className="shrink-0">
                <Shield className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">No LLM Training on Your Data</h3>
                <p className="text-slate-600">
                  Your assessment data is never used to train generalized Large Language Models. We use strict deterministic engines to calculate scores, ensuring your proprietary operational knowledge remains entirely yours.
                </p>
              </div>
            </div>

            <div className="flex gap-4 p-6 bg-slate-50 rounded-lg border border-slate-100">
              <div className="shrink-0">
                <Lock className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Strict Tenant Isolation</h3>
                <p className="text-slate-600">
                  We employ rigorous Row Level Security (RLS) and backend Role-Based Access Control (RBAC). Data from one organization can never cross the boundary to another.
                </p>
              </div>
            </div>

            <div className="flex gap-4 p-6 bg-slate-50 rounded-lg border border-slate-100">
              <div className="shrink-0">
                <Eye className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Explainable Intelligence</h3>
                <p className="text-slate-600">
                  We believe in "glass-box" software. Our platform explicitly tells you why a score was generated, what evidence triggered a risk alert, and how the Confidence Index was calculated.
                </p>
              </div>
            </div>

            <div className="flex gap-4 p-6 bg-slate-50 rounded-lg border border-slate-100">
              <div className="shrink-0">
                <FileCheck className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-900 mb-2">Assessment Limitations</h3>
                <p className="text-slate-600">
                  We are honest about our tool's capabilities. Our diagnostic engines provide powerful directional indicators and decision support, but they are not substitutes for comprehensive legal or compliance audits.
                </p>
              </div>
            </div>
          </div>

          <div className="border-t border-slate-200 pt-16 text-center">
            <h2 className="text-2xl font-bold text-slate-900 mb-6">Have specific security requirements?</h2>
            <Link
              to="/contact?interest=Security"
              className="inline-flex items-center justify-center text-white px-6 py-3 rounded-md font-medium hover:bg-slate-800 transition-colors" style={{ background: 'var(--tx-bg-dark)' }}
            >
              Contact our Security Team
            </Link>
          </div>

        </div>
      </section>
    </div>
  );
}
