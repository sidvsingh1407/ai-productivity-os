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
          <div className="mb-8 p-4 bg-bg-secondary rounded-lg border border-border-light">
            <p className="font-medium text-text-primary m-0">Version: v1.0</p>
            <p className="font-medium text-text-primary m-0">Effective Date: June 06, 2026</p>
            <p className="font-medium text-text-primary m-0">Last Updated: June 06, 2026</p>
          </div>

          <h2 className="text-h2 font-medium text-text-primary mt-8">1. Introduction</h2>
          <p>TarkaX respects your privacy and is committed to protecting it through our compliance with this policy. This Privacy Policy describes the types of information we may collect from you or that you may provide when you visit the TarkaX platform and our practices for collecting, using, maintaining, protecting, and disclosing that information.</p>
          <p>This policy applies to information we collect on our platform, in email, text, and other electronic messages between you and TarkaX.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">2. Information Collected</h2>
          <p>We collect several types of information from and about users of our platform, including:</p>
          <ul className="list-disc pl-6 space-y-2">
            <li><strong>Account Information:</strong> Name, Email Address, and Company Name.</li>
            <li><strong>Audit Data:</strong> Responses provided during AI Audits.</li>
            <li><strong>Workflow Data:</strong> Inputs and configurations provided during Workflow Diagnostics.</li>
            <li><strong>Prompt Data:</strong> Inputs used within the Prompt Improver features.</li>
            <li><strong>Analytics Usage:</strong> Usage details, IP addresses, and information collected through cookies and other tracking technologies. We use Google Analytics and Vercel Analytics to understand how our platform is used.</li>
          </ul>

          <h2 className="text-h2 font-medium text-text-primary mt-8">3. Data Storage and Retention</h2>
          <p>We store your data securely using Supabase servers located in Singapore. We retain your data according to our data retention principles, which restrict data storage to the period necessary to provide our services, comply with legal obligations, resolve disputes, and enforce our agreements. For detailed retention periods, please see our <a href="/data-retention" className="text-brand-primary hover:underline">Data Retention Policy</a>.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">4. Data Usage and AI Models</h2>
          <p>User data may be used to improve TarkaX where permitted by applicable law and subject to applicable consent, privacy settings, and legal requirements.</p>
          <p><strong>Current State:</strong> TarkaX currently relies exclusively on deterministic engines. We do not use external large language model (LLM) providers at this time.</p>
          <p><strong>Future State:</strong> TarkaX may integrate third-party AI providers in future releases. Any updates to our use of AI models and their data handling will be reflected in an updated version of this policy.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">5. User Rights and Account Deletion</h2>
          <p>You have the right to access, correct, or request the deletion of your personal data. You may initiate an account deletion process by contacting us directly. Upon account deletion, your personal data will be removed from our active systems, subject to legal and operational retention requirements.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">6. International Transfers</h2>
          <p>As TarkaX operates globally with primary operations in India and server infrastructure in Singapore, your information may be transferred to, and maintained on, computers located outside of your state, province, country, or other governmental jurisdiction where the data protection laws may differ from those from your jurisdiction. By using our platform, you consent to this transfer.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">7. Contact Us</h2>
          <p>To ask questions or comment about this privacy policy and our privacy practices, contact us at: privacy@tarkax.com.</p>
        </div>
      </div>
    </div>
  );
}
