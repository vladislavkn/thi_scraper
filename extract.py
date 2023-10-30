import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

# Download required datasets
nltk.download('stopwords')
nltk.download('punkt')

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_keywords(text, num_keywords=10):
    # Tokenize the text
    words = word_tokenize(text)

    # Remove punctuation and convert to lowercase
    words = [word.lower() for word in words if word.isalpha()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Get frequency distribution
    freq_dist = Counter(words)

    # Extract top keywords
    keywords = [word for word, freq in freq_dist.most_common(num_keywords)]

    return keywords

file_path = './test'
text = read_file(file_path)
print(text)

print(extract_keywords(text))
