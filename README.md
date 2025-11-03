# 🧠 Logician - Autonomous DevOps AI Assistant

A lightweight, RAG-powered AI assistant designed to help with DevOps tasks using embeddings and vector search.

## Features

- 🔍 **RAG (Retrieval-Augmented Generation)** - Context-aware responses using vector search
- 📊 **Qdrant Integration** - Fast vector similarity search
- 🎯 **Embeddings Wrapper** - Clean abstraction for multiple embedding providers
- 🛠️ **DevOps Focus** - Tailored for infrastructure and operations queries
- 🖥️ **CLI Interface** - Simple command-line interaction
- 🧪 **Test Coverage** - Unit tests included

## Quick Start

```bash
# Clone the repository
git clone https://github.com/wesleyscholl/logician.git
cd logician

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run the CLI
python main.py
```

## Project Structure

```
logician/
├── logician/          # Core package
│   ├── __init__.py
│   ├── cli.py        # Command-line interface
│   ├── embeddings.py # Embeddings wrapper
│   ├── qdrant.py     # Qdrant client
│   └── rag.py        # RAG orchestrator
├── tests/            # Unit tests
├── main.py           # Entry point
├── requirements.txt  # Dependencies
└── pyproject.toml    # Project metadata
```

## 📊 Project Status

**Status:** 🚧 **MVP/Prototype**

### Current State
- ✅ Basic CLI scaffold
- ✅ Embeddings wrapper abstraction
- ✅ Qdrant client stub
- ✅ RAG orchestrator foundation
- ✅ Unit tests for core imports
- ⚠️ Integration incomplete
- ⚠️ Limited DevOps knowledge base

### What Works
- Project structure and organization
- CLI entry point
- Module imports and basic architecture
- Development environment setup

### What Needs Work
- Full Qdrant integration and indexing
- Embedding generation and storage
- RAG retrieval logic
- DevOps knowledge base population
- End-to-end query processing

## 🗺️ Roadmap

### v0.2 (In Progress)
- 🔄 Complete Qdrant integration
- 🔄 Add document ingestion pipeline
- 🔄 Implement RAG query flow
- 🔄 Basic DevOps knowledge base (K8s, Docker, CI/CD)

### v0.3 (Planned)
- 📋 LLM integration for generation (OpenAI, Anthropic, local)
- 📋 Advanced query understanding
- 📋 Multi-step reasoning for complex DevOps tasks
- 📋 Conversation history and context

### v1.0 (Future Vision)
- 📋 Web UI for easier interaction
- 📋 Integration with DevOps tools (kubectl, docker, terraform)
- 📋 Action execution capabilities (read-only for safety)
- 📋 Team knowledge sharing features
- 📋 Custom knowledge base training
- 📋 Slack/Discord bot integration

## 🎯 Next Steps

### For Development
1. Populate vector database with DevOps documentation
2. Implement full RAG pipeline
3. Add LLM integration for response generation
4. Create example queries and expected outputs
5. Add integration tests

### For Contributors
- Review architecture in `logician/` package
- Check TODOs in source files
- Add DevOps knowledge sources
- Improve test coverage
- Document API usage

### For Users
- Currently for developers only
- Use as reference architecture for RAG systems
- Adapt for your specific domain
- Contribute DevOps knowledge sources

## 💡 Use Cases (When Complete)

- **DevOps Q&A:** "How do I debug a CrashLoopBackOff in Kubernetes?"
- **Best Practices:** "What's the recommended way to structure a multi-stage Dockerfile?"
- **Troubleshooting:** "My CI pipeline is slow, what are common bottlenecks?"
- **Knowledge Sharing:** Team-specific DevOps documentation search
- **Onboarding:** Help new engineers learn your infrastructure

## 🏗️ Architecture

```
User Query
    ↓
CLI Interface
    ↓
RAG Orchestrator
    ├→ Embeddings (query → vector)
    ├→ Qdrant (vector → relevant docs)
    └→ LLM (docs + query → response)
    ↓
Formatted Answer
```

## 🤝 Contributing

This is an early-stage project. Contributions welcome:
- Complete integration work
- Add DevOps knowledge sources
- Improve RAG retrieval logic
- Add more embedding providers
- Documentation and examples

## 📝 License

MIT License - See LICENSE file

## 🔧 Technical Stack

- **Python 3.8+**
- **Qdrant** - Vector database
- **Embeddings** - Configurable (OpenAI, SentenceTransformers, etc.)
- **CLI** - Click or argparse
- **Testing** - pytest

## 📚 Related Projects

- [vectro](https://github.com/wesleyscholl/vectro) - Vector quantization for embeddings
- [VoltAI](https://github.com/wesleyscholl/VoltAI) - Local-first AI document search

---

**Note:** This is an MVP/prototype. Not production-ready yet. Use as learning resource or foundation for your own RAG assistant.
