# Food-Segmenter - Server-side Application

This app detects and segments food items in images and calculates their area using a fine-tuned YOLOv8 model.

## Setup Instructions
Option 1: Run with Docker
1. Install Docker

2. Clone the repo or unzip the folder

3. In the project root, build the container:

   `docker build -t food-segmenter .`

4. Run the server
   
   `docker run -p 8000:8000 food-segmenter`

5. Open your browser

   `http://localhost:8000`


Option 2: Manual
1. Make a virtual environment:
   
   `python -m venv .venv`
   
   `source .venv/bin/activate`

3. Install dependencies:
   
   `pip install -r requirements.txt`

4. Run the app:
   
   `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`

## Test

Test client sending single image by running:

  `python client.py`

Stress testing by running:

  `python client_stress.py`


## Endpoints


Method	URL	Description

POST	/segment	
Segment a single image

POST	/segment_batch	
Segment multiple images



