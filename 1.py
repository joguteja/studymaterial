import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
from pypdf import PdfReader

# ==================================================
# CONFIGURATION
# ==================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY is not configured.")
    st.stop()

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.8-flash"


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Study Material Generator",
    page_icon="📚",
    layout="wide"
)


# ==================================================
# CSS
# ==================================================

st.markdown("""
<style>

/* ==================================================
   SKY BLUE AI BACKGROUND
   ================================================== */

.stApp {

    background:

        linear-gradient(
            rgba(125, 211, 252, 0.88),
            rgba(186, 230, 253, 0.92)
        ),

        url("https://images.unsplash.com/photo-1532012197267-da84d127e765?auto=format&fit=crop&w=2000&q=85");

    background-size: cover;

    background-position: center;

    background-attachment: fixed;

    min-height: 200vh;

    color: #111827;
}


/* ==================================================
   ANIMATED AI GLOW
   ================================================== */

.stApp::before {

    content: "";

    position: fixed;

    inset: 0;

    pointer-events: none;

    background:

        radial-gradient(
            circle at 10% 20%,
            rgba(255,255,255,0.55),
            transparent 20%
        ),

        radial-gradient(
            circle at 90% 25%,
            rgba(147,197,253,0.45),
            transparent 25%
        ),

        radial-gradient(
            circle at 50% 90%,
            rgba(192,132,252,0.25),
            transparent 30%
        );

    animation: glowAnimation 7s ease-in-out infinite;

    z-index: 0;
}


/* ==================================================
   MAIN CONTENT
   ================================================== */

.block-container {

    position: relative;

    z-index: 2;

    max-width: 1200px;

    margin: auto;

    padding-top: 2rem;

    padding-bottom: 3rem;
}


/* ==================================================
   TITLE
   ================================================== */

.title {

    text-align: center;

    font-size: 80px;

    font-weight: 900;

    letter-spacing: 1px;

    color: #172554;

    text-shadow:
        0 3px 12px
        rgba(255,255,255,0.75);

    animation:
        titleAnimation 2s ease;
}


/* ==================================================
   SUBTITLE
   ================================================== */

.subtitle {

    text-align: center;

    font-size: 30px;

    font-weight: 700;

    color: #1e3a8a;

    margin-bottom: 30px;

    text-shadow:
        0 2px 6px
        rgba(255,255,255,0.7);
}


/* ==================================================
   HEADINGS
   ================================================== */

h1,
h2,
h3 {

    color: #172554 !important;

    font-weight: 900 !important;
}


h2 {

    font-size: 50px !important;
}


h3 {

    font-size: 50px !important;
}


/* ==================================================
   SIDEBAR
   ================================================== */

section[data-testid="stSidebar"] {

    background:

        linear-gradient(
            180deg,
            #dbeafe,
            #bae6fd,
            #e0f2fe
        );

    border-right:
        2px solid
        rgba(37,99,235,0.20);

    box-shadow:
        5px 0 25px
        rgba(30,64,175,0.15);
}


section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {

    color:
        #172554 !important;

    font-size:
        50px !important;

    font-weight:
        900 !important;
}


section[data-testid="stSidebar"] label {

    color:
        #172554 !important;

    font-size:
        50px !important;

    font-weight:
        800 !important;
}


/* =========================================
   SIDEBAR - LARGE TEXT
   ========================================= */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #dbeafe,
            #bae6fd,
            #e0f2fe
        );

    border-right:
        2px solid
        rgba(37, 99, 235, 0.20);
}


/* Study Settings heading */

section[data-testid="stSidebar"] h2 {

    color: #172554 !important;

    font-size: 38px !important;

    font-weight: 900 !important;

    line-height: 1.2 !important;

    margin-bottom: 25px !important;
}


/* Labels */

section[data-testid="stSidebar"] label {

    color: #172554 !important;

    font-size: 20px !important;

    font-weight: 800 !important;

    line-height: 1.5 !important;
}


/* Text input */

section[data-testid="stSidebar"] input {

    background: rgba(255,255,255,0.95) !important;

    color: #111827 !important;

    border: 2px solid #60a5fa !important;

    border-radius: 12px !important;

    font-size: 19px !important;

    font-weight: 700 !important;

    min-height: 50px !important;

    padding: 10px 14px !important;
}


/* Placeholder text */

section[data-testid="stSidebar"] input::placeholder {

    color: #64748b !important;

    font-size: 18px !important;

    font-weight: 600 !important;

    opacity: 1 !important;
}


/* Dropdown */

section[data-testid="stSidebar"]
div[data-baseweb="select"] {

    background: white !important;

    border-radius: 12px !important;

    min-height: 50px !important;
}


/* Dropdown selected text */

section[data-testid="stSidebar"]
div[data-baseweb="select"] div {

    font-size: 19px !important;

    font-weight: 700 !important;

    color: #111827 !important;
}


/* Dropdown arrow */

section[data-testid="stSidebar"]
div[data-baseweb="select"] svg {

    width: 22px !important;

    height: 22px !important;
}


/* Tip box */

section[data-testid="stSidebar"] .stAlert {

    font-size: 18px !important;

    font-weight: 700 !important;

    line-height: 1.7 !important;

    padding: 18px !important;

    border-radius: 12px !important;
}



/* ==================================================
   SELECT BOX
   ================================================== */

section[data-testid="stSidebar"]
div[data-baseweb="select"] {

    background:
        rgba(255,255,255,0.90) !important;

    border-radius:
        12px !important;
}


/* ==================================================
   PDF UPLOAD CARD
   ================================================== */

[data-testid="stFileUploader"] {

    background:
        rgba(255,255,255,0.92);

    border:
        3px dashed
        #7c3aed;

    border-radius:
        20px;

    padding:
        18px;

    box-shadow:
        0 10px 30px
        rgba(30,64,175,0.18);

    transition:
        all 0.3s ease;
}


[data-testid="stFileUploader"]:hover {

    transform:
        translateY(-3px);

    border-color:
        #ec4899;

    box-shadow:
        0 15px 35px
        rgba(124,58,237,0.25);
}


[data-testid="stFileUploader"] label {

    color:
        #111827 !important;

    font-size:
        50px !important;

    font-weight:
        800 !important;
}


/* ==================================================
   GENERATE BUTTON
   ================================================== */

.stButton > button {

    width:
        100%;

    height:
        58px;

    border:
        none;

    border-radius:
        15px;

    color:
        white !important;

    font-size:
        50px !important;

    font-weight:
        900 !important;

    background:

        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed,
            #db2777,
            #2563eb
        );

    background-size:
        300% 100%;

    animation:
        buttonAnimation 5s linear infinite;

    box-shadow:
        0 8px 25px
        rgba(37,99,235,0.30);

    transition:
        all 0.3s ease;
}


.stButton > button:hover {

    transform:
        translateY(-4px);

    box-shadow:
        0 12px 35px
        rgba(124,58,237,0.40);
}


/* ==================================================
   GENERATED MATERIAL
   ================================================== */

.generated-material {

    background:
        rgba(255,255,255,0.96);

    padding:
        30px;

    border-radius:
        22px;

    border-left:
        8px solid
        #7c3aed;

    border-top:
        2px solid
        #bfdbfe;

    box-shadow:
        0 12px 35px
        rgba(30,64,175,0.18);

    animation:
        resultAnimation 0.6s ease;
}


/* ==================================================
   GENERATED TEXT
   ================================================== */

.generated-material p,
.generated-material li {

    color:
        #111827 !important;

    font-size:
        50px !important;

    font-weight:
        600 !important;

    line-height:
        1.8 !important;
}


.generated-material strong {

    color:
        #6d28d9 !important;

    font-size:
        50px !important;
}


.generated-material h1 {

    color:
        #1d4ed8 !important;

    font-size:
        50px !important;
}


.generated-material h2 {

    color:
        #7c3aed !important;

    font-size:
        50px !important;
}


.generated-material h3 {

    color:
        #be185d !important;

    font-size:
        50px !important;
}


/* ==================================================
   DOWNLOAD BUTTON
   ================================================== */

.stDownloadButton > button {

    width:
        100%;

    height:
        55px;

    border:
        none;

    border-radius:
        14px;

    background:

        linear-gradient(
            90deg,
            #2563eb,
            #7c3aed
        );

    color:
        white !important;

    font-size:
        20px !important;

    font-weight:
        900 !important;

    transition:
        all 0.3s ease;
}


.stDownloadButton > button:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 10px 30px
        rgba(37,99,235,0.35);
}


/* ==================================================
   ALERTS
   ================================================== */

.stAlert {

    border-radius:
        14px !important;

    font-size:
       10 px !important;

    font-weight:
        700 !important;
}


/* ==================================================
   DIVIDER
   ================================================== */

hr {

    border:
        none !important;

    height:
        2px !important;

    background:

        linear-gradient(
            90deg,
            transparent,
            #60a5fa,
            #a855f7,
            #ec4899,
            transparent
        ) !important;

    margin:
        28px 0 !important;
}


/* ==================================================
   FOOTER
   ================================================== */

.footer {

    text-align:
        center;

    color:
        #172554;

    font-size:
        20px;

    font-weight:
        800;

    margin-top:
        35px;
}


/* ==================================================
   ANIMATIONS
   ================================================== */

@keyframes titleAnimation {

    from {

        opacity:
            0;

        transform:
            translateY(-20px);
    }

    to {

        opacity:
            1;

        transform:
            translateY(0);
    }
}


@keyframes buttonAnimation {

    0% {
        background-position:
            0% 50%;
    }

    50% {
        background-position:
            100% 50%;
    }

    100% {
        background-position:
            0% 50%;
    }
}


@keyframes glowAnimation {

    0% {
        opacity:
            0.65;
    }

    50% {
        opacity:
            1;
    }

    100% {
        opacity:
            0.65;
    }
}


@keyframes resultAnimation {

    from {

        opacity:
            0;

        transform:
            translateY(20px);
    }

    to {

        opacity:
            1;

        transform:
            translateY(0);
    }
}


/* ==================================================
   HIDE STREAMLIT DEFAULT UI
   ================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="title">📚 AI Study Material Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    '🤖 Generate Notes • Exam Answers • MCQs • Revision Material'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("⚙️ Study Settings")

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: DBMS"
    )

    topic = st.text_input(
        "📝 Topic",
        placeholder="Example: Normalization"
    )

    level = st.selectbox(
        "🎯 Difficulty Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    material_type = st.selectbox(
        "📖 Material Type",
        [
            "Study Notes",
            "2 Mark Answer",
            "5 Mark Answer",
            "10 Mark Answer",
            "MCQs",
            "Revision Notes"
        ]
    )

    st.divider()

    st.info(
        "💡 Upload a PDF to generate study "
        "material from your notes."
    )


# ==================================================
# PDF UPLOAD
# ==================================================

st.subheader("📄 Upload Study Material")

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"]
)

pdf_text = ""

if uploaded_file:

    try:

        reader = PdfReader(uploaded_file)

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pdf_text += text + "\n"

        st.success(
            f"✅ PDF uploaded successfully — "
            f"{len(reader.pages)} pages"
        )

    except Exception as e:

        st.error(
            f"Unable to read PDF: {e}"
        )


# ==================================================
# CREATE PROMPT
# ==================================================

def create_prompt():

    source_text = ""

    if pdf_text:
        source_text = pdf_text[:50000]

    base = f"""
You are an expert academic tutor.

Create accurate, student-friendly study material.

Subject: {subject}
Topic: {topic}
Difficulty: {level}

Use simple English.
Use headings and bullet points.
Include examples where useful.
Make the answer suitable for college students.
"""

    if source_text:

        base += f"""

Use the following uploaded study material
as the primary source.

--- PDF CONTENT ---

{source_text}

--- END PDF CONTENT ---
"""

    if material_type == "Study Notes":

        base += """
Generate complete study notes.

Include:
1. Definition
2. Introduction
3. Important concepts
4. Detailed explanation
5. Example
6. Advantages
7. Disadvantages
8. Applications
9. Key points
10. Conclusion
"""

    elif material_type == "2 Mark Answer":

        base += """
Generate a short 2-mark exam answer.

Keep it concise.
Give a definition and 2-3 important points.
"""

    elif material_type == "5 Mark Answer":

        base += """
Generate a 5-mark exam answer.

Use:
- Introduction
- Main explanation
- Example
- Important points
- Conclusion

Keep the answer exam-ready.
"""

    elif material_type == "10 Mark Answer":

        base += """
Generate a detailed 10-mark exam answer.

Use:
- Introduction
- Definition
- Detailed explanation
- Subheadings
- Example
- Advantages
- Applications
- Conclusion

Make it suitable for writing in an examination.
"""

    elif material_type == "MCQs":

        base += """
Generate 10 multiple-choice questions.

Each question must contain:

A. option
B. option
C. option
D. option

Clearly mention the correct answer
and give a one-line explanation.
"""

    elif material_type == "Revision Notes":

        base += """
Generate quick revision notes.

Include:
- Important definitions
- Important formulas if applicable
- Key concepts
- Important differences
- Examples
- Exam tips

Keep it concise and easy to revise.
"""

    return base


# ==================================================
# GENERATE MATERIAL
# ==================================================

st.subheader("🚀 Generate Material")

if st.button("✨ Generate Study Material"):

    if not subject:

        st.warning("⚠️ Please enter a subject.")

    elif not topic:

        st.warning("⚠️ Please enter a topic.")

    else:

        prompt = create_prompt()

        with st.spinner(
            "🤖 Gemini is preparing your study material..."
        ):

            try:

                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt
                )

                result = response.text

                st.session_state["result"] = result

            except Exception as e:

                st.error(
                    f"Gemini API error: {e}"
                )


# ==================================================
# DISPLAY RESULT
# ==================================================

if "result" in st.session_state:

    st.divider()

    st.subheader("📖 Generated Study Material")

    st.markdown(
        '<div class="generated-material">',
        unsafe_allow_html=True
    )

    st.markdown(
        st.session_state["result"]
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    download_text = f"""
AI STUDY MATERIAL

Subject: {subject}
Topic: {topic}
Difficulty: {level}
Material Type: {material_type}

========================================

{st.session_state["result"]}
"""

    st.download_button(
        label="⬇️ Download Study Material",
        data=download_text,
        file_name="study_material.txt",
        mime="text/plain"
    )

    st.success(
        "🎉 Your study material is ready!"
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        📚 AI Study Material Generator
        • 🤖 Powered by Gemini AI
        • Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)