import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt

# Download once
nltk.download('punkt')

# Input
text = input("Enter a sentence: ")

# Tokenize
tokens = word_tokenize(text.lower())

# Remove punctuation
words = [w for w in tokens if w.isalpha()]

# Bag of Words
bow = Counter(words)

# Print result
print("\nBag of Words:")
for word, freq in bow.items():
    print(word, ":", freq)

# Simple bar graph
plt.bar(bow.keys(), bow.values())
plt.title("Word Frequency")
plt.xlabel("Words")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.show()
