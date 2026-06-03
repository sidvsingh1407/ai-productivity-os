import { useSearchParams } from 'react-router-dom';

export default function ContactPage() {
  const [searchParams] = useSearchParams();
  const initialInterest = searchParams.get('interest') || 'General Inquiry';

  return (
    <div className="bg-background min-h-screen flex flex-col">
      {/* Header */}
      <section className="pt-24 pb-12">
        <div className="max-w-3xl mx-auto px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-5xl font-light text-foreground tracking-tight mb-6">
            See What TarkaX Finds.
          </h1>
          <p className="text-xl text-gray-600 font-light leading-relaxed">
            Request a demo to explore the operational realities of your organization.
          </p>
        </div>
      </section>

      {/* Form Section */}
      <section className="py-12 flex-grow">
        <div className="max-w-2xl mx-auto px-6 lg:px-8">
          <div className="bg-white p-8 md:p-12 rounded-xl border border-gray-200 shadow-sm">
            <form className="space-y-6" onSubmit={(e) => e.preventDefault()}>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label htmlFor="firstName" className="block text-sm font-medium text-foreground">First Name</label>
                  <input
                    type="text"
                    id="firstName"
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-foreground/20 focus:border-foreground transition-colors"
                    placeholder="Jane"
                  />
                </div>
                <div className="space-y-2">
                  <label htmlFor="lastName" className="block text-sm font-medium text-foreground">Last Name</label>
                  <input
                    type="text"
                    id="lastName"
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-foreground/20 focus:border-foreground transition-colors"
                    placeholder="Doe"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <label htmlFor="email" className="block text-sm font-medium text-foreground">Work Email</label>
                <input
                  type="email"
                  id="email"
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-foreground/20 focus:border-foreground transition-colors"
                  placeholder="jane@company.com"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="organization" className="block text-sm font-medium text-foreground">Organization</label>
                <input
                  type="text"
                  id="organization"
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-foreground/20 focus:border-foreground transition-colors"
                  placeholder="Company Name"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="role" className="block text-sm font-medium text-foreground">Role</label>
                <input
                  type="text"
                  id="role"
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-foreground/20 focus:border-foreground transition-colors"
                  placeholder="e.g. Director of Operations"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="interest" className="block text-sm font-medium text-foreground">Area of Interest</label>
                <select
                  id="interest"
                  defaultValue={initialInterest}
                  className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-foreground/20 focus:border-foreground transition-colors bg-white"
                >
                  <option value="AI Audit">AI Audit</option>
                  <option value="Workflow Diagnostic">Workflow Diagnostic</option>
                  <option value="Forecasting Framework">Forecasting Framework</option>
                  <option value="General Inquiry">General Inquiry</option>
                </select>
              </div>

              <button
                type="submit"
                className="w-full px-8 py-4 bg-foreground text-background font-medium rounded-lg hover:bg-foreground/90 transition-all mt-8"
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