# Smart URL Shortener with QR Code Generation

A secure and responsive URL Shortener web application built using Flask, SQLAlchemy, SQLite, and Bootstrap. The application allows users to register, log in, generate shortened URLs, and automatically create QR codes for each shortened link.

--

## 🚀 Features

- User Registration & Login System
- Password Hashing using Werkzeug
- Session-Based Authentication
- URL Shortening Functionality
- Dynamic URL Redirection
- QR Code Generation for Short URLs
- User-Specific Dashboard
- Responsive Bootstrap UI
- SQLite Database Integration
- Flash Messages & Validation

---

## 🛠️ Technologies Used

- Python
- Flask
- SQLAlchemy
- SQLite
- Bootstrap 5
- HTML5
- CSS3
- Jinja2
- Werkzeug Security
- QRCode Library

---

## 📂 Project Structure

project/
│
├── static/
│   └── qr_codes/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   └── register.html
│
├── instance/
│   └── urls.db
│
├── main.py
├── requirements.txt
└── README.md

---

## ⚙️ Installation & Setup

### 1. Clone Repository

git clone <repository-link>

### 2. Create Virtual Environment

python -m venv .venv

### 3. Activate Virtual Environment

Windows:
.venv\Scripts\activate

### 4. Install Dependencies

pip install -r requirements.txt

### 5. Run Application

python main.py

---

## 🔐 Authentication Flow

- Users register with username and password
- Passwords are securely hashed before storage
- Session management is used for login/logout functionality
- Protected routes prevent unauthorized access

---

## 🔗 URL Shortening Workflow

1. User enters original URL
2. System generates unique short code
3. Short URL is stored in database
4. QR Code is generated automatically
5. Clicking short URL redirects to original website

---

## 📸 QR Code Generation

Each generated short URL automatically creates:
- QR image
- Stored in static/qr_codes/
- Displayed on dashboard
