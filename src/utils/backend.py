import requests
import os
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline

model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = pipeline("zero-shot-classification")

def is_text_file(file_path):
    estensioni_file_di_testo = ['.txt', '.html', '.css', '.py', '.js', '.md', '.json', '.php']
    file_extension = os.path.splitext(file_path)[1]
    return file_extension in estensioni_file_di_testo

def is_special_file(file_name):
    nomi_file_speciali = ['TEST', 'TODO', 'LICENSE']  # Aggiungi i nomi dei file speciali
    return file_name in nomi_file_speciali


def get_content(folder, outfile):
    for root, _, files in os.walk(folder):
        for file in files:
                # Ottieni il percorso completo del file corrente
                file_path = os.path.join(root, file)
                
                if is_text_file(file_path) or is_special_file(file_path):
                    print("Adding File: ", file_path)
                    # Leggi il contenuto del file
                    with open(file_path, 'r', encoding='utf-8') as input_file:
                        content = input_file.read()
                        outfile.write(f"\n--- File: {file_path} ---\n")
                        outfile.write(content)
                        outfile.write("\n--- End of File ---\n")

def get_repo_content(repo_url, repo_destination):
    user_name, repo_name = repo_url.split('/')[-2:]
    output_file = f"{user_name}_{repo_name}.txt"
    if os.path.isfile(output_file):
        print("Output file already exists. Exiting function.")
        return
    with open(output_file, "w") as outfile:
        get_content(repo_destination, outfile)

def create_embeddings_and_lines(file_path):
    print(f"Generating embeddings for file {file_path}")
    with open(file_path, 'r') as f:
        lines = f.readlines()
    embeddings = model.encode(lines)
    # Save embeddings and lines to a file
    np.savez(f"{file_path}_embeddings_lines.npz", embeddings=embeddings, lines=lines)
    return embeddings, lines

def load_embeddings_and_lines(file_path):
    data = np.load(f"{file_path}_embeddings_lines.npz", allow_pickle=True)
    embeddings = data['embeddings']
    lines = data['lines']
    return embeddings, lines

def similarity_search(query, embeddings, lines, k=30):
    response_data = ""
    query_embedding = model.encode([query])
    similarities = cosine_similarity(query_embedding, embeddings)
    print(similarities)
    top_k_indices = similarities[0].argsort()[-k:][::-1]

    for index in top_k_indices:
        response_data = response_data + lines[index]

    return response_data

def answers_agent(question, response_data):
    response = nlp(question, candidate_labels=response_data)
    return response['labels'][0]
