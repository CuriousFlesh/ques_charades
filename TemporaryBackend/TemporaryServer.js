const express = require('express');
const cors = require('cors');

const app = express();
const PORT = 5432;

app.use(cors());
app.use(express.json()); 

const questions = [
    "Is your character a real person?",
    "Is your character famous?",
    "Does your character have superpowers?",
    "Can your character speak more than one language?",
];

app.post('/question', (req, res) => {
    const { option } = req.body; 

    const nextQuestionIndex = (questions.indexOf(req.body.currentQuestion) + 1) % questions.length;
    const nextQuestion = questions[nextQuestionIndex];

    res.json({ question: nextQuestion });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
