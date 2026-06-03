import { useSearchParams } from 'react-router-dom';
import { SeoHead } from '../../components/geo/SeoHead';

export default function ContactPage() {
  const [searchParams] = useSearchParams();
  const initialInterest = searchParams.get('interest') || 'General Inquiry';

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

  return (
    <div className="bg-bg-primary min-h-screen flex flex-col animate-fade-up">
      <SeoHead
        title="Contact TarkaX | Request a Demo"
        description="Request a demo of TarkaX to explore the operational realities of your organization through our AI Audit and Workflow Diagnostic."
        canonical="https://tarkax.com/contact"
        schema={[breadcrumbSchema]}
      />
      {/* Header */}
      <section className="pt-[120px] pb-[80px]">
        <div className="max-w-3xl mx-auto px-6 lg:px-8 text-center">
          <h1 className="text-h1 text-text-primary mb-space-sm">
            See What TarkaX Finds.
          </h1>
          <p className="text-h3 font-normal text-text-secondary">
            Request a demo to explore the operational realities of your organization.
          </p>
        </div>
      </section>

      {/* Form Section */}
      <section className="pb-[120px] flex-grow">
        <div className="max-w-2xl mx-auto px-6 lg:px-8">
          <div className="bg-bg-primary p-space-lg rounded-lg border border-border-light shadow-card">
            <form className="space-y-space-md" onSubmit={(e) => e.preventDefault()}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-space-md">
                <div className="space-y-space-xs">
                  <label htmlFor="firstName" className="block text-label text-text-primary">First Name</label>
                  <input
                    type="text"
                    id="firstName"
                    className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary"
                    placeholder="Jane"
                  />
                </div>
                <div className="space-y-space-xs">
                  <label htmlFor="lastName" className="block text-label text-text-primary">Last Name</label>
                  <input
                    type="text"
                    id="lastName"
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
                  className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary"
                  placeholder="jane@company.com"
                />
              </div>

              <div className="space-y-space-xs">
                <label htmlFor="organization" className="block text-label text-text-primary">Organization</label>
                <input
                  type="text"
                  id="organization"
                  className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary"
                  placeholder="Company Name"
                />
              </div>

              <div className="space-y-space-xs">
                <label htmlFor="role" className="block text-label text-text-primary">Role</label>
                <input
                  type="text"
                  id="role"
                  className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors text-body bg-bg-primary"
                  placeholder="e.g. Director of Operations"
                />
              </div>

              <div className="space-y-space-xs">
                <label htmlFor="interest" className="block text-label text-text-primary">Area of Interest</label>
                <select
                  id="interest"
                  defaultValue={initialInterest}
                  className="w-full px-4 py-3 rounded-md border border-border-strong focus:outline-none focus:ring-2 focus:ring-accent-blue focus:border-transparent transition-colors bg-bg-primary text-body"
                >
                  <option value="AI Audit">AI Audit</option>
                  <option value="Workflow Diagnostic">Workflow Diagnostic</option>
                  <option value="Forecasting Framework">Forecasting Framework</option>
                  <option value="General Inquiry">General Inquiry</option>
                </select>
              </div>

              <button
                type="submit"
                className="w-full px-8 py-4 bg-accent-blue text-text-inverse text-body font-medium rounded-md shadow-sm hover:bg-accent-blue/90 transition-colors mt-space-lg"
              >
                Request a Demo
              </button>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
}