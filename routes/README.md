# Task Manager Application

![Task Manager](https://img.shields.io/badge/Task%20Manager-1.0.0-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-green)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.x-orange)

A modern and efficient task management application built with Flask, SQLAlchemy, and SQLite, designed to help users organize their tasks and manage their productivity.

## ✨ Features

- **User Authentication**: Secure login and registration system
- **Task Management**: Create, update, and delete tasks
- **Group Organization**: Categorize tasks into custom color-coded groups
- **Responsive UI**: Clean and intuitive user interface
- **Database Migrations**: Using Flask-Migrate for versioned database schema changes

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

2. **Create and activate a virtual environment**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install required packages**

```bash
pip install -r requirements.txt
```

4. **Initialize the database**

```bash
flask db upgrade
```

5. **Run the application**

```bash
python app.py
```

The application will be available at `http://localhost:5000`.

## 🛠️ Project Structure

```
task-manager/
├── app.py                 # Application entry point
├── models/
│   └── models.py          # Database models
├── routes/
│   ├── auth.py            # Authentication routes
│   └── other.py           # Task and group management routes
├── auths/
│   └── forms.py           # Form definitions
├── templates/             # HTML templates
├── migrations/            # Database migrations
└── instance/              # SQLite database
```

## 📊 Database Schema

The application uses three main models:
- **User**: Stores user account information
- **Task**: Represents individual tasks
- **Group**: Organizes tasks into categories

## 💡 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👏 Acknowledgments

- Flask framework
- SQLAlchemy ORM
- Flask-Login for authentication
- Flask-WTF for form handling

---

© 2025 Task Manager | Made with ❤️