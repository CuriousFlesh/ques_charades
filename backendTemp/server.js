const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 6969;

app.use(cors());
app.use(express.json());

const questions = [
    "Is your character a real person?",
    "Is your character famous?",
    "Does your character have superpowers?",
    "Can your character speak more than one language?",
];

app.post('/question', (req, res) => {
    try {
        const { option, currentQuestion } = req.body
        
    
        console.log('Received request:', req.body);

    
        if (!currentQuestion) {
            throw new Error('Current question is required');
        }

    
        const nextQuestionIndex = (questions.indexOf(currentQuestion) + 1) % questions.length;
        const nextQuestion = questions[nextQuestionIndex];

    
        res.json({ question: nextQuestion });
    } catch (error) {
    
        console.error('Error processing request:', error.message);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
