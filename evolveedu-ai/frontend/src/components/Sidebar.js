import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  Home,
  Map,
  BookOpen,
  HelpCircle,
  MessageSquare,
  Trophy,
  TrendingUp,
  Target
} from 'lucide-react';
import { motion } from 'framer-motion';

const mainItems = [
  { to: '/dashboard', label: 'Dashboard', icon: Home },
  { to: '/roadmap', label: 'Roadmap', icon: Map },
  { to: '/notes', label: 'Notes', icon: BookOpen },
  { to: '/quiz', label: 'Quiz', icon: HelpCircle },
  { to: '/tutor', label: 'Tutor', icon: MessageSquare },
];

const progressItems = [
  { label: 'Current Level', value: 'Intermediate', icon: Target },
  { label: 'Weekly Streak', value: '5 days', icon: TrendingUp },
  { label: 'Total XP', value: '420', icon: Trophy },
];

export default function Sidebar(){
  const location = useLocation();

  return (
    <aside className="w-64 bg-white/50 backdrop-blur-sm border-r border-slate-200/70 h-[calc(100vh-76px)] sticky top-[76px] overflow-y-auto">
      {/* Main Navigation */}
      <nav className="p-4">
        <div className="mb-6">
          <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-2">Navigation</h3>
          <div className="space-y-1">
            {mainItems.map((item, index) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.to;

              return (
                <motion.div
                  key={item.to}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <NavLink
                    to={item.to}
                    className={({isActive}) =>
                      `flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                        isActive 
                          ? 'bg-blue-50 text-blue-600 border border-blue-200 shadow-sm' 
                          : 'text-slate-600 hover:text-blue-600 hover:bg-slate-50'
                      }`
                    }
                  >
                    <Icon className="h-4 w-4" />
                    {item.label}
                    {isActive && (
                      <motion.div
                        layoutId="activeTab"
                        className="w-1.5 h-1.5 rounded-full bg-blue-500 ml-auto"
                        initial={false}
                        transition={{ type: "spring", stiffness: 500, damping: 30 }}
                      />
                    )}
                  </NavLink>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Progress Overview */}
        <div>
          <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3 px-2">Progress</h3>
          <div className="space-y-3">
            {progressItems.map((item, index) => {
              const Icon = item.icon;

              return (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                  className="bg-white rounded-lg border border-slate-200 p-3 shadow-sm"
                >
                  <div className="flex items-center gap-2 mb-1">
                    <Icon className="h-3 w-3 text-blue-500" />
                    <span className="text-xs text-slate-500">{item.label}</span>
                  </div>
                  <div className="text-sm font-semibold text-slate-800">{item.value}</div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </nav>
    </aside>
  );
}