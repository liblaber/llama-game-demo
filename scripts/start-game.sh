# Start the front end on port 8000
cd frontend
npm run start &

# Start the API on port 8001
cd ..
cd api
uvicorn main:app --host 0.0.0.0 --port 8001 --reload