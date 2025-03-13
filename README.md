# LLM Resume Generator

An AI-powered application for generating professional resumes using the Gemini AI model.

## Features

- Generate professional resumes with minimal input (name and position)
- Customize content with a markdown editor
- Handle image placeholders with upload, search, or AI generation
- Real-time preview with professional styling
- Export to multiple formats (PDF, DOCX, PPTX, Markdown, HTML)
- Available as a standalone application

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-generator.git
cd resume-generator
```

2. Set up the backend:
```bash
cd backend
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Set your Gemini API key:
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Running the application

1. Start the backend server:
```bash
cd backend
uvicorn app.main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Open your browser and navigate to `http://localhost:3000`

### Building an executable

To create a standalone executable:
```bash
python scripts/build_executable.py --output dist --name "Resume Generator"
```

## Using Docker

Alternatively, you can use Docker to run the application:
```bash
docker-compose up -d
```

Then navigate to `http://localhost:3000` in your browser.

## License

This project is licensed under the MIT License - see the LICENSE file for details.