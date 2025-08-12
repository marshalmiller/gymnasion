# Gymnasion Web App

A web-based version of the Gymnasion algorithmic literary training tool. This interactive web application provides the same functionality as the original Jupyter notebook and CLI tool, but in an accessible web interface.

## Features

- **Interactive Literary Training**: Real-time feedback on your writing
- **Elaboration Prompts**: Questions about adjectives, verbs, and objects
- **Quote Suggestions**: Contextual literary quotes for inspiration  
- **Authorial Imitation**: Practice writing in different authors' styles
- **Word Banishment**: Enforced vocabulary variation
- **Syntax Analysis**: Detection of repetitive patterns
- **Cohesive Backtracking**: Encouragement to revisit earlier themes
- **Progress Tracking**: Session state with banished words and imitation goals

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python app.py
   ```

3. **Open in Browser**:
   Navigate to `http://localhost:5000`

4. **Start Writing**:
   - Enter text in the input area
   - Press Enter or click "Submit Line"
   - Receive immediate feedback from Gymnasion
   - Type "***" to end your session

## Interface

### Main Sections

- **Your Writing**: Input area for composing text
- **Gymnasion's Guidance**: Real-time feedback and prompts
- **Status Panel**: Current session information including:
  - Word count
  - Active author imitation
  - Banished words list
  - Current status

### Controls

- **Submit Line**: Send your text for analysis
- **Reset Session**: Clear all progress and start fresh
- **Enter Key**: Quick submission (Shift+Enter for new lines)

## Technical Implementation

This web app is a simplified version of the original Gymnasion that:

- Uses Flask for the web framework
- Implements mock data for demonstration (no ML dependencies)
- Maintains session state for continuity
- Provides the same core functionality patterns
- Uses responsive design for mobile compatibility

## Differences from Original

- **Simplified NLP**: Uses basic text processing instead of SpaCy
- **Mock Data**: Pre-defined responses instead of ML models
- **No Dependencies**: Removed heavy ML libraries for easier deployment
- **Web Interface**: Modern, responsive design
- **Session Management**: Web-based state persistence

## Deployment

For production deployment:

1. Set a secure secret key
2. Configure a production WSGI server (e.g., Gunicorn)
3. Add proper error handling and logging
4. Implement user authentication if needed
5. Add SSL certificate for HTTPS

## Extension Ideas

- User accounts and saved sessions
- Integration with the original ML models
- Export functionality for completed works
- Social sharing of writing exercises
- Advanced analytics and progress tracking

## Original Project

This web app is based on the Gymnasion project by Kyle Booten (2018), which implements algorithmic literary training using natural language processing and machine learning techniques.
