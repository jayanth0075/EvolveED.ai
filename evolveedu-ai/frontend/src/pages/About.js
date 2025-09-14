import React, { useState, useEffect } from 'react';
import {
  Heart,
  Target,
  Users,
  Lightbulb,
  Award,
  Globe,
  Sparkles,
  Brain,
  TrendingUp,
  Shield,
  Clock,
  Star,
  CheckCircle,
  Quote,
  Github,
  Linkedin,
  Mail,
  ArrowRight
} from 'lucide-react';

const About = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [activeValue, setActiveValue] = useState(0);

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setActiveValue(prev => (prev + 1) % 4);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const values = [
    {
      icon: Heart,
      title: 'Student-Centric',
      description: 'Every decision we make prioritizes student success and learning outcomes.',
      color: 'from-red-500 to-pink-500'
    },
    {
      icon: Brain,
      title: 'AI-Powered Innovation',
      description: 'Leveraging cutting-edge AI to personalize and optimize the learning experience.',
      color: 'from-purple-500 to-indigo-500'
    },
    {
      icon: Globe,
      title: 'Accessibility',
      description: 'Making quality education accessible to learners worldwide, regardless of background.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: TrendingUp,
      title: 'Continuous Improvement',
      description: 'Constantly evolving our platform based on user feedback and technological advances.',
      color: 'from-green-500 to-emerald-500'
    }
  ];

  const stats = [
    { number: '10,000+', label: 'Students Served', icon: Users },
    { number: '500+', label: 'Career Paths', icon: Target },
    { number: '95%', label: 'Success Rate', icon: Award },
    { number: '24/7', label: 'AI Support', icon: Clock }
  ];

  const timeline = [
    {
      year: '2023',
      title: 'The Vision',
      description: 'Recognized the gap between traditional education and modern career requirements. Started developing AI-powered solutions.'
    },
    {
      year: '2024',
      title: 'Platform Development',
      description: 'Built the core AI algorithms for personalized learning and skill gap analysis using React and Django.'
    },
    {
      year: '2024',
      title: 'Beta Launch',
      description: 'Launched beta version with 1,000 students. Achieved 95% satisfaction rate and refined the platform.'
    },
    {
      year: 'Present',
      title: 'Scaling Impact',
      description: 'Serving 10,000+ students globally with continuous platform improvements and new feature releases.'
    }
  ];

  const team = [
    {
      name: 'Dr. Sarah Chen',
      role: 'CEO & Co-founder',
      bio: 'Former Google AI researcher with 10+ years in educational technology.',
      image: '👩‍💼'
    },
    {
      name: 'Mike Rodriguez',
      role: 'CTO & Co-founder',
      bio: 'Full-stack engineer specializing in AI/ML systems and scalable web applications.',
      image: '👨‍💻'
    },
    {
      name: 'Dr. Priya Patel',
      role: 'Head of AI Research',
      bio: 'PhD in Machine Learning with expertise in natural language processing and personalization.',
      image: '👩‍🔬'
    },
    {
      name: 'Alex Kim',
      role: 'Head of Product',
      bio: 'Former startup founder with deep understanding of student needs and market dynamics.',
      image: '👨‍🎓'
    }
  ];

  const testimonials = [
    {
      quote: "EvolvEd AI transformed my career journey. The personalized roadmap helped me land my dream job in just 6 months!",
      author: "Jessica Wong",
      role: "Software Engineer at Meta",
      rating: 5
    },
    {
      quote: "The skill gap analyzer was a game-changer. It showed me exactly what I was missing and how to fill those gaps efficiently.",
      author: "Carlos Martinez",
      role: "Data Scientist at Netflix",
      rating: 5
    },
    {
      quote: "As a working parent, the AI tutor's 24/7 availability meant I could learn at my own pace. Incredible platform!",
      author: "Aisha Johnson",
      role: "Product Manager at Spotify",
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse delay-500"></div>
      </div>

      {/* Hero Section */}
      <section className="relative pt-20 pb-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className={`text-center transform transition-all duration-1000 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-20 opacity-0'}`}>
            <div className="inline-flex items-center bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 rounded-full px-6 py-3 mb-8">
              <Sparkles className="w-4 h-4 mr-2 text-purple-400" />
              <span className="text-sm font-medium text-purple-200">Our Story & Mission</span>
            </div>

            <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent">
              About EvolvEd AI
            </h1>

            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto leading-relaxed">
              Empowering the next generation of learners through intelligent, personalized education technology
            </p>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 bg-white/10 backdrop-blur-sm border border-white/20 rounded-3xl p-8 mt-16">
            {stats.map((stat, index) => {
              const Icon = stat.icon;
              return (
                <div key={index} className="text-center">
                  <Icon className="w-8 h-8 text-purple-400 mx-auto mb-4" />
                  <div className="text-3xl md:text-4xl font-bold text-transparent bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text mb-2">
                    {stat.number}
                  </div>
                  <div className="text-gray-300 text-sm md:text-base">{stat.label}</div>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold mb-6">Our Mission</h2>
              <p className="text-lg text-gray-300 mb-6 leading-relaxed">
                At EvolvEd AI, we believe that every student deserves personalized guidance to achieve their career dreams.
                Traditional education systems often fail to bridge the gap between academic learning and real-world career requirements.
              </p>
              <p className="text-lg text-gray-300 mb-8 leading-relaxed">
                We're revolutionizing education by leveraging artificial intelligence to create personalized learning experiences
                that adapt to each student's unique goals, learning style, and pace. Our platform doesn't just teach - it guides,
                analyzes, and evolves with every learner.
              </p>
              <div className="space-y-4">
                <div className="flex items-start">
                  <CheckCircle className="w-6 h-6 text-green-400 mr-3 mt-1 flex-shrink-0" />
                  <span className="text-gray-200">Democratize access to personalized career guidance</span>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="w-6 h-6 text-green-400 mr-3 mt-1 flex-shrink-0" />
                  <span className="text-gray-200">Bridge the skills gap in today's job market</span>
                </div>
                <div className="flex items-start">
                  <CheckCircle className="w-6 h-6 text-green-400 mr-3 mt-1 flex-shrink-0" />
                  <span className="text-gray-200">Empower students to achieve their career aspirations</span>
                </div>
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-purple-600/20 to-blue-600/20 backdrop-blur-sm border border-white/20 rounded-3xl p-8 h-96 flex items-center justify-center">
                <div className="text-center">
                  <Target className="w-24 h-24 text-purple-400 mx-auto mb-6" />
                  <h3 className="text-2xl font-bold mb-4">Guiding 10,000+ Students</h3>
                  <p className="text-gray-300">Towards their dream careers with AI-powered precision</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-purple-900/50 to-blue-900/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Our Core Values</h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              The principles that guide every decision we make and every feature we build
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => {
              const Icon = value.icon;
              const isActive = activeValue === index;
              return (
                <div
                  key={index}
                  className={`bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 transition-all duration-500 hover:scale-105 ${
                    isActive ? 'ring-2 ring-purple-500 bg-white/20 transform scale-105' : ''
                  }`}
                >
                  <div className={`bg-gradient-to-r ${value.color} w-16 h-16 rounded-xl flex items-center justify-center mx-auto mb-4`}>
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold mb-3 text-center">{value.title}</h3>
                  <p className="text-gray-300 text-center">{value.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Timeline Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Our Journey</h2>
            <p className="text-xl text-gray-300">
              From vision to reality - how we're transforming education with AI
            </p>
          </div>

          <div className="space-y-8">
            {timeline.map((item, index) => (
              <div key={index} className="flex items-start group">
                <div className="flex-shrink-0 w-24 text-right pr-8">
                  <div className="text-2xl font-bold text-purple-400">{item.year}</div>
                </div>
                <div className="flex-shrink-0 w-4 h-4 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full mt-2 relative">
                  <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-0.5 h-20 bg-gradient-to-b from-purple-500 to-transparent"></div>
                </div>
                <div className="flex-1 pl-8 pb-8">
                  <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 group-hover:bg-white/20 transition-all duration-300">
                    <h3 className="text-xl font-bold mb-3">{item.title}</h3>
                    <p className="text-gray-300">{item.description}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-slate-900/50 to-purple-900/50">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Meet Our Team</h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Passionate experts in AI, education, and technology working together to revolutionize learning
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 text-center group hover:bg-white/20 transition-all duration-300 hover:scale-105">
                <div className="text-6xl mb-4">{member.image}</div>
                <h3 className="text-xl font-bold mb-2">{member.name}</h3>
                <p className="text-purple-400 font-semibold mb-3">{member.role}</p>
                <p className="text-gray-300 text-sm">{member.bio}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Student Success Stories</h2>
            <p className="text-xl text-gray-300">
              Real stories from students who transformed their careers with EvolvEd AI
            </p>
          </div>

          <div className="grid lg:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-8 group hover:bg-white/20 transition-all duration-300">
                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <Quote className="w-8 h-8 text-purple-400 mb-4" />
                <p className="text-gray-200 mb-6 italic">"{testimonial.quote}"</p>
                <div>
                  <div className="font-bold">{testimonial.author}</div>
                  <div className="text-purple-400 text-sm">{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section className="py-20 px-4 bg-gradient-to-r from-purple-900/50 to-blue-900/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-8">Built with Excellence</h2>
          <p className="text-xl text-gray-300 mb-12">
            Our platform leverages modern, scalable technologies to deliver exceptional performance
          </p>

          <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-3xl p-8">
            <div className="grid md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-5xl mb-4">⚛️</div>
                <h3 className="text-xl font-bold mb-2">React Frontend</h3>
                <p className="text-gray-300">Modern, responsive, and intuitive user experience</p>
              </div>
              <div className="text-center">
                <div className="text-5xl mb-4">🐍</div>
                <h3 className="text-xl font-bold mb-2">Django Backend</h3>
                <p className="text-gray-300">Robust, secure, and scalable server architecture</p>
              </div>
              <div className="text-center">
                <div className="text-5xl mb-4">🤖</div>
                <h3 className="text-xl font-bold mb-2">Advanced AI</h3>
                <p className="text-gray-300">Cutting-edge machine learning and NLP algorithms</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center bg-gradient-to-r from-purple-600/20 to-blue-600/20 backdrop-blur-sm border border-white/20 rounded-3xl p-12">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Join Our Mission
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Be part of the educational revolution. Start your personalized learning journey today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 px-8 py-4 rounded-full font-semibold transition-all duration-300 transform hover:scale-105 hover:shadow-2xl flex items-center justify-center">
              Get Started Free
              <ArrowRight className="w-5 h-5 ml-2" />
            </button>
            <button className="bg-white/10 backdrop-blur-sm border border-white/20 hover:bg-white/20 px-8 py-4 rounded-full font-semibold transition-all duration-300 flex items-center justify-center">
              <Mail className="w-5 h-5 mr-2" />
              Contact Us
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h3 className="text-2xl font-bold mb-4">EvolvEd AI</h3>
            <p className="text-gray-400 mb-6">Transforming education through artificial intelligence</p>
            <div className="flex justify-center space-x-6">
              <Github className="w-6 h-6 text-gray-400 hover:text-white cursor-pointer transition-colors" />
              <Linkedin className="w-6 h-6 text-gray-400 hover:text-white cursor-pointer transition-colors" />
              <Mail className="w-6 h-6 text-gray-400 hover:text-white cursor-pointer transition-colors" />
            </div>
          </div>

          <div className="border-t border-white/10 pt-8 text-center text-gray-400">
            <p>© 2024 EvolvEd AI. All rights reserved.</p>
            <p className="text-sm mt-2">
              Built with React & Django | Designed with ❤️ for students worldwide
            </p>
            <p className="text-xs mt-4">
              Privacy Policy | Terms of Service | Cookie Policy | Accessibility Statement
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default About;