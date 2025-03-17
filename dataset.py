import ollama

def read_data(filenames):
    print(" Reading data from files...")
    dataset = []
    for filename in filenames:
        with open(filename, 'r', encoding="utf8") as file:
            dataset.extend(file.readlines())
    print(f' Ready reading files ({len(dataset)} entries)')
    return dataset

def data_to_vec(data, model='hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'):
    return ollama.embed(model=model, input=data)['embeddings'][0]    

def create_dataset(filenames):
    print("Creating new dataset...")
    dataset = read_data(filenames)

    vector_dataset = []
    for chunk in dataset:
        vector_dataset.append(data_to_vec(chunk))

    return vector_dataset
