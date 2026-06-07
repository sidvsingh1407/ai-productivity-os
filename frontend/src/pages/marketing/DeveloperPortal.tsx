import React, { useState } from 'react';

export function DeveloperPortal() {
  const [activeSection, setActiveSection] = useState('overview');

  const navItems = [
    { id: 'overview', label: 'Overview' },
    { id: 'authentication', label: 'Authentication' },
    { id: 'quickstart', label: 'Quick Start' },
    { id: 'versioning', label: 'API Versioning' },
    { id: 'errors', label: 'Common Errors' },
    { id: 'audit', label: 'AI Audit API' },
    { id: 'workflow', label: 'Workflow API' },
    { id: 'risk', label: 'Risk Projection API' },
    { id: 'prompt', label: 'Prompt Intelligence API' }
  ];

  const scrollTo = (id: string) => {
    setActiveSection(id);
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  };

  return (
    <div className="bg-bg-primary min-h-screen text-text-primary font-sans pt-24">
      <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row gap-12 pb-24">

        {/* Sidebar Nav */}
        <aside className="w-full md:w-64 shrink-0 mt-8 md:sticky md:top-32 h-fit overflow-y-auto">
          <h3 className="text-sm font-semibold uppercase tracking-wider text-text-secondary mb-4">Documentation</h3>
          <nav className="space-y-1">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => scrollTo(item.id)}
                className={`block w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  activeSection === item.id
                    ? 'bg-accent-blue text-white'
                    : 'text-text-secondary hover:text-text-primary hover:bg-bg-secondary'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>
        </aside>

        {/* Content */}
        <div className="flex-1 max-w-4xl prose prose-slate">

          <section id="overview" className="mb-16 pt-8 scroll-mt-32">
            <h1 className="text-4xl font-bold mb-4">TarkaX Developer Portal</h1>

            <div className="bg-bg-secondary border border-border-strong rounded-lg p-6 mb-8 text-center sm:text-left">
               <h2 className="text-2xl font-bold mb-2">API Platform Coming Soon</h2>
               <p className="text-body text-text-secondary mb-4">
                  The TarkaX API is currently under active development. Soon you will be able to integrate TarkaX operational intelligence and diagnostic capabilities directly into your workflows.
               </p>
               <p className="text-body text-text-secondary mb-4">
                  Developers will be able to evaluate structural readiness, identify workflow bottlenecks, and continuously score prompts without manual intervention.
               </p>
               <div className="text-left mb-6">
                 <h3 className="font-semibold text-text-primary mb-2">Planned APIs:</h3>
                 <ul className="list-disc pl-5 text-body text-text-secondary space-y-1">
                   <li>AI Audit API</li>
                   <li>Workflow Diagnostic API</li>
                   <li>Prompt Intelligence API</li>
                 </ul>
               </div>
               <a
                 href="/contact"
                 className="inline-block px-4 py-2 bg-text-primary text-text-inverse text-sm font-medium rounded-md hover:bg-text-primary/90 transition-colors"
               >
                 Contact Us to Learn More
               </a>
            </div>

            <p className="text-xl text-text-secondary mb-8">
              Integrate TarkaX operational intelligence and diagnostic capabilities directly into your workflows.
            </p>
            <p>
              The TarkaX API is organized around REST. Our API has predictable resource-oriented URLs,
              accepts JSON-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes.
            </p>
            <div className="bg-bg-secondary border border-border-strong rounded-lg p-6 my-8">
              <h3 className="text-lg font-semibold mt-0">Base URL</h3>
              <code className="text-accent-blue bg-white px-2 py-1 rounded">https://api.tarkax.com</code>
            </div>
          </section>

          <section id="authentication" className="mb-16 pt-8 scroll-mt-32">
            <h2 className="text-3xl font-bold border-b border-border-light pb-2 mb-6">Authentication</h2>
            <p>
              The TarkaX API uses API keys to authenticate requests. You will be able to view and manage your API keys
              in the <span className="text-text-secondary font-medium italic">Developer Dashboard (Coming Soon)</span>.
            </p>
            <p>
              Authentication to the API is performed via the <code>X-API-Key</code> header. Do not use Bearer tokens for these product APIs.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-2">cURL Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto">
              <pre><code>curl -X POST https://api.tarkax.com/api/v1/audit \
  -H "X-API-Key: tkx_live_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '&#123;...&#125;'</code></pre>
            </div>

            <h3 className="text-xl font-semibold mt-6 mb-2">JavaScript Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto">
              <pre><code>fetch('https://api.tarkax.com/api/v1/audit', &#123;
  method: 'POST',
  headers: &#123;
    'X-API-Key': 'tkx_live_your_api_key_here',
    'Content-Type': 'application/json'
  &#125;,
  body: JSON.stringify(&#123;...&#125;)
&#125;);</code></pre>
            </div>

            <h3 className="text-xl font-semibold mt-6 mb-2">Python Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto">
              <pre><code>import requests

headers = &#123;
    'X-API-Key': 'tkx_live_your_api_key_here',
    'Content-Type': 'application/json'
&#125;
response = requests.post('https://api.tarkax.com/api/v1/audit', headers=headers, json=&#123;...&#125;)</code></pre>
            </div>

            <h3 className="text-xl font-semibold mt-8 mb-4">Authentication Behavior</h3>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Invalid Key:</strong> Returns <code>401 Unauthorized</code></li>
              <li><strong>Revoked/Expired Key:</strong> Returns <code>403 Forbidden</code></li>
              <li><strong>Rate Limit Exceeded:</strong> Returns <code>429 Too Many Requests</code></li>
            </ul>
          </section>

          <section id="quickstart" className="mb-16 pt-8 scroll-mt-32">
            <h2 className="text-3xl font-bold border-b border-border-light pb-2 mb-6">Quick Start</h2>

            <div className="space-y-12">
              <div>
                <h3 className="text-2xl font-bold mb-4">AI Audit Quick Start</h3>
                <ol className="list-decimal pl-6 space-y-4">
                  <li><strong>Obtain API Key:</strong> Navigate to the Developer Dashboard and create a new key.</li>
                  <li>
                    <strong>Example Request:</strong> Send a basic compliance payload.
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mt-2">
                      <pre><code>curl -X POST https://api.tarkax.com/api/v1/audit \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '&#123;"form_response": &#123;"has_documented_processes": true&#125;, "industry_type": "technology"&#125;'</code></pre>
                    </div>
                  </li>
                  <li>
                    <strong>Example Response:</strong>
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mt-2">
                      <pre><code>&#123;
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "total_score": 75,
  "rating": "Maturing",
  ...
&#125;</code></pre>
                    </div>
                  </li>
                  <li><strong>Expected Output:</strong> The system returns a scored assessment and actionable recommendations.</li>
                </ol>
              </div>

              <div>
                <h3 className="text-2xl font-bold mb-4">Workflow Quick Start</h3>
                <ol className="list-decimal pl-6 space-y-4">
                  <li><strong>Obtain API Key:</strong> Get your key from the Dashboard.</li>
                  <li>
                    <strong>Example Request:</strong> Provide process details.
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mt-2">
                      <pre><code>curl -X POST https://api.tarkax.com/workflows/ \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '&#123;"input_config": &#123;"process_name": "Onboarding"&#125;&#125;'</code></pre>
                    </div>
                  </li>
                  <li>
                    <strong>Example Response:</strong>
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mt-2">
                      <pre><code>&#123;
  "id": "workflow-id",
  "status": "completed",
  ...
&#125;</code></pre>
                    </div>
                  </li>
                  <li><strong>Expected Output:</strong> Diagnostic mapping identifying bottlenecks and root causes.</li>
                </ol>
              </div>

              <div>
                <h3 className="text-2xl font-bold mb-4">Risk Projection Quick Start</h3>
                <ol className="list-decimal pl-6 space-y-4">
                  <li><strong>Obtain API Key:</strong> Copy a valid API key.</li>
                  <li>
                    <strong>Example Request:</strong> Send scores.
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mt-2">
                      <pre><code>curl -X POST https://api.tarkax.com/api/v1/risk \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '&#123;"scores": &#123;"dimensions": &#123;"ops": 60&#125;&#125;&#125;'</code></pre>
                    </div>
                  </li>
                  <li>
                    <strong>Example Response:</strong>
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mt-2">
                      <pre><code>&#123;
  "risk_level": "Medium",
  "risk_score": 65,
  ...
&#125;</code></pre>
                    </div>
                  </li>
                  <li><strong>Expected Output:</strong> A risk level and actionable timelines.</li>
                </ol>
              </div>

              <div>
                <h3 className="text-2xl font-bold mb-4">Prompt Intelligence Quick Start</h3>
                <ol className="list-decimal pl-6 space-y-4">
                  <li><strong>Obtain API Key:</strong> Retrieve an API key.</li>
                  <li>
                    <strong>Example Request:</strong> Pass a basic prompt.
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mt-2">
                      <pre><code>curl -X POST https://api.tarkax.com/api/prompt-improver \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '&#123;"prompt": "Send an update email"&#125;'</code></pre>
                    </div>
                  </li>
                  <li>
                    <strong>Example Response:</strong>
                    <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mt-2">
                      <pre><code>&#123;
  "improved_prompt": "Draft an update email detailing progress on the current sprint...",
  "scores": &#123;"original_score": 20, "improved_score": 85&#125;
&#125;</code></pre>
                    </div>
                  </li>
                  <li><strong>Expected Output:</strong> Context-aware optimized prompt.</li>
                </ol>
              </div>
            </div>
          </section>

          <section id="versioning" className="mb-16 pt-8 scroll-mt-32">
            <h2 className="text-3xl font-bold border-b border-border-light pb-2 mb-6">API Versioning</h2>
            <p>
              Current Version: <strong>v1</strong>
            </p>
            <p>
              We consider changes to be backwards-compatible if they do not break existing integrations.
              Examples include adding new endpoints, adding new optional request parameters, or adding new properties to responses.
            </p>
            <p>
              If we introduce a backwards-incompatible change, we will release a new API version (e.g., v2).
              Older versions will be supported for at least 12 months after deprecation.
            </p>
          </section>

          <section id="errors" className="mb-16 pt-8 scroll-mt-32">
            <h2 className="text-3xl font-bold border-b border-border-light pb-2 mb-6">Common Errors</h2>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-border-strong text-sm">
                <thead>
                  <tr>
                    <th className="px-4 py-2 text-left font-semibold">Code</th>
                    <th className="px-4 py-2 text-left font-semibold">Meaning</th>
                    <th className="px-4 py-2 text-left font-semibold">Cause & Resolution</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-light">
                  <tr>
                    <td className="px-4 py-3 font-mono font-bold text-accent-red">401</td>
                    <td className="px-4 py-3">Unauthorized</td>
                    <td className="px-4 py-3">Missing or invalid API key. Ensure <code>X-API-Key</code> header is present.</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 font-mono font-bold text-accent-red">403</td>
                    <td className="px-4 py-3">Forbidden</td>
                    <td className="px-4 py-3">API key is revoked or lacks permissions. Generate a new key.</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 font-mono font-bold text-accent-red">422</td>
                    <td className="px-4 py-3">Unprocessable Entity</td>
                    <td className="px-4 py-3">Invalid request payload. Check documentation for required fields.</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 font-mono font-bold text-accent-red">429</td>
                    <td className="px-4 py-3">Rate Limited</td>
                    <td className="px-4 py-3">Exceeded tier rate limit. Check headers or upgrade your plan.</td>
                  </tr>
                  <tr>
                    <td className="px-4 py-3 font-mono font-bold text-accent-red">500</td>
                    <td className="px-4 py-3">Server Error</td>
                    <td className="px-4 py-3">An unexpected error occurred on our end. Contact support if it persists.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <section id="audit" className="mb-16 pt-8 scroll-mt-32">
            <h2 className="text-3xl font-bold border-b border-border-light pb-2 mb-6">AI Audit API</h2>
            <div className="flex items-center gap-3 mb-4">
              <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-mono text-sm font-bold">POST</span>
              <code className="text-lg">/api/v1/audit</code>
            </div>
            <p>
              Submit an assessment payload to the TarkaX intelligence engine. The API analyzes the form and evidence responses
              to determine maturity scores, findings, recommendations, and benchmark data.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-2">Request Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mb-6">
              <pre><code>&#123;
  "form_response": &#123;
    "has_documented_processes": true,
    "review_frequency": "Annually"
  &#125;,
  "evidence_response": &#123;
    "process_docs": "Attached manual v2"
  &#125;,
  "industry_type": "technology"
&#125;</code></pre>
            </div>

            <h3 className="text-xl font-semibold mt-6 mb-2">Response Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto">
              <pre><code>&#123;
  "id": "uuid",
  "total_score": 75,
  "rating": "Maturing",
  "intelligence": &#123;
    "findings": [...],
    "recommendations": [...]
  &#125;
&#125;</code></pre>
            </div>
          </section>

          <section id="workflow" className="mb-16 pt-8 scroll-mt-32">
            <h2 className="text-3xl font-bold border-b border-border-light pb-2 mb-6">Workflow Diagnostic API</h2>
            <div className="flex items-center gap-3 mb-4">
              <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-mono text-sm font-bold">POST</span>
              <code className="text-lg">/workflows/</code>
            </div>
            <p>
              Run a diagnostic pipeline on a specified operational workflow. Returns identified bottlenecks, root causes,
              and optimization blueprints. Note: this API expects Bearer token auth in the current architecture.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-2">Request Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mb-6">
              <pre><code>&#123;
  "input_config": &#123;
    "process_name": "Employee Onboarding",
    "steps": ["HR Setup", "IT Provisioning", "Manager Intro"]
  &#125;
&#125;</code></pre>
            </div>

            <h3 className="text-xl font-semibold mt-6 mb-2">Response Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto">
              <pre><code>&#123;
  "id": "uuid",
  "status": "completed",
  "intelligence": &#123;
    "executive_summary": &#123; ... &#125;,
    "bottlenecks": [...]
  &#125;
&#125;</code></pre>
            </div>
          </section>

          <section id="risk" className="mb-16 pt-8 scroll-mt-32">
            <h2 className="text-3xl font-bold border-b border-border-light pb-2 mb-6">Risk Projection API</h2>
            <div className="flex items-center gap-3 mb-4">
              <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-mono text-sm font-bold">POST</span>
              <code className="text-lg">/api/v1/risk</code>
            </div>
            <p>
              Generate future-state risk projections based on dimensional scores and findings. This stateless endpoint
              requires no historical database context.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-2">Request Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mb-6">
              <pre><code>&#123;
  "scores": &#123;
    "dimensions": &#123; "ops": 60, "sec": 45 &#125;,
    "missing_data_flags": []
  &#125;,
  "findings": []
&#125;</code></pre>
            </div>

            <h3 className="text-xl font-semibold mt-6 mb-2">Response Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto">
              <pre><code>&#123;
  "risk_level": "High",
  "risk_score": 82,
  "risk_timeline": &#123;
    "near_term": ["Immediate compliance exposure"]
  &#125;
&#125;</code></pre>
            </div>
          </section>

          <section id="prompt" className="mb-16 pt-8 scroll-mt-32">
            <h2 className="text-3xl font-bold border-b border-border-light pb-2 mb-6">Prompt Intelligence API</h2>
            <div className="flex items-center gap-3 mb-4">
              <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-mono text-sm font-bold">POST</span>
              <code className="text-lg">/api/prompt-improver</code>
            </div>
            <p>
              Stateless endpoint to rewrite and score prompts deterministically for better operational outcomes.
            </p>

            <h3 className="text-xl font-semibold mt-6 mb-2">Request Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto mb-6">
              <pre><code>&#123;
  "prompt": "Write an email to the client about the delay."
&#125;</code></pre>
            </div>

            <h3 className="text-xl font-semibold mt-6 mb-2">Response Example</h3>
            <div className="bg-slate-900 text-slate-200 rounded-lg p-4 font-mono text-sm overflow-x-auto">
              <pre><code>&#123;
  "improved_prompt": "Draft a formal email to the client regarding the Q3 delivery delay, including root cause and revised timeline.",
  "scores": &#123;
    "original_score": 30,
    "improved_score": 85
  &#125;,
  "validation": &#123;
    "passed": true,
    "errors": []
  &#125;
&#125;</code></pre>
            </div>
          </section>

        </div>
      </div>
    </div>
  );
}
