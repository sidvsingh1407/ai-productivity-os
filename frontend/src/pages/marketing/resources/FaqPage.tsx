import { Link } from 'react-router-dom';
import { SeoHead } from '../../../components/geo/SeoHead';
import { FAQSection } from '../../../components/geo/FAQSection';

export default function FaqPage() {
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
    },
    {
      question: "What exactly is Failure Intelligence?",
      answer: "It's the methodology of looking for structural reasons why things break or slow down, rather than blaming individual performance. We map the underlying systems to find the recurring failure patterns."
    }
  ];

  return (
    <div className="bg-bg-primary min-h-screen pt-24 pb-32">
      <SeoHead title="FAQ | TarkaX" description="Frequently asked questions about TarkaX diagnostic tools and methodology." />
      <FAQSection title="Frequently Asked Questions" faqItems={faqItems} />

      <div className="max-w-3xl mx-auto px-6 text-center mt-16">
        <p className="text-body text-text-secondary mb-4">Still have questions?</p>
        <Link to="/contact" className="px-6 py-3 bg-bg-secondary border border-border-strong rounded-md hover:bg-bg-tertiary transition-colors text-text-primary font-medium">
          Contact our team
        </Link>
      </div>
    </div>
  );
}
