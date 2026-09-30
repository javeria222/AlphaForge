FROM python:3.10-slim

# Create user with ID 1000 required by Hugging Face Spaces permissions
RUN useradd -m -u 1000 user
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code into container
COPY --chown=user . /app

USER user

# Hugging Face exposes port 7860 by default
EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]