import React from 'react';
import AnimatedCard from '../components/AnimatedCard';
import ProgressRing from '../components/ProgressRing';
import {
  Target,
  BookOpen,
  TrendingUp,
  Calendar,
  Award,
  Users,
  Brain,
  BarChart3
} from 'lucide-react';
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1,
    transition: {
      type: "spring",
      stiffness: 300,
      damping: 24
    }
  }
};

export default function Dashboard(){
  const weeklyProgress = [
    { day: 'Mon', completed: 4, total: 5 },
    { day: 'Tue', completed: 5, total: 5 },
    { day: 'Wed', completed: 3, total: 5 },
    { day: 'Thu', completed: 5, total: 5 },
    { day: 'Fri', completed: 2, total: 5 },
    { day: 'Sat', completed: 0, total: 3 },
    { day: 'Sun', completed: 0, total: 3 },
  ];

  return (
    <div className="p-6">
      {/* Welcome Header */}
      <motion.div
        className="mb-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold text-slate-800 mb-2">Welcome back, JAYANTH !!</h1>
        <p className="text-slate-600">Continue your journey to becoming a Full Stack Developer</p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants}>
          <AnimatedCard
            title="Skill Mastery"
            icon={Target}
            gradient="from-blue-500 to-cyan-500"
          >
            <div className="flex justify-center mt-4">
              <ProgressRing progress={65} size={100} />
            </div>
            <p className="text-center text-sm text-slate-600 mt-4">Based on your current progress</p>
          </AnimatedCard>
        </motion.div>

        <motion.div variants={itemVariants}>
          <AnimatedCard
            title="Learning Streak"
            icon={TrendingUp}
            gradient="from-green-500 to-emerald-500"
          >
            <div className="text-center mt-4">
              <div className="text-4xl font-bold text-green-600 mb-2">5</div>
              <p className="text-sm text-slate-600">consecutive days</p>
            </div>
            <div className="flex justify-between mt-4 text-xs text-slate-500">
              {weeklyProgress.map((day, index) => (
                <div key={index} className="text-center">
                  <div className={`w-2 h-2 rounded-full mx-auto mb-1 ${
                    day.completed > 0 ? 'bg-green-500' : 'bg-slate-300'
                  }`}></div>
                  {day.day}
                </div>
              ))}
            </div>
          </AnimatedCard>
        </motion.div>

        <motion.div variants={itemVariants}>
          <AnimatedCard
            title="Courses Completed"
            icon={Award}
            gradient="from-amber-500 to-orange-500"
          >
            <div className="text-center mt-4">
              <div className="text-4xl font-bold text-amber-600 mb-2">12</div>
              <p className="text-sm text-slate-600">of 24 total courses</p>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2 mt-4">
              <div
                className="bg-amber-500 h-2 rounded-full transition-all duration-700"
                style={{ width: '50%' }}
              ></div>
            </div>
          </AnimatedCard>
        </motion.div>

        <motion.div variants={itemVariants}>
          <AnimatedCard
            title="Community Rank"
            icon={Users}
            gradient="from-purple-500 to-pink-500"
          >
            <div className="text-center mt-4">
              <div className="text-4xl font-bold text-purple-600 mb-2">#42</div>
              <p className="text-sm text-slate-600">out of 500 learners</p>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2 mt-4">
              <div
                className="bg-purple-500 h-2 rounded-full"
                style={{ width: '92%' }}
              ></div>
            </div>
          </AnimatedCard>
        </motion.div>
      </motion.div>

      {/* Action Cards */}
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.div variants={itemVariants}>
          <AnimatedCard
            title="Skill Gap Analysis"
            icon={Brain}
            actionLabel="Analyze now"
            gradient="from-indigo-500 to-blue-500"
          >
            <p className="mb-4">Get a tailored skill-gap analysis and course suggestions based on your career goals.</p>
            <div className="flex items-center text-sm text-slate-500">
              <Calendar className="h-4 w-4 mr-1" />
              Last analyzed: 2 days ago
            </div>
          </AnimatedCard>
        </motion.div>

        <motion.div variants={itemVariants}>
          <AnimatedCard
            title="Personalized Roadmap"
            icon={Target}
            actionLabel="View roadmap"
            gradient="from-teal-500 to-green-500"
          >
            <p className="mb-4">Your personalized career roadmap with milestones and recommended learning paths.</p>
            <div className="flex items-center text-sm text-slate-500">
              <TrendingUp className="h-4 w-4 mr-1" />
              65% completion
            </div>
          </AnimatedCard>
        </motion.div>

        <motion.div variants={itemVariants}>
          <AnimatedCard
            title="Progress Analytics"
            icon={BarChart3}
            actionLabel="See details"
            gradient="from-rose-500 to-pink-500"
          >
            <p className="mb-4">Detailed analytics of your learning progress, time spent, and achievement unlocked.</p>
            <div className="flex items-center text-sm text-slate-500">
              <BookOpen className="h-4 w-4 mr-1" />
              24h learned this week
            </div>
          </AnimatedCard>
        </motion.div>
      </motion.div>
    </div>
  );
}