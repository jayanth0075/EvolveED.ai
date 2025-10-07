import React, { useState, useEffect } from 'react';
import {
  Target,
  Globe,
  Sparkles,
  Brain,
  Github,
  Linkedin,
  Mail,
  ArrowRight,
  Code,
  Zap,
  Rocket,
  Eye,
  Layers
} from 'lucide-react';

const About = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [activeValue, setActiveValue] = useState(0);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setActiveValue(prev => (prev + 1) % 4);
    }, 4000);

    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      clearInterval(interval);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  const values = [
    {
      icon: Brain,
      title: 'AI-First Innovation',
      description: 'Pioneering the future of education through advanced artificial intelligence and machine learning.',
      color: 'from-cyan-500 via-blue-500 to-purple-600',
      glow: 'shadow-cyan-500/25'
    },
    {
      icon: Eye,
      title: 'Vision-Driven',
      description: 'Creating intelligent systems that understand and adapt to each learner\'s unique journey.',
      color: 'from-purple-500 via-pink-500 to-red-500',
      glow: 'shadow-purple-500/25'
    },
    {
      icon: Rocket,
      title: 'Future-Ready',
      description: 'Building tomorrow\'s learning platform today with cutting-edge technology and innovation.',
      color: 'from-emerald-500 via-teal-500 to-cyan-500',
      glow: 'shadow-emerald-500/25'
    },
    {
      icon: Layers,
      title: 'Excellence',
      description: 'Committed to delivering exceptional user experiences through thoughtful design and robust engineering.',
      color: 'from-orange-500 via-yellow-500 to-red-500',
      glow: 'shadow-orange-500/25'
    }
  ];

  const team = [
    {
      name: 'A. Jayanth',
      role: 'Lead Developer & Co-founder',
      expertise: 'Full-Stack Development, AI Integration',
      gradient: 'from-cyan-400 to-blue-600',
      icon: Code
    },
    {
      name: 'Divij Mazumdar',
      role: 'AI Engineer & Co-founder',
      expertise: 'Machine Learning, Data Science',
      gradient: 'from-purple-400 to-pink-600',
      icon: Brain
    },
    {
      name: 'Kumbhar Kiran',
      role: 'Product Developer & Co-founder',
      expertise: 'Product Design, User Experience',
      gradient: 'from-emerald-400 to-teal-600',
      icon: Layers
    }
  ];

  const technologies = [
    { name: 'React', icon: '⚛️', desc: 'Modern Frontend Framework' },
    { name: 'Django', icon: '🐍', desc: 'Robust Backend Architecture' },
    { name: 'AI/ML', icon: '🤖', desc: 'Advanced Intelligence Systems' },
    { name: 'PostgreSQL', icon: '🐘', desc: 'Scalable Database Solution' },
    { name: 'TensorFlow', icon: '🧠', desc: 'Deep Learning Platform' },
    { name: 'Docker', icon: '🐳', desc: 'Containerized Deployment' }
  ];

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Dynamic Background */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-black via-gray-900 to-black"></div>
        <div
          className="absolute w-96 h-96 rounded-full opacity-20 blur-3xl transition-all duration-1000"
          style={{
            background: 'linear-gradient(45deg, #06b6d4, #8b5cf6, #ec4899)',
            left: mousePosition.x - 200,
            top: mousePosition.y - 200,
          }}
        ></div>
        <div className="absolute top-20 right-20 w-72 h-72 bg-gradient-to-r from-purple-600/10 to-cyan-600/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-20 left-20 w-80 h-80 bg-gradient-to-r from-emerald-600/10 to-blue-600/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Floating Elements */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-white/20 rounded-full animate-ping"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animationDelay: `${Math.random() * 5}s`,
              animationDuration: `${2 + Math.random() * 3}s`
            }}
          ></div>
        ))}
      </div>

      {/* Hero Section */}
      <section className="relative z-10 pt-24 pb-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className={`text-center transform transition-all duration-1500 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-20 opacity-0'}`}>
            <div className="inline-flex items-center bg-gradient-to-r from-cyan-500/20 to-purple-500/20 backdrop-blur-xl border border-white/10 rounded-full px-8 py-4 mb-8 shadow-2xl">
              <Sparkles className="w-5 h-5 mr-3 text-cyan-400 animate-pulse" />
              <span className="text-sm font-semibold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                The Future of AI-Powered Education
              </span>
            </div>

            <h1 className="text-6xl md:text-8xl font-black mb-8 leading-tight">
              <span className="bg-gradient-to-r from-white via-cyan-200 to-purple-200 bg-clip-text text-transparent">
                About
              </span>
              <br />
              <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                EvolvEd AI
              </span>
            </h1>

            <p className="text-2xl md:text-3xl text-gray-300 mb-6 max-w-5xl mx-auto leading-relaxed font-light">
              Revolutionizing education through intelligent technology
            </p>

            <p className="text-lg text-gray-400 max-w-4xl mx-auto leading-relaxed">
              Where artificial intelligence meets personalized learning to create extraordinary educational experiences
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="relative z-10 py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <div className="space-y-8">
              <div className="inline-block">
                <h2 className="text-5xl md:text-6xl font-black mb-2">
                  <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                    Our Mission
                  </span>
                </h2>
                <div className="h-1 w-32 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full"></div>
              </div>

              <p className="text-xl text-gray-300 leading-relaxed">
                We envision a world where every learner has access to intelligent, personalized education that adapts to their unique needs, goals, and learning style.
              </p>

              <p className="text-lg text-gray-400 leading-relaxed">
                EvolvEd AI breaks down traditional barriers in education by leveraging cutting-edge artificial intelligence to create dynamic learning experiences that evolve with each student's journey.
              </p>

              <div className="space-y-6">
                <div className="flex items-start group">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                    <Target className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white mb-2">Precision Learning</h3>
                    <p className="text-gray-400">AI-driven insights that identify exactly what you need to learn and when</p>
                  </div>
                </div>

                <div className="flex items-start group">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                    <Rocket className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white mb-2">Accelerated Growth</h3>
                    <p className="text-gray-400">Transform your career trajectory with intelligent guidance and support</p>
                  </div>
                </div>

                <div className="flex items-start group">
                  <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl flex items-center justify-center mr-4 group-hover:scale-110 transition-transform duration-300">
                    <Globe className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-xl font-bold text-white mb-2">Global Accessibility</h3>
                    <p className="text-gray-400">Breaking down geographical and economic barriers to quality education</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-3xl blur-xl"></div>
              <div className="relative bg-black/40 backdrop-blur-2xl border border-white/10 rounded-3xl p-12 shadow-2xl">
                <div className="text-center space-y-8">
                  <div className="relative">
                    <div className="w-24 h-24 mx-auto mb-6 relative">
                      <div className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full animate-spin" style={{animationDuration: '3s'}}></div>
                      <div className="absolute inset-1 bg-black rounded-full flex items-center justify-center">
                        <Brain className="w-10 h-10 text-white" />
                      </div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent mb-4">
                      AI-Powered Intelligence
                    </h3>
                    <p className="text-gray-300 leading-relaxed">
                      Advanced algorithms that understand your learning patterns, preferences, and goals to create the perfect educational experience.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="relative z-10 py-24 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-black mb-4">
              <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                Our Values
              </span>
            </h2>
            <div className="h-1 w-32 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full mx-auto mb-8"></div>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              The core principles that drive every decision and shape the future of intelligent education
            </p>
          </div>

          <div className="grid lg:grid-cols-4 gap-8">
            {values.map((value, index) => {
              const Icon = value.icon;
              const isActive = activeValue === index;
              return (
                <div
                  key={index}
                  className={`relative group transition-all duration-700 ${
                    isActive ? 'transform scale-105' : ''
                  }`}
                >
                  <div className={`absolute inset-0 bg-gradient-to-r ${value.color} opacity-20 rounded-3xl blur-xl transition-all duration-700 ${
                    isActive ? 'opacity-40 scale-110' : 'opacity-20'
                  }`}></div>

                  <div className="relative bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-8 h-full group-hover:bg-black/40 transition-all duration-500">
                    <div className="text-center space-y-6">
                      <div className={`w-16 h-16 mx-auto bg-gradient-to-r ${value.color} rounded-2xl flex items-center justify-center shadow-2xl ${value.glow} group-hover:scale-110 transition-transform duration-300`}>
                        <Icon className="w-8 h-8 text-white" />
                      </div>

                      <h3 className="text-2xl font-bold text-white">{value.title}</h3>
                      <p className="text-gray-300 leading-relaxed">{value.description}</p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="relative z-10 py-24 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-20">
            <h2 className="text-5xl md:text-6xl font-black mb-4">
              <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                Meet the Visionaries
              </span>
            </h2>
            <div className="h-1 w-32 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full mx-auto mb-8"></div>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              The brilliant minds behind EvolvEd AI, united by a passion for transforming education through technology
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {team.map((member, index) => {
              const Icon = member.icon;
              return (
                <div key={index} className="group relative">
                  <div className={`absolute inset-0 bg-gradient-to-r ${member.gradient} opacity-20 rounded-3xl blur-xl group-hover:opacity-40 transition-all duration-500`}></div>

                  <div className="relative bg-black/60 backdrop-blur-xl border border-white/10 rounded-3xl p-8 text-center group-hover:bg-black/40 transition-all duration-500 group-hover:scale-105">
                    <div className="space-y-6">
                      <div className="relative">
                        <div className={`w-20 h-20 mx-auto bg-gradient-to-r ${member.gradient} rounded-2xl flex items-center justify-center shadow-2xl group-hover:scale-110 transition-transform duration-300`}>
                          <Icon className="w-10 h-10 text-white" />
                        </div>
                      </div>

                      <div>
                        <h3 className="text-2xl font-bold text-white mb-2">{member.name}</h3>
                        <p className={`text-lg font-semibold bg-gradient-to-r ${member.gradient} bg-clip-text text-transparent mb-3`}>
                          {member.role}
                        </p>
                        <p className="text-gray-300 text-sm leading-relaxed">{member.expertise}</p>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Vision Section */}
      <section className="relative z-10 py-24 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-purple-500/10 rounded-3xl blur-2xl"></div>

            <div className="relative bg-black/40 backdrop-blur-2xl border border-white/10 rounded-3xl p-12 text-center">
              <div className="space-y-8">
                <div className="inline-block">
                  <Zap className="w-16 h-16 text-cyan-400 mx-auto mb-6 animate-pulse" />
                </div>

                <h2 className="text-4xl md:text-5xl font-black">
                  <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                    The Future is Here
                  </span>
                </h2>

                <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
                  We're not just building an educational platform – we're crafting the future of human learning.
                  Every algorithm, every feature, every interaction is designed to unlock human potential in ways never before possible.
                </p>

                <div className="pt-8">
                  <button className="group bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 px-10 py-4 rounded-full text-lg font-bold transition-all duration-300 transform hover:scale-105 hover:shadow-2xl flex items-center mx-auto">
                    Join the Revolution
                    <ArrowRight className="w-6 h-6 ml-3 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center space-y-8">
            <div>
              <h3 className="text-3xl font-black mb-2">
                <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                  EvolvEd AI
                </span>
              </h3>
              <p className="text-gray-400 text-lg">Transforming education through artificial intelligence</p>
            </div>

            <div className="flex justify-center space-x-8">
              <Github className="w-8 h-8 text-gray-400 hover:text-cyan-400 cursor-pointer transition-all duration-300 hover:scale-110" />
              <Linkedin className="w-8 h-8 text-gray-400 hover:text-purple-400 cursor-pointer transition-all duration-300 hover:scale-110" />
              <Mail className="w-8 h-8 text-gray-400 hover:text-pink-400 cursor-pointer transition-all duration-300 hover:scale-110" />
            </div>

            <div className="border-t border-white/10 pt-8 space-y-4">
              <p className="text-gray-400">© 2024 EvolvEd AI. All rights reserved.</p>
              <p className="text-sm text-gray-500">
                Built with React & Django | Designed with ❤️ for the future of education
              </p>
              <p className="text-xs text-gray-600">
                Privacy Policy | Terms of Service | Cookie Policy | Accessibility Statement
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default About;