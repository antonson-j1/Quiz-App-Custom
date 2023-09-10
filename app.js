const categorySelect = document.getElementById('category');
const startButton = document.getElementById('start');
const quizContainer = document.getElementById('quiz-container');
const submitButton = document.getElementById('submit');

let questions = []; // Array to store selected questions
let userAnswers = []; // Array to store user's answers

// API for questions
const apiURL = 'https://opentdb.com/api.php?amount=10';

function fetchQuestions(category) {
    return fetch(apiURL + '?category=${category}')
        .then(response=>json())
        .then(data => data.questions);                  
}

// Display questions on cards with answer text fields
function displayQuestions() {
    quizContainer.innerHTML = '';
    for (let i = 0; i < questions.length; i++) {
        const questionCard = document.createElement('div');
        questionCard.className = 'question-card';
        questionCard.innerHTML = `
            <h2>Question ${i + 1}</h2>
            <p>${questions[i].question}</p>
            <input type="text" id="answer-${i}" placeholder="Your Answer">
        `;
        quizContainer.appendChild(questionCard);
    }
}

// Calculate the user's score
function calculateScore() {
    let score = 0;
    for (let i = 0; i < questions.length; i++) {
        if (userAnswers[i].toLowerCase() === questions[i].correct_answer.toLowerCase()) {
            score++;
        }
    }
    return score;
}

startButton.addEventListener('click', () => {
    const selectedCategory = categorySelect.value;
    fetchQuestions(selectedCategory)
        .then((data) => {
            questions = data.slice(0, 10); // Randomly select 10 questions
            displayQuestions();
        });
});

submitButton.addEventListener('click', () => {
    // Get user's answers and store them in the 'userAnswers' array
    for (let i = 0; i < questions.length; i++) {
        userAnswers[i] = document.getElementById(`answer-${i}`).value;
    }

    // Calculate the user's score
    const score = calculateScore();
    alert(`Your Score: ${score}/${questions.length}`);

    // Send the score to the backend for tracking
    // You can use AJAX or fetch to send the data to the backend
});
