# Django Quiz & Events Web App

A full-featured web application for managing and taking quizzes, as well as viewing upcoming events. Built with Django and styled with TailwindCSS.

## Features

### Quiz Management
- **Quiz Listing**: Browse all available quizzes with titles, descriptions, and question counts
- **Dynamic Quiz Attempt**: Interactive quiz-taking interface with radio button answers
- **Automatic Scoring**: Real-time calculation of scores based on correct answers
- **User Authentication**: Login system with username pre-fill for authenticated users
- **Detailed Results**: View your score, percentage, and answer review with color-coded feedback
- **Quiz History**: Track all your quiz attempts with scores and timestamps (login required)

### Events Management
- **Events Listing**: View upcoming events with dates, locations, and descriptions
- **Responsive Design**: Mobile-friendly layout using TailwindCSS utilities

### User Authentication
- **Login/Logout System**: Secure user authentication
- **User-specific Features**: Personalized quiz history and submissions
- **Guest Access**: Take quizzes without authentication (with name entry)
- **Flash Messages**: User-friendly notifications for actions

### Additional Features
- Clean, modern UI with TailwindCSS
- Admin panel for content management
- Sample data fixtures for quick testing
- Message notifications for user actions
- Responsive navigation bar with auth status

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite3
- **Frontend**: HTML5, TailwindCSS (CDN)
- **Template Engine**: Django Template Language
- **Authentication**: Django Built-in Auth System
- **Python Version**: 3.13+

## Project Structure

```
Quiz_Event/
├── quiz_events_project/
│   ├── core/
│   │   ├── fixtures/
│   │   │   └── sample_data.json
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── quiz_events_project/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py
│   └── db.sqlite3
└── templates/
    ├── base.html
    └── core/
        ├── home.html
        ├── quiz_list.html
        ├── quiz_attempt.html
        ├── quiz_result.html
        ├── quiz_history.html
        ├── register.html
        ├── event_list.html
        └── login.html
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (optional, for cloning)

### Step 1: Clone the Repository
```bash
git clone https://github.com/diya8405/Quiz_Event_APP
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install django
```

### Step 4: Navigate to Project Directory
```bash
cd quiz_events_project
```

### Step 5: Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Load Sample Data
```bash
python manage.py loaddata sample_data
```

This will load:
- 1 Quiz with 3 questions (Python Programming Basics)
- 3 Events (Tech Conference, Python Workshop, Web Development Bootcamp)

### Step 7: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account for accessing the Django admin panel.

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`


## URL Routes

| URL Pattern | View | Description |
|-------------|------|-------------|
| `/` | `home` | Home page |
| `/quizzes/` | `quiz_list` | List all quizzes |
| `/quiz/<id>/attempt/` | `quiz_attempt` | Take a quiz |
| `/quiz/<id>/result/<submission_id>/` | `quiz_result` | View quiz results |
| `/history/` | `quiz_history` | View quiz history (login required) |
| `/events/` | `event_list` | List all events |
| `/login/` | `login_view` | User login |
| `/logout/` | `logout_view` | User logout |
| `/admin/` | Django Admin | Admin panel |


### Using the Application

1. **Browse Quizzes**: Click "Browse Quizzes" on the home page or navigate to the Quizzes page
2. **Take a Quiz**: Click "Start Quiz" on any quiz card
3. **Submit Answers**: Enter your name (or login) and select answers, then click "Submit Quiz"
4. **View Results**: See your score, percentage, and detailed answer review
5. **Check Events**: Navigate to the Events page to see upcoming events
6. **Login/Logout**: Use the navbar to login or logout
6. **Quiz History**: See your attempts and results (login require)

### Admin Panel Features

Access the admin panel to:
- Create new quizzes and questions
- Add/edit/delete events
- Manage user submissions
- View all quiz attempts and scores

## Sample Data

The fixture includes:

**Quiz**: Python Programming Basics
- Question 1: Creating a list in Python
- Question 2: Function definition keyword
- Question 3: Type of empty list

- add quiz 2 also with 3 quiestions

**Events**:
- Annual Tech Conference 2025 (December 15, 2025)
- Python Workshop for Beginners (December 10, 2025)
- Web Development Bootcamp (January 20, 2026)

## Models Overview

### Quiz
- Title, description, timestamps
- One-to-many relationship with Questions

### Question
- Text, question type
- Belongs to a Quiz
- One-to-many relationship with Answers

### Answer
- Answer text, is_correct flag
- Belongs to a Question

### UserSubmission
- User name, quiz reference, score, submission timestamp
- Tracks quiz attempts

### UserAnswer
- Links submissions to specific question answers
- Stores correctness flag

### Event
- Title, description, date, location
- Independent event management

## Development Notes

- **Project Type**: Interview/Assignment Task
- **Development Time**: 48 hours
- **Status**: Completed
- **Purpose**: Demonstrate Django proficiency, database modeling, template design, and authentication implementation

## Future Enhancements

Potential improvements for production:
- User registration system
- Quiz categories and tags
- Timer for timed quizzes
- Leaderboards and statistics
- Event registration functionality
- Email notifications
- Multiple choice and checkbox questions
- Image/media support in questions
- User profile pages
- Quiz history tracking

## Troubleshooting

### Template Not Found Error
Ensure templates are in the correct directory (`d:\Quiz_Event\templates\`)

### Static Files Not Loading
Run `python manage.py collectstatic` for production deployment

### Database Issues
Delete `db.sqlite3` and run migrations again:
```bash
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/Mac
python manage.py migrate
python manage.py loaddata sample_data
```

## License

This project was created as an assignment/interview task.


**Built with ❤️ using Django and TailwindCSS**
