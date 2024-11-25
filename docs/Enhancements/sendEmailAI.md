
# Send AI Email Schedule Feature

## Overview
The "Send AI Email Schedule" feature uses **Gemini AI** to generate and email a personalized task schedule to users. This feature ensures that users receive professional, structured, and motivating emails summarizing their tasks.

---

## Frontend Implementation
### HTML & JavaScript Integration
1. **Button in Dashboard**: 
    - The "Send Schedule" button (`#sendTaskEmail`) is located in the task dashboard, next to the "Export to CSV" button.
    - Upon clicking this button, a modal dialog is displayed to indicate the email's sending status.

2. **Frontend Workflow**:
    - When the button is clicked, it:
        1. Disables itself and updates its text to "Sending...".
        2. Sends an AJAX request to the backend `/send_task_email` route.
        3. Displays a modal with either:
            - A success message if the email is sent.
            - An error message if the process fails.

3. **Modal Dialog**:
    - A Bootstrap modal (`#emailSentModal`) is used to inform the user about the status of their email (success or failure).

### Frontend JavaScript Code
```javascript
$('#sendTaskEmail').click(function() {
    const button = $(this);
    const modalBody = $('#emailStatusMessage');
    
    button.prop('disabled', true);
    button.html(' Sending...');
    
    modalBody.html(`
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3">Generating your personalized schedule...</p>
        </div>
    `);
    
    $('#emailSentModal').modal('show');
    
    $.ajax({
        url: '/send_task_email',
        method: 'POST',
        success: function(response) {
            modalBody.html(`
                <div class="text-center">
                    <i class="fas fa-check-circle text-success fa-3x"></i>
                    <p class="mt-3">Task schedule has been sent to your email!</p>
                </div>
            `);
        },
        error: function(xhr) {
            const errorMsg = xhr.responseJSON?.error || 'Failed to send email. Please try again.';
            modalBody.html(`
                <div class="text-center">
                    <i class="fas fa-times-circle text-danger fa-3x"></i>
                    <p class="mt-3">${errorMsg}</p>
                </div>
            `);
        },
        complete: function() {
            button.prop('disabled', false);
            button.html(' Send Schedule');
        }
    });
});
```

---

## Backend Implementation
### Flask Route: `/send_task_email`
- **Route**: `POST /send_task_email`
- **Purpose**: Handles email sending requests by fetching tasks and using Gemini AI to generate email content.
- **Steps**:
    1. Validates that the user's email is present in the session.
    2. Retrieves tasks from the database using the `get_user_tasks` function.
    3. Generates an AI-powered email using the `generate_task_prompt` function.
    4. Sends the email via SMTP using Flask-Mail.

### Supporting Functions
#### 1. **`generate_task_prompt(tasks)`**
- **Purpose**: Constructs a prompt for Gemini AI to create a professional email.
- **Logic**:
    - Groups tasks into three categories:
        - Today's Tasks
        - This Week's Tasks
        - This Month's Tasks
    - Constructs a detailed and structured prompt that asks Gemini AI to create a motivational email with sections like:
        - Introduction
        - Task Breakdown
        - Prioritization Suggestions
        - Work-Life Balance Tips

#### 2. **`send_task_email(user_email, tasks)`**
- **Purpose**: Calls Gemini AI to generate email content and sends it to the user's email.
- **Key Steps**:
    - Uses the `generate_task_prompt` function to create a task-based prompt.
    - Calls Gemini AI's `generate_content` function to get the email text.
    - Converts the AI-generated markdown content into HTML using `markdown2`.
    - Sends the email using Flask-Mail.

#### 3. **`get_user_tasks(user_str_id)`**
- **Purpose**: Fetches user tasks due within the next 31 days from the MongoDB database.
- **Query**:
    - Filters tasks by the user's ID (`user_id`).
    - Includes only tasks due within the next 31 days.

### Python Code
```python
@app.route('/send_task_email', methods=['POST'])
def handle_email_request():
    try:
        user_email = session.get('email')
        if not user_email:
            return jsonify({'error': 'User email not found'}), 400

        user_id = session.get('user_id')
        tasks = get_user_tasks(user_id)
        
        success = send_task_email(user_email, tasks)
        if success:
            return jsonify({'message': 'Email sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send email'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

---

## AI Integration: Gemini AI
- **API Key**: Configured using the `genai.configure(api_key=GEMINI_API_KEY)` function.
- **Model**: Utilizes the `gemini-pro` model to generate content based on the provided task prompt.
- **Prompt Example**:
    ```
    As a professional task management assistant, create a concise, professional, and motivating email response for a user's task list. Use the following task data:
    - **Today's Tasks (X):** [Task List]
    - **This Week's Tasks (Y):** [Task List]
    - **This Month's Tasks (Z):** [Task List]
    ...
    ```

---

## Email Structure
- **Introduction**: Warm greeting and motivational tone.
- **Task Breakdown**: Categorized list of tasks.
- **Prioritization**: Suggestions for managing tasks efficiently.
- **Work-Life Balance Tips**: Brief tips for maintaining balance.
- **Conclusion**: Encouraging sign-off.

---

## Error Handling
- If the user's email is not found: Returns a `400` error with a relevant message.
- If tasks fail to load: Logs debug information and skips email generation.
- If email fails to send: Returns a `500` error.

---

## Dependencies
1. **Flask Extensions**:
    - `Flask-Mail`: For sending emails.
    - `PyMongo`: For database operations.
    - `Flask-Session`: For session management.
2. **Gemini AI SDK**:
    - Used for generating professional email content.
3. **Bootstrap Modal**: For user feedback on email status.
4. **jQuery**: For AJAX requests and DOM manipulation.

---

## Conclusion
This feature allows users to receive a professionally generated schedule email directly from their task dashboard. The combination of Flask, Gemini AI, and a user-friendly frontend ensures a seamless experience.

![Screenshot (32)](https://github.com/user-attachments/assets/b24a3c05-1312-4e7e-a593-9a0a67f764bb)

![Screenshot (33)](https://github.com/user-attachments/assets/c8c9026a-4317-4d0f-b97f-7bacc484f984)

![Screenshot (34)](https://github.com/user-attachments/assets/f9a15fd8-8e58-485e-83d0-33a6504a95f3)


# How to Send an AI-Generated Email Schedule?
* Log in to the application and ensure that your email is set in the session.

* Navigate to the "All Tasks" page in the dashboard.


* Click the Send Schedule button located in the top-right corner of the task table.


* A modal will appear, showing a loading spinner and a message saying "Generating your personalized schedule...".


* Wait for the confirmation message in the modal, which will indicate whether the email was successfully sent.


* Check your registered email inbox for the AI-generated schedule, formatted based on your tasks.

Example interaction:

* User Action: Clicks the "Send Schedule" button.

* System Response: A modal displays the email generation process, and upon completion, shows a confirmation message.

* Result: The user receives a personalized email with tasks categorized into "Today," "This Week," and "This Month."


