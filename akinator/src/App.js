import React, { useState, useEffect } from 'react';
import './App.css';
import splash from './resources/Aki.jpeg';

const App = () => {
  const [loading, setLoading] = useState(true);
  const [showQuestion, setShowQuestion] = useState(false); // New state for showing question

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 3000);
    return () => clearTimeout(timer);
  }, []);

  const handlePlayClick = () => {
    setShowQuestion(true); // When "Play" is clicked, show the question
  };

  return (
    <div className="App">
      {loading ? (
        <div className="splash-screen">
          <img src={splash} alt="Splash" className="splash-image" />
        </div>
      ) : showQuestion ? (
        <div className="question-screen">
          <div className="question-box">
            <h2>Is your character a real person?</h2>
            <div className="options">
              <button className="option-button">Yes</button>
              <button className="option-button">No</button>
              <button className="option-button">I Don’t Know</button>
            </div>
          </div>
        </div>
      ) : (
        <div className="main-screen">
          <button className="play-button" onClick={handlePlayClick}>Play</button>
        </div>
      )}
    </div>
  );
}

export default App;
