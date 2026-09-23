import gc

def get_embedding(text: str):
    return [0.1] * 384

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