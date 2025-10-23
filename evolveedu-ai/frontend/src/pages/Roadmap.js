import React, { useState } from 'react';
import AnimatedCard from '../components/AnimatedCard';
import {
  Target,
  CheckCircle,
  Circle,
  ChevronDown,
  ChevronRight,
  Star,
  Calendar,
  Clock,
  BookOpen
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Roadmap = () => {
  const [expandedModule, setExpandedModule] = useState(0);

  const careerPath = {
    title: "Full Stack Developer",
    description: "Master both frontend and backend technologies to build complete web applications",
    duration: "6-9 months",
    level: "Intermediate",
    progress: 65,
    modules: [
      {
        title: "HTML & CSS Fundamentals",
        description: "Learn the building blocks of web development",
        duration: "2 weeks",
        progress: 100,
        completed: true,
        lessons: [
          { title: "HTML Structure & Semantics", completed: true, duration: "2h" },
          { title: "CSS Layouts & Flexbox", completed: true, duration: "3h" },
          { title: "Responsive Design", completed: true, duration: "2h" },
        ]
      },
      {
        title: "JavaScript Mastery",
        description: "Master the language of the web",
        duration: "4 weeks",
        progress: 80,
        completed: false,
        lessons: [
          { title: "JavaScript Basics", completed: true, duration: "3h" },
          { title: "DOM Manipulation", completed: true, duration: "4h" },
          { title: "Async JavaScript", completed: true, duration: "3h" },
          { title: "Modern ES6+ Features", completed: false, duration: "3h" },
        ]
      },
      {
        title: "React & Frontend Frameworks",
        description: "Build modern user interfaces",
        duration: "6 weeks",
        progress: 40,
        completed: false,
        lessons: [
          { title: "React Fundamentals", completed: true, duration: "5h" },
          { title: "State Management", completed: true, duration: "4h" },
          { title: "React Router", completed: false, duration: "3h" },
          { title: "Advanced React Patterns", completed: false, duration: "4h" },
        ]
      },
      {
        title: "Backend Development",
        description: "Server-side programming and APIs",
        duration: "8 weeks",
        progress: 20,
        completed: false,
        lessons: [
          { title: "Node.js Fundamentals", completed: true, duration: "4h" },
          { title: "Express.js Framework", completed: false, duration: "5h" },
          { title: "Database Integration", completed: false, duration: "6h" },
          { title: "Authentication & Security", completed: false, duration: "4h" },
        ]
      },
      {
        title: "DevOps & Deployment",
        description: "Deploy and maintain your applications",
        duration: "3 weeks",
        progress: 0,
        completed: false,
        lessons: [
          { title: "Git & Version Control", completed: false, duration: "3h" },
          { title: "CI/CD Pipelines", completed: false, duration: "4h" },
          { title: "Cloud Deployment", completed: false, duration: "5h" },
        ]
      }
    ]
  };

  return (
    <div className="h-full">
      <main className="p-6">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-slate-800 mb-2">Learning Roadmap</h1>
            <p className="text-slate-600">Your personalized path to becoming a {careerPath.title}</p>
          </div>

          {/* Career Path Overview */}
          <AnimatedCard
            title={careerPath.title}
            icon={Target}
            className="mb-8"
            gradient="from-blue-500 to-purple-600"
          >
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
              <div className="flex items-center gap-3">
                <Calendar className="h-5 w-5 text-blue-500" />
                <div>
                  <div className="text-sm text-slate-600">Duration</div>
                  <div className="font-semibold text-slate-800">{careerPath.duration}</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Star className="h-5 w-5 text-amber-500" />
                <div>
                  <div className="text-sm text-slate-600">Level</div>
                  <div className="font-semibold text-slate-800">{careerPath.level}</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <BookOpen className="h-5 w-5 text-green-500" />
                <div>
                  <div className="text-sm text-slate-600">Progress</div>
                  <div className="font-semibold text-slate-800">{careerPath.progress}% Complete</div>
                </div>
              </div>
            </div>
            <p className="mt-4 text-slate-600">{careerPath.description}</p>
          </AnimatedCard>

          {/* Progress Bar */}
          <div className="bg-white rounded-xl p-6 border border-slate-200 shadow-sm mb-8">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-medium text-slate-700">Overall Progress</span>
              <span className="text-sm text-slate-600">{careerPath.progress}%</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-3">
              <div
                className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-700"
                style={{ width: `${careerPath.progress}%` }}
              ></div>
            </div>
          </div>

          {/* Modules List */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-slate-800 mb-4">Learning Modules</h2>

            {careerPath.modules.map((module, index) => (
              <motion.div
                key={index}
                className="bg-white rounded-xl border border-slate-200 overflow-hidden"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                {/* Module Header */}
                <button
                  className="w-full p-6 flex items-center justify-between text-left hover:bg-slate-50 transition-colors"
                  onClick={() => setExpandedModule(expandedModule === index ? null : index)}
                >
                  <div className="flex items-center gap-4">
                    <div className={`p-2 rounded-lg ${
                      module.completed ? 'bg-green-100 text-green-600' : 'bg-blue-100 text-blue-600'
                    }`}>
                      {module.completed ? (
                        <CheckCircle className="h-5 w-5" />
                      ) : (
                        <Target className="h-5 w-5" />
                      )}
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-800">{module.title}</h3>
                      <p className="text-sm text-slate-600">{module.description}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-sm font-medium text-slate-800">{module.duration}</div>
                      <div className="text-xs text-slate-500">{module.progress}% complete</div>
                    </div>
                    {expandedModule === index ? (
                      <ChevronDown className="h-5 w-5 text-slate-400" />
                    ) : (
                      <ChevronRight className="h-5 w-5 text-slate-400" />
                    )}
                  </div>
                </button>

                {/* Module Content */}
                <AnimatePresence>
                  {expandedModule === index && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="border-t border-slate-200"
                    >
                      <div className="p-6">
                        {/* Progress Bar */}
                        <div className="mb-6">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm text-slate-600">Module Progress</span>
                            <span className="text-sm font-medium text-slate-800">{module.progress}%</span>
                          </div>
                          <div className="w-full bg-slate-200 rounded-full h-2">
                            <div
                              className="bg-blue-500 h-2 rounded-full transition-all duration-700"
                              style={{ width: `${module.progress}%` }}
                            ></div>
                          </div>
                        </div>

                        {/* Lessons List */}
                        <div className="space-y-3">
                          <h4 className="font-medium text-slate-800 mb-3">Lessons</h4>
                          {module.lessons.map((lesson, lessonIndex) => (
                            <div
                              key={lessonIndex}
                              className="flex items-center justify-between p-3 rounded-lg bg-slate-50"
                            >
                              <div className="flex items-center gap-3">
                                {lesson.completed ? (
                                  <CheckCircle className="h-4 w-4 text-green-500" />
                                ) : (
                                  <Circle className="h-4 w-4 text-slate-400" />
                                )}
                                <span className={`text-sm ${
                                  lesson.completed ? 'text-slate-600 line-through' : 'text-slate-800'
                                }`}>
                                  {lesson.title}
                                </span>
                              </div>
                              <div className="flex items-center gap-2 text-slate-500">
                                <Clock className="h-3 w-3" />
                                <span className="text-xs">{lesson.duration}</span>
                              </div>
                            </div>
                          ))}
                        </div>

                        {/* Action Button */}
                        {!module.completed && (
                          <button className="w-full mt-6 bg-blue-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-600 transition-colors">
                            {module.progress > 0 ? 'Continue Learning' : 'Start Module'}
                          </button>
                        )}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            ))}
          </div>
        </main>
      </div>
  );
};

export default Roadmap;