import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useLocation, Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { Brain, Menu, X, LogIn, UserPlus, Home as HomeIcon, Info, Sparkles } from 'lucide-react';

// Import your page components
import Home from './pages/Home.js';
import About from './pages/About.js';
import Features from './pages/Features.js';
import Login from './pages/Login.js';
import Signup from './pages/Signup.js';
import Dashboard from './pages/Dashboard.js';
import Notes from './pages/Notes.js';
import Roadmap from './pages/Roadmap.js';
import Quiz from './pages/Quiz.js';
import Tutor from './pages/Tutor.js';
import Settings from './pages/settings.js';
import Profile from './pages/Profile.js';
import Planner from './pages/planner.js';

// Import your components
import Navbar from './components/Navbar.js';
import Sidebar from './components/Sidebar.js';
import Loader from './components/Loader.js';

// Landing Page Navigation Component
const LandingNav = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { to: '/', label: 'Home', icon: HomeIcon },
    { to: '/features', label: 'Features', icon: Sparkles },
    { to: '/about', label: 'About', icon: Info },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-md border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <div className="font-bold text-xl bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                EvolvEd AI
              </div>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navItems.map(item => {
              const Icon = item.icon;
              const isActive = location.pathname === item.to;

              return (
                <Link
                  key={item.to}
                  to={item.to}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive 
                      ? 'bg-white/10 text-cyan-400' 
                      : 'text-gray-300 hover:text-white hover:bg-white/5'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>

          {/* Auth Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <Link
              to="/login"
              className="flex items-center space-x-2 px-4 py-2 text-gray-300 hover:text-white transition-colors"
            >
              <LogIn className="h-4 w-4" />
              <span>Login</span>
            </Link>
            <Link
              to="/signup"
              className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-purple-500 hover:from-cyan-600 hover:to-purple-600 text-white rounded-lg font-medium transition-all transform hover:scale-105"
            >
              <UserPlus className="h-4 w-4" />
              <span>Sign Up</span>
            </Link>
          </div>

          {/* Mobile menu button */}
          <button
            className="md:hidden p-2 rounded-lg hover:bg-white/10 transition-colors"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="h-6 w-6 text-white" /> : <Menu className="h-6 w-6 text-white" />}
          </button>
        </div>
      </div>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            className="md:hidden bg-black/95 backdrop-blur-md border-t border-white/10"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
          >
            <div className="px-4 py-4 space-y-2">
              {navItems.map(item => {
                const Icon = item.icon;
                const isActive = location.pathname === item.to;

                return (
                  <Link
                    key={item.to}
                    to={item.to}
                    className={`flex items-center space-x-3 px-3 py-3 rounded-lg transition-colors ${
                      isActive 
                        ? 'bg-white/10 text-cyan-400' 
                        : 'text-gray-300 hover:text-white hover:bg-white/5'
                    }`}
                    onClick={() => setMobileMenuOpen(false)}
                  >
                    <Icon className="h-5 w-5" />
                    <span>{item.label}</span>
                  </Link>
                );
              })}

              <div className="border-t border-white/10 pt-4 mt-4 space-y-2">
                <Link
                  to="/login"
                  className="flex items-center space-x-3 px-3 py-3 text-gray-300 hover:text-white hover:bg-white/5 rounded-lg transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <LogIn className="h-5 w-5" />
                  <span>Login</span>
                </Link>
                <Link
                  to="/signup"
                  className="flex items-center space-x-3 px-3 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 text-white rounded-lg transition-colors"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <UserPlus className="h-5 w-5" />
                  <span>Sign Up</span>
                </Link>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  );
};

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/login" replace />;
};

// Layout Component for Protected Routes
const DashboardLayout = ({ children }) => {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar />
        <main className="flex-1 overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const location = useLocation();

  // Define route categories
  const publicRoutes = ['/', '/about', '/features'];
  const authRoutes = ['/login', '/signup'];
  const protectedRoutes = ['/dashboard', '/notes', '/roadmap', '/quiz', '/tutor', '/settings', '/profile', '/planner'];

  const isPublicRoute = publicRoutes.includes(location.pathname);
  const isAuthRoute = authRoutes.includes(location.pathname);
  const isProtectedRoute = protectedRoutes.some(route => location.pathname.startsWith(route));

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    if (token && userData) {
      try {
        setUser(JSON.parse(userData));
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }

    // Simulate loading time
    setTimeout(() => setLoading(false), 1000);
  }, []);

  const handleLogin = async (credentials) => {
    try {
      setLoading(true);
      // Simulate API call
      const mockResponse = {
        token: 'mock-jwt-token',
        user: {
          id: 1,
          email: credentials.email,
          name: credentials.email.split('@')[0]
        }
      };

      localStorage.setItem('token', mockResponse.token);
      localStorage.setItem('user', JSON.stringify(mockResponse.user));
      setUser(mockResponse.user);

      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async (userData) => {
    try {
      setLoading(true);
      // Simulate API call
      const mockResponse = {
        token: 'mock-jwt-token',
        user: {
          id: 1,
          email: userData.email,
          name: userData.name || userData.email.split('@')[0]
        }
      };

      localStorage.setItem('token', mockResponse.token);
      localStorage.setItem('user', JSON.stringify(mockResponse.user));
      setUser(mockResponse.user);

      // Redirect to dashboard
      window.location.href = '/dashboard';
    } catch (error) {
      console.error('Signup failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    window.location.href = '/';
  };

  if (loading) {
    return <Loader />;
  }

  return (
    <div className="min-h-screen bg-black">
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={
          <>
            <LandingNav />
            <Home />
          </>
        } />
        <Route path="/features" element={
          <>
            <LandingNav />
            <Features />
          </>
        } />
        <Route path="/about" element={
          <>
            <LandingNav />
            <About />
          </>
        } />

        {/* Auth Routes */}
        <Route path="/login" element={<Login onLogin={handleLogin} />} />
        <Route path="/signup" element={<Signup onSignup={handleSignup} />} />

        {/* Protected Routes - Now using DashboardLayout */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Dashboard />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/notes" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Notes />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/roadmap" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Roadmap />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/quiz" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Quiz />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/tutor" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Tutor />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/profile" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Profile />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/settings" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Settings />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/planner" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Planner />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        {/* Redirect unknown routes to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
};

export default App;