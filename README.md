# Prompt To Notify

A chatbot that performs web searches on demand and notifies users with relevant results in real time.

<p align="center">
   <img src="assets/brand-img.png" alt="Prompt To Notify Brand" height="300" width="500"/>
</p>

## Features

- Conversational chatbot interface using Gradio
- On-demand web search via Google Serper API
- Real-time push notifications using Pushover
- Persistent conversation memory with SQLite
- Powered by OpenAI GPT-4o-mini and LangChain/Graph

## Requirements

- Python 3.12+
- API keys for OpenAI, Google Serper, and Pushover

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/prompt-to-notify.git
   cd prompt-to-notify
   ```
2. Install dependencies (recommended: use a virtual environment):
   ```sh
   pip install -r requirements.txt
   ```
   Or, if using [uv](https://github.com/astral-sh/uv):
   ```sh
   uv pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root with the following variables:

```
OPENAI_API_KEY=blah
LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="blah"
LANGSMITH_PROJECT="blah"

SERPER_API_KEY=blah
PUSHOVER_TOKEN=blah
```

## Usage

Run the chatbot interface:

```sh
python main.py
```

This will launch a Gradio web interface in your browser.

## How it works

- The chatbot receives user input and determines if a web search or push notification is needed.
- Web searches are performed using the Google Serper API.
- Push notifications are sent via the Pushover API.
- All conversation history is stored in a local SQLite database (`memory.db`).

## Project Structure

- `main.py` — Main application code
- `pyproject.toml` — Project metadata and dependencies
- `README.md` — This file
- `uv.lock` — Lockfile for reproducible installs

## License

MIT License
