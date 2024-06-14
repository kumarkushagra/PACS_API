from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from functions import upload_zip
from datetime import datetime

app = FastAPI()

# Mount the 'static' directory to serve static files like index.html
app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint to render index.html
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return HTMLResponse(content=open("static/index.html", "r").read())

# Endpoint for uploading files and triggering the upload_zip function

@app.post("/upload-dicom/")
async def upload_dicom(
    dir_path: str = Form(...),
    csv_file: UploadFile = File(...),
    anonymize_flag: bool = Form(...)
):
    # Create log (txt) file 
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    name = f"log.{timestamp}.txt"

    with open(name, "w") as logFile:
        logFile.write(timestamp + "\n")



    # Save the uploaded CSV file
    csv_path = f"temp_{csv_file.filename}"
    with open(csv_path, "wb") as buffer:
        shutil.copyfileobj(csv_file.file, buffer)
    

    try:
        # Call the upload_zip function
        upload_zip(dir_path, csv_path, anonymize_flag,name)
        # Remove the temporary CSV file after processing
        # os.remove(csv_path)
        
        return JSONResponse(content={"detail": "DICOM files uploaded and processed successfully"}, status_code=200)
    except Exception as e:
        # Remove the temporary CSV file if an error occurs
        # os.remove(csv_path)
        raise HTTPException(status_code=500, detail=e)

    



