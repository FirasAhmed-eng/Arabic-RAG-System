import os
import pymupdf as pypdf
from camel_tools.utils.normalize import (
    normalize_alef_ar,
    normalize_alef_maksura_ar,
    normalize_teh_marbuta_ar,
)
from camel_tools.utils.dediac import dediac_ar
from langchain_core.documents import Document


def preprocess_text(raw_text):

    text = normalize_alef_ar(raw_text)
    text = normalize_alef_maksura_ar(text)
    text = normalize_teh_marbuta_ar(text)
    text = dediac_ar(text)

    # normalize whitespace
    text = " ".join(text.split())
    return text


def extract_text(path) -> list[Document]:
    pages = []

    try:
        with pypdf.open(path) as pdf:
            for page_num, page in enumerate(pdf, start=1):  # type: ignore
                text = page.get_text()
                if not text or not text.strip():
                    continue

                cleaned_text = preprocess_text(text)

                pages.append(
                    {
                        "page": page_num,
                        "text": cleaned_text,
                        "source": os.path.basename(path),
                    }
                )
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return pages

# --------- Enable comments for debugging ---------


# raw_text = extract_text("data/SDAIA.pdf")
# print(len(raw_text))


# with open("debug_output.txt", "w", encoding="utf-8") as f:
#     f.write(raw_text[9990:11000])


# sentence = "هَلْ ذَهَبْتَ إِلَى المَكْتَبَةِ؟"

# print(preprocess_text(sentence))
# with open("debug_output.txt", "w", encoding="utf-8") as f:
#     f.write(preprocess_text(sentence))
