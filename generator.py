import os

from main_functions import get_text_from_url


def generate_file_from_url(url: str):
    text = get_text_from_url(url)
    if len(text) < 200:
        return False
    opened_file = open(find_free_filename("./generated/"), "w", encoding="utf-8")
    opened_file.write(text)
    opened_file.close()
    return True


def find_free_filename(directory, iteration=0):
    desired_name = directory + "file_" + str(iteration) + ".txt"
    if os.path.isfile(desired_name):
        return find_free_filename(directory, iteration=iteration + 1)
    return desired_name


def get_apnotes_url(index: int):
    return "https://apnotes.net/notes-12e/ch%d-12e.html" % index


def generate_apnotes_files(count: int):
    for i in range(1, count + 1):
        url = get_apnotes_url(i)
        print(url)
        generate_file_from_url(url)


def generate_wiki_files(count: int):
    generated = 0
    while generated < count:
        if generate_file_from_url("https://en.wikipedia.org/wiki/Special:Random"):
            generated += 1
