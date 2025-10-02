import pdfplumber
import re

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''.join(page.extract_text() for page in pdf.pages)
    return text

resume_text = extract_text_from_pdf('C:/Users/10723269/Downloads/AniruddhaLaha_resume.pdf')
# print(resume_text)


# Extract email
email = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resume_text).group()
print("Email:", email)

# Extract phone number
phone = re.search(r'\b\d{10}\b', resume_text).group()
print("Phone:", phone)



skills = ['Python', 'Java', 'Machine Learning', 'Data Analysis']  # Example skill list
extracted_skills = [skill for skill in skills if skill.lower() in resume_text.lower()]
print("Skills:", extracted_skills)

import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(resume_text)
print(doc)


