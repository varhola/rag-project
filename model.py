from retrieval import retrieve
from helpers import ask_model
from dataset import FILE_DATA

def ask(question, answer, context):
    #retrieved_knowledge = retrieve(question)

    #titles = []
    keys = FILE_DATA.keys()
    threads = []
    for s in context:
        if s in keys:
            threads.append(FILE_DATA[s])
    #for s in retrieved_knowledge:
    #    if s[0] not in titles:
    #        threads.append(FILE_DATA[s[0]])
    #        titles.append(s[0])

    newline = '\n'

    prompt = f'''Answer only with yes or no.
    Use only the following discussion as context to answer the question. Don't make up any new information:
    {newline.join(threads)}
    '''

    question = 'Is answer "'+ answer + '" correct answer for question "' + question + '" based on the context from the discussions'

    answer = ask_model(prompt, question)
    return answer
