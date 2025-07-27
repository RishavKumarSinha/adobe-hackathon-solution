from sentence_transformers import SentenceTransformer

print("Downloading and saving the MiniLM model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
model.save('models/minilm')
print("Model saved to models/minilm")