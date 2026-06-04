import { SeoHead } from '../../components/geo/SeoHead';

export default function PrivacyPage() {
  return (
    <div className="bg-bg-primary min-h-screen animate-fade-up">
      <SeoHead
        title="Privacy Policy | TarkaX"
        description="Privacy policy and data handling practices for TarkaX."
        canonical="https://tarkax.com/privacy"
      />
      <div className="max-w-3xl mx-auto py-24 px-6">
        <h1 className="text-h1 font-semibold mb-8 border-b border-border-light pb-4">Privacy Policy</h1>
        <div className="prose text-body text-text-secondary space-y-6">
          <p>Last Updated: {new Date().toLocaleDateString()}</p>
          <h2 className="text-h2 font-medium text-text-primary mt-8">1. Introduction</h2>
          <p>TarkaX operates strictly as an intelligence organization. We respect your privacy and are committed to protecting it through our compliance with this policy.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">2. Information Collection</h2>
          <p>We collect information you provide directly to us through assessments and contact forms. This data is processed statelessly where possible and is strictly used to generate insights for your organization.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">3. AI Data Usage</h2>
          <p>TarkaX does not use client assessment responses to train foundational large language models. Our deterministic engines process inputs strictly according to predefined rulesets.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">4. Contact Us</h2>
          <p>To ask questions or comment about this privacy policy and our privacy practices, contact us at: privacy@tarkax.com.</p>
        </div>
      </div>
    </div>
  );
}
