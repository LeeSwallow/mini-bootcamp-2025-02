%!/bin/bash

source .venv/bin/activate
# Start the server
uvicorn main:app --host 0.0.0.0 --port 3031 --env-file .env --reload
