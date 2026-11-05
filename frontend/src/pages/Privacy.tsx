import React from 'react';
import ReactMarkdown from 'react-markdown';
import privacyContent from '../content/privacy.md?raw';
import { Link } from 'react-router-dom';

const Privacy: React.FC = () => {
  return (
    <div className="min-h-screen bg-white text-gray-900 font-sans py-12 px-6">
      <div className="max-w-[720px] mx-auto prose prose-gray">
        <div className="mb-8">
            <Link to="/" className="text-sm font-medium text-gray-500 hover:text-black">&larr; Back home</Link>
        </div>
        <ReactMarkdown>{privacyContent}</ReactMarkdown>
      </div>
    </div>
  );
};

export default Privacy;
