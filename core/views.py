from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import date
from .models import Quiz, Question, Answer, UserSubmission, UserAnswer, Event


def home(request):
    """Landing page with welcome message and navigation buttons."""
    return render(request, 'core/home.html')


def quiz_list(request):
    """Display list of all available quizzes."""
    quizzes = Quiz.objects.all().order_by('-created_at')
    context = {
        'quizzes': quizzes
    }
    return render(request, 'core/quiz_list.html', context)


def event_list(request):
    """Display list of upcoming events."""
    today = date.today()
    events = Event.objects.filter(date__gte=today).order_by('date')
    context = {
        'events': events
    }
    return render(request, 'core/event_list.html', context)


def start_quiz(request, quiz_id):
    """Display quiz questions for user to attempt."""
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__answers'), id=quiz_id)
    context = {
        'quiz': quiz
    }
    return render(request, 'core/quiz_attempt.html', context)


def submit_quiz(request, quiz_id):
    """Handle quiz submission and calculate score."""
    if request.method != 'POST':
        return redirect('core:start_quiz', quiz_id=quiz_id)
    
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__answers'), id=quiz_id)
    user_name = request.POST.get('user_name', 'Anonymous')
    
    # Calculate score
    score = 0
    questions = quiz.questions.all()
    
    # Create UserSubmission
    submission = UserSubmission.objects.create(
        quiz=quiz,
        user_name=user_name,
        score=0  # Will update after calculating
    )
    
    # Process each question
    for question in questions:
        answer_id = request.POST.get(f'question_{question.id}')
        
        if answer_id:
            try:
                selected_answer = Answer.objects.get(id=answer_id, question=question)
                is_correct = selected_answer.is_correct
                
                if is_correct:
                    score += 1
                
                # Create UserAnswer record
                UserAnswer.objects.create(
                    submission=submission,
                    question=question,
                    answer=selected_answer,
                    is_correct=is_correct
                )
            except Answer.DoesNotExist:
                pass
    
    # Update submission with final score
    submission.score = score
    submission.save()
    
    return redirect('core:quiz_result', submission_id=submission.id)


def quiz_result(request, submission_id):
    """Display quiz results for a user submission."""
    submission = get_object_or_404(
        UserSubmission.objects.prefetch_related('user_answers__question', 'user_answers__answer'),
        id=submission_id
    )
    
    total_questions = submission.quiz.questions.count()
    percentage = (submission.score / total_questions * 100) if total_questions > 0 else 0
    
    context = {
        'submission': submission,
        'total_questions': total_questions,
        'percentage': round(percentage, 2)
    }
    return render(request, 'core/quiz_result.html', context)
