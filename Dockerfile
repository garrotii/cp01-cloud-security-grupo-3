FROM node:24-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv ca-certificates && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/scanners
ENV PATH="/opt/scanners/bin:${PATH}"
ENV SEMGREP_SEND_METRICS=off SEMGREP_ENABLE_VERSION_CHECK=0
WORKDIR /lab
COPY requirements-scanners.txt .
RUN pip install --no-cache-dir -r requirements-scanners.txt && npm install -g npm@11.12.0 --ignore-scripts
COPY . .
ENTRYPOINT ["python", "scripts/scan.py"]
CMD ["inseguro"]
