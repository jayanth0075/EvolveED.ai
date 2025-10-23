import React, { useState } from "react";

// Planner component displays a weekly study schedule
export default function Planner() {
  // State holds the schedule for each day
  const [schedule] = useState([
    { day: "Monday", time: "2h: Python Basics" },
    { day: "Tuesday", time: "1h: Machine Learning" },
    { day: "Wednesday", time: "1.5h: ML Project" },
    { day: "Thursday", time: "Revision + Quiz" },
    { day: "Friday", time: "1h: Deep Learning" },
  ]);

  return (
    <section className="bg-white p-4 rounded-lg">
      {/* Title for the planner */}
      <h2 className="text-2xl font-bold text-blue-600 mb-4">Auto Study Planner</h2>
      <div className="bg-white border-2 border-blue-500 rounded-xl shadow-lg p-6 animate-fade-in">
        {/* Table displays the schedule */}
        <table className="w-full text-left">
          <thead>
            <tr>
              <th className="text-blue-700 font-bold text-lg">Day</th>
              <th className="text-blue-700 font-bold text-lg">Schedule</th>
            </tr>
          </thead>
          <tbody>
            {schedule.map((s, i) => (
              <tr key={i} className="border-b border-blue-200 last:border-b-0">
                <td className="py-3 font-semibold text-blue-600">{s.day}</td>
                <td className="py-3 text-blue-600">{s.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {/* Info message below the table */}
        <div className="mt-4 text-blue-600">
          Balanced for classes + skill-building. <span className="font-semibold">Customize as needed!</span>
        </div>
      </div>
    </section>
  );
}


















