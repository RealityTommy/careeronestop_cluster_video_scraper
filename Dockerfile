# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy local files to the container
COPY . .

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-transport-https ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir requests beautifulsoup4 pandas tqdm

# Set the default command to run the scraper
CMD ["python", "main.py"]
