import React, { useState, useEffect } from 'react';
import './App.css';
import splash from './resources/Aki.jpeg';
import akin1 from './resources/akin1.jpeg'; // Import the new image

const App = () => {
  const [loading, setLoading] = useState(true);
  const [showQuestion, setShowQuestion] = useState(false);
  const [question, setQuestion] = useState('');
  const [image, setImage] = useState(splash); // Track which image to display
  const [zooming, setZooming] = useState(false); // Track if the zooming animation is happening

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 3000);
    return () => clearTimeout(timer);
  }, []);

  const handlePlayClick = async () => {
    setZooming(true); // Trigger zoom-in animation

    // Wait for the zooming animation to finish (duration is 2 seconds)
    setTimeout(() => {
      setImage(akin1); // Switch to the second image after zoom
      setZooming(false); // Stop zooming after image switches
      setShowQuestion(true);
      fetchQuestion(); // Fetch the first question from the backend
    }, 2000); // Time delay for zooming (matches CSS animation duration)
  };

  const fetchQuestion = async (selectedOption = null) => {
    try {
      const response = await fetch('http://localhost:6969/question', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          option: selectedOption, // The user's answer (if any)
          currentQuestion: question || "Is your character a real person?", // Use a default question for the first fetch
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setQuestion(data.question); // Update question from backend
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
        <div className={`splash-screen ${zooming ? 'zoom' : ''}`}>
          <img src={image} alt="Splash" className="splash-image" />
          {!zooming && !showQuestion && (
            <div className="play-button-container">
              <button className="play-button" onClick={handlePlayClick}>Play</button>
            </div>
          )}
        </div>
      ) : showQuestion ? (
        <div className="question-screen">
          <img src={akin1} alt="Background" className="background-image" />
          <div className="question-box">
            <h2>{question}</h2>
            <div className="options">
              <button className="option-button" onClick={() => handleOptionClick('Yes')}>Yes</button>
              <button className="option-button" onClick={() => handleOptionClick('No')}>No</button>
              <button className="option-button" onClick={() => handleOptionClick("I Don't Know")}>I Don’t Know</button>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}

export default App;
