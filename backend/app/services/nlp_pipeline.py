import gc

def get_embedding(text: str):
    from sentence_transformers import SentenceTransformer
    
    # Load model locally for the request
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(text).tolist()
    
    # Immediately clear memory to stay under Render's 512MB limit
    del model
    gc.collect()
    
    return embedding

def extract_entities(text: str):
    import spacy
    
    # Load spacy locally for the request
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    skills = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PRODUCT", "SKILL"]]
    result = list(set(skills))
    
    # Immediately clear memory
    del nlp
    del doc
    gc.collect()
    
    return result