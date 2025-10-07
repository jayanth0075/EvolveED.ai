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
  Target,
  Calendar,
  Award,
  CalendarDays
} from 'lucide-react';
import { motion } from 'framer-motion';

const mainItems = [
  { to: '/dashboard', label: 'Dashboard', icon: Home },
  { to: '/roadmap', label: 'Roadmap', icon: Map },
  { to: '/notes', label: 'Notes', icon: BookOpen },
  { to: '/quiz', label: 'Quiz', icon: HelpCircle },
  { to: '/tutor', label: 'Tutor', icon: MessageSquare },
  { to: '/planner', label: 'Planner', icon: CalendarDays },
];

const progressItems = [
  {
    label: 'Current Level',
    value: 'Intermediate',
    icon: Target,
    color: 'text-blue-500',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200'
  },
  {
    label: 'Weekly Streak',
    value: '5 days',
    icon: TrendingUp,
    color: 'text-green-500',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200'
  },
  {
    label: 'Total XP',
    value: '420',
    icon: Trophy,
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-200'
  },
  {
    label: 'Achievements',
    value: '12',
    icon: Award,
    color: 'text-purple-500',
    bgColor: 'bg-purple-50',
    borderColor: 'border-purple-200'
  },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 bg-white/60 backdrop-blur-sm border-r border-slate-200/70 h-[calc(100vh-76px)] sticky top-[76px] overflow-y-auto">
      <div className="p-4">
        {/* Main Navigation */}
        <div className="mb-8">
          <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4 px-2">
            Navigation
          </h3>
          <div className="space-y-1">
            {mainItems.map((item, index) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.to;

              return (
                <motion.div
                  key={item.to}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05, duration: 0.3 }}
                >
                  <NavLink
                    to={item.to}
                    className={({ isActive }) =>
                      `relative flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                        isActive 
                          ? 'bg-blue-50 text-blue-600 border border-blue-200 shadow-sm' 
                          : 'text-slate-600 hover:text-blue-600 hover:bg-slate-50'
                      }`
                    }
                  >
                    <Icon className="h-4 w-4 flex-shrink-0" />
                    <span className="flex-1">{item.label}</span>
                    {isActive && (
                      <motion.div
                        layoutId="sidebarActiveTab"
                        className="w-2 h-2 rounded-full bg-blue-500"
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
          <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-4 px-2">
            Your Progress
          </h3>
          <div className="space-y-3">
            {progressItems.map((item, index) => {
              const Icon = item.icon;

              return (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + index * 0.1, duration: 0.3 }}
                  className={`${item.bgColor} rounded-lg border ${item.borderColor} p-3 shadow-sm hover:shadow-md transition-shadow duration-200`}
                >
                  <div className="flex items-center gap-2 mb-1">
                    <Icon className={`h-3.5 w-3.5 ${item.color} flex-shrink-0`} />
                    <span className="text-xs text-slate-600 font-medium">{item.label}</span>
                  </div>
                  <div className="text-sm font-bold text-slate-800 ml-5">{item.value}</div>
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="mt-8 p-4 bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg border border-slate-200">
          <h4 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            This Week
          </h4>
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-600">Study Time</span>
              <span className="font-semibold text-slate-800">8.5 hrs</span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-600">Quizzes Completed</span>
              <span className="font-semibold text-slate-800">12</span>
            </div>
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-600">Notes Created</span>
              <span className="font-semibold text-slate-800">7</span>
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}