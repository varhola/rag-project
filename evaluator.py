import csv
import random

from retrieval import retrieve
from model import ask, give_answer
from dataset import FILE_DATA
from helpers import read_gemini_json, write_json_file

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

def gemini_comparison(filename):
    gemini_results = read_gemini_json(filename)
    # With our retriever
    model_result = []
    for result in gemini_results:
        similar = retrieve(result["question"])
        context = []
        for s in similar:
            if s[0] not in context:
                context.append(s[0])
        generated_result = give_answer(result["question"], context)
        res = ""
        for r in generated_result:
            res += r['message']['content']
        result["model_answer"] = res
        model_result.append(result)
    write_json_file(model_result, "model_results_smol.json")

    # With correct contexts
    control_result = []
    for result in gemini_results:
        context = []
        if context != "N/A":
            context = result["expected_evidence"].split("<and>")
        generated_result = give_answer(result["question"], context)
        res = ""
        for r in generated_result:
            res += r['message']['content']
        result["model_answer"] = res
        control_result.append(result)
        #print(result["question"])
        #print(result["expected_answer"])
        #print(res.encode('utf-8'))
        #print()
    write_json_file(model_result, "control_results_smol.json")

    # With random contexts
    keys = list(FILE_DATA)
    control_result = []
    for result in gemini_results:
        context = context = keys[random.randint(0,len(FILE_DATA) - 1)]
        generated_result = give_answer(result["question"], context)
        res = ""
        for r in generated_result:
            res += r['message']['content']
        result["model_answer"] = res
        control_result.append(result)
    write_json_file(model_result, "random_results_smol.json")

def debug_retrieval(questions):
    print("Testing retrieval:")
    correct_count = 0
    enought_count = 0
    total_count = 0
    for question in questions:
        similar = retrieve(question[0])
        discussions = []
        for s in similar:
            discussions.append(s[0])
        if question[2] != "N/A":
            has_match = True
            for topic in question[2].split("<and>"):
                if topic not in discussions:
                    has_match = False
            if has_match:
                enought_count += 1

            for topic in discussions:
                if topic in question[2].split("<and>") or has_match:
                    correct_count += 1
                    break

            total_count += 1

    print(" Giving a correct context: " + str(correct_count) + "/" + str(total_count))
    print(" Giving all the necassary context: " + str(enought_count) + "/" + str(total_count))
    print()

def debug_questions(questions, rounds=0):
    print("Testing chatbot:")
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
        print(" Correct answers when using correct contexts: " + str(count) + "/" + str(total))
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
        print(" Correct answers with incorrect contexts: " + str(count) + "/" + str(total))