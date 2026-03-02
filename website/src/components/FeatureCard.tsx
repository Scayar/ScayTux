import React from 'react';

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
}

export function FeatureCard({ icon, title, description }: FeatureCardProps) {
  return (
    <div className="card p-6 hover:scale-[1.02] group">
      <div className="w-11 h-11 rounded-xl bg-tux-orange/10 flex items-center justify-center mb-4 text-tux-orange group-hover:bg-tux-orange/15 transition-colors duration-300">
        {icon}
      </div>
      <h3 className="text-[15px] font-semibold text-white mb-2">{title}</h3>
      <p className="text-sm text-tux-subtle leading-relaxed">{description}</p>
    </div>
  );
}
