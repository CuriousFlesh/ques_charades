import React, { useState, useEffect } from 'react';
import './App.css';
import splash from './resources/Aki.jpeg';

const App = () => {
  const [loading, setLoading] = useState(true);
  const [showQuestion, setShowQuestion] = useState(false);
  const [question, setQuestion] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 3000);
    return () => clearTimeout(timer);
  }, []);

  const handlePlayClick = async () => {
    setShowQuestion(true);
    await fetchQuestion(); // Fetch the first question from the backend
  };

  const fetchQuestion = async (selectedOption = null) => {
    try {
        const response = await fetch('http://localhost:5432/question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ option: selectedOption, currentQuestion: question }), // Include the current question
        });
        const data = await response.json();
        setQuestion(data.question);  // Update question from backend
    } catch (error) {
        console.error('Error fetching question:', error);
    }
  };

  const handleOptionClick = async (option) => {
    await fetchQuestion(option); // Fetch the next question based on the selected option
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
            <h2>{question}</h2>
            <div className="options">
              <button 
                className="option-button" 
                onClick={() => handleOptionClick('Yes')}
              >
                Yes
              </button>
              <button 
                className="option-button" 
                onClick={() => handleOptionClick('No')}
              >
                No
              </button>
              <button 
                className="option-button" 
                onClick={() => handleOptionClick("I Don't Know")}
              >
                I Don’t Know
              </button>
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
