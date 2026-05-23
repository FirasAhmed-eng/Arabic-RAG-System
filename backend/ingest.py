import pymupdf as pypdf
from camel_tools.utils import normalize
from camel_tools.utils.dediac import dediac_ar


def extract_text_for_llm(path):
    all_text = []
    with pypdf.open(path) as pdf:
        for page in pdf:
            text = page.get_text()
            if text:
                # Keep the raw, unaltered text
                all_text.append(f"--- Page {page.number} ---\n{text}")

    return "\n\n".join(all_text)


def preprocess_text(raw_text):
    # rem = remove

    norm_text = normalize.normalize_alef_ar(raw_text)
    norm_text = normalize.normalize_alef_maksura_ar(norm_text)
    norm_text = normalize.normalize_teh_marbuta_ar(norm_text)
    norm_text = dediac_ar(norm_text)
    return norm_text


# --------- Enable comments for debugging ---------


# raw_text = extract_text_for_llm("data/SDAIA.pdf")
# print(len(raw_text))


# with open("debug_output.txt", "w", encoding="utf-8") as f:
#     f.write(raw_text[9990:11000])


# sentence = "هَلْ ذَهَبْتَ إِلَى المَكْتَبَةِ؟"

# print(preprocess_text(sentence))
# with open("debug_output.txt", "w", encoding="utf-8") as f:
#     f.write(preprocess_text(sentence))
