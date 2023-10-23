#!/bin/bash

# 1. Delete the public folder and recreate it
rm -rf public
mkdir public

# 2. Move into the frontend/ directory
cd frontend/

# 3. Run `npm run build`
npm run build

# 4. Go back to the original directory
cd ..

# 5. Run docker-compose up
docker-compose up
