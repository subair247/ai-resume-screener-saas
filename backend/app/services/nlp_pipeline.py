import spacy
from sentence_transformers import SentenceTransformer

_nlp = None
_model = None

def _get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_embedding(text: str):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(text).tolist()

def extract_entities(text: str):
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "SKILL"]]
    return list(set(skills))