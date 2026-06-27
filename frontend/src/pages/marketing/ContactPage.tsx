import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import apiClient from '@/api/client';
import { SeoHead } from '../../components/geo/SeoHead';

export default function ContactPage() {
  const [searchParams] = useSearchParams();
  const initialInterest = searchParams.get('interest') || 'General Inquiry';

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    interest: initialInterest,
    message: '',
    consent_given: false
  });

  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://tarkax.com/"
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": "Contact",
        "item": "https://tarkax.com/contact"
      }
    ]
  };

  const mutation = useMutation({
    mutationFn: async (data: typeof formData) => {
      const response = await apiClient.post('/contact', {
        name: `${data.firstName} ${data.lastName}`.trim(),
        email: data.email,
        company: data.company,
        interest: data.interest,
        message: data.message,
        source_page: window.location.pathname,
        consent_given: data.consent_given
      });
      return response.data;
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    mutation.mutate(formData);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const value = e.target.type === 'checkbox' ? (e.target as HTMLInputElement).checked : e.target.value;
    setFormData(prev => ({ ...prev, [e.target.name]: value }));
  };

  return (
    <div className="bg-bg-primary min-h-screen flex flex-col animate-fade-up">
      <SeoHead
        title="Contact TarkaX | Request a Demo"
        description="Get in touch with TarkaX to learn how our Organizational Failure Intelligence platform can protect your operations."
        canonical="https://tarkax.com/contact"

        schema={breadcrumbSchema}
      />

      <section className="pt-24 pb-16 px-4 sm:px-6 lg:px-8 border-b border-border-light bg-bg-secondary">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-h1 font-semibold text-text-primary mb-4 tracking-tight">
            Contact TarkaX
          </h1>
          <p className="text-body text-text-secondary max-w-2xl mx-auto">
            Ready to identify capability gaps before they become critical failures? Fill out the form below and our team will be in touch shortly.
          </p>
        </div>
      </section>

      <section className="py-16 px-4 sm:px-6 lg:px-8 flex-grow">
        <div className="max-w-xl mx-auto">
          {mutation.isSuccess ? (
             <div className="p-8 bg-green-50 border border-green-200 rounded-md text-center">
               <h3 className="text-h3 font-medium text-green-900 mb-2">Message Received</h3>
               <p className="text-body text-green-800">Thank you for reaching out. A member of our intelligence team will contact you shortly.</p>
             </div>
          ) : (
          <div className="bg-bg-primary p-8 rounded-md border border-border-strong shadow-sm">
            <h2 className="text-h3 font-semibold text-text-primary mb-6">Send us a message</h2>
            <form className="space-y-space-md" onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md">
                <div className="space-y-space-xs">
                  <label htmlFor="firstName" className="block text-label text-text-primary">First Name</label>
                  <input
                    type="text"
                    id="firstName"
                    name="firstName"
                    required
                    value={formData.firstName}
                    onChange={handleChange}
                    className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary"
                    placeholder="Jane"
                  />
                </div>
                <div className="space-y-space-xs">
                  <label htmlFor="lastName" className="block text-label text-text-primary">Last Name</label>
                  <input
                    type="text"
                    id="lastName"
                    name="lastName"
                    required
                    value={formData.lastName}
                    onChange={handleChange}
                    className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary"
                    placeholder="Doe"
                  />
                </div>
              </div>

              <div className="space-y-space-xs">
                <label htmlFor="email" className="block text-label text-text-primary">Work Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary"
                  placeholder="jane@company.com"
                />
              </div>

              <div className="space-y-space-xs">
                <label htmlFor="company" className="block text-label text-text-primary">Company</label>
                <input
                  type="text"
                  id="company"
                  name="company"
                  value={formData.company}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary"
                  placeholder="Company Ltd."
                />
              </div>

              <div className="space-y-space-xs">
                <label htmlFor="interest" className="block text-label text-text-primary">Area of Interest</label>
                <select
                  id="interest"
                  name="interest"
                  value={formData.interest}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors bg-bg-primary text-body"
                >
                  <option value="Compliance Readiness">Compliance Readiness</option>
                  <option value="Workflow Intelligence">Workflow Intelligence</option>
                  <option value="Forecasting Framework">Forecasting Framework</option>
                  <option value="Benchmarking">Benchmarking</option>
                  <option value="Partnership">Partnership</option>
                  <option value="Demo Request">Demo Request</option>
                  <option value="General Inquiry">General Inquiry</option>
                </select>
              </div>

              <div className="space-y-space-xs">
                <label htmlFor="message" className="block text-label text-text-primary">Message (Optional)</label>
                <textarea
                  id="message"
                  name="message"
                  rows={4}
                  value={formData.message}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary resize-none"
                  placeholder="How can we help you?"
                ></textarea>
              </div>

              <div className="flex items-start space-x-3 pt-2">
                <input
                  type="checkbox"
                  id="consent_given"
                  name="consent_given"
                  required
                  checked={formData.consent_given}
                  onChange={handleChange}
                  className="mt-1 h-4 w-4 rounded border-border-strong text-accent-blue focus:ring-accent-blue bg-bg-primary"
                />
                <label htmlFor="consent_given" className="text-body text-text-secondary leading-tight">
                  I have read and agree to the <a href="/privacy" className="text-accent-blue hover:underline">Privacy Policy</a>.
                </label>
              </div>

              <button
                type="submit"
                disabled={mutation.isPending}
                className="w-full px-6 py-3 bg-text-primary text-bg-primary text-body font-medium rounded-md hover:bg-opacity-90 transition-opacity disabled:opacity-50"
              >
                {mutation.isPending ? 'Sending...' : 'Send Message'}
              </button>

              {mutation.isError && (
                 <p className="text-red-600 text-sm mt-2 text-center">There was an error sending your message. Please try again.</p>
              )}
            </form>
          </div>
          )}
        </div>
      </section>
    </div>
  );
}
