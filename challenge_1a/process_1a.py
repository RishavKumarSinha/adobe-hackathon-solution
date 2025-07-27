import fitz 
import json
from pathlib import Path
import time

INPUT_DIR = Path("/app/input")
OUTPUT_DIR = Path("/app/output")

def parse_pdf_for_outline(pdf_path: Path):
    """
    Parses a PDF file to extract its title and table of contents (outline),
    matching the required JSON schema.
    """
    try:
        doc = fitz.open(pdf_path)
        
        title = doc.metadata.get("title", pdf_path.stem)
        if not title:
            title = pdf_path.stem

        toc = doc.get_toc()
        
        outline_items = []
        for level, text, page in toc:
            outline_items.append({
                "level": f"H{level}", 
                "text": text,
                "page": page
            })

        output_data = {
            "title": title,
            "outline": outline_items
        }

    finally:
        if 'doc' in locals() and doc:
            doc.close()
            
    return output_data

def main():
    """
    Main function to process all PDFs in the input directory.
    """
    print("Starting Challenge 1a: PDF Outline Extraction...")
    start_time = time.time()
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(INPUT_DIR.glob("*.pdf"))
    if not pdf_files:
        print("Error: No PDF files found in /app/input. Make sure you've mounted the volume correctly.")
        return

    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        try:
            structured_data = parse_pdf_for_outline(pdf_file)
            
            output_filename = OUTPUT_DIR / f"{pdf_file.stem}.json"
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, ensure_ascii=False, indent=2)
                
            print(f"Successfully generated {output_filename.name}")
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
            
    end_time = time.time()
    print(f"Challenge 1a finished in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()