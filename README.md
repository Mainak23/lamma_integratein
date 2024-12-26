# Ollama Vision Model for Invoice Line Item Extraction via Flask API

This repository demonstrates the implementation of the Ollama Vision model to extract line items and other key information from invoices. It provides a Flask-based API that accepts a PDF file, processes it using the vision model, and returns structured data.

---

## Features

- **OCR-based Line Item Extraction**: Efficiently extracts table data such as line items from invoices.
- **Key Information Retrieval**: Identifies essential fields like invoice number, date, total amount, and vendor details.
- **Flask API Integration**: Simple endpoint for uploading PDFs and receiving processed data in JSON format.
- **Scalability**: Modular design for easy extension and integration with other applications.

---

## Getting Started

### Prerequisites

- Python 3.8+
- Install required libraries:
  ```bash
  pip install -r requirements.txt
  ```
- Ollama Vision model set up and accessible via API or SDK.
- Install Llama Vision:
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
