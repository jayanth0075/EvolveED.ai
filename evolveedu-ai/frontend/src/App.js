import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-hot-toast';

// Components
import Navbar from './components/Navbar.js';
import Sidebar from './components/Sidebar.js';
import Loader from './components/Loader.js';

// Pages
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

// Public Pages (Add these to your pages directory)
import Home from './pages/Home.js';
import About from './pages/About.js';
import Features from './pages/Features.js';

// API
import api from './api/api.js';

// Animated Background Component
const AnimatedBackground = () => (
  <div className="fixed inset-0 -z-10 overflow-hidden">
    <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900"></div>
    <div className="absolute inset-0 opacity-30">
      {[...Array(100)].map((_, i) => (
        <motion.div
          key={i}
          className="absolute w-1 h-1 bg-white rounded-full"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
          }}
          animate={{
            opacity: [0.1, 1, 0.1],
            scale: [0.5, 1, 0.5],
          }}
          transition={{
            duration: 2 + Math.random() * 3,
            repeat: Infinity,
            delay: Math.random() * 2,
          }}
        />
      ))}
    </div>
    <div className="absolute inset-0">
      <motion.div
        className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"
        animate={{
          x: [0, 100, 0],
          y: [0, -50, 0],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "linear",
        }}
      />
      <motion.div
        className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"
        animate={{
          x: [0, -100, 0],
          y: [0, 50, 0],
        }}
        transition={{
          duration: 25,
          repeat: Infinity,
          ease: "linear",
        }}
      />
    </div>
    <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
  </div>
);

const App = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  // Define route categories
  const publicRoutes = ['/', '/about', '/features'];
  const authRoutes = ['/login', '/signup'];
  const protectedRoutes = ['/dashboard', '/notes', '/roadmap', '/quiz', '/tutor', '/settings', '/profile', '/planner'];

  const isPublicRoute = publicRoutes.includes(location.pathname);
  const isAuthRoute = authRoutes.includes(location.pathname);
  const isProtectedRoute = protectedRoutes.includes(location.pathname);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    if (token && userData) {
      setUser(JSON.parse(userData));
    }

    setTimeout(() => setLoading(false), 1000);
  }, []);

  const handleLogin = async (credentials) => {
    try {
      setLoading(true);
      const response = await api.login(credentials);
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      setUser(response.user);
      toast.success('Welcome back!');
    } catch (error) {
      toast.error('Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async (userData) => {
    try {
      setLoading(true);
      const response = await api.signup(userData);
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify(response.user));
      setUser(response.user);
      toast.success('Account created successfully!');
    } catch (error) {
      toast.error('Signup failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    setSidebarOpen(false);
    toast.success('Logged out successfully!');
  };

  if (loading) return <Loader />;

  return (
    <div className="min-h-screen">
      <AnimatedBackground />

      {/* Public Routes - Always accessible */}
      {isPublicRoute && (
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/features" element={<Features />} />
          </Routes>
        </AnimatePresence>
      )}

      {/* Auth Routes - Accessible without authentication */}
      {isAuthRoute && (
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="/signup" element={<Signup onSignup={handleSignup} />} />
          </Routes>
        </AnimatePresence>
      )}

      {/* Protected Routes - Require authentication */}
      {isProtectedRoute && (
        <>
          {user ? (
            <>
              <Navbar
                user={user}
                onLogout={handleLogout}
                onMenuToggle={() => setSidebarOpen(!sidebarOpen)}
                sidebarOpen={sidebarOpen}
              />
              <Sidebar
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
              />

              <main className={`pt-20 transition-all duration-300 ${sidebarOpen ? 'lg:ml-64' : 'ml-0'}`}>
                <AnimatePresence mode="wait">
                  <Routes location={location} key={location.pathname}>
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/notes" element={<Notes />} />
                    <Route path="/roadmap" element={<Roadmap />} />
                    <Route path="/quiz" element={<Quiz />} />
                    <Route path="/tutor" element={<Tutor />} />
                    <Route path="/settings" element={<Settings />} />
                    <Route path="/profile" element={<Profile />} />
                    <Route path="/planner" element={<Planner />} />
                  </Routes>
                </AnimatePresence>
              </main>
            </>
          ) : (
            <Navigate to="/login" replace />
          )}
        </>
      )}

      {/* Redirect to home for unknown routes */}
      {!isPublicRoute && !isAuthRoute && !isProtectedRoute && (
        <Navigate to="/" replace />
      )}
    </div>
  );
};

export default App;