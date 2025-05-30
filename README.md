Hindi Movie Guessing Game Website
This project is a dynamic web application that can guess almost any Hindi movie ever made by asking a maximum of 30 and a minimum of 13 questions. The system uses a unique algorithm to divide a database of 6000 Hindi movies into subsets with each question, leveraging advanced technologies such as Django, React, generative AI, NLP, and sentiment analysis.

Features
Interactive Movie Guessing Game: Predicts a movie by asking a series of yes/no questions.
Custom Algorithm: Divides the movie database efficiently with each question to narrow down the options.
Generative AI: Integrated with the Gemma model for generating intelligent questions and enhancing user interaction.
NLP & Sentiment Analysis: Utilized for refining movie data and creating a more accurate and meaningful dataset.
Extensive Movie Database: Contains data for over 6000 Hindi movies, sourced through API calls and web scraping.
Technologies Used
Back End: Django (Python)
Front End: React (JavaScript)
Generative AI: Gemma model for intelligent question generation
APIs: Used for data enrichment during movie database creation
Web Scraping: Automated extraction of movie details
NLP: Enhanced the database with sentiment analysis
Installation and Setup
Follow the steps below to run the project on your local machine:

Clone the Repository:

bash
Copy code
git clone https://github.com/bky-yadav/ques_charades.git && cd ques_charades  
Set Up Backend:

Navigate to the backend directory:
bash
Copy code
cd backend  
Create a virtual environment and activate it:
bash
Copy code
python -m venv venv  
source venv/bin/activate  # For Linux/Mac  
venv\Scripts\activate     # For Windows  
Install dependencies and apply migrations:
bash
Copy code
pip install -r requirements.txt  
python manage.py migrate  
Start Django Server:

bash
Copy code
python manage.py runserver  
Set Up Frontend:

Navigate to the frontend directory:
bash
Copy code
cd ../frontend  
Install dependencies:
bash
Copy code
yarn install  # or npm install  
Start the React development server:
bash
Copy code
yarn start  # or npm start  
Access the Application:

Open the following URLs in your browser:
Django Back End: http://127.0.0.1:8000
React Front End: http://localhost:3000

**DATA PIPELINE**


![image](https://github.com/user-attachments/assets/769a7fe2-ef50-4841-9096-eef3368df869)

