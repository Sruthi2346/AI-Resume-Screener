import streamlit as st
import requests
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="AI Resume Screener", layout="wide")

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---------------- SIDEBAR ----------------
st.sidebar.title("☰ Menu")

menu = st.sidebar.radio(
    "Navigate",
    ["Home", "Users", "Downloads", "Ideas"]
)

# ---------------- HOME ----------------
if menu == "Home":
    st.title("🤖 AI Resume Screener")

    st.write("""
    This platform helps:
    - 👤 Candidates analyze their resume
    - 🧑‍💼 Recruiters screen multiple candidates
    
    Upload resume + job description to get AI-powered insights.
    """)

# ---------------- USERS ----------------
elif menu == "Users":

    role = st.radio("Select Role", ["Candidate", "Recruiter"])

    # ================= CANDIDATE =================
    if role == "Candidate":

        st.title("👤 Candidate Portal")

        resume = st.file_uploader("Upload Resume", type="pdf")
        jd = st.text_area("Enter Job Description")

        if st.button("Process Resume"):

            if not resume or not jd:
                st.error("Please upload resume and enter job description")
            else:
                response = requests.post(
                    f"{API_URL}/screening/",
                    files={"resume": (resume.name, resume, "application/pdf")},
                    data={"job_description": jd}
                )

                if response.status_code == 200:
                    data = response.json()
                    result = data.get("result", "")

                    st.subheader("📊 Result")

                    # Extract score
                    score = 0
                    for line in result.split("\n"):
                        if "Match Score" in line:
                            try:
                                score = int(line.split(":")[1].strip())
                            except:
                                score = 0

                    st.progress(score)
                    st.write(f"### Match Score: {score}%")

                    if score >= 70:
                        st.success("✅ Strong Profile")
                    else:
                        st.error("❌ Needs Improvement")

                    st.text(result)

                else:
                    st.error("Server Error")

    # ================= RECRUITER =================
    elif role == "Recruiter":

        st.title("🧑‍💼 Recruiter Portal")

        files = st.file_uploader(
            "Upload Resumes",
            type="pdf",
            accept_multiple_files=True
        )

        jd = st.text_area("Enter Job Description")

        if st.button("Process Candidates"):

            if not files or not jd:
                st.error("Upload resumes and enter job description")
            else:
                results = []

                for file in files:

                    response = requests.post(
                        f"{API_URL}/screening/",
                        files={"resume": (file.name, file, "application/pdf")},
                        data={"job_description": jd}
                    )

                    if response.status_code == 200:

                        data = response.json()
                        result_text = data.get("result", "")

                        name, email, score, decision = "N/A", "N/A", 0, "Rejected"

                        for line in result_text.split("\n"):
                            if "Name:" in line:
                                name = line.split(":",1)[1].strip()
                            elif "Email:" in line:
                                email = line.split(":",1)[1].strip()
                            elif "Match Score" in line:
                                try:
                                    score = int(line.split(":",1)[1].strip())
                                except:
                                    score = 0
                            elif "Final Decision" in line:
                                decision = line.split(":",1)[1].strip()

                        results.append({
                            "Name": name,
                            "Email": email,
                            "Score": score,
                            "Decision": decision,
                            "Details": result_text
                        })

                # Sort by score
                results = sorted(results, key=lambda x: x["Score"], reverse=True)

                df = pd.DataFrame(results)

                # ---------------- SUMMARY ----------------
                total = len(results)
                selected = sum(1 for r in results if r["Decision"].lower() == "selected")

                col1, col2, col3 = st.columns(3)
                col1.metric("Total", total)
                col2.metric("Selected", selected)
                col3.metric("Rejected", total - selected)

                # ---------------- DOWNLOAD ----------------
                import os
                import datetime

                # Create folder if not exists
                os.makedirs("app/ui/data", exist_ok=True)

                # Generate unique filename using timestamp
                filename = f"results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

                csv_path = os.path.join("app/ui/data", filename)

                # Save CSV
                df.to_csv(csv_path, index=False)

                # Download button
                with open(csv_path, "rb") as f:
                    st.download_button("Download CSV", f, filename)

                # ---------------- TABLE ----------------
                if not df.empty:
                    st.dataframe(df[["Name", "Email", "Score", "Decision"]])
                else:
                    st.warning("No data found")

                # ---------------- EXPANDABLE DETAILS ----------------
                st.subheader("📂 Candidate Details")

                for r in results:
                    with st.expander(f"{r['Name']} - Score {r['Score']}"):
                        st.text(r["Details"])

# ---------------- DOWNLOADS ----------------
elif menu == "Downloads":

    import os
    import pandas as pd

    st.title("⬇️ Downloads")

    folder = "app/ui/data"
    os.makedirs(folder, exist_ok=True)

    files = sorted(os.listdir(folder), reverse=True)

    if not files:
        st.info("No downloaded files available yet")
    else:
        st.write("### 📁 Available CSV Files")

        # Session state for toggle
        if "open_file" not in st.session_state:
            st.session_state.open_file = None

        for file in files:

            if file.endswith(".csv"):

                file_path = os.path.join(folder, file)

                col1, col2, col3, col4 = st.columns([4,1,1,1])

                # 📄 File name
                with col1:
                    st.write(f"📄 {file}")

                # 👁️ VIEW (TOGGLE)
                with col2:
                    if st.button("View", key=f"view_{file}"):

                        if st.session_state.open_file == file:
                            # CLOSE if already open
                            st.session_state.open_file = None
                        else:
                            # OPEN new file
                            st.session_state.open_file = file

                # ⬇️ DOWNLOAD
                with col3:
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="Download",
                            data=f,
                            file_name=file,
                            key=f"download_{file}"
                        )

                # 🗑 DELETE
                with col4:
                    if st.button("Delete", key=f"delete_{file}"):

                        os.remove(file_path)
                        st.success(f"{file} deleted")

                        # refresh UI
                        st.rerun()

                # 📊 SHOW TABLE (ONLY IF SELECTED)
                if st.session_state.open_file == file:
                    try:
                        df = pd.read_csv(file_path)
                        st.dataframe(df)
                    except Exception as e:
                        st.error(f"Error reading file: {e}")
                        
# ---------------- IDEAS ----------------
elif menu == "Ideas":

    st.title("💡 Job Ideas")

    jobs = [
        {"role": "Python Developer", "skills": "Python, FastAPI, SQL"},
        {"role": "Data Scientist", "skills": "Python, ML, Pandas"},
        {"role": "Frontend Developer", "skills": "HTML, CSS, React"},
    ]

    for job in jobs:
        st.subheader(job["role"])
        st.write("Required Skills:", job["skills"])
        st.divider()