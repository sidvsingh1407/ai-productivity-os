import React from 'react';
import { Link } from 'react-router-dom';

const Confirmed: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6 text-center">
      <div className="max-w-md bg-white p-8 rounded-lg shadow-sm border border-gray-200">
        <h1 className="text-2xl font-bold mb-4 text-black">You are confirmed.</h1>
        <p className="text-gray-700 mb-8">
          We will email you when we launch.
        </p>
        <Link to="/" className="text-black font-medium hover:underline">
          &larr; Back to Tarkaya
        </Link>
      </div>
    </div>
  );
};

export default Confirmed;
