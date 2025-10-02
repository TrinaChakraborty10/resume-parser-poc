import spacy
from modern_resume_parser import ResumeParser
import warnings

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