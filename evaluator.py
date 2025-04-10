import csv
import random

from retrieval import retrieve
from model import ask
from dataset import FILE_DATA

def read_answers(filename):
    res = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            if len(row) > 4:
                pass
            else:
                res.append(row)
    return res[1:]

def combined_evaluation(questions, rounds=5):
    for i in range(rounds):
        print("Round: " + str(i))
        correct_count = 0
        total_count = 0
        for question in questions:
            similar = retrieve(question[0])
            context = []
            for s in similar:
                context.append(s[0])
            answer = ask(question[0], question[1], context)
            for chunk in answer:
                if question[2] == "N/A":
                    if chunk['message']['content'] == "No":
                        correct_count += 1
                else:
                    if chunk['message']['content'] == "Yes":
                        correct_count += 1
            total_count += 1
        print(str(correct_count) + "/" + str(total_count))

def debug_retrieval(questions):
    correct_count = 0
    total_count = 0
    for question in questions:
        similar = retrieve(question[0])
        print(question[0])
        discussions = []
        for s in similar:
            discussions.append(s[0])
        if question[2] != "N/A":
            has_match = True
            for topic in question[2].split("<and>"):
                if topic not in discussions:
                    has_match = False
            if has_match:
                correct_count += 1
            total_count += 1

        #if question[2] != "N/A":
        #    has_match = True
        #    for topic in discussions:
        #        if topic in question[2].split("<and>") and not has_match:
        #            correct_count += 1
        #            has_match = True
        #    total_count += 1

        print(question[1])
        print(str(correct_count) + "/" + str(total_count))
        print()

def debug_questions(questions, rounds=10):
    same = []
    for i in range(rounds):
        print("Round " + str(i))
        # Correct contexts
        incorrect_indexes = []
        index = 0
        count = 0
        total = 0
        context = []
        for question in questions:
            if question[2] != "N/A":
                context = question[2].split("<and>")
                answer = ask(question[0], question[1], context)
                for chunk in answer:
                    if chunk['message']['content'] == "Yes":
                        count += 1
                    elif index in same or i == 0:
                        incorrect_indexes.append(index)
                    total += 1
                    break
            index += 1
        print(str(count) + "/" + str(total))
        same = incorrect_indexes
        # Incorrect contexts
        keys = list(FILE_DATA)
        index = 0
        count = 0
        total = 0
        for question in questions:
            if question[2] != "N/A":
                context = keys[random.randint(0,len(FILE_DATA) - 1)]
                answer = ask(question[0], question[1], context)
                for chunk in answer:
                    if chunk['message']['content'] == "Yes":
                        count += 1
                    total += 1
                    break
            index += 1
        print(str(count) + "/" + str(total))
    print(same)