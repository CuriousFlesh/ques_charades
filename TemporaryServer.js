const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 5432;

app.use(cors());
app.use(express.json()); // For parsing application/json

// Questions array
const questions = [
    "Is your character a real person?",
    "Is your character famous?",
    "Does your character have superpowers?",
    "Can your character speak more than one language?",
    // Add more questions as needed
];

// Route to get the next question
app.post('/question', (req, res) => {
    const { option } = req.body; // Get the selected option

    // Simple logic to get the next question
    // In a real scenario, you'd determine the next question based on the selected option
    const nextQuestionIndex = (questions.indexOf(req.body.currentQuestion) + 1) % questions.length;
    const nextQuestion = questions[nextQuestionIndex];

    res.json({ question: nextQuestion });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
