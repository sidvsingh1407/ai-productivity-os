#!/bin/bash

# Start backend
cd backend
python -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
npm run dev &
FRONTEND_PID=$!

cd ..
wait
