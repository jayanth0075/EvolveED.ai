import React from 'react';
import { motion } from 'framer-motion';

export default function Loader(){
  return (
    <div className="w-full h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="flex flex-col items-center gap-4">
        <motion.div
          className="w-16 h-16 rounded-full border-4 border-blue-200 border-t-blue-500"
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
        />
        <motion.p
          className="text-blue-600 font-medium"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          Loading your career journey...
        </motion.p>
      </div>
    </div>
  );
}