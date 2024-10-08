const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 6969;

// Middleware
app.use(cors());
app.use(express.json()); // Parse JSON requests

// Sample questions array
const questions = [
    "Is your character a real person?",
    "Is your character famous?",
    "Does your character have superpowers?",
    "Can your character speak more than one language?",
];

// Endpoint to handle POST requests for questions
app.post('/question', (req, res) => {
    try {
        const { option, currentQuestion } = req.body; // Destructure request body
        
        // Log the incoming request for debugging
        console.log('Received request:', req.body);

        // Check if currentQuestion is provided
        if (!currentQuestion) {
            throw new Error('Current question is required');
        }

        // Determine the next question
        const nextQuestionIndex = (questions.indexOf(currentQuestion) + 1) % questions.length;
        const nextQuestion = questions[nextQuestionIndex];

        // Send the next question as a response
        res.json({ question: nextQuestion });
    } catch (error) {
        // Log the error and send a response
        console.error('Error processing request:', error.message);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
