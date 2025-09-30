# TechCorp Inventory System - Password Reset Vulnerability Lab

🎯 **Cybersecurity Training Environment**

A professional-grade vulnerable web application designed for cybersecurity education, featuring a realistic password reset vulnerability that demonstrates authentication bypass techniques.

## 🏢 Application Overview

**TechCorp Inventory System** is a corporate asset management platform with:

- **Professional Interface**: Modern dark theme with responsive design
- **Role-Based Access Control**: Admin, Manager, HR, Employee, Supervisor roles
- **Real Business Logic**: Inventory tracking, user management, and authentication
- **Vulnerable Password Reset**: Intentional security flaw for educational purposes

## 🎓 Learning Objectives

This training lab teaches:
- **Password Reset Vulnerabilities**: Token validation bypass and parameter manipulation
- **Authorization Flaws**: Missing validation leading to privilege escalation
- **Manual & Automated Testing**: Using tools like Burp Suite and Python scripts
- **Security Best Practices**: Proper authentication mechanism implementation

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** installed
- **Web browser** (Chrome/Firefox recommended)
- **Burp Suite** (optional, for manual exploitation)

### 🐳 Docker Hub Deployment (Recommended)

```bash
# Pull and run from Docker Hub
docker pull cyberctf/password-reset-broken-logic:latest
docker run -p 3206:3206 cyberctf/password-reset-broken-logic:latest

# Access the application
# http://localhost:3206
```

### �️ Local Development

```bash
# Development mode (with hot reload)
cd build/deploy
docker-compose -f docker-compose.dev.yml up --build

# Production mode
docker-compose up --build -d
```

## 🔐 Training Accounts

| Username | Password | Role | Department |
|----------|----------|------|------------|
| **admin** | password123 | Administrator | IT Security |
| **manager** | password123 | Manager | Operations |
| **employee** | password123 | Employee | General |

*Note: Use these credentials to explore the application, then exploit the password reset vulnerability to gain unauthorized admin access.*
## 🎯 The Vulnerability

**Critical Security Flaw**: Password reset mechanism with token validation bypass

### Technical Details
- **Vulnerability Type**: Broken Authentication Logic
- **Impact**: Account Takeover & Privilege Escalation
- **Root Cause**: Insufficient validation of reset tokens and user parameters
- **CVSS Score**: 9.8 (Critical)

### Exploitation Steps
1. **Reconnaissance**: Identify valid user accounts
2. **Password Reset Request**: Initiate reset for any user account
3. **Parameter Manipulation**: Intercept and modify username parameter
4. **Token Bypass**: Exploit missing validation to target admin account
5. **Account Takeover**: Successfully change admin password
6. **Privilege Escalation**: Access admin dashboard with personal data

## 🛠️ Exploitation Methods

### 🔥 Manual Exploitation (Burp Suite)

```bash
# 1. Setup Burp Suite proxy
# 2. Navigate to http://localhost:3206/forgot_password
# 3. Request password reset for any user
# 4. Intercept the request
# 5. Change username parameter to 'admin'
# 6. Forward request and set new admin password
# 7. Login as admin with new credentials
```

### � Automated Exploitation

```bash
# Run automated test suite
python build/app/tests/main.py

# Run specific exploit scripts
cd build/app/tests
python solve.py
```

## 🏗️ Technical Architecture

### Technology Stack
- **Backend**: Python Flask 2.3.3
- **Database**: SQLite with persistent storage
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions with automated testing
- **Registry**: Docker Hub for image distribution

### Security Features (Intentionally Vulnerable)
- ✅ **Session Management**: Basic Flask sessions
- ✅ **Password Hashing**: Secure password storage
- ❌ **Token Validation**: Missing validation in password reset
- ❌ **CSRF Protection**: Not implemented
- ❌ **Rate Limiting**: No brute force protection

## 📊 Project Structure

```
Password-Reset-Broken-Logic/
├── 📁 .github/workflows/        # CI/CD Pipeline
│   └── ci-cd.yml                # Docker Hub automation
├── 📁 build/                    # Application Code
│   ├── 📁 app/                  # Main Application
│   │   ├── app.py               # Flask server
│   │   ├── __init__.py          # Database initialization
│   │   ├── Dockerfile           # Container build
│   │   ├── requirements.txt     # Python dependencies
│   │   ├── 📁 templates/        # HTML templates
│   │   ├── 📁 static/           # CSS/JS assets
│   │   └── 📁 tests/            # Test suite
│   │       └── main.py          # Test runner (GitHub Actions)
│   └── 📁 deploy/               # Deployment Configuration
│       ├── README.md            # Deployment guide
│       └── docker-compose.dev.yml  # Development config
├── docker-compose.yml           # Production deployment
├── .gitignore                   # Git ignore rules
└── README.md                    # This documentation
```

## 🚀 Deployment Options

### 🌟 Option 1: Docker Hub (Recommended)
```bash
# Pull pre-built image
docker pull cyberctf/password-reset-broken-logic:latest

# Run container
docker run -p 3206:3206 cyberctf/password-reset-broken-logic:latest

# Access application
open http://localhost:3206
```

### 🛠️ Option 2: Local Development
```bash
# Development with hot reload
cd build/deploy
docker-compose -f docker-compose.dev.yml up --build

# Production build
docker-compose up --build -d
```

### 🧪 Option 3: Test Suite
```bash
# Run comprehensive tests
python build/app/tests/main.py

# CI/CD compatible testing
cd build/app/tests && python main.py
```

## 🐳 Docker Hub Integration

This project features **automated CI/CD** with Docker Hub:

- **Repository**: `cyberctf/password-reset-broken-logic:latest`
- **Auto-build**: Triggered on push to main/master branch  
- **Testing**: Automated test execution before build
- **Documentation**: README automatically synced to Docker Hub

### Environment Variables
```bash
# Optional configuration
FLASK_ENV=production          # Default: production
DATABASE_PATH=/app/data/      # Default: /app/data/
```

## 🎓 Learning Outcomes

### 🔍 Vulnerability Analysis Skills
- **Authentication Bypass**: Understand token validation weaknesses
- **Parameter Manipulation**: Master request interception and modification
- **Privilege Escalation**: Learn horizontal and vertical privilege escalation
- **Impact Assessment**: Evaluate business impact of security flaws

### 🛠️ Practical Skills
- **Manual Testing**: Hands-on exploitation with Burp Suite
- **Automated Testing**: Python scripting for security testing
- **Tool Proficiency**: Industry-standard penetration testing tools
- **Documentation**: Professional security reporting

### 🛡️ Defensive Knowledge
- **Secure Coding**: Understand proper authentication implementation
- **Validation Techniques**: Token validation and authorization best practices
- **Security Controls**: CSRF protection, rate limiting, and session management

## 🛡️ Remediation & Best Practices

### ✅ Immediate Fixes
```python
# Proper token validation
def validate_reset_token(token, username):
    stored_token = get_user_reset_token(username)
    if not stored_token or stored_token != token:
        raise InvalidTokenError()
    
    if token_expired(stored_token):
        raise ExpiredTokenError()
    
    return True

# Authorization check
def reset_password(token, username, new_password):
    validate_reset_token(token, username)
    validate_user_permissions(current_user, username)
    update_password(username, new_password)
```

### 🔒 Security Enhancements
1. **Token Expiration**: Implement 15-minute token expiry
2. **Rate Limiting**: Max 3 reset attempts per hour per IP
3. **CSRF Protection**: Add anti-CSRF tokens to forms
4. **Audit Logging**: Log all password reset activities
5. **Multi-Factor Authentication**: Add SMS/email verification

### 📋 Security Checklist
- [ ] Validate all user inputs
- [ ] Implement proper session management
- [ ] Add comprehensive logging
- [ ] Test for all OWASP Top 10 vulnerabilities
- [ ] Regular security assessments
- [ ] Employee security training

## � Training Scenarios

### 🔰 Beginner (Guided)
1. Follow step-by-step exploitation guide
2. Use provided test accounts
3. Focus on understanding concepts
4. Use automated tools for verification

### 🔥 Intermediate (Semi-Guided)
1. Manual exploitation with Burp Suite
2. Develop custom Python scripts
3. Explore additional attack vectors
4. Document findings professionally

### 🏆 Advanced (Free-Form)
1. Chain multiple vulnerabilities
2. Develop comprehensive exploit
3. Create detailed security assessment
4. Propose complete remediation plan

## ⚠️ Legal & Ethical Guidelines

### ✅ Authorized Use
- **Educational environments only**
- **Controlled lab settings**
- **With explicit permission**
- **For learning purposes**

### ❌ Prohibited Use
- **Production systems**
- **Without authorization**
- **Malicious purposes**
- **Illegal activities**

---

## 🎉 Get Started Now!

```bash
# Quick start with Docker Hub
docker run -p 3206:3206 cyberctf/password-reset-broken-logic:latest

# Open your browser
open http://localhost:3206

# Start your security journey!
```

**🎯 Ready to master password reset vulnerabilities? Launch the lab and start your ethical hacking journey!**

---

*This lab is designed for educational purposes only. Always obtain proper authorization before testing security vulnerabilities.*
- **Database**: SQLite with persistent storage
- **Frontend**: Modern dark theme with TailwindCSS
- **Security**: Session-based authentication with role controls
- **Deployment**: Docker containerized application

## Testing and Validation

### Automated Testing
```bash
cd test
pip install -r requirements.txt
pytest test_app.py -v
```

### Manual Exploitation
```bash
cd test
python solve.py
```

### Burp Suite Testing
The application is fully compatible with Burp Suite for manual penetration testing. Configure your browser proxy and intercept the password reset workflow to identify the vulnerability.

## Security Features

- Role-based access control (Admin, Manager, Employee)
- Session management and authentication
- Password hashing with SHA256
- Modern responsive web interface
- Comprehensive inventory tracking

## Vulnerability Details

**Type**: Broken Authentication - Token Validation Bypass  
**Severity**: Critical  
**OWASP Category**: A07:2021 – Identification and Authentication Failures

The password reset functionality fails to properly validate reset tokens, allowing attackers to:
- Reset any user's password
- Bypass token expiration checks  
- Gain unauthorized access to privileged accounts
- Access sensitive business data

## Educational Value

This lab provides hands-on experience with:
- Web application security testing
- Authentication mechanism analysis
- HTTP request manipulation
- Business impact assessment
- Secure development practices

## Project Structure

```
├── .github/workflows/    # CI/CD automation
├── build/               # Application source code
├── deploy/              # Docker deployment files  
├── docs/                # Technical documentation
├── test/                # Automated security tests
└── README.md           # This file
```

## Requirements

- **Docker**: For containerized deployment
- **Python 3.11+**: For manual deployment or testing
- **Modern Browser**: Chrome, Firefox, Safari, or Edge
- **Burp Suite**: For manual penetration testing (optional)

## Support and Documentation

- **User Guide**: `docs/user-guide.md`
- **Technical Docs**: `docs/technical-docs.md`  
- **Security Analysis**: `docs/security-analysis.md`
- **Deployment Guide**: `deploy/README.md`

## Health Check

Verify the application is running:
```bash
curl -f http://localhost:3206/
```

## Development

For local development and testing:
```bash
cd build
pip install -r requirements.txt
python app.py
```

---

*This lab is designed for educational purposes only. Always obtain proper authorization before testing security vulnerabilities.*
