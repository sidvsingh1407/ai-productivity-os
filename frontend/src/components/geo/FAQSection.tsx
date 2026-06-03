import React from 'react';

export interface FAQItem {
  question: string;
  answer: string;
}

interface FAQSectionProps {
  faqItems: FAQItem[];
  title?: string;
  description?: string;
}

export function FAQSection({ faqItems, title = "Frequently Asked Questions", description }: FAQSectionProps) {
  return (
    <section className="py-[80px] bg-bg-primary border-t border-border-light">
      <div className="max-w-4xl mx-auto px-6 lg:px-8">
        <div className="text-center mb-space-xl">
          <h2 className="text-h2 text-text-primary mb-space-sm">{title}</h2>
          {description && (
            <p className="text-body text-text-secondary">{description}</p>
          )}
        </div>
        <div className="space-y-space-md">
          {faqItems.map((item, index) => (
            <div key={index} className="bg-bg-secondary p-space-md rounded-lg border border-border-light shadow-subtle">
              <h3 className="text-h3 text-text-primary mb-space-sm">{item.question}</h3>
              <p className="text-body text-text-primary leading-relaxed">{item.answer}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export function generateFAQSchema(faqItems: FAQItem[]) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqItems.map(item => ({
      "@type": "Question",
      "name": item.question,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": item.answer
      }
    }))
  };
}
