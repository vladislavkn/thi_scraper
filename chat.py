import json
import numpy as np

from utils.annotate_question import annotate_question
import spacy

nlp = spacy.load("en_core_web_sm")

f = open("results.json")
data = json.load(f)


def get_words_similarity(word1, word2):
    word1_vector = nlp(word1).vector
    word2_vector = nlp(word2).vector

    return word1_vector.dot(word2_vector) / (
        np.linalg.norm(word1_vector) * np.linalg.norm(word2_vector)
    )


def get_tags_similarity(tags1, tags2):
    similarity = 0
    for tag1 in tags1:
        similarity += max([get_words_similarity(tag1, tag2) for tag2 in tags2])

    return similarity


data_len = len(data)


def get_answer(question, process_cb):
    question_tags = annotate_question(question)
    best_similarity = 0
    best_answer = None
    best_index = 0
    for i, entry in enumerate(data):
        similarity = get_tags_similarity(question_tags, entry["tags"]) / len(
            question_tags
        )
        if similarity > best_similarity:
            best_similarity = similarity
            best_answer = entry["answer"]
            best_index = i
        if i % 10 == 0:
            process_cb(i / data_len)

    return best_answer, best_index


while True:
    question = input("U: ")
    answer, index = get_answer(question, lambda p: print(f"{p*100:.2f}%", end="\r"))
    print(end="\r")
    print(f"B: {answer} ({index})")
