# Resume Parser

A modern Python-based resume parser that extracts key information from PDF resumes using spaCy NLP and regular expressions. Now available as both a Python library and a **FastAPI web service**!

## 🚀 New: FastAPI Web Service

- **RESTful API**: Upload resumes via HTTP POST requests
- **Interactive Documentation**: Swagger UI at `/docs`
- **File Validation**: Automatic PDF validation and size limits
- **JSON Response**: Structured data extraction results
- **Error Handling**: Comprehensive error messages and logging
- **Multiple Formats**: Simple and detailed response formats

## Features

- **Name Extraction**: Uses spaCy NER and pattern matching to identify candidate names
- **Contact Information**: Extracts email addresses and phone numbers with multiple format support
- **Skills Detection**: Identifies technical skills from a comprehensive predefined list
- **Education Details**: Extracts college/university names and degree information
- **Work Experience**: Identifies company names and job designations
- **PDF Analysis**: Counts total pages and processes multi-page documents

## Requirements

- Python 3.8+
- Virtual environment (recommended)

## Installation

1. **Clone or download the project**
   ```bash
   cd resume-parser
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv myvenv
   .\myvenv\Scripts\Activate.ps1  # Windows PowerShell
   # or
   .\myvenv\Scripts\activate.bat  # Windows CMD
   # or
   source myvenv/bin/activate     # Linux/Mac
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   # or individually:
   pip install fastapi uvicorn python-multipart spacy pdfplumber requests
   ```

4. **Download spaCy English model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Method 1: FastAPI Web Service (Recommended)

Start the API server:
```bash
python app.py
# or use the batch file on Windows:
start_server.bat
```

The API will be available at:
- **Main API**: `http://localhost:8000`
- **Interactive Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

#### API Endpoints

**1. Upload Resume - Simple Format**
```bash
POST /upload-resume
Content-Type: multipart/form-data

# Example using curl:
curl -X POST "http://localhost:8000/upload-resume" -F "file=@resume.pdf"

# Example using Python requests:
import requests
with open('resume.pdf', 'rb') as f:
    response = requests.post('http://localhost:8000/upload-resume', 
                           files={'file': f})
    data = response.json()
```

**2. Parse Resume - Detailed Format**
```bash
POST /parse-resume
Content-Type: multipart/form-data

# Returns categorized data structure
```

**3. Health Check**
```bash
GET /health
# Returns: {"status": "healthy", "service": "resume-parser"}
```

#### Example Response
```json
{
  "success": true,
  "filename": "resume.pdf",
  "file_size_bytes": 245760,
  "extracted_data": {
    "name": "ANIRUDDHA LAHA",
    "email": "anilaha2502@gmail.com",
    "mobile_number": "9038503946",
    "skills": ["Python", "Docker", "AWS", "Kubernetes"],
    "college_name": "Brainware Group of Institution",
    "degree": "Bachelor of Technology",
    "designation": "Software Engineer",
    "company_names": ["TCS", "IBM"],
    "no_of_pages": 2,
    "total_experience": "5 years"
  }
}
```

### Method 2: Direct Python Usage

```python
from modern_resume_parser import ResumeParser

# Parse a resume
parser = ResumeParser("path/to/resume.pdf")
data = parser.get_extracted_data()

# Print results
print("Name:", data["name"])
print("Email:", data["email"])
print("Mobile Number:", data["mobile_number"])
print("Skills:", data["skills"])
print("College Name:", data["college_name"])
print("Degree:", data["degree"])
print("Designation:", data["designation"])
print("Company Names:", data["company_names"])
print("No Of Pages:", data["no_of_pages"])
print("Total Experience:", data["total_experience"])
```

### Running the Example

```bash
# Method 1: Start API server
python app.py

# Method 2: Direct parsing
python main_modern.py

# Method 3: Test the API
python test_api.py
```

## Extracted Information

The parser extracts the following information:

| Field | Description | Example |
|-------|-------------|---------|
| `name` | Full name of the candidate | "ANIRUDDHA LAHA" |
| `email` | Email address | "anilaha2502@gmail.com" |
| `mobile_number` | Phone number | "9038503946" |
| `skills` | List of technical skills | ["Python", "Docker", "AWS"] |
| `college_name` | Educational institution | "Brainware Group of Institution" |
| `degree` | Academic degree | "Bachelor of Technology" |
| `designation` | Job title/position | "Software Engineer" |
| `company_names` | List of companies | ["TCS", "IBM", "Microsoft"] |
| `no_of_pages` | Number of PDF pages | 2 |
| `total_experience` | Years of experience | "5 years" |

## Supported Formats

### Phone Numbers
- 10-digit format: `9038503946`
- Hyphenated: `903-850-3946`
- Parentheses: `(903) 850-3946`
- International: `+91-903-850-3946`

### Degrees
- Bachelor of Technology (B.Tech, BE)
- Master of Technology (M.Tech, ME)
- Bachelor/Master of Science (BS, MS)
- Bachelor/Master of Arts (BA, MA)
- MBA, PhD

### Skills Database
The parser recognizes 50+ technical skills including:
- **Programming Languages**: Python, Java, JavaScript, C++, C#, PHP, Ruby, Go, Rust
- **Web Technologies**: HTML, CSS, React, Angular, Vue, Node.js, Express
- **Frameworks**: Django, Flask, Spring, Laravel, Rails
- **Databases**: SQL, MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch
- **Cloud & DevOps**: AWS, Azure, Google Cloud, Docker, Kubernetes, Jenkins
- **Version Control**: Git, GitHub, GitLab, Bitbucket
- **Data Science**: Machine Learning, Deep Learning, AI, TensorFlow, PyTorch, Pandas, NumPy
- **Operating Systems**: Linux, Unix, Windows, MacOS
- **Methodologies**: Agile, Scrum, DevOps, CI/CD

## File Structure

```
resume-parser/
├── app.py                     # FastAPI web service (NEW!)
├── modern_resume_parser.py    # Main parser class
├── main_modern.py             # Example usage script
├── test_api.py                # API testing script
├── start_server.bat           # Windows server startup script
├── main.py                    # Legacy script (compatibility issues)
├── main1.py                   # Alternative implementation
├── requirements.txt           # Package dependencies
├── myvenv/                    # Virtual environment
└── README.md                  # This file
```

## Troubleshooting

### Common Issues

1. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Virtual Environment Issues**
   - Make sure virtual environment is activated
   - Check that packages are installed in the correct environment

3. **PDF Reading Errors**
   - Ensure PDF is not password protected
   - Check file path is correct and accessible

4. **Legacy pyresparser Issues**
   - Use `modern_resume_parser.py` instead of the old `pyresparser` package
   - The old package has compatibility issues with spaCy 3.x

### Error Resolution

If you encounter the error:
```
OSError: [E053] Could not read config file from ...pyresparser\config.cfg
```

This indicates you're using the old `pyresparser` package. Switch to using `modern_resume_parser.py` which is compatible with modern spaCy versions.

## Customization

### Adding New Skills
Edit the `skill_keywords` list in `_extract_skills()` method:

```python
skill_keywords = [
    'Python', 'Java', 'JavaScript',
    # Add your custom skills here
    'YourCustomSkill', 'AnotherSkill'
]
```

### Modifying Extraction Logic
Each extraction method can be customized:
- `_extract_name()`: Name detection patterns
- `_extract_email()`: Email regex patterns
- `_extract_phone()`: Phone number formats
- `_extract_skills()`: Skills database
- `_extract_education()`: Education institution patterns
- `_extract_companies()`: Company name filtering

## Dependencies

- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **python-multipart**: File upload support
- **spacy**: Natural Language Processing
- **pdfplumber**: PDF text extraction  
- **requests**: HTTP library for testing
- **re**: Regular expressions (built-in)
- **pathlib**: Path handling (built-in)

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues or questions:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify your PDF is readable and not corrupted
4. Check that the virtual environment is properly activated

## Version History

- **v2.0**: Modern implementation using spaCy 3.x (current)
- **v1.0**: Legacy implementation using pyresparser (deprecated due to compatibility issues)

## Reference
 - https://github.com/rex2231/Resume_Parser/blob/main/Res_parser.ipynb