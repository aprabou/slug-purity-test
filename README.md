# 🐌 Slug Purity Test - Anonymous Response Tracker

An anonymous form response tracking system for the UCSC Slug Purity Test. This system collects responses anonymously and provides aggregated analytics.

## 🏗️ Architecture

- **Frontend**: HTML form with 100 questions
- **Backend**: Flask web application
- **Database**: SQLite with anonymous response aggregation
- **Analytics**: Real-time results dashboard

## 📋 Features

- ✅ Anonymous response collection
- ✅ Real-time response aggregation
- ✅ Results dashboard with sorting
- ✅ API endpoint for data access
- ✅ Mobile-responsive design
- ✅ Preview functionality before submission

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip

### Installation

1. **Clone/Download the project**
   ```bash
   cd slug-purity-test
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Main form: http://localhost:3000
   - Results dashboard: http://localhost:3000/results
   - API endpoint: http://localhost:3000/api/results

## 📊 Database Schema

### Table: `question_stats`
| Column       | Type    | Description                        |
|-------------|---------|-----------------------------------|
| question_id | INTEGER | Question number (1-100), PRIMARY KEY |
| yes_count   | INTEGER | Number of "Yes" responses         |

## 🔧 API Endpoints

### `GET /`
- **Description**: Serves the main purity test form
- **Response**: HTML form with 100 questions

### `POST /submit`
- **Description**: Handles form submission
- **Input**: Form data with checked questions
- **Response**: Redirect to thank you page

### `GET /results`
- **Description**: Analytics dashboard
- **Response**: HTML page with aggregated results

### `GET /api/results`
- **Description**: JSON API for results data
- **Response**: 
  ```json
  {
    "total_submissions": 42,
    "question_stats": {
      "1": 25,
      "2": 38,
      ...
    },
    "timestamp": "2025-08-30T12:34:56"
  }
  ```

## 📱 Usage

### Taking the Test
1. Visit the main page
2. Check boxes for experiences you've had
3. Use "Preview My Score" to see results before submitting
4. Click "Submit My Responses" to save anonymously

### Viewing Results
1. Visit `/results` for the dashboard
2. Sort by question number, popularity, or percentage
3. View real-time analytics and statistics

## 🔒 Privacy & Security

- **Anonymous**: No personal data or IP addresses stored
- **Aggregated**: Only question counts are maintained
- **Secure**: No session tracking or user identification
- **GDPR Compliant**: No personal data collection

## 🏭 Production Deployment

### Environment Variables
```bash
FLASK_ENV=production
FLASK_APP=app.py
DATABASE_URL=sqlite:///responses.db  # or PostgreSQL URL
```

### Deployment Options

#### 1. Render/Heroku
```bash
# Add to Procfile
web: gunicorn app:app

# Add gunicorn to requirements.txt
gunicorn==21.2.0
```

#### 2. VPS with Nginx
```bash
# Install dependencies
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:3000 app:app
```

#### 3. Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:app"]
```

## 📈 Scaling Considerations

- **Database**: Switch to PostgreSQL for production
- **Caching**: Add Redis for frequently accessed results
- **Rate Limiting**: Implement to prevent spam
- **Load Balancing**: Use multiple app instances
- **CDN**: Serve static assets via CDN

## 🛠️ Development

### Project Structure
```
slug-purity-test/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── responses.db          # SQLite database (auto-created)
├── templates/
│   ├── index.html        # Main form template
│   └── results.html      # Results dashboard
├── static/
│   └── Banana_slugs_logo.png
└── venv/                 # Virtual environment
```

### Adding Questions
1. Update the questions list in `templates/results.html`
2. Modify the form in `templates/index.html`
3. Update the database initialization if needed

### Customization
- **Styling**: Modify CSS in template files
- **Questions**: Update question lists in templates
- **Scoring**: Modify calculation logic in JavaScript
- **Analytics**: Extend the results dashboard

## 🐛 Troubleshooting

### Common Issues

1. **Database errors**: Ensure write permissions in project directory
2. **Port conflicts**: Change port in `app.run(port=5001)`
3. **Template not found**: Verify templates directory exists
4. **Static files not loading**: Check static directory structure

### Debug Mode
```bash
export FLASK_DEBUG=1
python app.py
```

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

Built with ❤️ for the UCSC Slug community!
