import ollama

def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)

def retrieve(dataset, query, top_n=3, similarity_function=cosine_similarity, model='hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'):
    query_embedding = ollama.embed(model=model, input=query)['embeddings'][0]
    similarities = []
    for chunk, embedding in dataset:
        similarity = similarity_function(query_embedding, embedding)
        similarities.append((chunk, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]

def ask(dataset, input_query, model='hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'):
    retrieved_knowledge = retrieve(dataset, input_query)
    newline = ord('\n')

    instruction_prompt = f'''You are a helpful chatbot.
    Use only the following pieces of context to answer the question. Don't make up any new information:
    {str(newline).join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])}
    '''

    stream = ollama.chat(
        model=model,
        messages=[
            {'role': 'system', 'content': instruction_prompt},
            {'role': 'user', 'content': input_query},
        ],
        stream=True,
    )

    return stream
