from helpers import ask_model
from dataset import FILE_DATA

def ask(question, answer, context):
    keys = FILE_DATA.keys()
    threads = []
    for s in context:
        if s in keys:
            threads.append(FILE_DATA[s])

    newline = '\n'

    prompt = f'''Answer only with yes or no.
    Use only the following discussion as context to answer the question. Don't make up any new information:
    {newline.join(threads)}
    '''

    question = 'Is answer "'+ answer + '" correct answer for question "' + question + '" based on the context from the discussions'

    answer = ask_model(prompt, question)
    return answer


def give_answer(question, context):
    keys = FILE_DATA.keys()
    threads = []
    for s in context:
        if s in keys:
            threads.append(FILE_DATA[s])

    newline = '\n'

    prompt = f'''Give only the answer and nothing else. Answer shortly in one sentence. If not enought information is given, answer only with "Insufficient information".
    Use only the following discussion as context to answer the question. Don't make up any new information:
    {newline.join(threads)}
    '''

    answer = ask_model(prompt, question)
    return answer