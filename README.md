<div align="center">

# 🗂️ Task Manager Web Application

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4%2B-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwind-css&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A modern, full-stack task management solution built with Django and MongoDB**

[Features](#-features) • [Demo](#-screenshots) • [Installation](#-installation) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🎯 Overview

Task Manager is a **production-ready** web application designed to streamline personal and team productivity. Built with modern web technologies, it offers a seamless experience for creating, organizing, and tracking tasks with enterprise-grade security and scalability.

### Why Task Manager?

- 🔐 **Secure Authentication** - Built on Django's robust authentication system
- 🚀 **High Performance** - Leveraging MongoDB's NoSQL capabilities for fast data operations
- 📱 **Responsive Design** - Beautiful UI that works flawlessly across all devices
- 🎨 **Modern Interface** - Clean, intuitive design with Tailwind CSS
- 🔒 **Data Isolation** - Complete privacy with user-specific task management

---

## ✨ Features

### 🔐 Authentication & Security
- User registration with validation
- Secure login/logout functionality
- Session-based authentication
- Protected routes with `@login_required` decorator
- Password encryption and secure storage

### 📝 Task Management
- **Full CRUD Operations** - Create, Read, Update, and Delete tasks effortlessly
- **Rich Task Attributes** - Title, description, priority levels, and due dates
- **Status Tracking** - Toggle between Completed and Pending states
- **Priority Levels** - Low, Medium, and High priority classification
- **Bulk Operations** - Clear all completed tasks in one click

### 📊 Dashboard & Analytics
- **Real-time Statistics** - Live counters for total, pending, and completed tasks
- **Smart Filtering** - Filter by status (All, Pending, Completed) and priority (High)
- **Visual Indicators** - Color-coded priority badges and status markers
- **Progress Tracking** - Monitor task completion rates at a glance

### 🎨 User Experience
- **Responsive Design** - Optimized for desktop, tablet, and mobile devices
- **Modern UI** - Gradient accents and smooth transitions
- **Toast Notifications** - Instant feedback for all user actions
- **Intuitive Navigation** - Clean, user-friendly interface

---

## 📸 Screenshots

<div align="center">

### 🔑 Authentication

<table>
  <tr>
    <td width="50%">
      <img src="images/Login.png" alt="Login Page" />
      <p align="center"><strong>Secure Login Interface</strong></p>
    </td>
    <td width="50%">
      <img src="images/Register.png" alt="Register Page" />
      <p align="center"><strong>User Registration</strong></p>
    </td>
  </tr>
</table>

### 📊 Dashboard & Task Management

<table>
  <tr>
    <td width="50%">
      <img src="images/Dashbord.png" alt="Dashboard" />
      <p align="center"><strong>Analytics Dashboard</strong></p>
    </td>
    <td width="50%">
      <img src="images/Tasks.png" alt="Task Management" />
      <p align="center"><strong>Task Management Interface</strong></p>
    </td>
  </tr>
</table>

### 🗄️ Database Architecture

<img src="images/MongoDB.jpeg" alt="MongoDB Structure" width="80%" />
<p align="center"><strong>MongoDB Compass - Database View</strong></p>

</div>

---

## 🛠️ Tech Stack

<div align="center">

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwind-css&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)

### Database
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![PyMongo](https://img.shields.io/badge/PyMongo-13AA52?style=flat-square&logo=mongodb&logoColor=white)

### Tools & DevOps
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat-square&logo=visual-studio-code&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat-square&logo=postman&logoColor=white)

</div>

### Technology Details

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, Tailwind CSS, JavaScript | Responsive UI with modern styling |
| **Backend** | Django 5.0, Python 3.10+ | RESTful API and business logic |
| **Database** | MongoDB 4.4+ | NoSQL document storage for tasks |
| **Authentication** | Django Auth + SQLite | User management and sessions |
| **Driver** | PyMongo | MongoDB integration |

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                     Client Browser                      │
│                   (HTML/CSS/JS)                         │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP/HTTPS
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Django Backend                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Views      │  │  Middleware  │  │   Forms      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────┬────────────────────────────────┬───────────┘
             │                                │
             ▼                                ▼
┌────────────────────────┐      ┌────────────────────────┐
│   SQLite Database      │      │   MongoDB Database     │
│  (User Auth/Sessions)  │      │   (Task Documents)     │
└────────────────────────┘      └────────────────────────┘
```

### Key Architecture Decisions

- **Hybrid Database Approach** - SQLite for Django authentication, MongoDB for task data
- **Direct PyMongo Integration** - No ORM overhead for maximum performance
- **RESTful API Design** - Clean separation between frontend and backend
- **Session-based Authentication** - Secure user sessions with Django middleware

---

## 🚀 Installation

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher** - [Download Python](https://www.python.org/downloads/)
- **MongoDB Community Server** - [Download MongoDB](https://www.mongodb.com/try/download/community)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **pip** (Python package manager)

### Step-by-Step Setup

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/yourusername/task-manager.git
cd task-manager
```

#### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

#### 4️⃣ Configure MongoDB

Ensure MongoDB is running on your system:

```bash
# Check if MongoDB is running
mongosh
```

Update `config/settings.py` if needed:

```python
# MongoDB Configuration
MONGODB_URI = "mongodb://localhost:27017"
MONGODB_NAME = "task_manager_db"
```

#### 5️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6️⃣ Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

#### 7️⃣ Start Development Server

```bash
python manage.py runserver
```

🎉 **Success!** Open your browser and navigate to:

👉 **http://127.0.0.1:8000/**

---

## 💻 Usage

### Quick Start Guide

1. **Register an Account** - Create your user profile
2. **Login** - Access your personal dashboard
3. **Create Tasks** - Add tasks with title, description, priority, and due date
4. **Manage Tasks** - Update status, edit details, or delete tasks
5. **Filter & Organize** - Use filters to focus on specific task categories
6. **Track Progress** - Monitor your productivity with dashboard statistics

### Task Creation

```javascript
// Example task structure
{
  "title": "Complete Project Documentation",
  "description": "Write comprehensive README and API docs",
  "priority": "High",
  "due_date": "2024-12-31",
  "status": "Pending",
  "user_id": "user@example.com"
}
```

---

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register/` | Create new user account |
| POST | `/login/` | Authenticate user |
| GET | `/logout/` | End user session |

### Task Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks/` | Retrieve all tasks |
| POST | `/tasks/create/` | Create new task |
| PUT | `/tasks/<id>/update/` | Update existing task |
| DELETE | `/tasks/<id>/delete/` | Delete task |
| POST | `/tasks/<id>/toggle/` | Toggle task completion |

---

## 🗺️ Roadmap

### Version 2.0 (Upcoming)

- [ ] 🏷️ Task categories and custom tags
- [ ] 📧 Email verification and notifications
- [ ] 🎯 Drag-and-drop task reordering
- [ ] 👥 Team collaboration features
- [ ] 📱 Progressive Web App (PWA) support
- [ ] 🐳 Docker containerization
- [ ] 📊 Advanced analytics and reporting
- [ ] 🔄 Task recurring/repetition
- [ ] 💾 Export tasks to CSV/PDF
- [ ] 🌙 Dark mode theme

### Long-term Goals

- [ ] Mobile native applications (iOS/Android)
- [ ] Integration with calendar services
- [ ] AI-powered task suggestions
- [ ] Real-time collaboration with WebSockets

---

## 🤝 Contributing

Contributions are what make the open-source community amazing! Any contributions you make are **greatly appreciated**.

### How to Contribute

1. **Fork the Project**
2. **Create your Feature Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting PR

---

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## 👨‍💻 Author

**Vivek**

- GitHub: [@VivekGhule](https://github.com/VivekGhule/Task_Manger)
- LinkedIn: [vivekghule7](https://www.linkedin.com/in/vivekghule7/)
- Email: vivekghule777@gmail.com

---

## 🙏 Acknowledgments

- [Django Documentation](https://docs.djangoproject.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/) for icons
- All contributors who help improve this project

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Built with ❤️ using Django and MongoDB**

[Report Bug](https://github.com/yourusername/task-manager/issues) • [Request Feature](https://github.com/yourusername/task-manager/issues)

</div>