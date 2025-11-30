from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
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
    
    # Pre-fill username if user is authenticated
    default_username = request.user.username if request.user.is_authenticated else ''
    
    context = {
        'quiz': quiz,
        'default_username': default_username,
        'is_authenticated': request.user.is_authenticated
    }
    return render(request, 'core/quiz_attempt.html', context)


def submit_quiz(request, quiz_id):
    """Handle quiz submission and calculate score."""
    if request.method != 'POST':
        return redirect('core:start_quiz', quiz_id=quiz_id)
    
    quiz = get_object_or_404(Quiz.objects.prefetch_related('questions__answers'), id=quiz_id)
    
    # Get username from POST or authenticated user
    if request.user.is_authenticated:
        user_name = request.user.username
    else:
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


@login_required
def quiz_history(request):
    """Display quiz history for the logged-in user."""
    submissions = UserSubmission.objects.filter(
        user_name=request.user.username
    ).select_related('quiz').order_by('-submitted_at')
    
    # Calculate percentage for each submission
    submissions_with_stats = []
    for submission in submissions:
        total_questions = submission.quiz.questions.count()
        percentage = (submission.score / total_questions * 100) if total_questions > 0 else 0
        submissions_with_stats.append({
            'submission': submission,
            'total_questions': total_questions,
            'percentage': round(percentage, 2)
        })
    
    context = {
        'submissions_with_stats': submissions_with_stats
    }
    return render(request, 'core/quiz_history.html', context)


def register(request):
    """Handle user registration."""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully for {username}! Please login.')
            return redirect('core:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserCreationForm()
    
    context = {'form': form}
    return render(request, 'core/register.html', context)


def user_login(request):
    """Handle user login."""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            next_url = request.GET.get('next', 'core:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'core/login.html')


def user_logout(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')
