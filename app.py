import os
import tempfile
from pathlib import Path
import fitz
import streamlit as st
from dotenv import load_dotenv
from PIL import Image as PILImage

from agno.agent import Agent
from agno.media import Image as AgnoImage
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools


# ---------------------------------------------------------
# PAGE CONFIGURATION
# Must be the first Streamlit command
# ---------------------------------------------------------

st.set_page_config(
    page_title="Medical Image Analysis",
    page_icon="🩺",
    layout="centered",
)


# ---------------------------------------------------------
# API KEY CONFIGURATION
# ---------------------------------------------------------

load_dotenv()

try:
    GOOGLE_API_KEY = st.secrets.get(
        "GOOGLE_API_KEY",
        os.getenv("GOOGLE_API_KEY"),
    )
except Exception:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error(
        "GOOGLE_API_KEY is missing. Add it to Streamlit Secrets "
        "or your local .env file."
    )
    st.stop()

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# ---------------------------------------------------------
# MEDICAL ANALYSIS PROMPT
# ---------------------------------------------------------

MEDICAL_ANALYSIS_PROMPT = """
You are an AI medical-image interpretation assistant.

Carefully examine the uploaded image and provide a structured response.

### 1. Image Type and Region
- Identify the likely imaging modality.
- Identify the visible anatomical region.
- Comment on image quality and limitations.

### 2. Visible Findings
- Describe visible structures systematically.
- Mention possible abnormalities and their locations.
- Clearly state when something cannot be determined from the image.
- Do not invent measurements or clinical details.

### 3. Possible Interpretation
- Provide possible explanations for the visible findings.
- State the confidence level as low, moderate, or high.
- Mention reasonable alternative possibilities.
- Clearly highlight findings that may require urgent medical review.

### 4. Patient-Friendly Explanation
- Explain the observations in simple language.
- Avoid unnecessary medical jargon.
- Do not claim that the interpretation is a confirmed diagnosis.

### 5. Recommended Next Steps
- Suggest the appropriate healthcare professional.
- Mention whether routine, prompt, or urgent review may be appropriate.
- Recommend comparison with the official radiology report and clinical history.

### 6. Important Disclaimer
- State that this AI analysis is educational only.
- State that only a qualified healthcare professional can provide a diagnosis.

Use clear Markdown headings.
"""


# ---------------------------------------------------------
# INITIALIZE AGENT
# ---------------------------------------------------------

medical_agent = Agent(
    model=Gemini(
        id="gemini-3-flash-preview",
        api_key=GOOGLE_API_KEY,
    ),
    tools=[DuckDuckGoTools()],
    markdown=True,
    instructions=[
        "Never present an AI interpretation as a confirmed diagnosis.",
        "Do not invent measurements, patient history, or test results.",
        "Mention uncertainty and image limitations.",
        "Recommend professional medical review.",
    ],
)


# ---------------------------------------------------------
# ANALYSIS FUNCTION
# ---------------------------------------------------------

def analyze_medical_image(image_path: str) -> str:
    """Send a medical image to the Gemini-powered Agno agent."""

    response = medical_agent.run(
        MEDICAL_ANALYSIS_PROMPT,
        images=[
            AgnoImage(filepath=image_path)
        ],
    )

    content = getattr(response, "content", None)

    if content:
        return str(content)

    return str(response)


# ---------------------------------------------------------
# STREAMLIT INTERFACE
# ---------------------------------------------------------

st.title("🩺 Medical Image Analysis Tool")

st.markdown(
    """
Upload a medical image such as an X-ray, CT image, MRI image,
ultrasound image, or other clinical scan for an AI-assisted explanation.
"""
)

st.warning(
    "This tool is for educational purposes only. It does not replace "
    "a radiologist, doctor, or official medical report."
)

st.sidebar.header("Upload Medical Image")

uploaded_file = st.sidebar.file_uploader(
    "Choose a medical image or PDF",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
        "bmp",
        "pdf",
    ],
)
def convert_pdf_to_images(pdf_file) -> list[str]:
    """Convert every PDF page into a temporary PNG image."""

    temporary_paths = []

    pdf_bytes = pdf_file.getvalue()
    pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)

        pixmap = page.get_pixmap(
            matrix=fitz.Matrix(2, 2),
            alpha=False,
        )

        temporary_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".png",
        )

        temporary_file.close()
        pixmap.save(temporary_file.name)
        temporary_paths.append(temporary_file.name)

    pdf_document.close()

    return temporary_paths
if uploaded_file is None:
    st.info("Upload a medical image or PDF from the sidebar to begin.")

else:
    file_extension = Path(uploaded_file.name).suffix.lower()

    if file_extension == ".pdf":
        st.info(
            "PDF uploaded successfully. Each page will be converted "
            "into an image for analysis."
        )

        analyze_button = st.sidebar.button(
            "Analyze PDF",
            type="primary",
            use_container_width=True,
        )

        if analyze_button:
            temporary_paths = []

            try:
                with st.spinner("Converting and analyzing the PDF..."):
                    temporary_paths = convert_pdf_to_images(
                        uploaded_file
                    )

                    if not temporary_paths:
                        st.error("The PDF does not contain any pages.")
                        st.stop()

                    for page_number, image_path in enumerate(
                        temporary_paths,
                        start=1,
                    ):
                        st.subheader(f"PDF Page {page_number}")

                        st.image(
                            image_path,
                            caption=f"Page {page_number}",
                            use_container_width=True,
                        )

                        report = analyze_medical_image(image_path)

                        st.markdown(
                            f"### Analysis for Page {page_number}"
                        )
                        st.markdown(report)

            except Exception as error:
                st.error(f"Unable to analyze the PDF: {error}")

            finally:
                for temporary_path in temporary_paths:
                    if os.path.exists(temporary_path):
                        os.remove(temporary_path)

    else:
        try:
            preview_image = PILImage.open(uploaded_file)

            st.image(
                preview_image,
                caption="Uploaded medical image",
                use_container_width=True,
            )

        except Exception as image_error:
            st.error(
                f"Unable to open the uploaded image: {image_error}"
            )
            st.stop()

        analyze_button = st.sidebar.button(
            "Analyze Image",
            type="primary",
            use_container_width=True,
        )

        if analyze_button:
            file_suffix = file_extension

            if file_suffix not in {
                ".jpg",
                ".jpeg",
                ".png",
                ".webp",
                ".bmp",
            }:
                file_suffix = ".png"

            temporary_path = None

            try:
                uploaded_file.seek(0)

                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=file_suffix,
                ) as temporary_file:
                    temporary_file.write(
                        uploaded_file.getbuffer()
                    )
                    temporary_path = temporary_file.name

                with st.spinner("Analyzing the medical image..."):
                    report = analyze_medical_image(
                        temporary_path
                    )

                st.subheader("🩺 AI-Assisted Analysis")
                st.markdown(report)

            except Exception as error:
                st.error(
                    f"Unable to analyze the image: {error}"
                )
            finally:
                if (
                    temporary_path
                    and os.path.exists(temporary_path)
                ):
                    os.remove(temporary_path)