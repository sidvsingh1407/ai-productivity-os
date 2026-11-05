import React from 'react';
import { Link } from 'react-router-dom';

const Contact: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6 text-center">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm border border-gray-200">
        <h1 className="text-2xl font-bold mb-4 text-black">Contact Us</h1>
        <p className="text-gray-700 mb-8">
          You can reach us at <a href="mailto:privacy@tarkaya.com" className="text-black font-medium hover:underline">privacy@tarkaya.com</a>.
        </p>
        <Link to="/" className="text-sm font-medium text-gray-500 hover:text-black">
          &larr; Back home
        </Link>
      </div>
    </div>
  );
};

export default Contact;
