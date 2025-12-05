# MySecureApp — CA3 Secure Application Programming Project

This repository contains an open-source Python Flask web application developed for the CA3 Secure Application Programming project. The purpose of this project is to demonstrate insecure coding practices, identify vulnerabilities, and then implement secure controls following best practices and OWASP guidelines.

The project includes **two versions** of the same application:
- **Insecure Version** — intentionally vulnerable (SQL Injection, XSS, Sensitive Data Exposure)
- **Secure Version** — fully patched version with all mitigations applied (CSRF, hashing, parameterized SQL, security headers)

---

## 📌 Branch Structure

| Branch | Description |
|--------|-------------|
| `main` | Default GitHub branch (not used for development) |
| `insecure` | Fully insecure, intentionally vulnerable implementation |
| `secure` | Secure, professionally hardened implementation |

Use the GitHub branch selector to switch between secure and insecure versions.

---

# 🚀 How to Install & Run the Application

## 1️⃣ Clone the Repository
```bash 
git clone https://github.com/akz0015z/MySecureApp.git
cd MySecureApp

```
# 🔴 Running the Insecure Version (Intentionally Vulnerable)

**Switch to insecure branch:**  
```bash
git checkout insecure
```

**Install dependencies:**  
```bash
pip install -r requirements.txt
```

**Run the application:**  
```bash
python app.py
```

### ❌ Insecure Features (on purpose)
- ❌ SQL Injection vulnerabilities  
- ❌ Stored XSS  
- ❌ Reflected XSS  
- ❌ DOM-Based XSS  
- ❌ Plaintext password storage  
- ❌ No CSRF protection  
- ❌ No security headers  
- ❌ Weak session management  
- ❌ No logging or monitoring  

**The insecure version is used for:**  
- Demonstrating vulnerabilities  
- ZAP scanning  
- Documentation of OWASP Top 10 issues  


---

# 🟢 Running the Secure Version (Fully Patched)

**Switch to secure branch:**  
```bash
git checkout secure
```

**Install secure dependencies:**  
```bash
pip install flask-wtf flask-bcrypt flask-talisman email-validator
pip install -r requirements.txt
```

**Run the application:**  
```bash
python app.py
```

---

## ✅ Secure Features Implemented
- ✅ Parameterized SQL (SQL Injection Prevention)  
- ✅ Password Hashing (Flask-Bcrypt)  
- ✅ CSRF Protection (Flask-WTF)  
- ✅ Security Headers & CSP (Flask-Talisman)  
- ✅ Sanitized Inputs (XSS Mitigation)  
- ✅ Strong Session Management  
- ✅ Logging & Monitoring (`logs/app.log`)  
- ✅ Homepage redirect to `/login`  


---

# 📁 Project Technology Stack
- Python 3  
- Flask Web Framework  
- SQLite3 Database  
- Flask-WTF (CSRF protection)  
- Flask-Bcrypt (Password hashing)  
- Flask-Talisman (Security Headers + CSP)  
- HTML / CSS Templates  
- Git & GitHub version control  


---

# 🛠 Branch Switching Commands
```bash
git checkout insecure   # Use the insecure version
git checkout secure     # Use the secure version
git checkout main       # Default branch (not used for development)
```


---

# 🌿 Logging (Secure Version Only)

Logs stored at:
```
logs/app.log
```

Logged events include:
- User registration  
- User login  
- Profile updates  
- Timestamps for monitoring  


---

# 👤 Author
**Student:** akz0015z  
**Developed for:** Secure Application Programming  


---

# 🔗 Repo Link  
https://github.com/akz0015z/MySecureApp

---
