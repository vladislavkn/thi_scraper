import spacy

nlp = spacy.load("en_core_web_sm")


def annotate_text(text):
    doc = nlp(text)

    if not is_meaningful(doc):
        return None

    question = get_question_type(doc)

    if not question:
        return None

    context = set(
        [w.lower() for w in [get_subject(doc), *get_objects(doc)] if w is not None]
    )

    if len(context) == 0:
        return None

    return [question, *context]


def is_meaningful(doc):
    meaningful_words = [
        token for token in doc if not token.is_stop and not token.is_punct
    ]
    return len(meaningful_words) > 3


def get_question_type(doc):
    questions_count = {"where": 0, "who": 0, "how many": 0, "what": 0, "when": 0}
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            questions_count["who"] += 1
        if ent.label_ in ["FAC", "GPE", "LOC"]:
            questions_count["where"] += 1
        if ent.label_ in ["PRODUCT", "WORK_OF_ART", "ORG"]:
            questions_count["what"] += 1
        if ent.label_ in ["EVENT", "DATE", "TIME"]:
            questions_count["when"] += 1
        if ent.label_ in ["PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"]:
            questions_count["how many"] += 1

    if sum(questions_count.values()) == 0:
        return None

    return max(questions_count.keys(), key=lambda k: questions_count[k])


def get_subject(doc):
    root = None
    for token in doc:
        if "ROOT" in token.dep_:
            return token.text

    return None


def get_objects(doc):
    objects = []
    for token in doc:
        if "obj" in token.dep_ or "nsubj" in token.dep_:
            objects.append(token.text)

    return objects[1:3]
