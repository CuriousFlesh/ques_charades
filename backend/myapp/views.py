from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
import os
from django.conf import settings

# Define the path to the CSV file
csv_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', 'movies_attr_with_questions.csv')
df = pd.read_csv(csv_path)
question_list = [col for col in df.columns if col != 'title']
rem_df = df.copy()  # Copy to track remaining movies during filtering
asked_questions = {}  # Store asked questions and user responses

def choose_question(questions, rem_df):
    best_question = None
    smallest_diff = float('inf')
    
    for question in questions:
        value_counts = rem_df[question].value_counts()
        yes_count = value_counts.get('Yes', 0)
        no_count = value_counts.get('No', 0)
        
        diff = abs(yes_count - no_count)
        if diff < smallest_diff:
            smallest_diff = diff
            best_question = question
    
    return best_question

@csrf_exempt
def get_question(request):
    global rem_df, question_list, asked_questions

    if request.method == 'GET':
        # Reset remaining movies and questions for a new game session
        rem_df = df.copy()
        question_list = [col for col in df.columns if col != 'title']
        
        # Choose the first question
        if question_list:
            initial_question = choose_question(question_list, rem_df)
            return JsonResponse({"question": initial_question})
        else:
            return JsonResponse({"error": "No questions available."})

    elif request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)
            selected_option = data.get('option', '').strip().capitalize()
            current_question = data.get('currentQuestion')

            # Check if the response is "Don't Know" and remove the question from the remaining data
            if current_question and selected_option == "I don't know":
                if len(question_list)==0:
                    return JsonResponse({"message": "The movie cannot be guessed, please try again"})

                question_list.remove(current_question)  # Remove from the list of remaining questions
                rem_df = rem_df.drop(columns=[current_question])  # Drop the column from the DataFrame

            elif current_question and selected_option in ["Yes", "No"]:
                # Store the answer to the previous question and filter rem_df based on the answer
                asked_questions[current_question] = selected_option
                rem_df = rem_df[rem_df[current_question] == selected_option]
                question_list.remove(current_question)

            # Choose the next question
            if len(rem_df) > 1 and question_list:
                next_question = choose_question(question_list, rem_df)
                return JsonResponse({"question": next_question})
            elif len(rem_df) == 1:
                # Only one movie left, return its title
                movie_title = rem_df.iloc[0]['title']
                return JsonResponse({"message": "Match found", "movie": movie_title})
            elif len(rem_df) == 0:
                # No more movies match the answers
                return JsonResponse({"message": "The movie cannot be guessed, please try again"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
