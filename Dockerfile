# Stage 1: Build the React frontend
FROM node:18-slim AS build-frontend
WORKDIR /frontend
COPY frontend/package.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build the FastAPI backend
FROM python:3.9-slim
WORKDIR /app

# Install backend dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend

# Copy built frontend from Stage 1
COPY --from=build-frontend /frontend/dist ./frontend/dist

# Copy OpenEnv config, inference script and environment template
COPY openenv.yaml .
COPY inference.py .
COPY .env .

# Expose port (HF Space default)
EXPOSE 7860

# Run with uvicorn
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "7860"]
