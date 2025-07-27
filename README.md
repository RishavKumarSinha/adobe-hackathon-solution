# Adobe India Hackathon 2025 - Solution

This repository contains the complete solution for Challenges 1a and 1b, developed by Team Codient. The solution is packaged as a single, efficient, and offline-capable Docker container.

---

## Team Information 

* **Team Name:** Codient
* **Team Leader:** Gopal Ranjan
* **Member:** Rishav Kumar Sinha

---

## Architecture Overview

The solution is designed as a modular Python application with two main components:

1.  **Challenge 1a (`challenge_1a/`):** A high-performance PDF-to-JSON processor. It uses the **PyMuPDF** library for fast text and structure extraction, ensuring it meets the strict 10-second performance constraint.
2.  **Challenge 1b (`challenge_1b/`):** A persona-based document analysis engine. It leverages a lightweight, offline **Sentence Transformer model (`all-MiniLM-L6-v2`)** to find semantically relevant content across multiple documents based on a user's task. The model is pre-packaged within the Docker image to ensure zero network dependency.

A master `main.py` script acts as an entrypoint, routing execution to the appropriate challenge based on the `CHALLENGE` environment variable.

---

## Tech Stack 

* **Language:** Python 3.10
* **PDF Processing:** PyMuPDF (`fitz`)
* **NLP/ML:** `sentence-transformers`, `torch` (CPU)
* **Containerization:** Docker

---

## How to Build and Run

### Build the Docker Image

From the root of the repository, run:

```bash
docker build --platform linux/amd64 -t adobe-solution .
```

### Running Challenge 1a

This command processes all PDFs from a local ./input_1a directory and saves JSONs to ./output_1a.

Place your test PDFs in a folder named input_1a.

Create an empty folder named output_1a.

Run the container:

```bash
docker run --rm \
  -e CHALLENGE=1a \
  -v $(pwd)/input_1a:/app/input:ro \
  -v $(pwd)/output_1a:/app/output \
  --network none \
  adobe-solution
```

### Running Challenge 1b

This command runs the analysis for a specific collection.

Prepare your input folder (e.g., my_collection) containing challenge1b_input.json and a PDFs/ subdirectory.

Create an empty folder named output_1b.

Run the container:

```bash
docker run --rm \
  -e CHALLENGE=1b \
  -v $(pwd)/my_collection:/app/input:ro \
  -v $(pwd)/output_1b:/app/output \
  --network none \
  adobe-solution
```

---

## Constraints and Considerations

1. Execution Time: PyMuPDF and the MiniLM model are highly optimized for speed.

2. Model Size: all-MiniLM-L6-v2 is ~80MB, well under the 200MB limit.

3. Network: The container is fully self-contained with no internet access required at runtime (--network none).

4. Architecture: The Dockerfile specifies linux/amd64 for compatibility.

---

## Acknowledgements

As students from Mechanical and Civil engineering backgrounds, we had a fantastic time diving into this challenge and learning to build a complete prototype, completely on our own. From wrangling a Docker container to taming an AI model, this was an incredible learning sprint for us two non-CS engineers. A huge thank you to Adobe for the opportunity!
