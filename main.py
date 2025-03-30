from dataset import create_dataset, DATASET
from retrieval import retrieve

create_dataset()

input_query = "Li Hua has a difficult client. When did he solve that client's project?"

similar = retrieve(input_query)
print(input_query)
for s in similar:
    print(s)

#answer_stream = ask(dataset, input_query)

#for chunk in answer_stream:
#    print(chunk['message']['content'], end='', flush=True)