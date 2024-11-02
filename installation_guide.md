```markdown
# Installation Guide

## Prerequisites

1. **Python 3.8 or above** - Download and install from [Python's official website](https://www.python.org/downloads/).
2. **MongoDB** - Install MongoDB Community Edition by following the guide on [MongoDB's official website](https://docs.mongodb.com/manual/installation/).
3. **Git** - Install Git for version control by following the guide on [Git's official website](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Steps for Setup and Execution

1. **Clone the repository**
   ```bash
   git clone https://github.com/aayushbrahmbhatt/Simplii.git
   cd Simplii
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add the following environment variables:
   ```plaintext
   MONGO_URI=mongodb://localhost:27017/simplii
   SECRET_KEY=your_secret_key
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=465
   MAIL_USE_SSL=True
   MAIL_USERNAME=your_email@gmail.com
   MAIL_PASSWORD=your_password
   ```

5. **Run MongoDB Locally**

   Start the MongoDB server in a new terminal window:
   ```bash
   mongod
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**

   Open your web browser and go to:
   ```
   http://127.0.0.1:5000/
   ```

8. **Testing**

   Run tests to ensure the application functions as expected:
   ```bash
   python -m unittest discover -s tests
   ```

9. **Deactivating the Virtual Environment** (when done)
   ```bash
   deactivate
   ```

## Troubleshooting

- **MongoDB Connection Issues**: Ensure MongoDB is running on the default port 27017.
- **Environment Variables Not Set**: Check the `.env` file for correct formatting.
- **Email Issues**: Make sure your email server settings and credentials are correct.

For additional help, refer to the official documentation or open an issue on the [GitHub repository](https://github.com/aayushbrahmbhatt/Simplii/issues).
```
