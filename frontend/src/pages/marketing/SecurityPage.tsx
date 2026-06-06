import { SeoHead } from '../../components/geo/SeoHead';

export default function SecurityPage() {
  return (
    <div className="bg-bg-primary min-h-screen animate-fade-up">
      <SeoHead
        title="Security Overview | TarkaX"
        description="Security practices and infrastructure at TarkaX."
        canonical="https://tarkax.com/security"
      />
      <div className="max-w-3xl mx-auto py-24 px-6">
        <h1 className="text-h1 font-semibold mb-8 border-b border-border-light pb-4">Security Overview</h1>
        <div className="prose text-body text-text-secondary space-y-6">
          <div className="mb-8 p-4 bg-bg-secondary rounded-lg border border-border-light">
            <p className="font-medium text-text-primary m-0">Version: v1.0</p>
            <p className="font-medium text-text-primary m-0">Effective Date: June 06, 2026</p>
            <p className="font-medium text-text-primary m-0">Last Updated: June 06, 2026</p>
          </div>

          <h2 className="text-h2 font-medium text-text-primary mt-8">1. Introduction</h2>
          <p>At TarkaX, we take the security of your operational data seriously. This document outlines the fundamental security practices and infrastructure we employ to protect your information.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">2. Authentication</h2>
          <p>We use robust authentication mechanisms to verify user identities before granting access to the platform. Passwords and credentials are not stored in plaintext and are securely hashed using modern cryptographic standards.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">3. Data Storage</h2>
          <p>All platform data is stored securely on Supabase servers located in Singapore. We rely on their underlying infrastructure for physical security, redundancy, and environmental controls.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">4. Access Controls</h2>
          <p>We implement strict logical access controls. User access is restricted to their respective organizational data. We utilize role-based access control (RBAC) and Row Level Security (RLS) policies within our database to ensure that data isolation is maintained across tenant boundaries.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">5. Encryption Practices</h2>
          <p>Data transmitted between your browser and our servers is encrypted in transit using Transport Layer Security (TLS). Data at rest is encrypted according to the standards provided by our infrastructure providers.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">6. Responsible Disclosure</h2>
          <p>We welcome reports from security researchers and users who believe they have found a vulnerability in our systems. If you have discovered a potential security issue, please contact us immediately at security@tarkax.com. We ask that you provide detailed information to allow us to reproduce and address the issue responsibly.</p>
        </div>
      </div>
    </div>
  );
}
