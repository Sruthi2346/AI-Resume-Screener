from fastapi import FastAPI, UploadFile, Form
from app.parsepdf import parse_pdf
from app.agents.resume_extractor import extract_resume_data

app = FastAPI()


@app.post("/screening/")
async def screening(resume: UploadFile, job_description: str = Form(...)):
    
    # 📄 Extract text from PDF
    resume_text = parse_pdf(resume.file)

    # 🔗 Combine Resume + Job Description
    combined_text = f"""
    Resume:
    {resume_text}

    Job Description:
    {job_description}
    """

    # 🤖 Get AI response
    result = extract_resume_data(combined_text)

    # ✅ Return clean result
    return {
        "result": result
    }