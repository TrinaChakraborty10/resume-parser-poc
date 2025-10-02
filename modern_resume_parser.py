import spacy
import re
import pdfplumber
from pathlib import Path

class ModernResumeParser:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.nlp = spacy.load('en_core_web_sm')
        self.text = self._extract_text_from_pdf()
        
    def _extract_text_from_pdf(self):
        """Extract text from PDF using pdfplumber"""
        with pdfplumber.open(self.pdf_path) as pdf:
            text = ''.join(page.extract_text() or '' for page in pdf.pages)
        return text
    
    def get_extracted_data(self):
        """Extract various information from resume"""
        data = {
            "name": self._extract_name(),
            "email": self._extract_email(),
            "mobile_number": self._extract_phone(),
            "skills": self._extract_skills(),
            "college_name": self._extract_education(),
            "degree": self._extract_degree(),
            "designation": self._extract_designation(),
            "company_names": self._extract_companies(),
            "no_of_pages": self._get_page_count(),
            "total_experience": self._extract_experience()
        }
        return data
    
    def _extract_name(self):
        """Extract name using spaCy NER and common patterns"""
        # First try spaCy NER on the first part of the document
        doc = self.nlp(self.text[:1000])  # Check first 1000 chars
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                # Filter out common false positives
                if len(ent.text.split()) >= 2 and ent.text.lower() not in ['microsoft azure', 'bachelor of technology']:
                    return ent.text
        
        # Fallback: Look for name patterns in the first few lines
        lines = self.text.split('\n')[:10]  # Check first 10 lines
        for line in lines:
            line = line.strip()
            # Skip empty lines and lines with emails/phones
            if line and '@' not in line and not re.search(r'\d{10}', line):
                # Check if line looks like a name (2-4 words, mostly alphabetic)
                words = line.split()
                if 2 <= len(words) <= 4 and all(word.isalpha() for word in words):
                    return line
        
        return None
    
    def _extract_email(self):
        """Extract email using regex"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.text)
        return emails[0] if emails else None
    
    def _extract_phone(self):
        """Extract phone number using regex"""
        # Multiple phone patterns
        patterns = [
            r'\b\d{10}\b',  # 10 digits
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',  # XXX-XXX-XXXX format
            r'\b\(\d{3}\)\s?\d{3}[-.]?\d{4}\b',  # (XXX) XXX-XXXX format
            r'\b\+\d{1,3}[-.]?\d{3,4}[-.]?\d{3,4}[-.]?\d{3,4}\b'  # International format
        ]
        
        for pattern in patterns:
            phones = re.findall(pattern, self.text)
            if phones:
                return phones[0]
        return None
    
    def _extract_skills(self):
        """Extract skills from a predefined list"""
        # Common technical skills - you can expand this list
        skill_keywords = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
            'HTML', 'CSS', 'React', 'Angular', 'Vue', 'Node.js', 'Express',
            'Django', 'Flask', 'Spring', 'Laravel', 'Rails',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch',
            'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins',
            'Git', 'GitHub', 'GitLab', 'Bitbucket',
            'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'Analytics',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Pandas', 'NumPy',
            'Linux', 'Unix', 'Windows', 'MacOS',
            'Agile', 'Scrum', 'DevOps', 'CI/CD'
        ]
        
        found_skills = []
        text_lower = self.text.lower()
        
        for skill in skill_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_education(self):
        """Extract education information"""
        # Common university/college keywords
        edu_keywords = [
            'university', 'college', 'institute', 'school', 'institution',
            'IIT', 'NIT', 'MIT', 'Stanford', 'Harvard'
        ]
        
        # Look for education section patterns
        education_patterns = [
            r'(?i)education.*?\n(.*?(?:university|college|institute|institution).*?)(?:\n|$)',
            r'(?i)(.*?(?:university|college|institute|institution).*?)(?:\n.*?(?:degree|bachelor|master|b\.?tech|m\.?tech))',
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, self.text, re.MULTILINE | re.DOTALL)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[0]
                    # Clean up the match
                    match = re.sub(r'\s+', ' ', match.strip())
                    if len(match) > 5 and len(match) < 100:  # Reasonable length
                        return match
        
        # Fallback to NER
        doc = self.nlp(self.text)
        for ent in doc.ents:
            if ent.label_ == "ORG":
                org_text = ent.text.lower()
                if any(keyword in org_text for keyword in edu_keywords) and len(ent.text) > 10:
                    return ent.text
        return None
    
    def _extract_degree(self):
        """Extract degree information"""
        degree_patterns = [
            r'\b(B\.?Tech|Bachelor of Technology|BE|Bachelor of Engineering)\b',
            r'\b(M\.?Tech|Master of Technology|ME|Master of Engineering)\b',
            r'\b(PhD|Ph\.D|Doctor of Philosophy)\b',
            r'\b(MBA|Master of Business Administration)\b',
            r'\b(BS|Bachelor of Science|MS|Master of Science)\b',
            r'\b(BA|Bachelor of Arts|MA|Master of Arts)\b'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, self.text, re.IGNORECASE)
            if matches:
                return matches[0]
        return None
    
    def _extract_designation(self):
        """Extract current or recent job designation"""
        # Common job titles
        job_titles = [
            'Software Engineer', 'Senior Software Engineer', 'Lead Software Engineer',
            'Data Scientist', 'Data Analyst', 'Business Analyst',
            'Product Manager', 'Project Manager', 'Program Manager',
            'DevOps Engineer', 'Full Stack Developer', 'Frontend Developer', 'Backend Developer',
            'Machine Learning Engineer', 'AI Engineer', 'Research Scientist'
        ]
        
        for title in job_titles:
            if title.lower() in self.text.lower():
                return title
        return None
    
    def _extract_companies(self):
        """Extract company names using NER"""
        doc = self.nlp(self.text)
        companies = []
        
        # Common false positives to filter out
        false_positives = [
            'university', 'college', 'school', 'institute', 'institution',
            'bachelor of technology', 'master of science', 'phd', 'degree',
            'certification', 'certifications', 'version control', 'cicd',
            'iac', 'rbac', 'api management', 'cloud security', 'hands'
        ]
        
        for ent in doc.ents:
            if ent.label_ == "ORG":
                # Filter out educational institutions and false positives
                ent_lower = ent.text.lower().strip()
                if (not any(fp in ent_lower for fp in false_positives) and
                    len(ent.text.strip()) > 2 and
                    len(ent.text.strip()) < 50 and
                    not ent.text.strip().startswith('•')):
                    companies.append(ent.text.strip())
        
        return list(set(companies))  # Remove duplicates
    
    def _get_page_count(self):
        """Get number of pages in PDF"""
        with pdfplumber.open(self.pdf_path) as pdf:
            return len(pdf.pages)
    
    def _extract_experience(self):
        """Extract total experience (basic implementation)"""
        # Look for patterns like "X years experience", "X+ years", etc.
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s+)?experience',
            r'(\d+)\+?\s*years?\s*in',
            r'experience.*?(\d+)\+?\s*years?'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, self.text.lower())
            if matches:
                return f"{matches[0]} years"
        return None

# Usage function to replace the original ResumeParser
def ResumeParser(pdf_path):
    return ModernResumeParser(pdf_path)