import { SeoHead } from '../../components/geo/SeoHead';

export default function CookiesPage() {
  return (
    <div className="bg-bg-primary min-h-screen animate-fade-up">
      <SeoHead
        title="Cookie Policy | TarkaX"
        description="Information about how TarkaX uses cookies."
        canonical="https://tarkax.com/cookies"
      />
      <div className="max-w-3xl mx-auto py-24 px-6">
        <h1 className="text-h1 font-semibold mb-8 border-b border-border-light pb-4">Cookie Policy</h1>
        <div className="prose text-body text-text-secondary space-y-6">
          <div className="mb-8 p-4 bg-bg-secondary rounded-lg border border-border-light">
            <p className="font-medium text-text-primary m-0">Version: v1.0</p>
            <p className="font-medium text-text-primary m-0">Effective Date: June 06, 2026</p>
            <p className="font-medium text-text-primary m-0">Last Updated: June 06, 2026</p>
          </div>

          <h2 className="text-h2 font-medium text-text-primary mt-8">1. Introduction</h2>
          <p>TarkaX uses cookies and similar tracking technologies to track the activity on our service and hold certain information. This Cookie Policy explains what cookies are, how we use them, and your choices regarding their use.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">2. What are Cookies?</h2>
          <p>Cookies are small files placed on your computer, mobile device, or any other device by a website, containing the details of your browsing history on that website among its many uses.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">3. How We Use Cookies</h2>
          <p>We use both session and persistent cookies for the purposes set out below:</p>

          <h3 className="text-h3 font-medium text-text-primary mt-6">Essential Cookies</h3>
          <p><strong>Type:</strong> Session Cookies<br/>
             <strong>Administered by:</strong> Us<br/>
             <strong>Purpose:</strong> These cookies are essential to provide you with services available through the platform and to enable you to use some of its features. They help to authenticate users and prevent fraudulent use of user accounts. Without these cookies, the services that you have asked for cannot be provided, and we only use these cookies to provide you with those services.</p>

          <h3 className="text-h3 font-medium text-text-primary mt-6">Analytics Cookies</h3>
          <p><strong>Type:</strong> Persistent Cookies<br/>
             <strong>Administered by:</strong> Third-Parties (e.g., Google Analytics, Vercel Analytics)<br/>
             <strong>Purpose:</strong> These cookies are used to track information about traffic to the platform and how users use the platform. The information gathered via these cookies may directly or indirectly identify you as an individual visitor. This is because the information collected is typically linked to a pseudonymous identifier associated with the device you use to access the platform. We use this information to improve the platform and understand user interactions.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">4. Consent Management and User Controls</h2>
          <p>You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent. However, if you do not accept cookies, you may not be able to use some parts of our service.</p>
          <p>Upon your first visit to the TarkaX platform, you will be presented with a cookie banner allowing you to accept or reject non-essential cookies. Your preference is persisted on your device. If you wish to change your preferences later, you can clear your browser's cookies to be prompted again.</p>

          <h2 className="text-h2 font-medium text-text-primary mt-8">5. Contact Us</h2>
          <p>If you have any questions about our use of cookies, you can contact us at: privacy@tarkax.com.</p>
        </div>
      </div>
    </div>
  );
}
