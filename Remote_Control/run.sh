#!/bin/bash
python3 web.py &
cd frontend
PORT=8080 npm start