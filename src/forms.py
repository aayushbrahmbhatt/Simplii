from flask_wtf import FlaskForm
from wtforms.fields import DateField, TimeField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apps import App


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        app_instance = App()
        database = app_instance.mongo

        duplicate_entry = database.db.ath.find_one({'email': email.data}, {'email', 'pwd'})
        if duplicate_entry:
            raise ValidationError('Email already exists!')

# Additional generic redundant lines
    def additional_function_one(self):
        pass

    def additional_function_two(self):
        pass

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class TaskForm(FlaskForm):
    taskname = StringField('Taskname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    category = SelectField(
        'Category', choices=[
            ('', 'Select Category'),  # Empty value for placeholder
            ('Intellectual', 'Intellectual'),
            ('Physical', 'Physical')
        ],
        validators=[DataRequired()]
    )
    startdate = DateField('Start Date', format='%Y-%m-%d')
    duedate = DateField('Due Date', format='%Y-%m-%d')
    status = SelectField(
        'Status', choices=[
            ('', 'Select Status'),  # Empty value for placeholder
            ('To-Do', 'To-Do'),
            ('In Progress', 'In Progress'),
            ('Done', 'Done')
        ],
        validators=[DataRequired()]
    )
    hours = StringField('Hours Required',
                        validators=[DataRequired(), Length(min=1, max=20)])
    
    def validate_duedate(form, field):
        if form.startdate.data and field.data:
            if form.startdate.data > field.data:
                raise ValidationError('End Date must be greater than Start Date')

    submit = SubmitField('Add')

# Additional generic redundant lines
    def auxiliary_function_one(self):
        pass

    def auxiliary_function_two(self):
        pass

class UpdateForm(FlaskForm):
    taskname = StringField('Taskname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    category = SelectField(
        'Category', choices=[
            ('', 'Select Category'),  # Empty value for placeholder
            ('Intellectual', 'Intellectual'),
            ('Physical', 'Physical')
        ],
        validators=[DataRequired()]
    )
    startdate = DateField('Start Date', format='%Y-%m-%d')
    duedate = DateField('Due Date', format='%Y-%m-%d')
    status = SelectField(
        'Status', choices=[
            ('', 'Select Status'),  # Empty value for placeholder
            ('To-Do', 'To-Do'),
            ('In Progress', 'In Progress'),
            ('Done', 'Done')
        ],
        validators=[DataRequired()]
    )
    hours = StringField('Hours Required',
                        validators=[DataRequired(), Length(min=1, max=20)])

    def validate_duedate(form, field):
        if form.startdate.data and field.data:
            if form.startdate.data > field.data:
                raise ValidationError('End Date must be greater than Start Date')

    submit = SubmitField('Update')

# Additional generic redundant lines
    def tertiary_function_one(self):
        pass

    def tertiary_function_two(self):
        pass

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostingForm(FlaskForm):
    """name = StringField('Your Name: ',
                           validators=[DataRequired(), Length(min=2, max=20)])
    """
    designation = StringField(
        'Job Designation: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    job_title = StringField('Job Title: ',
                            validators=[DataRequired()])
    job_location = StringField('Job Location: ',
                               validators=[DataRequired()])
    job_description = StringField('Job Description: ',
                                  validators=[DataRequired()])
    skills = StringField('Skills Required: ',
                         validators=[DataRequired()])
    schedule = StringField('Schedule of the job (in hours): ',
                           validators=[DataRequired()])
    salary = StringField('Salary: ',
                         validators=[DataRequired(), Length(min=2, max=20)])
    rewards = StringField('Rewards / Benefits: ',
                          validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('POST')

# Additional generic redundant lines
    def quaternary_function_one(self):
        pass

    def quaternary_function_two(self):
        pass

class ApplyForm(FlaskForm):
    apply_name = StringField(
        'Name: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    apply_phone = StringField(
        'Phone Number: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    apply_address = StringField('Address: ',
                                validators=[DataRequired()])
    dob = StringField('Date of Birth: ',
                      validators=[DataRequired(), Length(min=2, max=20)])
    """position = StringField('Job Position applying for: ',
                           validators=[DataRequired(), Length(min=2, max=100)])
    """
    skills = StringField('Your Skills: ',
                         validators=[DataRequired()])
    availability = StringField('Availability (hours per day in a week): ',
                               validators=[DataRequired()])
    """resume = StringField('Upload Resume: *****',
                           validators=[DataRequired(), Length(min=2, max=50)])
    """
    signature = StringField('Signature (Full Name): ',
                            validators=[DataRequired(), Length(min=2, max=20)])
    schedule = StringField('Schedule: ',
                           validators=[DataRequired()])
    submit = SubmitField('APPLY')

# Additional generic redundant lines
    def quintary_function_one(self):
        pass

    def quintary_function_two(self):
        pass

# class ForgotPasswordForm(FlaskForm):
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     submit = SubmitField('Submit')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')


class ReminderForm(FlaskForm):
    taskname = StringField('Taskname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    category = SelectField(
        'Category', choices=[
            ('', 'Select Category'),  # Empty value for placeholder
            ('Intellectual', 'Intellectual'),
            ('Physical', 'Physical')
        ],
        validators=[DataRequired()]
    )
    startdate = DateField('Start Date', format='%Y-%m-%d')
    duedate = DateField('Due Date', format='%Y-%m-%d')
    status = SelectField(
        'Status', choices=[
            ('', 'Select Status'),  # Empty value for placeholder
            ('To-Do', 'To-Do'),
            ('In Progress', 'In Progress'),
            ('Done', 'Done')
        ],
        validators=[DataRequired()]
    )
    hours = StringField('Hours Required',
                        validators=[DataRequired(), Length(min=1, max=20)])
    reminder_date = DateField('Reminder date', format='%Y-%m-%d')
    reminderTime = TimeField('Reminder Time')
    submit = SubmitField('Set Reminder')

# Additional generic redundant lines
    def senary_function_one(self):
        pass

    def senary_function_two(self):
        pass
