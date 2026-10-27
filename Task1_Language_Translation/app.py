
import os

import requests
import streamlit as st
from dotenv import load_dotenv
from sarvamai import SarvamAI

# Load the API key from the local .env file
load_dotenv()

st.set_page_config(
    page_title="Language Translator",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 Language Translation Tool")
st.write("Translate text between different languages.")

# Language codes used by MyMemory
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Japanese": "ja",
    "Chinese": "zh",
}

# Corresponding language codes used by Sarvam Translate
SARVAM_CODES = {
    "en": "en-IN",
    "hi": "hi-IN",
    "te": "te-IN",
    "ta": "ta-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
}

# Keep these languages on MyMemory because they worked
# well in your earlier tests.
MYMEMORY_PREFERRED = {
    "ml", "es", "it", "ar", "ja"
}


def translate_with_sarvam(text, source, target):
    """Translate using Sarvam's official Python SDK."""
    api_key = os.getenv("SARVAM_API_KEY")

    if not api_key:
        raise ValueError(
            "SARVAM_API_KEY is missing. Check your local .env file."
        )

    client = SarvamAI(api_subscription_key=api_key)

    result = client.text.translate(
        input=text,
        source_language_code=SARVAM_CODES[source],
        target_language_code=SARVAM_CODES[target],
        model="sarvam-translate:v1",
    )

    return result.translated_text


def translate_with_mymemory(text, source, target):
    """Translate using the MyMemory API."""
    response = requests.get(
        "https://api.mymemory.translated.net/get",
        params={
            "q": text,
            "langpair": f"{source}|{target}",
        },
        timeout=25,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("responseStatus") != 200:
        raise RuntimeError(
            data.get("responseDetails", "MyMemory translation failed.")
        )

    translated = data.get("responseData", {}).get("translatedText", "")

    if not translated:
        raise RuntimeError("MyMemory returned no translation.")

    return translated


col1, col2 = st.columns(2)

with col1:
    source_name = st.selectbox(
        "Translate from",
        list(LANGUAGES.keys()),
        index=0,
    )

with col2:
    target_name = st.selectbox(
        "Translate to",
        list(LANGUAGES.keys()),
        index=1,
    )

input_text = st.text_area(
    "Enter text",
    placeholder="Example: Hello, how are you?",
    height=160,
)

if st.button("🌐 Translate", type="primary", use_container_width=True):

    source = LANGUAGES[source_name]
    target = LANGUAGES[target_name]

    if not input_text.strip():
        st.warning("Please enter some text.")

    elif source == target:
        st.warning("Choose two different languages.")

    elif len(input_text) > 2000:
        st.warning("Please enter 2,000 characters or fewer.")

    else:
        # Use MyMemory for your five previously successful languages.
        use_mymemory = (
            source in MYMEMORY_PREFERRED
            or target in MYMEMORY_PREFERRED
        )

        # Sarvam is used only when both selected languages are supported.
        use_sarvam = (
            not use_mymemory
            and source in SARVAM_CODES
            and target in SARVAM_CODES
        )

        try:
            with st.spinner("Translating..."):

                if use_sarvam:
                    translated = translate_with_sarvam(
                        input_text, source, target
                    )
                    provider = "Sarvam AI"

                else:
                    translated = translate_with_mymemory(
                        input_text, source, target
                    )
                    provider = "MyMemory"

            st.subheader("Translated Text")
            st.text_area(
                "Result",
                value=translated,
                height=160,
            )

            st.caption(f"Translation provider: {provider}")

            st.download_button(
                "Download translation",
                data=translated,
                file_name="translation.txt",
                mime="text/plain",
            )

        except requests.RequestException:
            st.error(
                "Could not connect to MyMemory. "
                "Check your internet connection and try again."
            )

        except Exception as error:
            # Avoid displaying request details or credentials.
            st.error("Translation failed.")
            st.caption(
                "Check your API key, account limits, selected "
                "languages, and terminal error message. "
                "Never share your API key."
            )

st.divider()
st.caption(
    "Built with Python, Streamlit, Sarvam AI, "
    "Requests, and MyMemory."
)
