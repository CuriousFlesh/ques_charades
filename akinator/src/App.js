import React, { useState, useEffect } from 'react';
import './App.css';
import splash from './resources/Aki.jpeg';
import akin1 from './resources/akin1.jpeg'; 

const App = () => {
  const [loading, setLoading] = useState(true);
  const [showQuestion, setShowQuestion] = useState(false);
  const [question, setQuestion] = useState('');
  const [image, setImage] = useState(splash); 
  const [zooming, setZooming] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 3000);
    return () => clearTimeout(timer);
  }, []);

  const handlePlayClick = async () => {
    setZooming(true); 

    
    setTimeout(() => {
      setImage(akin1); 
      setZooming(false); 
      setShowQuestion(true);
      fetchQuestion(); 
    }, 2000); 
  };

  const fetchQuestion = async (selectedOption = null) => {
    try {
      const response = await fetch('http://localhost:8000/myapp/get_questions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          option: selectedOption, 
          currentQuestion: question || "Is your character a real person?", 
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setQuestion(data.question); 
    } catch (error) {
      console.error('Error fetching question:', error);
    }
  };

  const handleOptionClick = async (option) => {
    await fetchQuestion(option); 
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
