import os
import pickle
import random

import sklearn
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier

from main_functions import get_text_from_url
from vectorize_language_data import vectorize

WIKI_LANGUAGES = ["fr", "en", "ru", "es", "de", "nl"]


def url_gen(lang):
    return "https://%s.wikipedia.org/wiki/Special:Random" % lang


def random_from_lang(lang, n=500):
    url = url_gen(lang)
    for i in range(n):
        text = get_text_from_url(url)
        yield text


def paired_data_generator(n_per_lang=500):
    for lang in WIKI_LANGUAGES:
        for page in random_from_lang(lang, n_per_lang):
            print("Loading page in language %s" % lang)
            yield (1 if lang == "en" else 0), page


def paired_data(n_per_lang=100):
    if os.path.isfile("wiki_language_data.pkl"):
        print("Loading cached language data...")
        result = pickle.load(open("wiki_language_data.pkl", "rb"))
        print("Loaded cached language data")
        return result
    print("Loading language data...")
    result = [item for item in paired_data_generator(n_per_lang)]
    print("Loaded language data. Saving...")
    pickle.dump(result, open("wiki_language_data.pkl", "wb"))
    print("Saved language data")
    return result


def split_paired_data(data, prop_testing=0.25):
    random.shuffle(data)
    num_testing = int(len(data) * prop_testing)
    testing_data = data[:num_testing]
    training_data = data[num_testing:]
    return testing_data, training_data


def compute_input_output_split(data):
    return [vectorize(input_val) for output, input_val in data], [output for output, input_val in data]


def data_input_output_split(data, prop_testing=0.25):
    testing_data, training_data = split_paired_data(data, prop_testing)
    return compute_input_output_split(testing_data), compute_input_output_split(training_data)


def train_model(training_vectors, training_labels):
    model = RandomForestClassifier()
    model.fit(training_vectors, training_labels)
    pickle.dump(model, open("language_model.pkl", "wb"))
    return model


def test_model(model, testing_vectors, testing_labels):
    predicted_labels = model.predict(testing_vectors)
    print("F-0.5 score of:", sklearn.metrics.fbeta_score(predicted_labels, testing_labels, 0.5))


if __name__ == "__main__":
    (testing_vectors, testing_labels), (training_vectors, training_labels) = data_input_output_split(paired_data())
    model = train_model(training_vectors, training_labels)
    test_model(model, testing_vectors, testing_labels)
