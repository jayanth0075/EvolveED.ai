// Tutor page placeholder
import React, { useState } from "react";

export default function Tutor() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  function handleAsk() {
    // Simulate AI answer
    setAnswer("Great question! For Data Scientist roles, focus on Python, ML libraries, SQL, and projects.");
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-fuchsia-700 mb-4">AI Q&A Tutor</h2>
      <div className="flex gap-3 mb-6">
        <input
          className="input flex-1"
          type="text"
          placeholder="Ask your career/study question..."
          value={question}
          onChange={e => setQuestion(e.target.value)}
        />
        <button className="btn-gradient" onClick={handleAsk}>Ask AI</button>
      </div>
      {answer && (
        <div className="bg-cyan-50 p-6 rounded-xl shadow animate-fade-in text-lg text-cyan-900">
          <strong>AI Tutor:</strong> {answer}
        </div>
      )}
    </div>
  );
}
