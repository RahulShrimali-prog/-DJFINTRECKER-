# 💰 DJFINTRECKER

**DJFINTRECKER** is a personal finance tracking web app built using Django. It allows users to manage and track their income and expenses with ease.

## 🔧 Features

- 🧾 Add, edit, and delete income & expense entries
- 📊 View financial summary and balance
- 🔐 User authentication (Login/Logout)
- 🎨 Clean and responsive Bootstrap 5 design
- 🗃️ SQLite database for data storage

## 🗂️ Project Structure

djfintracker/
├── djfintracker/ # Project settings
├── finance/ # Finance tracking app
├── db.sqlite3 # Database
├── manage.py # Entry point



## ⚙️ How to Run the Project Locally

```bash
# Step 1: Clone the repository
git clone https://github.com/yourusername/djfintracker.git
cd djfintracker

# Step 2: Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux

# Step 3: Install requirements
pip install -r requirements.txt

# Step 4: Apply migrations
python manage.py migrate

# Step 5: Run the server
python manage.py runserver
