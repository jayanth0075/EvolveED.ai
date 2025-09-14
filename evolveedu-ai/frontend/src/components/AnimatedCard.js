import React from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRight, ChevronRight } from 'lucide-react';

export default function AnimatedCard({
  title,
  children,
  onClick,
  actionLabel,
  className = '',
  icon: Icon,
  gradient = 'from-blue-500 to-blue-600'
}) {
  return (
    <motion.div
      className={`group relative bg-white rounded-xl border border-slate-200 p-6 shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden ${className}`}
      whileHover={{ y: -4 }}
      onClick={onClick}
    >
      {/* Gradient accent */}
      <div className={`absolute top-0 left-0 w-full h-1 bg-gradient-to-r ${gradient}`}></div>

      {/* Content */}
      <div className="relative">
        {Icon && (
          <div className="mb-4">
            <div className={`p-3 rounded-lg bg-gradient-to-r ${gradient} w-fit`}>
              <Icon className="h-6 w-6 text-white" />
            </div>
          </div>
        )}

        <h3 className="text-lg font-semibold text-slate-800 mb-2">{title}</h3>
        <div className="text-slate-600 text-sm leading-relaxed">{children}</div>

        {actionLabel && (
          <div className="mt-4 flex items-center text-blue-600 group-hover:text-blue-700 transition-colors">
            <span className="text-sm font-medium">{actionLabel}</span>
            <ChevronRight className="h-4 w-4 ml-1 group-hover:translate-x-1 transition-transform" />
          </div>
        )}
      </div>

      {/* Hover effect */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
    </motion.div>
  );
}