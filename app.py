import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image as PILImage

from agno.agent import Agent
from agno.media import Image as AgnoImage
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Medical Image Analyzer",
    page_icon="🩺",
    layout="wide",
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
        "GOOGLE_API_KEY is missing. Add it in Streamlit Secrets "
        "or in your local .env file."
    )
    st.stop()

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


# ---------------------------------------------------------
# AI AGENT
# ---------------------------------------------------------

medical_agent = Agent(
    model=Gemini(
        id="gemini-2.0-flash",
        api_key=GOOGLE_API_KEY,
    ),
    tools=[DuckDuckGoTools()],
    markdown=True,
    instructions=[
        "You are an AI medical image analysis assistant.",
        "Carefully examine the uploaded medical image.",
        "Describe visible findings in simple language.",
        "Mention possible abnormalities and their locations.",
        "Do not provide a definitive medical diagnosis.",
        "Recommend consultation with a qualified medical professional.",
        "Mention urgent warning signs when appropriate.",
    ],
)


# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------

st.title("🩺 AI Medical Image Analyzer")

st.write(
    "Upload a medical scan or image to receive an AI-assisted explanation."
)

st.warning(
    "This application is for educational purposes only and does not replace "
    "professional medical diagnosis."
)

uploaded_file = st.file_uploader(
    "Upload a medical image",
    type=["jpg", "jpeg", "png", "webp"],
)


# ---------------------------------------------------------
# IMAGE ANALYSIS
# ---------------------------------------------------------

if uploaded_file is not None:
    try:
        image = PILImage.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Uploaded Image")
            st.image(
                image,
                caption="Uploaded medical image",
                use_container_width=True,
            )

        with col2:
            st.subheader("AI Analysis")

            if st.button(
                "Analyze Image",
                type="primary",
                use_container_width=True,
            ):
                with st.spinner("Analyzing the image..."):
                    suffix = Path(uploaded_file.name).suffix or ".png"

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=suffix,
                    ) as temporary_file:
                        image.save(temporary_file.name)
                        temporary_path = temporary_file.name

                    try:
                        response = medical_agent.run(
                            """
                            Analyze this medical image carefully.

                            Provide the response using these sections:

                            1. Image type
                            2. Visible observations
                            3. Possible findings
                            4. Severity or urgency
                            5. Recommended next steps
                            6. Important medical disclaimer
                            """,
                            images=[
                                AgnoImage(filepath=temporary_path)
                            ],
                        )

                        result = getattr(
                            response,
                            "content",
                            str(response),
                        )

                        st.markdown(result)

                    finally:
                        if os.path.exists(temporary_path):
                            os.remove(temporary_path)

    except Exception as error:
        st.error(f"Unable to process the image: {error}")

else:
    st.info("Upload an image to begin the analysis.")