from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Sample questions data (You can replace this with more dynamic logic or a database query)
questions = [
    "Is the movie from the 1990s?",
    "Is the movie in Hindi?",
    "Is the lead actor a male?",
    "Is the movie directed by a famous director?",
    "Is the movie a romantic genre?"
]

current_question_index = 0
@csrf_exempt
def get_question(request):
    global current_question_index

    if request.method == 'POST':
        try:
            # Parse the incoming JSON data from the request
            data = json.loads(request.body)

            # Extract the selected option and the current question (if provided)
            selected_option = data.get('option')
            current_question = data.get('currentQuestion')

            # You can process the selected_option here (for now, it's just a placeholder)
            print(f"User selected: {selected_option} for question: {current_question}")

            # Determine the next question
            if current_question_index < len(questions):
                # Fetch the next question based on the current question index
                next_question = questions[current_question_index]
                current_question_index += 1  # Move to the next question for the next iteration
            else:
                # If all questions have been asked, return a completion message
                next_question = "No more questions. Thank you for playing!"

            # Return the next question as a JSON response
            return JsonResponse({"question": next_question})

        except json.JSONDecodeError:
            # Handle JSON parsing error
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    return JsonResponse({"error": "Invalid request method"}, status=405)
