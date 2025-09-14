import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Cog6ToothIcon,
  BellIcon,
  ShieldCheckIcon,
  UserIcon,
  EyeIcon,
  MoonIcon,
  SunIcon
} from '@heroicons/react/24/outline';

const Settings = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [emailUpdates, setEmailUpdates] = useState(false);
  const [privacy, setPrivacy] = useState('public');

  const pageVariants = {
    initial: { opacity: 0, y: 20 },
    in: { opacity: 1, y: 0 },
    out: { opacity: 0, y: -20 }
  };

  const pageTransition = {
    type: 'tween',
    ease: 'anticipate',
    duration: 0.5
  };

  return (
    <motion.div
      initial="initial"
      animate="in"
      exit="out"
      variants={pageVariants}
      transition={pageTransition}
      className="max-w-4xl mx-auto p-6"
    >
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Settings</h1>
        <p className="text-gray-400">Manage your account preferences and settings</p>
      </div>

      <div className="grid gap-6">
        {/* Appearance Settings */}
        <motion.div
          className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.2 }}
        >
          <div className="flex items-center mb-4">
            <EyeIcon className="h-6 w-6 text-purple-400 mr-3" />
            <h2 className="text-xl font-semibold text-white">Appearance</h2>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-white font-medium">Dark Mode</h3>
              <p className="text-gray-400 text-sm">Toggle between light and dark themes</p>
            </div>
            <button
              onClick={() => setDarkMode(!darkMode)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                darkMode ? 'bg-purple-600' : 'bg-gray-200'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  darkMode ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>
        </motion.div>

        {/* Notification Settings */}
        <motion.div
          className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.2 }}
        >
          <div className="flex items-center mb-4">
            <BellIcon className="h-6 w-6 text-purple-400 mr-3" />
            <h2 className="text-xl font-semibold text-white">Notifications</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-white font-medium">Push Notifications</h3>
                <p className="text-gray-400 text-sm">Receive notifications about updates</p>
              </div>
              <button
                onClick={() => setNotifications(!notifications)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  notifications ? 'bg-purple-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    notifications ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-white font-medium">Email Updates</h3>
                <p className="text-gray-400 text-sm">Get updates via email</p>
              </div>
              <button
                onClick={() => setEmailUpdates(!emailUpdates)}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  emailUpdates ? 'bg-purple-600' : 'bg-gray-200'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    emailUpdates ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
            </div>
          </div>
        </motion.div>

        {/* Privacy Settings */}
        <motion.div
          className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.2 }}
        >
          <div className="flex items-center mb-4">
            <ShieldCheckIcon className="h-6 w-6 text-purple-400 mr-3" />
            <h2 className="text-xl font-semibold text-white">Privacy</h2>
          </div>

          <div>
            <h3 className="text-white font-medium mb-2">Profile Visibility</h3>
            <p className="text-gray-400 text-sm mb-4">Choose who can see your profile</p>

            <div className="space-y-2">
              {['public', 'friends', 'private'].map((option) => (
                <label key={option} className="flex items-center">
                  <input
                    type="radio"
                    name="privacy"
                    value={option}
                    checked={privacy === option}
                    onChange={(e) => setPrivacy(e.target.value)}
                    className="h-4 w-4 text-purple-600 border-gray-300 focus:ring-purple-500"
                  />
                  <span className="ml-2 text-white capitalize">{option}</span>
                </label>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Account Settings */}
        <motion.div
          className="bg-white/10 backdrop-blur-md rounded-xl p-6 border border-white/20"
          whileHover={{ scale: 1.02 }}
          transition={{ duration: 0.2 }}
        >
          <div className="flex items-center mb-4">
            <UserIcon className="h-6 w-6 text-purple-400 mr-3" />
            <h2 className="text-xl font-semibold text-white">Account</h2>
          </div>

          <div className="space-y-4">
            <button className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
              Change Password
            </button>
            <button className="w-full bg-gray-600 hover:bg-gray-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
              Export Data
            </button>
            <button className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
              Delete Account
            </button>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Settings;