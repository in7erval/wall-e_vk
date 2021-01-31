from constants import BEGIN, END
import random
from db import connection
import db
import datetime


def get_strings(peer_id):
    resp = db.execute_read_query(connection, f"SELECT text FROM messages WHERE peer_id={peer_id}")
    strings = list()
    for a in resp:
        strings.append(a[0])
    return strings


def create_dict(peer_id):
    strings = get_strings(peer_id)
    strs = set(strings)
    strings = list()
    for x in strs:
        strings.append(x.replace(",", " ").replace("?", " ").replace("!", " ").replace(".", " ").split())
    dictionary = {BEGIN: set(), END: set()}
    for i in range(len(strings)):
        x = strings[i]
        for j in range(len(x)):
            if x[j] not in dictionary.keys():
                dictionary[x[j]] = set()
    for x in strings:
        if len(x) > 0:
            dictionary[BEGIN].add(x[0])
    for x in strings:
        if len(x) > 1:
            for i in range(len(x) - 1):
                if x[i] not in dictionary.keys():
                    dictionary[x[i]] = set()
                dictionary[x[i]].add(x[i + 1])
        if len(x) > 0:
            dictionary[x[len(x) - 1]].add(END)
    return dictionary


def generate(peer_id, length):
    generated = ""
    dictionary = create_dict(peer_id)
    count = 0
    while len(generated.split(" ")) < length and count < 10000:
        generated = find(dictionary).strip().capitalize()
        count += 1
    return generated


def find(dictionary, generated=""):
    words = list(dictionary.get(BEGIN))
    while True:
        word = random.choice(words)
        if word == END:
            break
        generated += (word + " ")
        words = list(dictionary.get(word))
    return generated


def dict_to_readable(dictionary):
    readable = ""
    for key in dictionary:
        readable += f"'{key}': {dictionary[key]}\n"
    return readable


def dict_to_file(dictionary):
    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    basename = "dict"
    filename = "_".join([basename, suffix]) + ".txt"
    tf = open(filename, "a+")
    for key in dictionary:
        tf.write(f"'{key}': {dictionary[key]}\n")
    tf.close()
    return filename
