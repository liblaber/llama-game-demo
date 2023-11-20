# Script to be run after the dev container has been created

# Install the Python dependencies
cd api
pip install -r requirements.txt

# Install the front end NPM packages
cd ..
cd frontend
npm install
