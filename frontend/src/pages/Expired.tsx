import React from 'react';
import { WaitlistForm } from '../components/WaitlistForm';

const Expired: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6 text-center">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm border border-gray-200">
        <h1 className="text-2xl font-bold mb-4 text-black">Link Expired</h1>
        <p className="text-gray-700 mb-8">
          This confirmation link has expired. Enter your email again.
        </p>
        <WaitlistForm />
      </div>
    </div>
  );
};

export default Expired;
