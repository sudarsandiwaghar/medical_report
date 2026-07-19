
import os
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
import streamlit as st

# Set your API Key (Replace with your actual key)
GOOGLE_API_KEY = "AIzaSyCr35hxFvSNbqWg0PWkMMLwzjL0M2dLJA"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Ensure API Key is provided
if not GOOGLE_API_KEY:
    raise ValueError("Please set your Google API Key in GOOGLE_API_KEY")

# Initialize the Medical Agent
medical_agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[DuckDuckGoTools()],
    markdown=True
)

# Medical Analysis Query
query = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the medical image and structure your response as follows:

### 1. Image Type & Region
- Identify imaging modality (X-ray/MRI/CT/Ultrasound/etc.).
- Specify anatomical region and positioning.
- Evaluate image quality and technical adequacy.

### 2. Key Findings
- Highlight primary observations systematically.
- Identify potential abnormalities with detailed descriptions.
- Include measurements and densities where relevant.

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level.
- List differential diagnoses ranked by likelihood.
- Support each diagnosis with observed evidence.
- Highlight critical/urgent findings.

### 4. Patient-Friendly Explanation
- Simplify findings in clear, non-technical language.
- Avoid medical jargon or provide easy definitions.
- Include relatable visual analogies.

### 5. Research Context
- Use DuckDuckGo search to find recent medical literature.
- Search for standard treatment protocols.
- Provide 2–3 key references supporting the analysis.

Ensure a structured and medically accurate response using clear markdown formatting.
"""

# Function to analyze medical image
if uploaded_file is not None:
    st.image(
        uploaded_file,
        caption="Uploaded Image",
        use_container_width=True
    )

    if st.sidebar.button(
        "Analyze Image",
        type="primary",
        use_container_width=True
    ):
        file_suffix = Path(uploaded_file.name).suffix.lower()

        if not file_suffix:
            file_suffix = ".png"

        temporary_upload_path = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=file_suffix,
                delete=False
            ) as temporary_file:
                temporary_file.write(uploaded_file.getbuffer())
                temporary_upload_path = temporary_file.name

            with st.spinner("🔍 Analyzing the image..."):
                report = analyze_medical_image(
                    temporary_upload_path
                )

            st.subheader("🩺 Analysis Report")
            st.markdown(report)

        except Exception as error:
            st.error(f"Unable to process the image: {error}")

        finally:
            if (
                temporary_upload_path
                and os.path.exists(temporary_upload_path)
            ):
                os.remove(temporary_upload_path)
else:
    st.info("Upload a medical image from the sidebar to begin.")

# Streamlit UI setup
st.set_page_config(page_title="Medical Image Analysis", layout="centered")
st.title("🩺 Medical Image Analysis Tool 🧠")
st.markdown(
"""
Welcome to the **Medical Image Analysis** tool! 🧑‍⚕️  
Upload a medical image (X-ray, MRI, CT, Ultrasound, etc.), and our AI-powered system will analyze it, providing detailed findings, diagnosis, and research insights.  
Let's get started!
"""
)

# Upload image section
st.sidebar.header("Upload Your Medical Image:")
uploaded_file = st.sidebar.file_uploader("Choose a medical image file", type=["jpg", "jpeg", "png", "bmp", "gif"])

# Button to trigger analysis
if uploaded_file is not None:
    # Display the uploaded image in Streamlit
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.sidebar.button("Analyze Image"):
        with st.spinner("🔍 Analyzing the image... Please wait."):
            # Save the uploaded image to a temporary file
            image_path = f"temp_image.{uploaded_file.type.split('/')[1]}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Run analysis on the uploaded image
            report = analyze_medical_image(image_path)

            # Display the report
            st.subheader("🩺 Analysis Report")
            st.markdown(report, unsafe_allow_html=True)

            # Clean up the saved image file
            os.remove(image_path)
else:
    st.warning("⚠️ Please upload a medical image to begin analysis.")

import os
from PIL import Image as PILImage
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
import streamlit as st

# Set your API Key (Replace with your actual key)
GOOGLE_API_KEY = "AIzaSyCr35hxFvSNbqWg0PWkMMLwzjL0M2dLJA"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Ensure API Key is provided
if not GOOGLE_API_KEY:
    raise ValueError("Please set your Google API Key in GOOGLE_API_KEY")

# Initialize the Medical Agent
medical_agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"),
    tools=[DuckDuckGoTools()],
    markdown=True
)

# Medical Analysis Query
query = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the medical image and structure your response as follows:

### 1. Image Type & Region
- Identify imaging modality (X-ray/MRI/CT/Ultrasound/etc.).
- Specify anatomical region and positioning.
- Evaluate image quality and technical adequacy.

### 2. Key Findings
- Highlight primary observations systematically.
- Identify potential abnormalities with detailed descriptions.
- Include measurements and densities where relevant.

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level.
- List differential diagnoses ranked by likelihood.
- Support each diagnosis with observed evidence.
- Highlight critical/urgent findings.

### 4. Patient-Friendly Explanation
- Simplify findings in clear, non-technical language.
- Avoid medical jargon or provide easy definitions.
- Include relatable visual analogies.

### 5. Research Context
- Use DuckDuckGo search to find recent medical literature.
- Search for standard treatment protocols.
- Provide 2–3 key references supporting the analysis.

Ensure a structured and medically accurate response using clear markdown formatting.
"""

# Function to analyze medical image
if uploaded_file is not None:
    st.image(
        uploaded_file,
        caption="Uploaded Image",
        use_container_width=True
    )

    if st.sidebar.button(
        "Analyze Image",
        type="primary",
        use_container_width=True
    ):
        file_suffix = Path(uploaded_file.name).suffix.lower()

        if not file_suffix:
            file_suffix = ".png"

        temporary_upload_path = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=file_suffix,
                delete=False
            ) as temporary_file:
                temporary_file.write(uploaded_file.getbuffer())
                temporary_upload_path = temporary_file.name

            with st.spinner("🔍 Analyzing the image..."):
                report = analyze_medical_image(
                    temporary_upload_path
                )

            st.subheader("🩺 Analysis Report")
            st.markdown(report)

        except Exception as error:
            st.error(f"Unable to process the image: {error}")

        finally:
            if (
                temporary_upload_path
                and os.path.exists(temporary_upload_path)
            ):
                os.remove(temporary_upload_path)
else:
    st.info("Upload a medical image from the sidebar to begin.")

# Streamlit UI setup
st.set_page_config(page_title="Medical Image Analysis", layout="centered")
st.title("🩺 Medical Image Analysis Tool 🧠")
st.markdown(
"""
Welcome to the **Medical Image Analysis** tool! 🧑‍⚕️  
Upload a medical image (X-ray, MRI, CT, Ultrasound, etc.), and our AI-powered system will analyze it, providing detailed findings, diagnosis, and research insights.  
Let's get started!
"""
)

# Upload image section
st.sidebar.header("Upload Your Medical Image:")
uploaded_file = st.sidebar.file_uploader("Choose a medical image file", type=["jpg", "jpeg", "png", "bmp", "gif"])

# Button to trigger analysis
if uploaded_file is not None:
    # Display the uploaded image in Streamlit
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    if st.sidebar.button("Analyze Image"):
        with st.spinner("🔍 Analyzing the image... Please wait."):
            # Save the uploaded image to a temporary file
            image_path = f"temp_image.{uploaded_file.type.split('/')[1]}"
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Run analysis on the uploaded image
            report = analyze_medical_image(image_path)

            # Display the report
            st.subheader("🩺 Analysis Report")
            st.markdown(report, unsafe_allow_html=True)

            # Clean up the saved image file
            os.remove(image_path)
else:
    st.warning("⚠️ Please upload a medical image to begin analysis.")

