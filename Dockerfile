# Use an official Python runtime as the base image
FROM python:3.12-slim-bullseye

# Install NPM
ENV NODE_VERSION=20.9.0
RUN apt-get -y update; apt-get -y install curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

# Set environment variables
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8001
ENV UVICORN_RELOAD=true

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./api /app/api
COPY ./frontend /app/frontend
COPY ./scripts /app/scripts

# Install the required packages
RUN chmod +x ./scripts/*.sh
RUN ./scripts/post-create.sh

# Expose port 8000 and 8001
EXPOSE 8000
EXPOSE 8001

# Start the web app and API
CMD ["/bin/bash", "-c", "./scripts/start-game.sh"]
