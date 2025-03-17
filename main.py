from model import ask
from dataset import create_dataset

input_files = ['cat-facts.txt']
dataset = create_dataset(input_files)

input_query = input('Ask me a question: ')

answer_stream = ask(dataset, input_query)

for chunk in answer_stream:
    print(chunk['message']['content'], end='', flush=True)