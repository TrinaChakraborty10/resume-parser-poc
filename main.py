import spacy
from modern_resume_parser import ResumeParser
import warnings
# Ignore warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Parse the resume file
resparser = ResumeParser("C://Users//Aditi//Downloads//SANSKRITA_SINGH_RESUME.pdf")
data = resparser.get_extracted_data()

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
