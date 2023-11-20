# Start the API on port 8000
cd api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload