# Redditor 🤖

**AI-Powered Reddit Agent System**

A collection of AI agent pipelines for automating Reddit tasks. Each pipeline runs independently with specialized AI agents for content analysis, engagement, and automation.

## Features

- 🔌 **Reddit API Integration** - Full PRAW wrapper with OAuth2 authentication
- 🤖 **AI Agent Pipelines** - Modular agents for different tasks
- ⏰ **Scheduled Execution** - Cron-like scheduling with APScheduler
- 📊 **Content Analysis** - Sentiment analysis and engagement scoring
- 💬 **Comment Generation** - Context-aware response generation
- 📁 **Pipeline Framework** - Extensible base for custom agents

## Installation

```bash
# Clone the repository
git clone https://github.com/AgenticCompany/redditor.git
cd redditor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Quick Start

```bash
# Check CLI is working
redditor --help

# Show configuration
redditor config show

# List available pipelines
redditor pipeline list

# Run a specific pipeline
redditor pipeline run content-analyzer --subreddit python
```

## Configuration

Create a `.env` file in the project root with your credentials:

```env
# Reddit API Credentials
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=redditor/0.1.0
REDDIT_USERNAME=your_username
REDDIT_PASSWORD=your_password

# AI API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## Project Structure

```
redditor/
├── src/redditor/
│   ├── __init__.py       # Package init
│   ├── main.py           # FastAPI entry point
│   ├── config.py         # Configuration management
│   ├── cli.py            # CLI commands
│   ├── api/              # REST API routes
│   ├── agents/           # AI agent implementations
│   ├── pipelines/        # Pipeline definitions
│   ├── reddit/           # Reddit API wrapper
│   ├── database/         # Database operations
│   └── utils/            # Shared utilities
├── tests/
│   ├── unit/
│   └── integration/
└── .seedgpt/             # Project management
```

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src/redditor

# Format code
black src/
ruff check src/ --fix

# Type checking
mypy src/
```

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
