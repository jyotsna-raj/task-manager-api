import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
from nltk.util import ngrams

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

text = "I am learning NLP and enjoying it"

tokens = word_tokenize(text)
print("Tokens:", tokens)

stemmer = PorterStemmer()
stems = [stemmer.stem(w) for w in tokens]
print("Stemming:", stems)

lemmatizer = WordNetLemmatizer()
lemmas = [lemmatizer.lemmatize(w) for w in tokens]
print("Lemmatization:", lemmas)

pos = pos_tag(tokens)
print("POS Tags:", pos)

bigrams = list(ngrams(tokens, 2))
print("Bigrams:", bigrams)
