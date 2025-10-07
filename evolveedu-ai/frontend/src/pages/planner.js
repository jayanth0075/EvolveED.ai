import React, { useState } from "react";

export default function Planner() {
  const [schedule, setSchedule] = useState([
    { day: "Monday", time: "2h: Python Basics" },
    { day: "Tuesday", time: "1h: Machine Learning" },
    { day: "Wednesday", time: "1.5h: ML Project" },
    { day: "Thursday", time: "Revision + Quiz" },
    { day: "Friday", time: "1h: Deep Learning" },
  ]);

  return (
    <section>
      <h2 className="text-2xl font-bold text-cyan-700 mb-4">Auto Study Planner</h2>
      <div className="bg-white rounded-xl shadow-md p-6 animate-fade-in">
        <table className="w-full text-left">
          <thead>
            <tr className="text-fuchsia-700">
              <th>Day</th>
              <th>Schedule</th>
            </tr>
          </thead>
          <tbody>
            {schedule.map((s, i) => (
              <tr key={i} className="border-b last:border-b-0">
                <td className="py-2 font-semibold">{s.day}</td>
                <td className="py-2">{s.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="mt-4 text-gray-700">
          Balanced for classes + skill-building. <span className="font-semibold text-fuchsia-600">Customize as needed!</span>
        </div>
      </div>
    </section>
  );
}


















