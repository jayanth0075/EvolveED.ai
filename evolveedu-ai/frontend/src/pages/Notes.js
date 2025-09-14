import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';
import AnimatedCard from '../components/AnimatedCard';
import Modal from '../components/Modal';
import {
  Plus,
  Search,
  FileText,
  BookOpen,
  Calendar,
  Download,
  Share,
  Edit,
  Trash2,
  Bookmark
} from 'lucide-react';
import { motion } from 'framer-motion';

const Notes = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [notes, setNotes] = useState([
    {
      id: 1,
      title: 'React Hooks Cheatsheet',
      content: 'useState, useEffect, useContext, useReducer, useCallback, useMemo, useRef, useImperativeHandle, useLayoutEffect, useDebugValue',
      category: 'react',
      date: '2024-01-15',
      tags: ['react', 'hooks', 'cheatsheet'],
      isBookmarked: true
    },
    {
      id: 2,
      title: 'JavaScript Array Methods',
      content: 'map, filter, reduce, find, some, every, includes, flat, flatMap, from, of',
      category: 'javascript',
      date: '2024-01-10',
      tags: ['javascript', 'arrays', 'methods'],
      isBookmarked: false
    },
    {
      id: 3,
      title: 'CSS Grid Layout',
      content: 'grid-template-columns, grid-template-rows, grid-gap, grid-column, grid-row, align-items, justify-items',
      category: 'css',
      date: '2024-01-05',
      tags: ['css', 'grid', 'layout'],
      isBookmarked: true
    }
  ]);

  const categories = [
    { id: 'all', label: 'All Notes', count: notes.length },
    { id: 'react', label: 'React', count: notes.filter(n => n.category === 'react').length },
    { id: 'javascript', label: 'JavaScript', count: notes.filter(n => n.category === 'javascript').length },
    { id: 'css', label: 'CSS', count: notes.filter(n => n.category === 'css').length },
    { id: 'bookmarked', label: 'Bookmarked', count: notes.filter(n => n.isBookmarked).length }
  ];

  const filteredNotes = notes.filter(note => {
    const matchesSearch = note.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         note.content.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' ||
                          (selectedCategory === 'bookmarked' ? note.isBookmarked : note.category === selectedCategory);

    return matchesSearch && matchesCategory;
  });

  const toggleBookmark = (id) => {
    setNotes(notes.map(note =>
      note.id === id ? { ...note, isBookmarked: !note.isBookmarked } : note
    ));
  };

  return (
    <div className="min-h-screen">
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold text-slate-800 mb-2">Notes & Summaries</h1>
              <p className="text-slate-600">Your personalized learning notes and AI-generated summaries</p>
            </div>
            <button
              onClick={() => setIsModalOpen(true)}
              className="flex items-center gap-2 bg-blue-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-600 transition-colors"
            >
              <Plus className="h-4 w-4" />
              New Note
            </button>
          </div>

          {/* Search and Filter */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
            {/* Search */}
            <div className="lg:col-span-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Search notes..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                />
              </div>
            </div>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="border border-slate-300 rounded-lg px-4 py-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
            >
              {categories.map(category => (
                <option key={category.id} value={category.id}>
                  {category.label} ({category.count})
                </option>
              ))}
            </select>
          </div>

          {/* Notes Grid */}
          {filteredNotes.length === 0 ? (
            <div className="text-center py-12">
              <BookOpen className="h-12 w-12 text-slate-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-slate-600 mb-2">No notes found</h3>
              <p className="text-slate-500">Try adjusting your search or create a new note</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredNotes.map((note, index) => (
                <motion.div
                  key={note.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <AnimatedCard
                    title={note.title}
                    icon={FileText}
                    className="h-full"
                  >
                    <p className="text-slate-600 text-sm mb-4 line-clamp-3">{note.content}</p>

                    {/* Tags */}
                    <div className="flex flex-wrap gap-1 mb-4">
                      {note.tags.map(tag => (
                        <span
                          key={tag}
                          className="px-2 py-1 bg-slate-100 text-slate-600 text-xs rounded-full"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>

                    {/* Meta and Actions */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 text-slate-500 text-sm">
                        <Calendar className="h-4 w-4" />
                        {new Date(note.date).toLocaleDateString()}
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => toggleBookmark(note.id)}
                          className={`p-1 rounded hover:bg-slate-100 transition-colors ${
                            note.isBookmarked ? 'text-amber-500' : 'text-slate-400'
                          }`}
                        >
                          <Bookmark className="h-4 w-4" fill={note.isBookmarked ? 'currentColor' : 'none'} />
                        </button>
                        <button className="p-1 rounded hover:bg-slate-100 text-slate-400 transition-colors">
                          <Edit className="h-4 w-4" />
                        </button>
                        <button className="p-1 rounded hover:bg-slate-100 text-slate-400 transition-colors">
                          <Share className="h-4 w-4" />
                        </button>
                        <button className="p-1 rounded hover:bg-slate-100 text-red-400 transition-colors">
                          <Trash2 className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </AnimatedCard>
                </motion.div>
              ))}
            </div>
          )}

          {/* AI Summary Section */}
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-slate-800 mb-6">AI-Powered Summaries</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <AnimatedCard
                title="Document Summarizer"
                icon={Download}
                actionLabel="Upload Document"
                gradient="from-purple-500 to-pink-500"
              >
                <p className="mb-4">Upload any learning material and get an AI-generated summary with key points and concepts.</p>
                <ul className="text-sm text-slate-600 space-y-1">
                  <li>• Supports PDF, DOCX, and text files</li>
                  <li>• Extracts key concepts and definitions</li>
                  <li>• Creates study-ready summaries</li>
                </ul>
              </AnimatedCard>

              <AnimatedCard
                title="Video Transcripts"
                icon={BookOpen}
                actionLabel="Process Video"
                gradient="from-green-500 to-emerald-500"
              >
                <p className="mb-4">Provide a video URL and get transcriptions with summarized key takeaways and learning points.</p>
                <ul className="text-sm text-slate-600 space-y-1">
                  <li>• YouTube and other platform support</li>
                  <li>• Timestamped key moments</li>
                  <li>• Quiz question generation</li>
                </ul>
              </AnimatedCard>
            </div>
          </div>
        </main>
      </div>

      {/* Create Note Modal */}
      <Modal
        open={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Create New Note"
        size="lg"
      >
        <div className="p-6">
          <form className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Title</label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                placeholder="Note title"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Content</label>
              <textarea
                rows={6}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                placeholder="Write your note here..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-2">Tags (comma separated)</label>
              <input
                type="text"
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
                placeholder="react, javascript, hooks"
              />
            </div>

            <div className="flex gap-3">
              <select className="flex-1 border border-slate-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all">
                <option value="react">React</option>
                <option value="javascript">JavaScript</option>
                <option value="css">CSS</option>
                <option value="html">HTML</option>
                <option value="backend">Backend</option>
              </select>

              <button
                type="button"
                className="flex items-center gap-2 px-4 py-2 bg-slate-100 text-slate-700 rounded-lg hover:bg-slate-200 transition-colors"
              >
                <Bookmark className="h-4 w-4" />
                Bookmark
              </button>
            </div>

            <div className="flex justify-end gap-3 pt-4">
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 text-slate-600 hover:text-slate-800 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
              >
                Create Note
              </button>
            </div>
          </form>
        </div>
      </Modal>
    </div>
  );
};

export default Notes;