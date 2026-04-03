# AI-Powered Document Analysis & Extraction

An AI-driven API that processes documents (PDF, DOCX, Images) and extracts structured insights such as summaries, entities, and sentiment.

---

## Overview
This system automates document understanding by combining OCR and NLP techniques to transform unstructured data into meaningful information.

Designed for real-world applications such as legal analysis, business reports, and academic research.

---

## Features

- PDF and DOCX text extraction  
- OCR support (Tesseract / Google Vision API)  
- AI-based document summarization  
- Entity extraction (Names, Dates, Organizations, Monetary values)  
- Sentiment analysis  
- Fast and scalable API  
- API key-based authentication  

---

## Tech Stack

| Layer        | Technology                          |
|-------------|------------------------------------|
| Backend     | Python, FastAPI                    |
| NLP         | spaCy, NLTK                        |
| Sentiment   | TextBlob                           |
| OCR         | Tesseract OCR, Google Vision API   |
| File Parsing| PyMuPDF, python-docx               |
| Deployment  | Render, Railway                    |

---

## Setup Instructions

### Prerequisites
- Python 3.9 or above  
- pip  

---

### 1. Clone the repository
```bash
git clone https://github.com/yamini-p-cse/document-analysis.git
cd document-analysis


##Install dependencies
pip install -r requirements.txt

##Configure environment variables
Create a .env file:
API_KEY=your_api_key_here

##API Usage
Endpoint
POST /api/document-analyze

##Headers
x-api-key: YOUR_API_KEY
Content-Type: application/json
##Request Body
{
  "file": "BASE64_ENCODED_FILE"
}


##Sample Response
{
  "summary": "This document discusses...",
  "entities": {
    "names": ["John Doe"],
    "dates": ["2024"],
    "organizations": ["ABC Corp"],
    "money": ["$5000"]
  },
  "sentiment": "Positive"
}

##How It Works
Document Processing
  The system extracts text from PDF and DOCX files. For scanned or image-based inputs, OCR is used to retrieve text.
NLP Processing
  spaCy is used for entity recognition
  NLTK is used for summarization
  TextBlob is used for sentiment analysis
Workflow
  User sends a Base64 encoded file
  Backend extracts text
  AI processes the content
  Structured JSON response is returned

##AI Tools Used
spaCy: Named Entity Recognition
NLTK: Text summarization
TextBlob: Sentiment analysis
Tesseract OCR: Image text extraction
Google Vision API (optional): Advanced OCR
Known Limitations
Free hosting platforms may go idle after inactivity
OCR accuracy depends on image quality
Large files may increase processing time
Summarization is basic and not LLM-based
ChatGPT (OpenAI): Assisted in concept understanding, debugging, and implementation guidance
Blackbox AI: Assisted in code generation, debugging, and accelerating development workflow

##Architecture Overview

Client (API Request)
↓
FastAPI Backend
↓
Processing Layer (OCR + NLP + AI)
↓
Response (JSON Output)

##Future Improvements
Integration of LLM-based summarization
Multilingual document support
Web-based dashboard
Real-time document processing
Use Cases
Legal document analysis
Business report summarization
Academic research assistance
Healthcare document processing

##Author
Yamini P
