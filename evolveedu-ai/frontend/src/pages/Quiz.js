// Quiz page placeholder
import React, { useState } from "react";
import Loader from "../components/Loader";

export default function Quiz() {
  const [quizStarted, setQuizStarted] = useState(false);

  function startQuiz() {
    setQuizStarted(true);
    // Simulate quiz loading and display
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-fuchsia-700 mb-4">Quiz Maker</h2>
      <p className="mb-6 text-lg text-gray-700">
        Auto-generate adaptive quizzes from your notes.
      </p>
      {!quizStarted ? (
        <button className="btn-gradient" onClick={startQuiz}>Start Quiz</button>
      ) : (
        <Loader />
      )}
    </div>
  );
}
