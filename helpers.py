import ollama
import json

EMBEDDING_MODEL = 'hf.co/CompendiumLabs/bge-base-en-v1.5-gguf'
LANGUAGE_MODEL = 'hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF'

def data_to_vec(data, model=EMBEDDING_MODEL):
    return ollama.embed(model=model, input=data)['embeddings'][0]  

def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)

def ask_model(prompt, question, model=LANGUAGE_MODEL):
    stream = ollama.chat(
        model=model,
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': question},
        ],
        stream=True,
    )

    return stream

def read_gemini_json(filename):
    with open(filename, encoding="utf8") as f:
        d = json.load(f)
        return d
    
def write_json_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)