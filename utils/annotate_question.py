import spacy

nlp = spacy.load("en_core_web_sm")


def annotate_question(text):
    doc = nlp(text)
    question_word = get_question_word(doc)
    tags = [question_word, get_subject(doc), *get_objects(doc)]
    if len(tags) == 0:
        return None
    return [w for w in tags if w is not None]


def get_question_word(doc):
    words = [token.text.lower() for token in doc]
    for word in ["what", "where", "who", "how many", "when"]:
        if word in words:
            return word


def get_subject(doc):
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            return token.text

    return None


def get_objects(doc):
    objects = []
    for token in doc:
        if "obj" in token.dep_ or "nsubj" in token.dep_:
            objects.append(token.text)

    return objects[1:3]
