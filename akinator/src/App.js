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
  const [guessedMovie, setGuessedMovie] = useState(null); // New state to hold guessed movie title
  const [gameOver, setGameOver] = useState(false); // To control if the game is over
  const [message, setMessage] = useState(''); // To show the message when the movie can't be guessed

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
      fetchInitialQuestion(); // Fetch the initial question when the game starts
    }, 2000);
  };

  // Function to fetch the initial question using a GET request
  const fetchInitialQuestion = async () => {
    try {
      const response = await fetch('http://localhost:8000/myapp/get_questions/', {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch initial question');
      }

      const data = await response.json();
      setQuestion(data.question); // Set the initial question
    } catch (error) {
      console.error('Error fetching initial question:', error);
    }
  };

  // Function to fetch the next question based on the selected option using a POST request
  const fetchNextQuestion = async (selectedOption) => {
    try {
      const response = await fetch('http://localhost:8000/myapp/get_questions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          option: selectedOption,
          currentQuestion: question,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch next question');
      }

      const data = await response.json();

      // Check if the response contains a "Match found" message
      if (data.message === "Match found") {
        setGuessedMovie(data.movie); // Store the guessed movie title
        setShowQuestion(false); // Hide the question box
        setGameOver(true); // End the game and show the result options
      } else if (data.message === "The movie cannot be guessed, please try again") {
        // Handle the case where the movie cannot be guessed
        setMessage("The movie cannot be guessed, please try again");
        setGameOver(true); // End the game and show the error message
      } else {
        setQuestion(data.question); // Update to the next question
      }
    } catch (error) {
      console.error('Error fetching next question:', error);
    }
  };

  const handleOptionClick = async (option) => {
    await fetchNextQuestion(option); // Fetch next question based on selected answer
  };

  const handleGuessValidation = (isCorrect) => {
    if (isCorrect) {
      setGuessedMovie(null);
      setGameOver(false);
      setShowQuestion(true);
      fetchInitialQuestion(); 
    } else {
      setMessage("The movie cannot be guessed, please try again"); // Set the message for wrong guesses
      setGameOver(true); // End the game
      setGuessedMovie(null);
      setGameOver(false);
      setShowQuestion(true);
      fetchInitialQuestion(); 
    }
  };

  const handlePlayAgain = () => {
    // Reset game states to start a new game
    setGuessedMovie(null);
    setGameOver(false);
    setShowQuestion(true);
    fetchInitialQuestion(); // Fetch the initial question again
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
      ) : gameOver ? (
        <div className="question-screen">
          <img src={akin1} alt="Background" className="background-image" />
          <div className="question-box">
            {guessedMovie ? (
              <>
                <h2>The movie guessed is: {guessedMovie}</h2>
                <div className="options">
                  <button className="option-button" onClick={() => handleGuessValidation(true)}>Correct Guess</button>
                  <button className="option-button" onClick={() => handleGuessValidation(false)}>Wrong Guess</button>
                </div>
              </>
            ) : (
              <>
                <h2>{message}</h2>
                <button className="option-button" onClick={handlePlayAgain}>Play Again</button> {/* Play Again Button */}
              </>
            )}
          </div>
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
