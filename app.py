from fastapi import FastAPI, UploadFile, File, HTTPException
from langserve import add_routes
from chain import create_summarization_chain
import pypdf
import tempfile
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("llm-summarizer")


# Create FastAPI app
app = FastAPI(
    title="Text Summarization API",
    description="An API for summarizing text using Google's Gemini model",
    version="1.0.0",
)

# Create the summarization chain
summarization_chain = create_summarization_chain()

# Define some helper functions to upload files
def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# Add LangServe route
add_routes(
    app,
    summarization_chain,
    path="/summarize",
)
# Endpoint for file upload and summarization
@app.post("/upload-and-summarize")
async def upload_and_summarize(file: UploadFile = File(...)):
    try:
        # Read file content
        file_content = await file.read()
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file_content)
        temp_file_path = temp_file.name
        temp_file.close()
        extracted_text = extract_text_from_pdf(temp_file_path)
        # Process with summarization chain
        result = summarization_chain.invoke({"text": extracted_text})
        
        # return {"summary": result["text"]}
        return {"summary": result["output"]["text"]}
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Add langchain route for pdf uploads
add_routes(
    app,
    summarization_chain,
    path="/upload-and-summarize",
)

if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8080, reload=True)