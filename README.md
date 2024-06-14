# Upload DICOM Data

This project facilitates the uploading, processing, and anonymizing of DICOM series via an API. Below are the steps and details for setting up and using the project.

## Setup Instructions

1. **Ensure Server Configuration**: Ensure Orthanc is running and accessible at port 8042. If Orthanc is hosted on a different port, update the port number in `main.py`.

2. **Ensure fastAPI is hosted**: Ensure that the 'main.py' has also been hosted using the command 'uvicorn main:app --reload'. 

3. **Install Requirements**: Make sure all necessary dependencies are installed. These dependencies are typically listed in `requirements.txt` or the import statements within `main.py`.

## File Description

### functions.py

This file contains user-defined functions essential for processing and handling DICOM data.

#### Functionality Overview

1. **`load_dicom(dir_path)`**:
   - **Purpose**: Loads DICOM files from a specified directory.
   - **Parameters**: 
     - `dir_path` (str): The path to the directory containing DICOM files.
   - **Returns**: A list of DICOM file objects.

2. **`anonymize_dicom(dicom_files)`**:
   - **Purpose**: Anonymizes the given DICOM files.
   - **Parameters**: 
     - `dicom_files` (list): A list of DICOM file objects to be anonymized.
   - **Returns**: A list of anonymized DICOM file objects.

3. **`load_csv(csv_path)`**:
   - **Purpose**: Loads data from a CSV file.
   - **Parameters**: 
     - `csv_path` (str): The path to the CSV file.
   - **Returns**: DataFrame containing the CSV data.

4. **`process_dicom_and_csv(dicom_files, csv_data)`**:
   - **Purpose**: Processes DICOM files and CSV data together.
   - **Parameters**: 
     - `dicom_files` (list): A list of DICOM file objects.
     - `csv_data` (DataFrame): DataFrame containing the CSV data.
   - **Returns**: A combined dataset or processed output.

5. **`save_processed_data(data, output_path)`**:
   - **Purpose**: Saves processed data to a specified path.
   - **Parameters**: 
     - `data` (any): The data to be saved.
     - `output_path` (str): The path where the data should be saved.
   - **Returns**: None

6. **`upload_data(url, data)`**:
   - **Purpose**: Uploads data to a specified URL.
   - **Parameters**: 
     - `url` (str): The endpoint URL where the data should be uploaded.
     - `data` (any): The data to be uploaded.
   - **Returns**: Response from the server.

### main.py

This file contains the main script to run the application. It integrates all functions and handles the overall logic.

#### Functionality Overview

The `main.py` script performs the following tasks:

1. **Import necessary modules and functions**:
   ```python
   from functions import load_dicom, anonymize_dicom, load_csv, process_dicom_and_csv, save_processed_data, upload_data
   import os
   ```

2. **Define constants and configurations**:
   ```python
   DICOM_DIR = '/path/to/dicom/files'
   CSV_PATH = '/path/to/csv/file.csv'
   OUTPUT_PATH = '/path/to/output/file'
   UPLOAD_URL = 'http://localhost:8000/upload-dicom/'
   ANONYMIZE = True
   ```

3. **Load DICOM files**:
   ```python
   dicom_files = load_dicom(DICOM_DIR)
   ```

4. **Anonymize DICOM files if the flag is set**:
   ```python
   if ANONYMIZE:
       dicom_files = anonymize_dicom(dicom_files)
   ```

5. **Load CSV data**:
   ```python
   csv_data = load_csv(CSV_PATH)
   ```

6. **Process DICOM files and CSV data together**:
   ```python
   processed_data = process_dicom_and_csv(dicom_files, csv_data)
   ```

7. **Save the processed data**:
   ```python
   save_processed_data(processed_data, OUTPUT_PATH)
   ```

8. **Upload the processed data**:
   ```python
   response = upload_data(UPLOAD_URL, processed_data)
   print(response)
   ```

### index.html

This file provides a simple web interface for users to upload DICOM data and an accompanying CSV file.

#### HTML Structure

- **Header**: Contains metadata and title.
- **Body**:
  - A form to upload DICOM data and a CSV file.
  - Fields include directory path for DICOM files, an option to anonymize data, and a file input for the CSV file.
  - The form uses POST method to send data to the specified endpoint.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload DICOM Data</title>
</head>
<body>
    <h2>Upload DICOM Data</h2>
    <form id="uploadForm" action="http://localhost:8000/upload-dicom/" method="POST" enctype="multipart/form-data">
        <label for="dir_path">Directory Path (dir_path):</label><br>
        <input type="text" id="dir_path" name="dir_path" value="/path/to/your/directory" required><br><br>
        
        <label for="anonymize_flag">Anonymize Flag (anonymize_flag):</label><br>
        <input type="checkbox" id="anonymize_flag" name="anonymize_flag" checked>
        <label for="anonymize_flag">Anonymize Data</label><br><br>
        
        <label for="csv_file">Upload CSV File:</label><br>
        <input type="file" id="csv_file" name="csv_file" required accept=".csv"><br><br>
        
        <input type="submit" value="Submit">
    </form>
</body>
</html>
```

## Function Explanation

### Endpoint

The `/upload-dicom/` endpoint is defined to handle the uploading process. Here’s how it works:

```python
@app.post("/upload-dicom/")
async def upload_dicom_data(dir_path: str, anonymize_flag: bool, csv_file: UploadFile):
    dicom_files = load_dicom(dir_path)
    
    if anonymize_flag:
        dicom_files = anonymize_dicom(dicom_files)
    
    csv_data = load_csv(csv_file.file)
    
    processed_data = process_dicom_and_csv(dicom_files, csv_data)
    
    save_processed_data(processed_data, OUTPUT_PATH)
    
    response = upload_data(UPLOAD_URL, processed_data)
    return response
```

#### Explanation:

1. **`upload_dicom_data(dir_path: str, anonymize_flag: bool, csv_file: UploadFile)`**:
   - This function is an asynchronous HTTP POST endpoint that accepts `dir_path`, `anonymize_flag`, and `csv_file` parameters.
   - `dir_path` represents the directory path containing DICOM series to upload.
   - `anonymize_flag` indicates whether to anonymize the DICOM data.
   - `csv_file` is the CSV file uploaded by the user.

2. **`load_dicom(dir_path)`**: Loads DICOM files from the specified directory.

3. **`anonymize_dicom(dicom_files)`**: Anonymizes the DICOM files if the anonymize flag is set.

4. **`load_csv(csv_file.file)`**: Loads data from the uploaded CSV file.

5. **`process_dicom_and_csv(dicom_files, csv_data)`**: Processes the DICOM files and CSV data together.

6. **`save_processed_data(processed_data, OUTPUT_PATH)`**: Saves the processed data to the specified output path.

7. **`upload_data(UPLOAD_URL, processed_data)`**: Uploads the processed data to the specified URL and returns the server response.

## Additional Functions

### Delete All Studies

There is a function available to delete all studies stored in the PACS server:

```python
import requests

# Base URL for the Orthanc instance
ORTHANC_URL = 'http://localhost:8000'

def delete_all_studies():
    # Endpoint to retrieve all studies
    studies_url = f'{ORTHANC_URL}/studies'
    
    try:
        # Get all studies
        response = requests.get(studies_url)
        response.raise_for_status()
        study_ids = response.json()
        
        # Delete each study
        for study_id in study_ids:
            study_delete_url = f'{ORTHANC_URL}/studies/{study_id}'
            delete_response = requests.delete(study_delete_url)
            delete_response.raise_for_status()
            print(f'Successfully deleted study: {study_id}')
    
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    delete_all_studies()
```

#### Explanation:

- **`delete_all_studies()`**:
  - Retrieves all study IDs from the PACS server.
  - Deletes each study using its StudyID.
  - Prints a success message for each deleted study or an error message if an exception occurs.

### Anonymized Copy

Every time this code is executed, it automatically creates an anonymized copy of all studies present in the PACS server. This functionality is handled within the anonymization process in the

 `main.py` script.

By following these steps and using the provided functions, you can efficiently manage the uploading, processing, and anonymizing of DICOM data via an API.
