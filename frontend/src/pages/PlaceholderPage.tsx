import React from 'react';
import { useNavigate } from 'react-router-dom';

export const PlaceholderPage: React.FC<{ title: string }> = ({ title }) => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm border border-gray-100 text-center space-y-6">
        <h1 className="text-2xl font-serif text-gray-900">{title}</h1>
        <p className="text-gray-600">
          This is a placeholder page for the {title} route. The Operational Notice acknowledgment has been successfully verified.
        </p>
        <button
          onClick={() => navigate('/')}
          className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-md transition-colors"
        >
          Return Home
        </button>
      </div>
    </div>
  );
};
