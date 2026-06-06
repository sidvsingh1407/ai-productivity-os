import React from 'react';
import { BookOpen, FileText } from 'lucide-react';

export default function ResearchPage() {
  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="bg-slate-900 text-white py-20">
        <div className="container mx-auto px-4 max-w-4xl text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Research & Frameworks</h1>
          <p className="text-xl text-slate-300 mb-8">
            The intellectual property, theories, and studies driving the TarkaX Intelligence Engine.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="py-20">
        <div className="container mx-auto px-4 max-w-5xl">

          <div className="grid md:grid-cols-2 gap-12">

            {/* Framework 1 */}
            <div className="border border-slate-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow">
              <div className="bg-slate-50 p-8 border-b border-slate-200 flex items-center justify-between">
                <h3 className="text-xl font-bold text-slate-900">The Failure Intelligence Framework</h3>
                <BookOpen className="text-blue-600 w-6 h-6" />
              </div>
              <div className="p-8">
                <p className="text-slate-600 mb-6">
                  An exploration of the 10 most common structural failures in enterprise technology deployments, and how deterministic logic engines can predict them before they cascade into operational reality.
                </p>
                <div className="inline-flex items-center text-sm font-medium text-slate-400 cursor-not-allowed">
                  <FileText className="w-4 h-4 mr-2" />
                  Whitepaper Coming Soon
                </div>
              </div>
            </div>

            {/* Framework 2 */}
            <div className="border border-slate-200 rounded-xl overflow-hidden hover:shadow-lg transition-shadow">
              <div className="bg-slate-50 p-8 border-b border-slate-200 flex items-center justify-between">
                <h3 className="text-xl font-bold text-slate-900">Operational Consistency vs. Innovation Theater</h3>
                <BookOpen className="text-blue-600 w-6 h-6" />
              </div>
              <div className="p-8">
                <p className="text-slate-600 mb-6">
                  Why organizations that index highly on 'Awareness' but poorly on 'Governance' are statistically more likely to experience critical data leaks during AI transformation initiatives.
                </p>
                <div className="inline-flex items-center text-sm font-medium text-slate-400 cursor-not-allowed">
                  <FileText className="w-4 h-4 mr-2" />
                  Report Coming Soon
                </div>
              </div>
            </div>

          </div>

        </div>
      </section>
    </div>
  );
}
