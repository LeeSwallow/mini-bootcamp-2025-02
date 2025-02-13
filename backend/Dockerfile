FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y python3-venv gcc && apt-get clean
RUN apt-get install -y curl && curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3031", "--env-file", ".env", "--reload"]
