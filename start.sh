#!/bin/bash

# Check for .env file
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Creating template .env file..."
    echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
    echo "UNSPLASH_API_KEY=your_unsplash_api_key_here" >> .env
    echo "Please edit the .env file and add your API keys"
    exit 1
fi

# Start services
echo "Starting LLM Resume Generator..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 5

# Display access information
echo "======================="
echo "LLM Resume Generator is running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "======================="
echo "To stop the application, run: docker-compose down"