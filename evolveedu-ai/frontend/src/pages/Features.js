import React, { useState, useEffect } from 'react';
import {
  Brain,
  Target,
  MessageSquare,
  FileText,
  Trophy,
  Settings,
  Sparkles,
  Zap,
  BookOpen,
  ChevronRight,
  CheckCircle,
  ArrowRight,
  Users,
  Clock,
  Star,
  TrendingUp,
  Search,
  Database
} from 'lucide-react';

const Features = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const mainFeatures = [
    {
      id: 'roadmaps',
      icon: Target,
      title: 'Personalized Learning Roadmaps',
      description: 'AI-powered career guidance that creates customized learning paths tailored to your specific career goals.',
      details: [
        'Analyze 1000+ career paths with real job market data',
        'Generate step-by-step learning sequences',
        'Recommend specific courses, certifications, and projects',
        'Adapt to your learning speed and preferences',
        'Integration with top learning platforms'
      ],
      color: 'from-purple-500 to-pink-500',
      bgColor: 'from-purple-500/20 to-pink-500/20'
    },
    {
      id: 'analyzer',
      icon: Brain,
      title: 'Skill Gap Analyzer',
      description: 'Advanced AI algorithms that identify exactly what skills you need to develop for your target career.',
      details: [
        'Real-time job market analysis and trends',
        'Compare your current skills with industry requirements',
        'Prioritize skills by importance and demand',
        'Track skill development progress over time',
        'Benchmark against industry professionals'
      ],
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'from-blue-500/20 to-cyan-500/20'
    },
    {
      id: 'tutor',
      icon: MessageSquare,
      title: 'Q&A AI Tutor',
      description: 'Get instant, intelligent answers to your study questions with our 24/7 AI-powered tutoring system.',
      details: [
        'Natural language processing for complex questions',
        'Context-aware responses based on your learning path',
        'Multi-subject expertise across various domains',
        'Interactive problem-solving sessions',
        'Learning history tracking for personalized help'
      ],
      color: 'from-green-500 to-emerald-500',
      bgColor: 'from-green-500/20 to-emerald-500/20'
    },
    {
      id: 'summarizer',
      icon: FileText,
      title: 'All-in-One Summarizer',
      description: 'Transform lengthy study materials into concise, actionable summaries with AI-powered content analysis.',
      details: [
        'Process PDFs, videos, articles, and textbooks',
        'Extract key concepts and main points',
        'Generate visual mind maps and diagrams',
        'Create flashcards and quiz questions',
        'Multi-format export options'
      ],
      color: 'from-orange-500 to-red-500',
      bgColor: 'from-orange-500/20 to-red-500/20'
    },
    {
      id: 'dashboard',
      icon: Trophy,
      title: 'Gamified Progress Dashboard',
      description: 'Stay motivated with engaging progress tracking, achievements, and gamification elements.',
      details: [
        'Visual progress tracking with milestones',
        'Achievement badges and reward systems',
        'Leaderboards and social learning features',
        'Daily challenges and learning streaks',
        'Comprehensive analytics and insights'
      ],
      color: 'from-indigo-500 to-purple-500',
      bgColor: 'from-indigo-500/20 to-purple-500/20'
    },
    {
      id: 'management',
      icon: Database,
      title: 'Django Admin Management',
      description: 'Robust backend system for managing student profiles, roadmaps, and learning analytics.',
      details: [
        'Comprehensive student profile management',
        'Course and roadmap content management',
        'Advanced analytics and reporting',
        'User role and permission management',
        'System monitoring and maintenance tools'
      ],
      color: 'from-teal-500 to-blue-500',
      bgColor: 'from-teal-500/20 to-blue-500/20'
    }
  ];

  const benefits = [
    { icon: Clock, title: 'Save 60% Learning Time', desc: 'Focused learning paths eliminate unnecessary content' },
    { icon: Target, title: '95% Career Match Rate', desc: 'AI ensures perfect alignment with career goals' },
    { icon: Users, title: 'Community Learning', desc: 'Connect with peers on similar learning journeys' },
    { icon: TrendingUp, title: 'Real-time Updates', desc: 'Content stays current with industry trends' }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
      </div>

      {/* Header Section */}
      <section className="relative pt-20 pb-16 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <div className={`transform transition-all duration-1000 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-20 opacity-0'}`}>
            <div className="inline-flex items-center bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 rounded-full px-6 py-3 mb-8">
              <Sparkles className="w-4 h-4 mr-2 text-purple-400" />
              <span className="text-sm font-medium text-purple-200">Advanced AI-Powered Features</span>
            </div>

            <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent">
              Powerful Features
            </h1>

            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Discover how EvolvEd AI transforms your learning experience with cutting-edge artificial intelligence and personalized guidance.
            </p>
          </div>
        </div>
      </section>

      {/* Main Features */}
      <section className="py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid gap-12">
            {mainFeatures.map((feature, index) => {
              const Icon = feature.icon;
              const isEven = index % 2 === 0;

              return (
                <div key={feature.id} className="group">
                  <div className={`grid lg:grid-cols-2 gap-12 items-center ${!isEven ? 'lg:grid-flow-col-dense' : ''}`}>
                    {/* Content */}
                    <div className={`${!isEven ? 'lg:col-start-2' : ''}`}>
                      <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-8 group-hover:bg-white/10 transition-all duration-500">
                        <div className={`bg-gradient-to-r ${feature.color} w-16 h-16 rounded-xl flex items-center justify-center mb-6`}>
                          <Icon className="w-8 h-8 text-white" />
                        </div>

                        <h3 className="text-3xl font-bold mb-4">{feature.title}</h3>
                        <p className="text-gray-300 text-lg mb-6">{feature.description}</p>

                        <div className="space-y-3">
                          {feature.details.map((detail, idx) => (
                            <div key={idx} className="flex items-start">
                              <CheckCircle className="w-5 h-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                              <span className="text-gray-200">{detail}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Visual */}
                    <div className={`${!isEven ? 'lg:col-start-1' : ''}`}>
                      <div className={`relative bg-gradient-to-br ${feature.bgColor} backdrop-blur-sm border border-white/20 rounded-3xl p-8 h-80 flex items-center justify-center group-hover:scale-105 transition-all duration-500`}>
                        <div className="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent rounded-3xl"></div>
                        <Icon className={`w-32 h-32 text-white/80`} />
                        <div className="absolute top-4 right-4">
                          <Zap className="w-6 h-6 text-yellow-400 animate-pulse" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-purple-900/50 to-blue-900/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Why Choose EvolvEd AI?</h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Experience the benefits of AI-powered learning that adapts to your unique needs and goals
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => {
              const Icon = benefit.icon;
              return (
                <div key={index} className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 text-center group hover:bg-white/20 transition-all duration-300 hover:scale-105">
                  <div className="bg-gradient-to-br from-purple-500 to-blue-500 w-16 h-16 rounded-xl flex items-center justify-center mx-auto mb-4">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-lg font-bold mb-2">{benefit.title}</h3>
                  <p className="text-gray-300 text-sm">{benefit.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-8">Built with Modern Technology</h2>
          <p className="text-xl text-gray-300 mb-12">
            EvolvEd AI leverages cutting-edge technologies to deliver a seamless learning experience
          </p>

          <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-3xl p-8">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-4xl mb-4">⚛️</div>
                <h3 className="text-xl font-bold mb-2">React Frontend</h3>
                <p className="text-gray-300">Modern, responsive user interface</p>
              </div>
              <div className="text-center">
                <div className="text-4xl mb-4">🐍</div>
                <h3 className="text-xl font-bold mb-2">Django Backend</h3>
                <p className="text-gray-300">Robust, scalable server architecture</p>
              </div>
              <div className="text-center">
                <div className="text-4xl mb-4">🤖</div>
                <h3 className="text-xl font-bold mb-2">AI Integration</h3>
                <p className="text-gray-300">Advanced machine learning algorithms</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-purple-600/20 to-blue-600/20 backdrop-blur-sm border border-white/20 rounded-3xl p-12">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Experience the Future of Learning
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Join thousands of students already using AI to accelerate their career success
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-8 py-4 rounded-full font-semibold transition-all duration-300 transform hover:scale-105 hover:shadow-2xl flex items-center justify-center">
              Start Free Trial
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
            <button className="bg-white/10 backdrop-blur-sm border border-white/20 hover:bg-white/20 px-8 py-4 rounded-full font-semibold transition-all duration-300">
              Schedule Demo
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-8 px-4 text-center text-gray-400">
        <div className="max-w-6xl mx-auto">
          <p>© 2024 EvolvEd AI. All rights reserved. Built with React & Django.</p>
          <p className="text-sm mt-2">Revolutionizing education through artificial intelligence and personalized learning.</p>
        </div>
      </footer>
    </div>
  );
};

export default Features;
