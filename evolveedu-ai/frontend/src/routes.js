import {
  Home,
  BookOpen,
  Map,
  Brain,
  MessageCircle,
  Calendar,
  User,
  Settings,
  LogOut
} from 'lucide-react';

export const routes = [
  {
    path: '/dashboard',
    name: 'Dashboard',
    icon: Home,
    description: 'Overview of your learning progress'
  },
  {
    path: '/notes',
    name: 'Smart Notes',
    icon: BookOpen,
    description: 'Generate notes from YouTube videos'
  },
  {
    path: '/roadmap',
    name: 'Career Roadmap',
    icon: Map,
    description: 'Personalized career guidance'
  },
  {
    path: '/quiz',
    name: 'AI Quizzes',
    icon: Brain,
    description: 'Test your knowledge'
  },
  {
    path: '/tutor',
    name: 'AI Tutor',
    icon: MessageCircle,
    description: 'Chat with your personal AI tutor'
  },
  {
    path: '/planner',
    name: 'Study Planner',
    icon: Calendar,
    description: 'Plan your learning schedule'
  }
];

export const userMenuItems = [
  {
    name: 'Profile',
    icon: User,
    action: 'profile',
    path: '/profile'
  },
  {
    name: 'Settings',
    icon: Settings,
    action: 'settings',
    path: '/settings'
  },
  {
    name: 'Logout',
    icon: LogOut,
    action: 'logout',
    danger: true
  }
];