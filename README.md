# Disetech - Digital Solutions for Africa

![Disetech Logo](https://via.placeholder.com/150x50?text=Disetech+Logo) <!-- Replace with actual logo -->

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-red?style=flat-square&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=flat-square&logo=postgresql)
![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat-square&logo=render)

Modern web development and digital solutions tailored for the African market.

---

## 🚀 Features

- **🌍 Africa-Focused Solutions**: Custom digital solutions addressing local challenges and opportunities
- **📱 Modern Tech Stack**: Flask backend with SQLAlchemy ORM for robust data management
- **✉️ Integrated Communications**: Mailgun email service integration for reliable messaging
- **📝 Blog System**: Comprehensive content management for articles, news, and insights
- **📱 Responsive Design**: Optimized experience across all devices and screen sizes
- **🔧 RESTful API**: Clean API endpoints for seamless integration and data access
- **🚀 Production Ready**: Configured for deployment on Render.com with proper environment handling

---

## 🛠️ Technologies Used

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Lightweight and flexible web framework
- **SQLAlchemy** - Powerful ORM for database management
- **PostgreSQL** - Production database (SQLite for development)
- **Mailgun API** - Email service integration

### Frontend
- **HTML5, CSS3, JavaScript** - Modern web standards
- **Font Awesome** - Professional icon library
- **Responsive Design** - Mobile-first approach

### DevOps & Deployment
- **Render.com** - Cloud hosting platform
- **Environment Variables** - Secure configuration management
- **Database Migrations** - Version-controlled database changes
- **Gunicorn** - Production WSGI server

---

## 📂 Project Structure

```
Disetech/
├── app.py                  # Main application file
├── wsgi.py                 # WSGI entry point for production
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore             # Git ignore patterns
├── static/                 # Static files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── images/            # Image assets
├── templates/              # Flask templates
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── blog/              # Blog-related templates
│   │   ├── post.html      # Individual blog post
│   │   └── category.html  # Category listings
│   └── components/        # Reusable components
└── README.md              # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (for production) or SQLite (for development)
- Mailgun account (for email functionality)
- Git

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/chegeMP/Disetech.git
cd Disetech
```

#### 2. Set up a virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual credentials
```

**Required Environment Variables:**
```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_APP=app.py

# Database Configuration
DATABASE_URL=postgresql://username:password@localhost/disetech
# For development with SQLite:
# DATABASE_URL=sqlite:///disetech.db

# Mailgun Configuration
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN=your-mailgun-domain
MAILGUN_BASE_URL=https://api.mailgun.net/v3

# Email Settings
MAIL_DEFAULT_SENDER=noreply@yourdomain.com
ADMIN_EMAIL=admin@yourdomain.com
```

#### 5. Initialize the database
```bash
flask init-db
```

#### 6. Run the application
```bash
# Development mode
flask run

# The application will be available at http://localhost:5000
```

---

## 🌐 API Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/subscribe` | POST | Newsletter subscription | `email`, `name` (optional) |
| `/api/contact` | POST | Contact form submission | `name`, `email`, `message` |
| `/api/posts` | GET | Get published blog posts | `limit`, `offset`, `category` |
| `/api/posts/<slug>` | GET | Get single blog post | `slug` (URL parameter) |
| `/api/categories` | GET | Get blog categories | None |

### API Usage Examples

#### Subscribe to Newsletter
```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'
```

#### Get Blog Posts
```bash
curl http://localhost:5000/api/posts?limit=10&offset=0
```

#### Submit Contact Form
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello, I am interested in your services."
  }'
```

---

## 🚀 Deployment

### Production Deployment on Render.com

#### 1. Create a new Web Service on Render
- Connect your GitHub repository
- Select the `main` branch

#### 2. Configure Build Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --bind 0.0.0.0:5000 wsgi:app`

#### 3. Set Environment Variables
Configure the following environment variables in your Render dashboard:
```
SECRET_KEY=your-production-secret-key
FLASK_ENV=production
DATABASE_URL=your-postgresql-connection-string
MAILGUN_API_KEY=your-mailgun-api-key
MAILGUN_DOMAIN=your-mailgun-domain
MAILGUN_BASE_URL=https://api.mailgun.net/v3
```

#### 4. Database Setup
- Add a PostgreSQL database in Render
- Use the provided connection string as your `DATABASE_URL`

#### 5. Deploy
- Render will automatically deploy your application
- Monitor the build logs for any issues

### Alternative Deployment Options

#### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

#### Local Production Testing
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

---

## 🧪 Testing

### Manual Testing
1. **Home Page**: Visit `http://localhost:5000` to test the main interface
2. **Blog System**: Navigate to blog posts and categories
3. **Contact Form**: Test the contact form submission
4. **Newsletter**: Test the newsletter subscription feature
5. **API Endpoints**: Use curl or Postman to test API responses

### API Testing with Postman
Import the following collection for comprehensive API testing:
```json
{
  "info": {
    "name": "Disetech API",
    "description": "Test collection for Disetech API endpoints"
  },
  "item": [
    {
      "name": "Get Blog Posts",
      "request": {
        "method": "GET",
        "url": "{{base_url}}/api/posts"
      }
    },
    {
      "name": "Subscribe to Newsletter",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/subscribe",
        "body": {
          "mode": "raw",
          "raw": "{\"email\": \"test@example.com\", \"name\": \"Test User\"}"
        }
      }
    }
  ]
}
```

---

## 📊 Performance & Analytics

### Key Metrics
- **Page Load Speed**: Optimized for < 2 seconds
- **Mobile Responsiveness**: 100% mobile-friendly
- **SEO Optimization**: Structured data and meta tags
- **Email Deliverability**: Mailgun integration for reliable delivery

### Monitoring
- **Error Logging**: Comprehensive error tracking
- **Performance Monitoring**: Response time tracking
- **User Analytics**: Traffic and engagement metrics

---

## 🤝 Contributing

We welcome contributions to improve Disetech! Here's how you can help:

### Getting Started
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Add comments for complex logic
- Test your changes before submitting
- Update documentation as needed

### Code Review Process
- All PRs require review before merging
- Ensure all tests pass
- Maintain code quality standards
- Update relevant documentation

---

## 🔐 Security

- **Environment Variables**: Sensitive data stored securely
- **Input Validation**: All user inputs are validated and sanitized
- **Email Security**: Mailgun provides secure email delivery
- **Database Security**: SQLAlchemy prevents SQL injection
- **HTTPS**: SSL/TLS encryption in production

---

## 📋 Roadmap

### Phase 1 (Current)
- [x] Core Flask application structure
- [x] Blog system with categories
- [x] Email integration with Mailgun
- [x] RESTful API endpoints
- [x] Responsive design
- [x] Production deployment

### Phase 2 (Upcoming)
- [ ] User authentication system
- [ ] Admin dashboard for content management
- [ ] Advanced blog features (tags, search)
- [ ] Email newsletter automation
- [ ] Performance optimization

### Phase 3 (Future)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Mobile application
- [ ] Integration with social media platforms
- [ ] E-commerce capabilities

---

## 🆘 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Check your DATABASE_URL in .env
# Ensure PostgreSQL is running
# Verify database credentials
```

**Email Not Sending**
```bash
# Verify Mailgun API key and domain
# Check MAILGUN_BASE_URL configuration
# Ensure email templates are properly configured
```

**Static Files Not Loading**
```bash
# Check Flask static folder configuration
# Verify file paths in templates
# Clear browser cache
```

### Getting Help
1. Check the [Issues](https://github.com/chegeMP/Disetech/issues) page
2. Create a new issue with detailed information
3. Contact the development team
4. Review the documentation

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Contact

**Mark Chege** - [@chegehchad](https://twitter.com/chegehchad) - mark@disetech.com

**Project Link**: [https://github.com/chegeMP/Disetech](https://github.com/chegeMP/Disetech)

**Live Demo**: [https://disetech.onrender.com](https://disetech.onrender.com) <!-- Update with actual URL -->

---

## 🙏 Acknowledgments

- **Flask Community** for the excellent web framework
- **Mailgun** for reliable email service
- **Render.com** for seamless deployment platform
- **Font Awesome** for beautiful icons
- **African tech community** for inspiration and support
- **Open source contributors** who make projects like this possible

---

## 📈 Stats

![GitHub stars](https://img.shields.io/github/stars/chegeMP/Disetech?style=social)
![GitHub forks](https://img.shields.io/github/forks/chegeMP/Disetech?style=social)
![GitHub issues](https://img.shields.io/github/issues/chegeMP/Disetech)
![GitHub pull requests](https://img.shields.io/github/issues-pr/chegeMP/Disetech)

---

**🌍 Empowering Africa Through Digital Solutions 🌍**

*Last updated: July 2025*
