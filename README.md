# CareerOneStop Cluster Overview Scraper

This project is a web scraper designed to extract information from CareerOneStop cluster overview pages. It reads a list of cluster URLs from an input CSV file, scrapes each page for key information (such as the cluster description, video URL, and transcript), and outputs the data into a new CSV file.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Output](#output)
- [Troubleshooting](#troubleshooting)

## Features
- Scrapes cluster descriptions, video URLs, and transcripts from CareerOneStop.
- Uses Docker for ease of setup and consistent environment.
- Cleans up special characters and ensures normalized output.
- Outputs the collected data to a CSV file for easy analysis.

## Project Structure
- `main.py` - The main Python script that handles scraping.
- `Dockerfile` - Configures the Docker environment for the project.
- `docker-compose.yml` - Defines the Docker service and volume mounts.
- `input/` - Folder to store the input CSV file (`clusters.csv`).
- `output/` - Folder where the output CSV file (`cluster_data_output.csv`) will be saved.

## Setup and Installation
### Prerequisites
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/) if it's not already installed.
- **Docker Compose**: Comes bundled with Docker on most platforms.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd cluster-overview-scraper
   ```

2. **Prepare Input CSV**:
   - Place `clusters.csv` in the `input/` directory.
   - Ensure it includes columns for `Cluster` (or `Cluster Name`) and `URL` (or `Cluster URL`), with each row representing a cluster name and the associated URL.

3. **Build and Run the Docker Container**:
   - Run the following command to build and start the container:
     ```bash
     docker-compose up --build
     ```

## Usage
1. **Start Scraping**:
   - The container will start scraping data from each cluster URL listed in `clusters.csv`.
   - A progress bar will indicate the current status of the scraping.

2. **View the Output**:
   - When complete, the data will be saved as `cluster_data_output.csv` in the `output/` directory.

## Output
The output CSV file (`cluster_data_output.csv`) will contain the following columns:

| Cluster Name                          | Description                                                          | Video URL                                         | Transcript                                                                 |
|---------------------------------------|----------------------------------------------------------------------|---------------------------------------------------|---------------------------------------------------------------------------|
| Example Cluster                       | Cleaned cluster description                                          | https://cdn.example.com/cluster-video-url.mp4     | Cleaned transcript text without unwanted special characters              |

## Troubleshooting
- **File Not Found**: Ensure `clusters.csv` is in the `input/` directory. The input file path is set to `input/clusters.csv`.
- **Special Characters**: If special characters appear in the output, the code includes text normalization to clean up the text. You can further customize the `clean_text` function if needed.
- **Error in Column Names**: If you encounter a `KeyError` related to column names, check that the input CSV has either `Cluster` or `Cluster Name` and `URL` or `Cluster URL` as headers. The script is designed to handle either.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing
Feel free to submit issues or pull requests for improvements or bug fixes.
```

This `README.md` provides instructions and guidance for setting up, running, and troubleshooting the project, making it easy for others to understand and use. Let me know if you'd like additional details or sections!