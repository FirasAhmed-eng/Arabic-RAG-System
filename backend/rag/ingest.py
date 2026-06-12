import re
import os
import io
import pymupdf as pypdf
import pytesseract
from PIL import Image
from camel_tools.utils.normalize import (
    normalize_alef_ar,
    normalize_alef_maksura_ar,
    normalize_teh_marbuta_ar,
)
from camel_tools.utils.dediac import dediac_ar

from backend.rag.vector import vector_embedding
from backend.rag.chunking import chunk_text


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


def extract_text(path) -> list[dict]:
    pages = []

    try:
        with pypdf.open(path) as pdf:
            for page_num, page in enumerate(pdf, start=1): # type: ignore
                # 1. First attempt: Extract standard embedded text
                text = page.get_text().strip()

                # 2. Fallback: If text is empty or unusually short (e.g., < 20 chars, like a stray header), use OCR
                if len(text) < 20:
                    # Convert the PDF page to a high-resolution image
                    pix = page.get_pixmap(dpi=300)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    
                    # Run OCR. 'ara+eng' allows it to detect Arabic and English seamlessly.
                    text = pytesseract.image_to_string(img, lang="ara+eng").strip()

                # 3. If it's STILL empty after OCR (e.g., a blank page), skip it
                if not text:
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
        print(f"Error reading PDF {path}: {e}")
        
    return pages


def process_pdf(path: str, collection_name: str):
    raw_text = extract_text(path)
    
    # Failsafe in case the PDF was completely empty/unreadable
    if not raw_text:
        return {"pages": 0, "chunks": 0, "error": "No text could be extracted."}
        
    chunks = chunk_text(raw_text)
    vector_embedding(chunks, collection_name)
    
    return {
        "pages": len(raw_text),
        "chunks": len(chunks),
    }