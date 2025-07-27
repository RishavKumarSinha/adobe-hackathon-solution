import json
from pathlib import Path
import time
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import torch
import fitz  

MODEL_PATH = Path("/app/models/minilm")
INPUT_DIR = Path("/app/input") 
OUTPUT_DIR = Path("/app/output") 

def extract_structured_chunks(pdf_path: Path):
    """
    Extracts content from a PDF, chunking it by sections found in the table of contents.
    This is the key to getting section titles.
    """
    chunks = []
    try:
        doc = fitz.open(pdf_path)
        toc = doc.get_toc()

        if not toc:
            for page in doc:
                chunks.append({
                    "title": f"Page {page.number + 1}",
                    "text": page.get_text("text").strip(),
                    "page": page.number + 1,
                    "document": pdf_path.name
                })
            return chunks

        for i, (level, title, page_num) in enumerate(toc):
            try:
                start_page = page_num - 1
                end_page = toc[i+1][2] - 1 if i + 1 < len(toc) else len(doc)
                
                section_text = ""
                for page_index in range(start_page, end_page):
                    section_text += doc[page_index].get_text("text")

                section_text = ' '.join(section_text.strip().split())

                if section_text:
                    chunks.append({
                        "title": title,
                        "text": section_text,
                        "page": page_num,
                        "document": pdf_path.name
                    })
            except Exception:
                continue
    finally:
        if 'doc' in locals() and doc:
            doc.close()
            
    return chunks

def main():
    """
    Main function to process a collection based on challenge1b_input.json.
    """
    print("Starting Challenge 1b: Persona-Based Analysis...")
    start_time = time.time()
    
    input_json_path = INPUT_DIR / "challenge1b_input.json"
    if not input_json_path.exists():
        print(f"Error: {input_json_path} not found!")
        return
        
    with open(input_json_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    print("Loading NLP model...")
    device = "cpu"
    model = SentenceTransformer(str(MODEL_PATH), device=device)
    print("Model loaded.")

    task_description = input_data["job_to_be_done"]["task"]
    documents = input_data["documents"]
    
    all_chunks = []
    for doc_info in documents:
        pdf_path = INPUT_DIR / "PDFs" / doc_info["filename"]
        if pdf_path.exists():
            print(f"Extracting chunks from {pdf_path.name}...")
            all_chunks.extend(extract_structured_chunks(pdf_path))
        else:
            print(f"Warning: {pdf_path.name} not found.")

    if not all_chunks:
        print("Error: No text chunks could be extracted from any PDF.")
        return

    print("Creating embeddings...")
    task_embedding = model.encode(task_description, convert_to_tensor=True)
    chunk_texts = [chunk['text'] for chunk in all_chunks]
    chunk_embeddings = model.encode(chunk_texts, convert_to_tensor=True, batch_size=32)

    print("Calculating similarity and ranking...")
    cosine_scores = util.cos_sim(task_embedding, chunk_embeddings)[0]
    
    for i, chunk in enumerate(all_chunks):
        chunk['score'] = cosine_scores[i].item()
    
    ranked_chunks = sorted(all_chunks, key=lambda x: x['score'], reverse=True)
    
    print("Formatting final output...")
    top_n_chunks = ranked_chunks[:5] 

    output_data = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": input_data["persona"]["role"],
            "job_to_be_done": task_description,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }
    
    for i, chunk in enumerate(top_n_chunks):
        output_data["extracted_sections"].append({
            "document": chunk["document"],
            "section_title": chunk["title"],
            "importance_rank": i + 1,
            "page_number": chunk["page"]
        })
        output_data["subsection_analysis"].append({
            "document": chunk["document"],
            "refined_text": chunk["text"],
            "page_number": chunk["page"]
        })

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_filename = OUTPUT_DIR / "challenge1b_output.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)
        
    end_time = time.time()
    print(f"Challenge 1b finished in {end_time - start_time:.2f} seconds.")
    print(f"Output generated at {output_filename}")

if __name__ == "__main__":
    main()