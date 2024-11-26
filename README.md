
# Simplii - Task Management Web and Android Application
[![DOI](https://zenodo.org/badge/720901435.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Github](https://img.shields.io/badge/language-python-red.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Code Coverage]()
[![Python Style Checker](https://github.com/CSC510SEFALL2024/Simplii/actions/workflows/style_checker.yml/badge.svg)](https://github.com/CSC510SEFALL2024/Simplii/actions/workflows/style_checker.yml)
[![Close as a feature](https://github.com/CSC510SEFALL2024/Simplii/actions/workflows/close_as_a_feature.yml/badge.svg)](https://github.com/CSC510SEFALL2024/Simplii/actions/workflows/close_as_a_feature.yml)
[![GitHub version](https://img.shields.io/github/v/release/CSC510SEFALL2024/Simplii)](https://github.com/prateeksingamsetty/Simplii/releases)
[![Lint Python](https://github.com/CSC510SEFALL2024/Simplii/actions/workflows/syntax_checker.yml/badge.svg)](https://github.com/CSC510SEFALL2024/Simplii/actions/workflows/syntax_checker.yml)

<a href="https://github.com/CSC510SEFALL2024/Simplii/forks" target="blank">
<img src="https://img.shields.io/github/forks/CSC510SEFALL2024/Simplii?style=flat-square" alt="Simplii forks"/>
</a>
<a href="https://github.com/CSC510SEFALL2024/Simplii/stargazers" target="blank">
<img src="https://img.shields.io/github/stars/CSC510SEFALL2024/Simplii?style=flat-square" alt="Simplii stars"/>
</a>
<a href="https://github.com/CSC510SEFALL2024/Simplii/issues" target="blank">
<img src="https://img.shields.io/github/issues/CSC510SEFALL2024/Simplii?style=flat-square" alt="Simplii issues"/>
</a>
<a href="https://github.com/CSC510SEFALL2024/Simplii/issues?q=is%3Aissue+is%3Aclosed" target="blank">
<img src="https://img.shields.io/github/issues-closed/CSC510SEFALL2024/Simplii" alt="Simplii issues closed"/>
</a>
<a href="https://github.com/CSC510SEFALL2024/Simplii/pulls" target="blank">
<img src="https://img.shields.io/github/issues-pr/CSC510SEFALL2024/Simplii?style=flat-square" alt="Simplii pull-requests"/>
</a>

# Simplii 5.0

<h3>Are you trying to manage tasks? Simplii keep track of them, with all new Simplii 5.0!!! </h3>

Simplii is a versatile task management application available on both web and Android platforms. It offers a seamless experience for managing tasks efficiently.

# App Hosting

## Link to Demonstration Video of the Project: 


# Table of Contents  

- [Why Simplii?](#why-simplii)
- [Use Case](#use-case)
- [Built with:](#built-with)
- [Enhancements](#enhancements)
  - [Register](#register)
  - [Welcome Email](#welcome-email)
  - [Login](#login)
  - [Dashboard](#dashboard)
  - [Dashbord Filters](#dashboard-filters)
  - [About Page](#about-page)
  - [Add Task Page](#add-task-page)
  - [Edit Task Page](#edit-task-page)
  - [Deadlines](#deadlines)
  - [Kanban Board](#kanban-board)
  - [Reminder Schedule](#reminder-schedule)
  - [MongoDB Users Table](#mongodb-users-table)
  - [MongoDB Tasks Table](#mongodb-tasks-table)
  - [MongoDB Reminders Table](#mongodb-reminders-table)
- [Steps for Execution:](#steps-for-execution)
- [Source Code](#source-code)
- [Delta](#delta)
- [Future Scope](#future-scope)
- [Team Members](#team-members)
- [Contribution](#contribution)
- [License](#license)

## Why Simplii?

- Simplii has a user-friendly UI, equally appealing to people of all ages and also people learning to use technology.
- Multi-User Login
- User can add new tasks based on their category.<br>
- Users can update tasks as and when they work on them.<br>
- User can keep track of not just work that is in progress, but also completed tasks.<br>
- Tasks can be viewed based on the priority of the deadline.<br>
- Users can set up email reminders when a task approaches a deadline.<br>
- A kanban board type of view for easy tasks status visualization.<br>
- Users can set reminders of important tasks and plan accordingly.

## Use Case

- All people who love to multi-task their way through life would love Simplii as it helps them keep track of various tasks in the most simple manner.
- Anyone who is new to technology and would be overwhelmed by amazing and well-developed organizing applications like Google Calendar/Apple Calendar would love Simplii.
- Anyone with a need to keep up with the day-to-day tasks and wants to manage them effectively.

## Built with:

- Python
- JavaScript
- HTML5
- CSS3
- Bootstrap
- Flask
- MongoDB
- Android Studio
- Firebase

## Features

### User Interface Register 
<p> You can create your own account and register on the website. You can store your data and can access the data whenever required. </p>
<p align="center"><img width="700" src="./assets/Register.png"></p>

### Welcome Email 
<p> Once your register for Simplii, you get a welcome email from us appreciating your interest in using our website and welcoming you onboard. </p>
<p align="center"><img width="700" src="./assets/welcome email.png"></p>

### Email Verification using Regex
<p>Check if the Email is valid or not.</p>
<p align="center"><img width="700" src="./assets/Regex.png"></p>

### OTP verification
<p>OTP is sent to the email ID of the User trying to login and it is verified.</p>
<p align="center"><img width="700" src="./assets/OTP.png"></p>
<p align="center"><img width="700" src="assets/otp1.jpg"></p>
<p align="center"><img width="700" src="assets/otp sent.jpg"></p>
 
### User Interface Login 
<p> Once you create an account, you can login to the website using your credentials </p>
<p align="center"><img width="700" src="./assets/login .png"></p>
 
### Dashboard
<p> Once you login, you see your dashboard </p>
<p align="center"><img width="700" src="./assets/dashboard.png"></p>

### Dashboard Filters
<p> Dashboard's tasks listed can be filtered and viewed as per the user requirements. </p>
<p align="center"><img width="700" src="./assets/filter.png"></p>

### User Interface About Page
<p> When you click on the about on the navigation bar, you are redirected to a page that consists information about Simplii </p>
<p align="center"><img width="700" src="./assets/about.png"></p>

### Add Task Page
<p> When you click on the add task on the navigation bar, you are redirected to a page that consists of a form. Here, you can fill the details regarding the task you want to add and click on add task. The task is added to the database and you can view it on the dashboard </p>
<p align="center"><img width="700" src="./assets/add task.png"></p>

### Edit Task Page
<p> When you view the task on the dashboard, you can see the option to edit the task details. When you click on edit, the edit task form opens up and you can make necessary changes to the task details and update them. </p>
<p align="center"><img width="700" src="./assets/update task.png"></p>

### Chatbot Integrated
<p>Chatbot is implemented as a new feature which will guide to manage your task and assist you with any queries related to the chatbot</p>
<p align="center"><img width="700" src="./assets/chatbot.jpg"></p>
<p align="center"><img width="700" src="./assets/chatbot example.jpg"></p>

### Deadlines
<p> When you click on the deadline tab on the navigation bar, you are redirected to the deadlines page. This page consists of all your tasks in the order of

 deadlines. The deadlines are categorized based on the priority as 1 day left, 3 days left, 5 days left and overdue. When the task is overdue, it is highlighted in red and a mail is sent to the user notifying that the deadline for a particular task is done. </p>
<p align="center"><img width="700" src="./assets/recommend.png"></p>

### Kanban Board
<p> Tasks are also organized in kanban board type of view to help users visualize the status of the task easily. </p>
<p align="center"><img width="700" src="./assets/kanbanBoard.png"></p>

### Reminder Schedule
<p> Reminders are scheduled to notify the user when a task deadline is approaching. Users can schedule reminders from the dashboard. </p>
<!-- <p align="center"><img width="700" src="./assets/reminder schedule.png"></p> -->

## Enhancements
### Dark Mode
<p> Added persistant dark and light themes to the application.  
  
* _Light Theme Application SS:_
  
![Screenshot 2024-11-25 152147](https://github.com/user-attachments/assets/b405f266-18fd-49e3-b353-3a6a881baf2d)


* _Dark Theme Application SS:_

![Screenshot 2024-11-25 152235](https://github.com/user-attachments/assets/626f7c69-f219-452a-a11d-abab0883f2a3)

### AI Email Schedule and Tasks

* Loading animation while sending email.

![Screenshot (32)](https://github.com/user-attachments/assets/e6a4888b-8a15-488a-b532-a9b6f715ee20)

* Acknowledgement for email send.

![Screenshot (33)](https://github.com/user-attachments/assets/dc30ee13-4915-409d-953a-65ad7f9e93cd)

* Example email synthesized using AI

![Screenshot (34)](https://github.com/user-attachments/assets/5621b87f-c94f-4436-8870-d21a4916a904)

### Export tasks to .csv file

* Users can export current tasks to a csv file and download

![Screenshot 2024-11-25 153519](https://github.com/user-attachments/assets/adfe8584-7701-48d9-ae1a-9a72b00d23cc)


### MongoDB Users Table
<p> Users details are saved in the database. User's data is protected.</p>
<p align="center"><img width="700" src="./assets/mongodb users.png"></p>

### MongoDB Tasks Table
<p> Tasks related data of each user is stored in the MongoDB tasks table.</p>
<p align="center"><img width="700" src="./assets/mongodb tasks.png"></p>

### MongoDB Reminders Table
<p> Reminders are stored and managed in the MongoDB reminders table.</p>
<p align="center"><img width="700" src="./assets/mongodb reminders.png"></p>

## Steps for Execution:

1. Clone the repository: `git clone https://github.com/aayushbrahmbhatt/Simplii.git`
2. Install the necessary dependencies: `pip install -r requirements.txt`
3. Run the application: `python app.py`

## Delta

- **Added Dark Mode**: Added persisting dark mode to the application. 
- **Export Task to .csv**: Users can export their tasks to a csv file
- **AI Schedule Email**: Receive email from AI to get a brief of your tasks and a schedule. 

## Future Scope

1. Add AI-driven task prioritization.
2. Integrate with other calendars like Google Calendar.
3. Add dark mode for the mobile application.
4. Improve notifications for the mobile application.

## Team Members

- **Anurag Gorkar** - AnuragGorkar
- **Aryan Iguva** - aryansharma2k2
- **Harsh Vora** - harshvora7

## Contribution

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
