# 🚀 AISplain

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/GevOkeefe/AISplain?style=for-the-badge)](https://github.com/GevOkeefe/AISplain/stargazers)

[![GitHub forks](https://img.shields.io/github/forks/GevOkeefe/AISplain?style=for-the-badge)](https://github.com/GevOkeefe/AISplain/network)

[![GitHub issues](https://img.shields.io/github/issues/GevOkeefe/AISplain?style=for-the-badge)](https://github.com/GevOkeefe/AISplain/issues)

[![GitHub license](https://img.shields.io/github/license/GevOkeefe/AISplain?style=for-the-badge)](LICENSE)

**Your AI assistant for intelligent document summarization and interactive Q&A.**

</div>

## 📖 Overview

AISplain is an AI-powered web application designed to help users quickly understand and interact with their documents. It leverages advanced natural language processing (NLP) and a vector database to provide efficient document summarization and a conversational interface for asking questions about your uploaded content. This project aims to simplify information extraction from extensive texts, making knowledge retrieval intuitive and fast.

## ✨ Features

-   **Intelligent Document Processing**: Upload various document types (e.g. PDFs) for comprehensive analysis and ingestion into the knowledge base.
-   **AI-driven Summarization**: Generate concise, accurate summaries of your uploaded documents to quickly grasp their core content.
-   **Interactive Chat (Q&A)**: Engage in a natural language conversation with your documents. Ask specific questions and receive contextually relevant answers extracted directly from your content.
-   **Persistent Vector Database**: Utilizes SentenceTransformer to efficiently store and retrieve document embeddings, ensuring fast and accurate information recall.
-   **OpenAI LLM Integration**: Leverages powerful Large Language Models from OpenAI to power summarization and conversational AI capabilities.
-   **Containerized Deployment**: Easy setup and scalable deployment using Docker and Docker Compose for a consistent development and production environment.

## 🛠️ Tech Stack

**Backend:**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

**Database (Vector Store):**

[![SentenceTransformer](https://img.shields.io/badge/SentenceTransformer-5566C3?style=for-the-badge&logo=chroma&logoColor=white)](https://github.com/huggingface/sentence-transformers/tree/main)

**Document Processing:**

[![pypdf](https://img.shields.io/badge/pypdf-lightgrey?style=for-the-badge)](https://pypdf.readthedocs.io/)

**Frontend:**

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)

[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

**DevOps:**

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

[![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)

## 🚀 Quick Start

Follow these steps to get AISplain up and running on your local machine.

### Prerequisites

-   [Python](https://www.python.org/downloads/) 3.9 or higher
-   [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
-   [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/install/) (recommended for containerized setup)

### Installation (using Docker Compose - Recommended)

1.  **Clone the repository**
    ```bash
    git clone https://github.com/GevOkeefe/AISplain.git
    cd AISplain
    ```

2.  **Start the services**
    This will build the application image and start both the Flask application and the SentenceTransformer vector store.
    ```bash
    docker compose up --build
    ```
    The application will be accessible at `http://localhost:5000`.

### Installation (Local Python Environment)

1.  **Clone the repository**
    ```bash
    git clone https://github.com/GevOkeefe/AISplain.git
    cd AISplain
    ```

2.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Start development server**
    ```bash
    flask run
    ```

5.  **Open your browser**
    Visit `http://localhost:5000`

## 📁 Project Structure

```
AISplain/
├── .gitignore          # Specifies intentionally untracked files to ignore
├── Dockerfile          # Defines the Docker image for the Flask application
├── LICENSE             # Project license file (Apache 2.0)
├── ai.py               # Core AI logic for LLM interaction, summarization, and chat
├── app.py              # Main Flask application entry point, defines web routes
├── docStore.py         # Handles document ingestion, chunking, embedding, and SentenceTransformer integration
├── docker-compose.yml  # Defines multi-container Docker application (app + SentenceTransformer)
├── model/              # (Empty) Placeholder for AI models
├── requirements.txt    # Lists all Python dependencies
├── templates/          # HTML templates served by Flask (e.g., index.html)
└── var/                # Directory for persistent data, including SentenceTransformer storage and uploaded files
```

## ⚙️ Configuration

### Configuration Files

-   `ai.py`: Replace `your_model_name` in `model_path='model/your_model_name'` on line 9 with your model name in `/model` directory

## 📚 API Reference

The Flask application exposes several endpoints to manage documents and interact with the AI chat.

### Frontend Routes

-   **`/`** (GET): Serves the main application page (`index.html`), which typically includes the document upload and chat interfaces.

### API Endpoints

-   **`/upload`** (POST):
    -   **Description**: Handles the upload of documents. It processes the document, extracts text, chunks it, creates embeddings, and stores them in the SentenceTransformer vector store.
    -   **Request Body**: `multipart/form-data` containing a `file` field.
    -   **Response**: JSON indicating success or failure of the upload.

-   **`/chat`** (POST):
    -   **Description**: Processes a user's chat message against the stored documents. It retrieves relevant document chunks from SentenceTransformer and uses an LLM to generate a coherent response.
    -   **Request Body**: `application/json` with a `message` field (the user's query).
    -   **Response**: `application/json` containing the AI's `response` and potentially `source_documents`.

## 🚀 Deployment

The project is designed for easy deployment using Docker.

### Deployment Options

-   **Docker Compose**: The `docker-compose.yml` file provides a robust way to deploy the application and its SentenceTransformer dependency. It's suitable for both local development and single-server production deployments.
    ```bash
    docker compose up -d # Run services in detached mode
    ```
-   **Kubernetes / Cloud Orchestration**: The Docker image can be further deployed to container orchestration platforms like Kubernetes, AWS ECS, Google Cloud Run, or Azure Container Apps for scalable and highly available deployments.
-   **Traditional Hosting**: While containerization is recommended, the Python Flask application can also be deployed to traditional Python web hosting environments (e.g., Heroku, custom VPS) by ensuring all dependencies from `requirements.txt` are installed and the `gunicorn` server is configured correctly. You would also need to manage SentenceTransformer persistence separately.

## 🤝 Contributing

We welcome contributions to AISplain! If you're interested in improving the project, please consider the following:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Commit your changes with a clear message.
5.  Push your branch and open a pull request.

### Development Setup for Contributors

Follow the **Local Python Environment** setup steps in the [Quick Start](#quick-start) section to set up your development environment.

## 📄 License

This project is licensed under the [Apache License 2.0](LICENSE) - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

-   [Flask](https://flask.palletsprojects.com/) - The web framework used.
-   [SentenceTransformer](https://github.com/huggingface/sentence-transformers/tree/main) - The open-source embedding database.
-   [pypdf](https://pypdf.readthedocs.io/) - For PDF parsing capabilities.

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [GevOkeefe](https://github.com/GevOkeefe)

</div>

