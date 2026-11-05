import React from 'react';

interface ProductCardProps {
  name: string;
  copy: string;
}

export const ProductCard: React.FC<ProductCardProps> = ({ name, copy }) => {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 shadow-sm">
      <h3 className="text-xl font-semibold mb-3 text-black">{name}</h3>
      <p className="text-gray-700 leading-relaxed">{copy}</p>
    </div>
  );
};
