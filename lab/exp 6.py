import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

df = pd.read_csv("downsampled_dataset.csv")

documents = (df["TITLE"].fillna('') + " " + df["ABSTRACT"].fillna('')).tolist()

vectorizer = CountVectorizer(stop_words='english')
X = vectorizer.fit_transform(documents)

lda = LatentDirichletAllocation(n_components=3, random_state=42)
lda.fit(X)

words = vectorizer.get_feature_names_out()

for i, topic in enumerate(lda.components_):
    top_words = [words[j] for j in topic.argsort()[-8:]]
    top_values = [topic[j] for j in topic.argsort()[-8:]]

    print("Topic", i+1)
    print(top_words)
    print()

    plt.figure()
    plt.bar(top_words, top_values)
    plt.title(f"Topic {i+1}")
    plt.xticks(rotation=45)
    plt.show()
