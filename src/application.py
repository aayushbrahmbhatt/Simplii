from datetime import datetime, timedelta
from smtplib import SMTPException
from bson.objectid import ObjectId
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
import pytz
from werkzeug.security import generate_password_hash
import schedule
import time
import atexit
import os
import random
import requests
from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import markdown2

from apscheduler.schedulers.background import BackgroundScheduler

from tabulate import tabulate
from flask_wtf import form
from flask import app, render_template, session, url_for, flash, redirect, request, Response, Flask
from flask_pymongo import PyMongo
from flask import json
from flask.helpers import make_response
from flask.json import jsonify
from flask_mail import Mail, Message
from pymongo import ASCENDING
from forms import ForgotPasswordForm, RegistrationForm, LoginForm, ResetPasswordForm, PostingForm, ApplyForm, TaskForm, UpdateForm,ReminderForm
import bcrypt
import os
import csv
import sys
import openai
import asyncio
from openai import AsyncOpenAI
from utils import format_gcal_date
#added this here
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask import jsonify
import google.generativeai as genai
from flask_mail import Mail, Message
from datetime import datetime, timedelta

class OTPForm(FlaskForm):
    otp = StringField('Enter OTP', validators=[DataRequired()])
    submit = SubmitField('Verify')
from flask_login import LoginManager, login_required

from firebase_config import auth

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/simplii'
mongo = PyMongo(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "dummysinghhh@gmail.com"
app.config['MAIL_PASSWORD'] = "wbjf dsfu mper nqfv"
mail = Mail(app)

# Initialize the URLSafeTimedSerializer with your secret key and a salt
serializer = URLSafeTimedSerializer(app.secret_key, salt='password-reset')

scheduler = BackgroundScheduler()

GEMINI_API_KEY = "AIzaSyCvSkPBAgEFnXLOhYIxkJthYZ8KemKENao"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_task_prompt(tasks):
    today = datetime.now().date()
    this_week_end = today + timedelta(days=(6-today.weekday()))
    this_month_end = (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    today_tasks = []
    week_tasks = []
    month_tasks = []
    
    for task in tasks:
        due_date = datetime.strptime(task['duedate'], '%Y-%m-%d').date()
        if due_date == today:
            today_tasks.append(task)
        elif due_date <= this_week_end:
            week_tasks.append(task)
        elif due_date <= this_month_end:
            month_tasks.append(task)

    prompt =    f"""
                As a professional task management assistant, create a concise, professional, and motivating email response for a user's task list. Use the following task data:

                - **Today's Tasks ({len(today_tasks)}):** {', '.join(t['taskname'] for t in today_tasks) if today_tasks else 'None'}
                - **This Week's Tasks ({len(week_tasks)}):** {', '.join(t['taskname'] for t in week_tasks) if week_tasks else 'None'}
                - **This Month's Tasks ({len(month_tasks)}):** {', '.join(t['taskname'] for t in month_tasks) if month_tasks else 'None'}

                Please ensure the email is structured and formatted as follows:

                1. **A crisp and motivational introduction:** Greet the user warmly and set a positive tone for task management.
                2. **Task Breakdown:** Provide a concise, well-structured breakdown of tasks by category (Today, This Week, This Month). If there are no tasks in a specific category, acknowledge this in a professional and encouraging way.
                3. **Time Allocation & Priorities:** Recommend time allocation and priorities for tasks in each category (if applicable). Be specific and actionable.
                4. **Work-Life Balance Tips:** Include short, practical tips to help the user maintain balance.
                5. **Conclusion:** End on a motivating and uplifting note. If all tasks are completed, congratulate the user and encourage proactive planning for future tasks.
                6. **Sign-Off:** Conclude the email with "Best regards, Simplii AI".

                Formatting Requirements:
                - Use a clear and professional email format with proper sections and spacing.
                - Use bullet points or numbered lists where appropriate for better readability.
                - Keep the tone formal yet encouraging.
                - Ensure the email is concise, avoiding unnecessary verbosity.

                Make sure to handle cases where there are no tasks across one or all categories, providing a meaningful and positive message in such scenarios. The email must remain polished and professional in every case.
                """

    return prompt

def send_task_email(user_email, tasks):
    try:
        print("Here in send_task_email")
        prompt = generate_task_prompt(tasks)
        response = model.generate_content(prompt)
        
        # Convert Markdown to HTML
        email_html_content = markdown2.markdown(response.text)

        msg = Message(
            'Your Personalized Task Schedule',
            sender='dummysinghhh@gmail.com',
            recipients=[user_email]
        )
        msg.html = email_html_content
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

# Add this route to your Flask app
@app.route('/send_task_email', methods=['POST'])
def handle_email_request():
    try:
        # Log route access
        app.logger.info("Route accessed: /send_task_email")
        print("Starting email request handler")

        # Get user email from session
        user_email = session.get('email')
        if not user_email:
            app.logger.error("User email not found in session")
            return jsonify({'error': 'User email not found'}), 400

        # Get tasks from database
        user_id = session.get('user_id')
        tasks = get_user_tasks(user_id)  # Implement this function
        
        # Debug logging
        print(f"Debug info - Email: {user_email}, UserId: {user_id}, Tasks: {tasks}")
        
        # Commented out email sending logic
        success = send_task_email(user_email, tasks)
        if success:
            app.logger.info(f"Email sent successfully to {user_email}")
            return jsonify({'message': 'Email sent successfully'}), 200
        else:
            app.logger.error(f"Failed to send email to {user_email}")
            return jsonify({'error': 'Failed to send email'}), 500

    except Exception as e:
        app.logger.error(f"Error in handle_email_request: {str(e)}")
        return jsonify({'error': str(e)}), 500

def get_user_tasks(user_str_id) :
    user_id = ObjectId(user_str_id)
    current_date = datetime.now().date()

    # Calculate the date 7 days from now
    thirty_days_later = current_date + timedelta(days=31)

    print(f"Debug info - UserId: {user_id}, Current Date: {current_date}, Thirty Days Later: {thirty_days_later.strftime('%Y-%m-%d')}")

    relevant_tasks = mongo.db.tasks.find({
                'user_id': user_id,
                'duedate': {
                    # '$gte': current_date.strftime('%Y-%m-%d'),
                    '$lte': thirty_days_later.strftime('%Y-%m-%d')
                }
            }).sort('duedate', 1)

    tasksListContent = list(relevant_tasks)
    return tasksListContent


def fetch_tasks():
    print("fetch_tasks called")
    # Calculate the current date
    current_date = datetime.now().date()

    # Calculate the date 7 days from now
    seven_days_later = current_date + timedelta(days=7)

    users = mongo.db.users.find()
    with app.app_context():  # Create an application context
        for u in users:
            relevant_tasks = mongo.db.tasks.find({
                'user_id': u['_id'],
                'duedate': {
                    # '$gte': current_date.strftime('%Y-%m-%d'),
                    '$lte': seven_days_later.strftime('%Y-%m-%d')
                }
            }).sort('duedate', 1)

            tasksListContent = list(relevant_tasks)

            table_html = "<table border='1'><tr><th>Task Name</th><th>Category</th><th>Start Date</th><th>Due Date</th><th>Status</th><th>Hours</th></tr>"
            for user_tasks in tasksListContent:
                # Create an HTML table from the task data
                table_html += f"<tr><td>{user_tasks['taskname']}</td><td>{user_tasks['category']}</td><td>{user_tasks['startdate']}</td><td>{user_tasks['duedate']}</td><td>{user_tasks['status']}</td><td>{user_tasks['hours']}</td></tr>"
            table_html += "</table>"

            # Compose the email
            msg = Message('Welcome to Simplii: Your Task Scheduling Companion', sender='dummysinghhh@gmail.com', recipients=[u['email']])

            # Create the text version of the email with the table
            email_body = f"Here are your tasks due in next 7 days:\n\n{table_html}"
            msg.html = email_body
            try:
                mail.send(msg)  # Attempt to send the email
                print(f"Email sent to {u['email']} successfully.")
            except SMTPException as e:
                # Handle SMTP errors
                print(f"Failed to send email to {u['email']}. Error: {str(e)}")
            except Exception as e:
                # Handle other exceptions
                print(f"An error occurred while sending an email to {u['email']}. Error: {str(e)}")


    # flash("Email reminders sent for tasks with due dates in the specified range.", 'success')
    print('***************')

@app.route("/")
@app.route("/home")
def home():
    ############################
    # home() function displays the homepage of our website.
    # route "/home" will redirect to home() function.
    # input: The function takes session as the input
    # Output: Out function will redirect to the login page
    # ##########################
    if session.get('email'):

        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

# Reset Password route
@app.route("/resetPassword/<token>", methods=['GET', 'POST'])
def resetPassword(token):
    if request.method == 'GET':
        try:
            # Verify the token and get the associated email
            email = serializer.loads(token, max_age=3600)  # Max age in seconds (1 hour)

            # Here, you can add code to identify the user by their email and present a password reset form
            # For example, you can store the email in a session or a hidden form field to ensure it's the same user

            return render_template('resetPassword.html', email=email)

        except SignatureExpired:
            flash('The password reset link has expired.', 'error')
            return redirect(url_for('forgotPassword'))
        except BadSignature:
            flash('Invalid password reset link.', 'error')
            return redirect(url_for('forgotPassword'))

    elif request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        new_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
        # Update the user's password in the database
        user = mongo.db.users.find_one({'email': email})
        if user:
            user_id = user['_id']
            # Update the password for the user with the specified ID
            mongo.db.users.update_one(
                {"_id": user_id},
                {"$set": {"pwd": new_password}}
            )

            flash('Password reset successful. You can now log in with your new password.', 'success')
            return redirect(url_for('login'))

    return render_template('resetPassword.html')

# Handle cases where the user is not found or the old password doesn't match
# You can redirect to an appropriate page or display an error message.

@app.route("/forgotPassword", methods=['GET', 'POST'])
def forgotPassword():
    ############################
    # forgotPassword() redirects the user to dummy template.
    # route "/forgotPassword" will redirect to forgotPassword() function.
    # input: The function takes session as the input
    # Output: Out function will redirect to the dummy page
    # ##########################
    if not session.get('user_id'):
        form = ForgotPasswordForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                email = request.form.get('email')
                # id = mongo.db.users.find_one({'email': email})
                user = mongo.db.users.find_one({'email': email})



                if user:
                    # Generate a reset token
                    reset_token = serializer.dumps(email, salt='password-reset')

                    # Store the reset token in the user's document in the database
                    mongo.db.users.update_one({'_id': user['_id']}, {'$set': {'reset_token': reset_token}})

                    # Send a reset password email
                    reset_link = url_for('resetPassword', token=reset_token, _external=True)
                    msg = Message('Password Reset', sender=app.config['MAIL_USERNAME'], recipients=[email])
                    msg.body = f'Visit the following link to reset your password: {reset_link}'
                    mail.send(msg)

                    flash('Password reset link sent to your email.', 'info')
                else:
                    flash('Email address not found.', 'error')
        
    else:
        return redirect(url_for('home'))
    return render_template('forgotPassword.html', title='Register', form=form)


# @app.route('/chatbot', methods=['GET', 'POST'])
# def chatbot():
#     if request.method == 'POST':
#         user_input = request.form['user_input']
        
#         # Generate a prompt based on user input
#         prompt = f"User task-related query: {user_input}. Provide task management insights or assistance."

#         # Call Gemini API
#         response = call_gemini_api(prompt)
        
#         # Return the response to the frontend as JSON
#         return jsonify(response=response)
    
#     # Render chatbot page template
#     return render_template('chatbot.html')

# def call_gemini_api(prompt):
#     # Gemini API headers and data payload
#     headers = {
#         "Authorization": f"Bearer {GEMINI_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "prompt": prompt,
#         "model": "gemini"  # specify model as needed
#     }
    
#     # Make the API request to Gemini
#     response = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}", headers=headers, json=data)
    
#     # Check for a valid response
#     if response.status_code == 200:
#         return response.json().get("response", "Sorry, I didn't understand that.")
#     else:
#         return "There was an error processing your request."


@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_input = request.form['user_input']
        
        gemini_prompt = f"Provide a detailed and engaging response to the following question: {user_input}"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": gemini_prompt}]}]
        }

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            chatbot_response = response.json()['candidates'][0]['content']['parts'][0]['text']
            return render_template('chatbot.html', user_input=user_input, chatbot_response=chatbot_response)
        else:
            return jsonify({"error": "Failed to fetch response from Gemini API."}), 500

    return render_template('chatbot.html')



@app.route("/recommend")
def recommend():
    ############################
    # recommend() function opens the task_recommendation.csv file and displays the data of the file
    # route "/recommend" will redirect to recommend() function.
    # input: The function opens the task_recommendation.csv
    # Output: Our function will redirect to the recommend page for showing the data
    # ##########################
   

    if session.get('user_id'):
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)

        # Fetch all tasks for the user and sort by 'duedate' in ascending order
        tasks = list(mongo.db.tasks.find({'user_id': user_id}).sort('duedate', ASCENDING))
        return render_template('recommend.html', title='Recommend', tasks=tasks)
    else:
        return redirect(url_for('home'))
    

@app.route("/kanbanBoard", methods=['GET', 'POST'])
def kanbanBoard():
    ############################
    # kanbanBoard() function opens the task_recommendation.csv file and displays the data of the file
    # route "/kanbanBoard" will redirect to kanbanBoard() function.
    # input: The function opens the task_recommendation.csv
    # Output: Our function will display tasks in a Kanban Board format
    # Output: Our function will display tasks in a Kanban Board format
    # ##########################
    if session.get('user_id'):
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)

        # Separate tasks based on status
        todo_tasks = list(mongo.db.tasks.find({'user_id': user_id, 'status': 'To-Do'}).sort('duedate', ASCENDING))
        in_progress_tasks = list(mongo.db.tasks.find({'user_id': user_id, 'status': 'In Progress'}).sort('duedate', ASCENDING))
        done_tasks = list(mongo.db.tasks.find({'user_id': user_id, 'status': 'Done'}).sort('duedate', ASCENDING))
        return render_template('kanbanBoard.html', title='KanbanBoard', todo_tasks=todo_tasks, in_progress_tasks=in_progress_tasks, done_tasks=done_tasks)

    else:
        return redirect(url_for('home'))

@app.route("/update_task_status", methods=['POST'])
def update_task_status():
    ############################
    # update_task_status() function updates the tasks status by changing in the KanbanBoard.
    # route "/update_task_status" will redirect to kanbanBoard() function.
    # input: The function O/p of sortable from KanbanBoard actions.
    # Output: Our function will display updated tasks in a Kanban Board format
    # ##########################
    try:
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        task_id = request.form.get('task')
        new_status = request.form.get('status')

        # Your MongoDB update query here
        # Make sure to replace 'user_id' and 'taskname' with your actual field names
        update_result = mongo.db.tasks.update_one(
            {'user_id': user_id, 'taskname': task_id},
            {'$set': {'status': new_status}}
        )

        if update_result.modified_count > 0:
            flash(f'Task Updated!', 'success')
            return jsonify({'task': task_id, 'status': new_status})
        else:
            return jsonify({'error': 'Failed to update task status'})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route("/send_email_reminders", methods=['GET', 'POST'])
def send_email_reminders():
    if session.get('user_id'):
        if request.method == 'POST':
            due_date = request.form.get('duedate')  # Get the due date input from the form
            user_str_id = session.get('user_id')
            user_id = ObjectId(user_str_id)
            
            # Convert the due date to a datetime object
            due_date=datetime.strptime(due_date, '%Y-%m-%d').date()

            # Fetch tasks whose due date falls within the specified range
            relevant_tasks = mongo.db.tasks.find({
                'user_id': user_id,
                'duedate': {'$lt': due_date.strftime('%Y-%m-%d')}  # Convert due_date back to string for comparison
            }).sort('duedate', 1)

            # Convert the cursor to a list of dictionaries
            relevant_tasks = list(relevant_tasks)

            # Create an HTML table from the task data
            table_html = "<table border='1'><tr><th>Task Name</th><th>Category</th><th>Start Date</th><th>Due Date</th><th>Status</th><th>Hours</th></tr>"

            for task in relevant_tasks:
                table_html += f"<tr><td>{task['taskname']}</td><td>{task['category']}</td><td>{task['startdate']}</td><td>{task['duedate']}</td><td>{task['status']}</td><td>{task['hours']}</td></tr>"

            table_html += "</table>"

            # Compose the email
            email= session.get('email')
            msg = Message('Welcome to Simplii: Your Task Scheduling Companion', sender='dummysinghhh@gmail.com', recipients=[email])

            # Create the text version of the email with the table
            email_body = f"Here are your tasks:\n\n{table_html}"
            msg.html = email_body
            mail.send(msg)

            flash("Email reminders sent for tasks with due dates in the specified range.", 'success')
            return render_template('recommend.html', title='Recommend', tasks=relevant_tasks)
        
        # Handle GET request, presumably to display tasks
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        tasks = mongo.db.tasks.find({
            'user_id': user_id,
        })
        return render_template('recommend.html', tasks=tasks)
    else:
        return redirect(url_for('home'))

@app.route("/dashboard")
def dashboard():
    ############################
    # dashboard() function displays the tasks of the user
    # route "/dashboard" will redirect to dashboard() function.
    # input: The function takes session as the input and fetches user tasks from Database
    # Output: Our function will redirect to the dashboard page with user tasks being displayed
    ############################
    # Check if user is logged in; if not, redirect to login
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        # Fetch user tasks if session is valid
        tasks = mongo.db.tasks.find({'user_id': ObjectId(session['user_id'])})
        task_list = []
        for task in tasks:
            task["gcal_link"] = format_gcal_date(task.get('taskname'), task.get('startdate'), task.get('duedate'))
            task_list.append(task)

        return render_template('dashboard.html', tasks=task_list)
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        return redirect(url_for('login'))

@app.route("/gpt", methods=['GET', 'POST'])
def gpt():
    ############################
    # dashboard() function displays the tasks of the user
    # route "/dashboard" will redirect to dashboard() function.
    # input: The function takes session as the input and fetches user tasks from Database
    # Output: Our function will redirect to the dashboard page with user tasks being displayed
    # ##########################
    params = request.url.split('?')[1].split('+')
    # for i in range(len(params)):
    #     params[i] = params[i].split('=')
    # for i in range(len(params)):
    #     if "%" in params[i][1]:
    #         index = params[i][1].index('%')
    #         params[i][1] = params[i][1][:index] + \
    #                        " " + params[i][1][index + 3:]
    # d = {}
    # for i in params:
    #     d[i[0]] = i[1]
    return render_template('gpt.html', searchQuery=params)


@app.route("/about")
def about():
    # ############################
    # about() function displays About Us page (about.html) template
    # route "/about" will redirect to about() function.
    # ##########################
    return render_template('about.html', title='About')

@app.route("/reminderscheduled")
def reminderscheduled():
    if session.get('user_id'):
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)

        reminderScheduler = list(mongo.db.reminderScheduler.find({'user_id':user_id}).sort('reminder_date', ASCENDING))
        # print("reminder scheduled ",reminderScheduler)
        return render_template('remindersScheduled.html', title='reminderScheduler', reminderScheduler=reminderScheduler)

    else:
        return redirect(url_for('home'))

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    ############################
    # contact() function allows users to send support messages.
    # route "/contact" will redirect to contact() function.
    # input: The function takes session as the input
    # Output: Our function will render the contact support page
    # ##########################
    
    if request.method == 'POST':
        message = request.form.get('message')
        user_email = session.get('email')

        # Send the message to support (here you can implement the sending logic)
        flash('Your message has been sent to support!', 'success')
    
    return render_template('contact.html')

@app.route("/activity")
@login_required
def activity():
    ############################
    # activity() function displays a log of user activities.
    # route "/activity" will redirect to activity() function.
    # input: The function takes session as the input
    # Output: Our function will render the activity log page
    # ##########################
    
    user_id = session.get('user_id')
    activities = list(mongo.db.activities.find({'user_id': user_id}).sort('timestamp', -1))
    
    return render_template('activity.html', activities=activities)


@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    ############################
    # settings() function displays account settings for the user.
    # route "/settings" will redirect to settings() function.
    # input: The function takes session as the input
    # Output: Our function will render the settings page
    # ##########################
    
    if request.method == 'POST':
        # Update user settings
        notifications_enabled = request.form.get('notifications_enabled') == 'on'
        mongo.db.users.update_one({'_id': session.get('user_id')}, {'$set': {'notifications_enabled': notifications_enabled}})
        flash('Settings updated successfully!', 'success')
    
    user = mongo.db.users.find_one({'_id': session.get('user_id')})
    return render_template('settings.html', user=user)

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    ############################
    # profile() function displays and updates user profile information.
    # route "/profile" will redirect to profile() function.
    # input: The function takes session as the input
    # Output: Our function will redirect to the profile page
    # ##########################
    
    if request.method == 'POST':
        # Get updated user information
        email = request.form.get('email')
        name = request.form.get('name')

        # Update the user's information in the database
        mongo.db.users.update_one({'_id': session.get('user_id')}, {'$set': {'email': email, 'name': name}})
        flash('Profile updated successfully!', 'success')
    
    user = mongo.db.users.find_one({'_id': session.get('user_id')})
    return render_template('profile.html', user=user)


# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     # ############################
#     # register() function displays the Registration portal (register.html) template
#     # route "/register" will redirect to register() function.
#     # RegistrationForm() called and if the form is submitted then various values are fetched and updated into database
#     # Input: Username, Email, Password, Confirm Password
#     # Output: Value update in database and redirected to home login page
#     # ##########################
#     if not session.get('email'):
#         form = RegistrationForm()
#         if form.validate_on_submit():
#             if request.method == 'POST':
#                 username = request.form.get('username')
#                 email = request.form.get('email')
#                 password = request.form.get('password')
#                 mongo.db.users.insert_one({'name': username, 'email': email, 'pwd': bcrypt.hashpw(
#                     password.encode("utf-8"), bcrypt.gensalt()), 'tasksList':[], 'temp': None})
#                 auth.create_user_with_email_and_password(email, password)
#                 msg = Message('Welcome to Simplii: Your Task Scheduling Companion', sender='dummysinghhh@gmail.com', recipients=[email])
#                 msg.body = f"Hey {username},\n\n" \
#                 "We're excited to welcome you to Simplii, your new task scheduling companion. Simplii is here to help you stay organized, meet deadlines, and achieve your goals efficiently.\n\n" \
#                 "With Simplii, you can schedule your tasks, set deadlines, and work on them with ease. Never miss an important deadline again!\n\n" \
#                 "Thank you for choosing Simplii. We're thrilled to have you on board. If you have any questions or need assistance, feel free to reach out to us.\n\n" \
#                 "Best regards,\n" \
#                 "The Simplii Team"
#                 mail.send(msg)
#                 print("Message sent!")
#                 flash(f'Account created for {form.username.data}!', 'success')
#                 return redirect(url_for('home'))
#     else:
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)

# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     # ############################
#     # register() function displays the Registration portal (register.html) template
#     # route "/register" will redirect to register() function.
#     # RegistrationForm() called and if the form is submitted then various values are fetched and updated into database
#     # Input: Username, Email, Password, Confirm Password
#     # Output: Value update in database and redirected to home login page
#     # ##########################
#     if not session.get('email'):
#         form = RegistrationForm()
#         if form.validate_on_submit():
#             if request.method == 'POST':
#                 username = request.form.get('username')
#                 email = request.form.get('email')
#                 password = request.form.get('password')
#                 mongo.db.users.insert_one({'name': username, 'email': email, 'pwd': bcrypt.hashpw(
#                     password.encode("utf-8"), bcrypt.gensalt()), 'tasksList':[], 'temp': None})
#                 auth.create_user_with_email_and_password(email, password)
#                 msg = Message('Welcome to Simplii: Your Task Scheduling Companion', sender='dummysinghhh@gmail.com', recipients=[email])
#                 msg.body = f"Hey {username},\n\n" \
#                 "We're excited to welcome you to Simplii, your new task scheduling companion. Simplii is here to help you stay organized, meet deadlines, and achieve your goals efficiently.\n\n" \
#                 "With Simplii, you can schedule your tasks, set deadlines, and work on them with ease. Never miss an important deadline again!\n\n" \
#                 "Thank you for choosing Simplii. We're thrilled to have you on board. If you have any questions or need assistance, feel free to reach out to us.\n\n" \
#                 "Best regards,\n" \
#                 "The Simplii Team"
#                 mail.send(msg)
#                 print("Message sent!")
#                 flash(f'Account created for {form.username.data}!', 'success')
#                 return redirect(url_for('home'))
#     else:
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)


# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if not session.get('email'):
#         form = RegistrationForm()
#         if form.validate_on_submit():
#             if request.method == 'POST':
#                 username = request.form.get('username')
#                 email = request.form.get('email')
#                 password = request.form.get('password')

#                 otp = random.randint(100000, 999999)
                
#                 mongo.db.users.insert_one({
#                     'name': username,
#                     'email': email,
#                     'pwd': bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
#                     'tasksList': [],
#                     'otp': otp,  
#                     'is_verified': False  
#                 })

#                 msg = Message('Your OTP for Simplii Registration', sender='dummysinghhh@gmail.com', recipients=[email])
#                 msg.body = f"Hello {username},\n\nYour OTP for registration is: {otp}\n\nPlease enter this code to complete your registration.\n\nThank you,\nThe Simplii Team"
#                 mail.send(msg)
#                 print("OTP sent!")

#                 session['email'] = email
#                 flash(f'OTP sent to {email}. Please verify your email to complete registration.', 'info')
                
#                 return redirect(url_for('otp_verification'))
#     else:
#         return redirect(url_for('home'))
#     return render_template('register.html', title='Register', form=form)

# @app.route("/otp_verification", methods=['GET', 'POST'])
# def otp_verification():
#     # Redirect to login if no email in session
#     if 'email' not in session:
#         return redirect(url_for('login'))

#     # Initialize the form
#     form = OTPForm()

#     # Validate form submission
#     if form.validate_on_submit():  # Check if form was submitted and is valid
#         otp_entered = form.otp.data
#         user = mongo.db.users.find_one({'email': session['email']})

#         if user and user['otp'] == int(otp_entered):  # OTP matches
#             mongo.db.users.update_one({'email': session['email']}, {'$set': {'is_verified': True, 'otp': None}})
#             session['user'] = user['name']
#             flash('Your account has been verified successfully!', 'success')
#             return redirect(url_for('dashboard'))
#         else:
#             flash('Invalid OTP. Please try again.', 'danger')

#     # Render the template with the form
#     return render_template('otp_verification.html', title='OTP Verification', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if not session.get('email'):
        form = RegistrationForm()
        if form.validate_on_submit():
            if request.method == 'POST':
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')

                otp = random.randint(100000, 999999)
                
                # Save user details in MongoDB without OTP
                mongo.db.users.insert_one({
                    'name': username,
                    'email': email,
                    'pwd': bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()),
                    'tasksList': [],
                    'is_verified': False  
                })
                auth.create_user_with_email_and_password(email, password)

                # Send OTP email
                msg = Message('Your OTP for Simplii Registration', sender='dummysinghhh@gmail.com', recipients=[email])
                msg.body = f"Hello {username},\n\nYour OTP for registration is: {otp}\n\nPlease enter this code to complete your registration.\n\nThank you,\nThe Simplii Team"
                mail.send(msg)
                print("OTP sent!")

                # Store OTP in session
                session['email'] = email
                session['otp'] = otp  # Store OTP in session
                flash(f'OTP sent to {email}. Please verify your email to complete registration.', 'info')
                
                return redirect(url_for('otp_verification'))
    else:
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/otp_verification", methods=['GET', 'POST'])
def otp_verification():
    # Redirect to login if no email in session
    if 'email' not in session:
        return redirect(url_for('login'))

    # Initialize the form
    form = OTPForm()

    # Validate form submission
    if form.validate_on_submit():  # Check if form was submitted and is valid
        otp_entered = form.otp.data

        # Retrieve OTP from session instead of MongoDB
        if 'otp' in session and session['otp'] == int(otp_entered):  # OTP matches
            # Update user as verified in MongoDB
            mongo.db.users.update_one({'email': session['email']}, {'$set': {'is_verified': True}})
            session.pop('otp')  # Clear OTP from session after successful verification
            session['user'] = session['email']
            flash('Your account has been verified successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid OTP. Please try again.', 'danger')

    # Render the template with the form
    return render_template('otp_verification.html', title='OTP Verification', form=form)



@app.route("/deleteTask", methods=['GET', 'POST'])
def deleteTask():
    ############################
    # deleteTask() function will delete the particular user task from database.
    # route "/deleteTask" will redirect to deleteTask() function.
    # input: The function takes email, task, status, category as the input and fetches from the database
    # Output: Out function will delete the particular user task from database
    # ##########################
    if request.method == 'POST':
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        task = request.form.get('task')
        status = request.form.get('status')
        category = request.form.get('category')
        print("task, status, category ", task, status, category)
        id = mongo.db.tasks.find_one(
            {'user_id': user_id, 'taskname': task, 'status': status, 'category': category}, {'_id'})
        print("id in delete task ",id)
        mongo.db.tasks.delete_one({'_id': id['_id']})
        return "Success"
    else:
        return "Failed"


@app.route("/task", methods=['GET', 'POST'])
def task():
    # ############################
    # task() function displays the Add Task portal (task.html) template
    # route "/task" will redirect to task() function.
    # TaskForm() called and if the form is submitted then new task values are fetched and updated into database
    # Input: Task, Category, start date, end date, number of hours
    # Output: Value update in database and redirected to home login page
    # ##########################
    if session.get('user_id'):
        form = TaskForm()
        if form.validate_on_submit():
            print("inside form")
            if request.method == 'POST':
                user_str_id = session.get('user_id')
                user_id = ObjectId(user_str_id)
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                status = request.form.get('status')
                task_id = mongo.db.tasks.insert_one({'user_id': user_id,
                                       'taskname': taskname,
                                       'category': category,
                                       'startdate': startdate,
                                       'duedate': duedate,
                                       'status': status,
                                       'hours': hours})

                #Now update the user schema's TaskList field with the taskId(Basically append the new task id to that array)
                user_document = mongo.db.users.find_one({'_id': user_id})
                tasks_list = user_document.get('tasksList', [])
                tasks_list.append(task_id)

                # Update the user's tasksList field
                # mongo.db.users.update_one(
                #     {'_id': user_id},
                #     {
                #         '$set': {'tasksList': tasks_list}
                #     }
                # )
            flash(f' {form.taskname.data} Task Added!', 'success')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))
    return render_template('task.html', title='Task', form=form)


@app.route("/schedule_reminder", methods=['GET', 'POST'])
def scheduleReminder():
    print("Schedule reminders")
    ############################
    # scheduleRemainder() function displays the remainder.html page for updations
    # route "/scheduleRemainder" will redirect to updateTask() function.
    # input: The function takes various task values as Input
    # Output: Out function will redirect to the updateTask page
    # ##########################

    params = request.url.split('?')[1].split('&')
    for i in range(len(params)):
        params[i] = params[i].split('=')
    for i in range(len(params)):
        if "%" in params[i][1]:
            index = params[i][1].index('%')
            params[i][1] = params[i][1][:index] + \
                           " " + params[i][1][index + 3:]
    d = {}
    for i in params:
        d[i[0]] = i[1]

    form = ReminderForm()
    form.taskname.data = d['taskname']
    form.category.data = d['category']
    form.status.data = d['status']
    form.hours.data = d['hours']
    form.startdate.data = d['startdate']
    form.duedate.data = d['duedate']

    if request.method == 'POST':
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        task_str_id = request.form.get('task_id')  # assuming 'task_id' is part of the form data
        task_id = ObjectId(task_str_id)
        taskname = form.taskname.data
        startdate = form.startdate.data
        duedate = form.duedate.data
        category = form.category.data
        reminder_date = request.form.get('reminder_date')
        reminder_time_str = request.form.get('reminderTime')

        # Convert to datetime objects
        reminder_date_str = datetime.strptime(reminder_date + ' ' + reminder_time_str, '%Y-%m-%d %H:%M')

        # Insert a new document into the "reminderScheduler" collection
        reminderScheduler_id = mongo.db.reminderScheduler.insert_one({
            'user_id': user_id,
            'task_id': task_id,
            'taskname': taskname,
            'category': category,
            'startdate':startdate,
            'duedate':duedate,
            'reminder_date': reminder_date_str,
            'reminder_time': reminder_time_str,
        })

        # Now, update the user schema's TaskList field
        mongo.db.users.update_one(
            {'_id': user_id},
            {'$addToSet': {'tasksList': reminderScheduler_id.inserted_id}}
        )

        # reminder_date = datetime.strptime(reminder_date_str, '%Y-%m-%d %H:%M')

        # relevant_reminders = list(mongo.db.reminderScheduler.find({
        #     'user_id': user_id,
        #     'reminder_date': {'$lt': reminder_date_str}
        # }).sort('reminder_date', 1))

        # due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        #
        # # Fetch tasks whose due date falls within the specified range
        # relevant_tasks = mongo.db.tasks.find({
        #     'user_id': user_id,
        #     'duedate': {'$lt': due_date.strftime('%Y-%m-%d')}  # Convert due_date back to string for comparison
        # }).sort('duedate', 1)

        # Convert the cursor to a list of dictionaries
        # relevant_reminders = list(relevant_reminders)
        # print("relevant reminders ",relevant_reminders)

        # Create an HTML table from the reminder data
        # reminder_table_html = ("<table border='1'>"
        #                        "<tr>"  "<th>Task Name</th>"
        #                                "<th>Category</th>"
        #                                "<th>Start Date</th>"
        #                                "<th>Due Date</th></tr>")

        # for reminder in relevant_reminders:
        # reminder_table_html += f"<tr><td>{reminder['taskname']}</td><td>{reminder['category']}</td><td>{reminder['startdate']}</td><td>{reminder['duedate']}</tr>"

        # reminder_table_html += "</table>"

        # Compose the reminder email
        email = session.get('email')
        msg = Message('Reminder: Upcoming Task', sender='dummysinghhh@gmail.com', recipients=[email])
        scheduled = int(time.mktime(reminder_date_str.timetuple()))
        print("time of reminder", scheduled)
        msg.extra_headers = {'X-SMTPAPI': json.dumps({'send_at': scheduled})}
        # Create the HTML version of the email with the reminder table
        # reminder_email_body = f"Here are your upcoming reminders:\n\n{reminder_table_html}"
        reminder_email_body = f"There is an upcoming reminder for you!!\n"
        msg.html = reminder_email_body
        mail.send(msg)

        # schedule.every().day.at(reminder_date).do(scheduleReminder)

        flash(f'Reminder Scheduled!', 'success')
        return redirect(url_for('home'))
    return render_template('remainder.html',title='Reminder',form=form)

async def chatgptquery(query):
    client = AsyncOpenAI(api_key = os.getenv('OPENAI_API_KEY'))  # defaults to os.environ.get("OPENAI_API_KEY")
    messages = []
    user_query = query + "\n Give the output in html format"
    messages.append({"role": "user", "content": user_query})
    completion = await client.chat.completions.create(model="gpt-3.5-turbo", messages=messages) 
    reply = completion.choices[0].message.content
    
    return reply
        
@app.route("/feedback", methods=['GET', 'POST'])
@login_required
def feedback():
    ############################
    # feedback() function allows users to submit their feedback.
    # route "/feedback" will redirect to feedback() function.
    # input: The function takes session as the input
    # Output: Our function will render the feedback page
    # ##########################
    
    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        user_email = session.get('email')

        # Store feedback in the database
        mongo.db.feedback.insert_one({'email': user_email, 'feedback': feedback_text, 'timestamp': datetime.now()})
        flash('Thank you for your feedback!', 'success')
    
    return render_template('feedback.html')


@app.route("/editTask", methods=['GET', 'POST'])
def editTask():
    ############################
    # editTask() function helps the user to edit a particular task and update in database.
    # route "/editTask" will redirect to editTask() function.
    # input: The function takes email, task, status, category as the input
    # Output: Out function will update new values in the database
    # ##########################
    if request.method == 'POST':
        user_str_id = session.get('user_id')
        user_id = ObjectId(user_str_id)
        task = request.form.get('task')
        status = request.form.get('status')
        category = request.form.get('category')
        id = mongo.db.tasks.find_one(
            {'user_id': user_id, 'taskname': task, 'status': status, 'category': category})
        print("id in edit task ", id)
        return json.dumps({'taskname': id['taskname'], 'category': id['category'], 'startdate': id['startdate'], 'duedate': id['duedate'], 'status': id['status'], 'hours': id['hours']}), 200, {
            'ContentType': 'application/json'}
    else:
        return "Failed"

@app.route("/user_guide")
def user_guide():
    ############################
    # user_guide() function displays a guide for using the application.
    # route "/user_guide" will redirect to user_guide() function.
    # input: The function does not require session
    # Output: Our function will render the user guide page
    # ##########################
    
    return render_template('user_guide.html')


@app.route("/updateTask", methods=['GET', 'POST'])
def updateTask():
    ############################
    # updateTask() function displays the updateTask.html page for updations
    # route "/updateTask" will redirect to updateTask() function.
    # input: The function takes variious task values as Input
    # Output: Out function will redirect to the updateTask page
    # ##########################
    if session.get('user_id'):
        print("params in updateTask ", request.url)
        params = request.url.split('?')[1].split('&')
        for i in range(len(params)):
            params[i] = params[i].split('=')
        for i in range(len(params)):
            if "%" in params[i][1]:
                index = params[i][1].index('%')
                params[i][1] = params[i][1][:index] + \
                    " " + params[i][1][index + 3:]
        d = {}
        for i in params:
            d[i[0]] = i[1]

        form = UpdateForm()

        form.taskname.data = d['taskname']
        form.category.data = d['category']
        form.status.data = d['status']
        form.hours.data = d['hours']
        
        # Assuming that 'd['startdate']' and 'd['duedate']' are date strings in a format like 'YYYY-MM-DD'
        # Convert them to datetime objects
        startdate_str = d['startdate']
        duedate_str = d['duedate']
        # Convert to datetime objects
        startdate_datetime = datetime.strptime(startdate_str, '%Y-%m-%d')
        duedate_datetime = datetime.strptime(duedate_str, '%Y-%m-%d')

        # Now, set the datetime objects in the form
        form.startdate.data = startdate_datetime
        form.duedate.data = duedate_datetime
        

        if form.validate_on_submit():
            if request.method == 'POST':
                user_str_id = session.get('user_id')
                user_id = ObjectId(user_str_id)
                taskname = request.form.get('taskname')
                category = request.form.get('category')
                startdate = request.form.get('startdate')
                duedate = request.form.get('duedate')
                hours = request.form.get('hours')
                status = request.form.get('status')
                mongo.db.tasks.update_one({'user_id': user_id, 'taskname': d['taskname'], 'startdate': d['startdate'], 'duedate': d['duedate']},
                                      {'$set': {'taskname': taskname, 'startdate': startdate, 'duedate': duedate, 'category': category, 'status': status, 'hours': hours}})
            flash(f' {form.taskname.data} Task Updated!', 'success')
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('home'))
    return render_template('updateTask.html', title='Task', form=form)

@app.route("/task_history")
@login_required
def task_history():
    ############################
    # task_history() function displays the history of completed tasks.
    # route "/task_history" will redirect to task_history() function.
    # input: The function takes session as the input
    # Output: Our function will render the task history page
    # ##########################
    
    user_id = session.get('user_id')
    completed_tasks = list(mongo.db.tasks.find({'user_id': user_id, 'status': 'completed'}).sort('duedate', ASCENDING))
    
    return render_template('task_history.html', completed_tasks=completed_tasks)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # ############################
    # login() function displays the Login form (login.html) template
    # route "/login" will redirect to login() function.
    # LoginForm() called and if the form is submitted then various values are fetched and verified from the database entries
    # Input: Email, Password, Login Type
    # Output: Account Authentication and redirecting to Dashboard
    # ##########################
    if not session.get('user_id'):
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                temp = mongo.db.users.find_one({'email': form.email.data}, {
                    'email', 'name', 'pwd'})
                flash('You have been logged in!', 'success')
                session['email'] = temp['email']
                session['name'] = temp['name']
                session['user_id'] = str(temp['_id'])
                return redirect(url_for('dashboard'))
            except Exception as e:
                print(f"Error during login: {e}")
                flash(
                    'Login Unsuccessful. Please check username and password',
                    'danger')
    else:
        print("session details ", session)
        return redirect(url_for('home'))
    return render_template(
        'login.html',
        title='Login',
        form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    # ############################
    # logout() function just clears out the session and returns success
    # route "/logout" will redirect to logout() function.
    # Output: session clear
    # ##########################
    session.clear()
    return "success"

@app.route("/notifications")
@login_required
def notifications():
    ############################
    # notifications() function displays user notifications.
    # route "/notifications" will redirect to notifications() function.
    # input: The function takes session as the input
    # Output: Our function will render the notifications page
    # ##########################
    
    user_id = session.get('user_id')
    notifications = list(mongo.db.notifications.find({'user_id': user_id}).sort('timestamp', -1))
    
    return render_template('notifications.html', notifications=notifications)


@app.route("/dummy", methods=['GET'])
def dummy():
    # ############################
    # dummy() function performs the functionality displaying the message "feature will be added soon"
    # route "/dummy" will redirect to dummy() function.
    # Output: redirects to dummy.html
    # ##########################
    """response = make_response(
                redirect(url_for('home'),200),
            )
    response.headers["Content-Type"] = "application/json",
    response.headers["token"] = "123456"
    return response"""
    return "Page Under Maintenance"

if __name__ == '__main__':
    scheduler.add_job(func=fetch_tasks, trigger="cron", day_of_week = "*", hour = 00, minute = 00)
    scheduler.start()
    app.run(debug=True, use_reloader = False)