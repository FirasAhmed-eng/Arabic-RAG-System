import re
import os
import pymupdf as pypdf
from camel_tools.utils.normalize import (
    normalize_alef_ar,
    normalize_alef_maksura_ar,
    normalize_teh_marbuta_ar,
)
from camel_tools.utils.dediac import dediac_ar
from langchain_core.documents import Document

from vector import vector_embedding
from chunking import chunk_text

collection_name = "rag"


def preprocess_text(raw_text):

    text = normalize_alef_ar(raw_text)
    text = normalize_alef_maksura_ar(text)
    text = normalize_teh_marbuta_ar(text)
    text = dediac_ar(text)

    # Replace punctuation with single spaces
    text = re.sub(r"[^\w\s]", " ", text)
    # Collapse multiple spaces into one space
    text = re.sub(r"\s+", " ", text)
    # Remove trailing and leading spaces
    text = text.strip()
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


raw_text = extract_text("data/SDAIA.pdf")
chunks = chunk_text(raw_text)
print(len(chunks))

vector_embedding(chunks, collection_name)

print("Collection ready.")
