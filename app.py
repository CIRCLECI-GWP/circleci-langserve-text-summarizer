from fastapi import FastAPI, UploadFile, File, HTTPException
from langserve import add_routes
from chain import create_summarization_chain
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

# Add LangServe routes
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
        content = await file.read()
        text = content.decode("utf-8")
        # Process with summarization chain
        result = summarization_chain.invoke({"text": text})
        
        return {"summary": result["text"]}
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)