import React from 'react';
import Navbar from '../components/Navbar';
import Sidebar from '../components/Sidebar';

export default function Profile(){
  return (
    <div>
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <h1 className="text-2xl font-bold mb-4">Profile</h1>
          <p>User profile page coming soon.</p>
        </main>
      </div>
    </div>
  );
}