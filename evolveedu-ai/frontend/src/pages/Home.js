```jsx
import React, { useState, useEffect } from 'react';
import { Brain, Target, TrendingUp, Sparkles, ArrowRight, Play } from 'lucide-react';

const Home = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [activeFeature, setActiveFeature] = useState(0);

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % 3);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    { icon: Target, title: 'Personalized Learning', desc: 'AI-crafted roadmaps for your dream career' },
    { icon: Brain, title: 'Smart Analysis', desc: 'Identify skill gaps with precision AI insights' },
    { icon: TrendingUp, title: 'Gamified Progress', desc: 'Track growth with engaging milestones' },
  ];

  const stats = [
    { number: '10K+', label: 'Students Guided' },
    { number: '500+', label: 'Career Paths' },
    { number: '95%', label: 'Success Rate' },
    { number: '24/7', label: 'AI Support' },
  ];

  return (
    <div className="bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-y-auto">
      <div className="relative z-10 min-h-screen">
        {/* Hero Section */}
        <section className="relative pt-20 pb-32 px-4">
          <div className="max-w-7xl mx-auto">
            <div
              className={`text-center transform transition-all duration-1000 ${
                isVisible ? 'translate-y-0 opacity-100' : 'translate-y-20 opacity-0'
              }`}
            >
              <div className="inline-flex items-center bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 rounded-full px-6 py-3 mb-8">
                <Sparkles className="w-4 h-4 mr-2 text-purple-400" />
                <span className="text-sm font-medium text-purple-200">Powered by Advanced AI Technology</span>
              </div>

              <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent">
                EvolvEd AI
              </h1>

              <p className="text-xl md:text-2xl text-gray-300 mb-4 max-w-4xl mx-auto leading-relaxed">
                Your Intelligent Student Assistant for Career Success
              </p>

              <p className="text-lg text-gray-400 mb-12 max-w-3xl mx-auto">
                Transform your learning journey with AI-powered personalized roadmaps, skill gap analysis, and real-time
                tutoring. Achieve your career goals faster than ever before.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
                <button className="group bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-8 py-4 rounded-full font-semibold transition-all duration-300 transform hover:scale-105 hover:shadow-2xl flex items-center">
                  Get Started Free
                  <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                </button>

                <button className="group flex items-center bg-white/10 backdrop-blur-sm border border-white/20 hover:bg-white/20 px-8 py-4 rounded-full font-semibold transition-all duration-300">
                  <Play className="w-5 h-5 mr-2" />
                  Watch Demo
                </button>
              </div>
            </div>

            {/* Feature Highlights */}
            <div className="grid md:grid-cols-3 gap-8 mb-20">
              {features.map((feature, index) => {
                const Icon = feature.icon;
                return (
                  <div
                    key={index}
                    className={`relative bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-8 transition-all duration-500 hover:bg-white/20 hover:scale-105 ${
                      activeFeature === index ? 'ring-2 ring-purple-500 bg-white/20' : ''
                    }`}
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-purple-500/10 to-blue-500/10 rounded-2xl" />
                    <div className="relative">
                      <div className="bg-gradient-to-br from-purple-500 to-blue-500 w-16 h-16 rounded-xl flex items-center justify-center mb-6">
                        <Icon className="w-8 h-8 text-white" />
                      </div>
                      <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                      <p className="text-gray-300">{feature.desc}</p>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Stats Section */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 bg-white/10 backdrop-blur-sm border border-white/20 rounded-3xl p-8">
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold text-transparent bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text mb-2">
                    {stat.number}
                  </div>
                  <div className="text-gray-300 text-sm md:text-base">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* How It Works Section */}
        <section className="py-20 px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-6">How It Works</h2>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto">
                Our AI-powered platform guides you through every step of your learning journey
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-12">
              <div className="text-center group">
                <div className="bg-gradient-to-br from-purple-600 to-blue-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Target className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-4">1. Set Your Goal</h3>
                <p className="text-gray-300">
                  Tell us your dream career and our AI analyzes thousands of job requirements to create your perfect
                  learning path.
                </p>
              </div>

              <div className="text-center group">
                <div className="bg-gradient-to-br from-purple-600 to-blue-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  <Brain className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-4">2. Analyze Skills</h3>
                <p className="text-gray-300">
                  Our Skill Gap Analyzer identifies exactly what you need to learn and recommends the best resources.
                </p>
              </div>

              <div className="text-center group">
                <div className="bg-gradient-to-br from-purple-600 to-blue-600 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
                  <TrendingUp className="w-10 h-10 text-white" />
                </div>
                <h3 className="text-2xl font-bold mb-4">3. Track Progress</h3>
                <p className="text-gray-300">
                  Monitor your growth with gamified dashboards and get real-time support from our AI tutor.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4">
          <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-purple-600/20 to-blue-600/20 backdrop-blur-sm border border-white/20 rounded-3xl p-12">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to Transform Your Future?</h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of students who are already using AI to accelerate their careers
            </p>
            <button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-10 py-4 rounded-full text-lg font-semibold transition-all duration-300 transform hover:scale-105 hover:shadow-2xl">
              Start Your Journey Today
            </button>
          </div>
        </section>

        {/* Footer */}
        <footer className="border-t border-white/10 py-8 px-4 text-center text-gray-400">
          <div className="max-w-6xl mx-auto">
            <p>© 2024 EvolvEd AI. All rights reserved. Built with React & Django.</p>
            <p className="text-sm mt-2">Empowering students through intelligent learning technology.</p>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default Home;
```