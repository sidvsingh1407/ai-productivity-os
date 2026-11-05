import React from 'react';
import { ComingSoonLayout } from '../components/ComingSoonLayout';

const Subprocessors: React.FC = () => {
  return (
    <ComingSoonLayout isShell={true}>
      <div className="py-8 text-cs-text-secondary">
        <h1 className="text-3xl md:text-4xl font-semibold mb-8 text-cs-text-primary">Subprocessors</h1>
        <table className="w-full text-left">
          <tbody>
            <tr><td>Supabase</td></tr>
            <tr><td>Render</td></tr>
            <tr><td>Vercel</td></tr>
            <tr><td>Resend</td></tr>
            <tr><td>Google Gemini</td></tr>
          </tbody>
        </table>
      </div>
    </ComingSoonLayout>
  );
};

export default Subprocessors;
