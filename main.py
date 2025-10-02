import spacy
from pyresparser import ResumeParser
import warnings
import nltk
nltk.download('stopwords')
# Ignore warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Parse the resume file
data = ResumeParser("C:/Users/10723269/Downloads/AniruddhaLaha_resume.pdf").get_extracted_data()

# Print extracted data
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
# nlp = spacy.load('en_core_web_sm')
# doc = nlp(resume_text)

# # file:///C:/Users/10723269/Downloads/AniruddhaLaha_resume.pdf


# skills = ['Python', 'Java', 'Machine Learning', 'Data Analysis']  # Example skill list
# extracted_skills = [skill for skill in skills if skill.lower() in resume_text.lower()]
# print("Skills:", extracted_skills)
