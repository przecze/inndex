FROM --platform=linux/amd64 python:3.13-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install "uv~=0.9.30" && uv pip install --system --no-cache-dir -r requirements.txt

COPY app.py ./
COPY .streamlit/ ./.streamlit/
COPY prompt/ ./prompt/
COPY data/ ./data/
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

EXPOSE 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
