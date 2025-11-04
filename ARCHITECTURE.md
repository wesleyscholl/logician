# Logician Architecture

This document describes the architecture, design decisions, and technical implementation of Logician - a RAG-powered AI assistant for DevOps automation.

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Logician System                         │
└─────────────────────────────────────────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
    ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
    │  User   │          │   RAG   │          │   LLM   │
    │Interface│          │ Pipeline│          │ Engine  │
    └────┬────┘          └────┬────┘          └────┬────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
         ┌────▼────┐      ┌───▼───┐      ┌────▼────┐
         │ Vector  │      │ Doc   │      │ Action  │
         │  Store  │      │Parser │      │ Executor│
         └─────────┘      └───────┘      └─────────┘
```

## 📦 Core Components

### 1. User Interface Layer

**Purpose:** Interact with users via CLI, web interface, or API

**Components:**
- **CLI (Click/Typer)** - Primary interface for command-line operations
- **Web UI (Streamlit/Gradio)** - Optional visual interface for non-technical users
- **REST API (FastAPI)** - Programmatic access for integrations

**Responsibilities:**
- Accept user queries and commands
- Display results and recommendations
- Handle authentication and session management
- Provide feedback during long-running operations

### 2. RAG Pipeline

**Purpose:** Retrieve relevant context from documentation and past decisions

**Components:**

#### 2.1 Document Ingestion
```python
class DocumentIngestion:
    """
    Ingest and preprocess documentation.
    """
    def ingest_markdown(path: str) -> List[Document]:
        """Parse markdown files with metadata."""
        pass
    
    def ingest_code(path: str, language: str) -> List[Document]:
        """Parse code files with syntax awareness."""
        pass
    
    def ingest_yaml(path: str) -> List[Document]:
        """Parse Kubernetes YAML with structure preservation."""
        pass
```

**Supported Formats:**
- Markdown (.md) - Documentation, runbooks, guides
- Code (.py, .sh, .yaml) - Scripts, configs, manifests
- Logs (.log, .txt) - Historical logs and incidents
- JSON/YAML - Configuration files and data

#### 2.2 Text Chunking
```python
class TextChunker:
    """
    Intelligently chunk documents for embedding.
    """
    def chunk_by_tokens(
        text: str,
        chunk_size: int = 512,
        overlap: int = 128
    ) -> List[str]:
        """Token-aware chunking with overlap."""
        pass
    
    def chunk_by_structure(
        document: Document,
        preserve_headers: bool = True
    ) -> List[str]:
        """Structure-aware chunking (headers, code blocks)."""
        pass
```

**Chunking Strategies:**
- **Token-based** - Fixed token chunks with overlap (512 tokens, 128 overlap)
- **Semantic** - Preserve logical units (paragraphs, code functions)
- **Hierarchical** - Maintain document structure (headers, sections)

#### 2.3 Embedding Generation
```python
class EmbeddingGenerator:
    """
    Generate vector embeddings for text chunks.
    """
    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for text chunks."""
        pass
    
    def embed_query(self, query: str) -> List[float]:
        """Generate embedding for search query."""
        pass
```

**Models Supported:**
- **OpenAI** - text-embedding-ada-002 (1536 dims)
- **Sentence Transformers** - all-MiniLM-L6-v2 (384 dims)
- **Cohere** - embed-english-v3.0 (1024 dims)

#### 2.4 Vector Store
```python
class VectorStore:
    """
    Store and search vector embeddings.
    """
    def add_documents(
        self,
        documents: List[Document],
        embeddings: List[List[float]],
        metadata: List[Dict]
    ):
        """Add documents with embeddings to store."""
        pass
    
    def similarity_search(
        self,
        query_embedding: List[float],
        k: int = 10,
        filter: Dict = None
    ) -> List[Document]:
        """Retrieve top-k similar documents."""
        pass
```

**Storage Options:**
- **ChromaDB** - Default, simple, local-first
- **Pinecone** - Production, managed, scalable
- **Qdrant** - Self-hosted, feature-rich
- **Weaviate** - GraphQL interface, hybrid search

### 3. LLM Engine

**Purpose:** Generate responses using retrieved context

**Components:**

#### 3.1 Prompt Engineering
```python
class PromptBuilder:
    """
    Build context-aware prompts for LLM.
    """
    def build_rag_prompt(
        self,
        query: str,
        context: List[Document],
        system_prompt: str = None
    ) -> str:
        """Construct RAG prompt with retrieved context."""
        template = """
        You are Logician, a DevOps AI assistant.
        
        Context from documentation:
        {context}
        
        User question: {query}
        
        Provide a detailed answer based on the context.
        If the context doesn't contain the answer, say so.
        """
        return template.format(context=context, query=query)
```

**Prompt Templates:**
- **General Query** - Standard QA with context
- **Troubleshooting** - Debug assistance with logs/errors
- **Code Generation** - Generate scripts/configs from requirements
- **Best Practices** - Recommendations based on patterns

#### 3.2 LLM Integration
```python
class LLMEngine:
    """
    Interface with various LLM providers.
    """
    def __init__(self, provider: str = "openai", model: str = "gpt-4"):
        self.provider = provider
        self.model = model
    
    def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Generate response from LLM."""
        pass
    
    def stream(self, prompt: str) -> Iterator[str]:
        """Stream response tokens for real-time display."""
        pass
```

**Supported LLMs:**
- **OpenAI** - GPT-4, GPT-3.5-turbo
- **Anthropic** - Claude 3 Opus/Sonnet
- **Open Source** - Llama 2, Mistral (via Ollama)
- **Azure OpenAI** - Enterprise deployments

#### 3.3 Response Post-Processing
```python
class ResponseProcessor:
    """
    Clean and format LLM responses.
    """
    def extract_code_blocks(response: str) -> List[str]:
        """Extract code blocks from markdown."""
        pass
    
    def add_citations(
        response: str,
        sources: List[Document]
    ) -> str:
        """Add source citations to response."""
        pass
```

### 4. Action Executor

**Purpose:** Execute recommended actions with user approval

**Components:**

#### 4.1 Command Executor
```python
class CommandExecutor:
    """
    Execute shell commands safely.
    """
    def execute(
        self,
        command: str,
        dry_run: bool = True,
        timeout: int = 300
    ) -> Dict[str, Any]:
        """
        Execute command with safety checks.
        
        Returns:
            {
                "stdout": str,
                "stderr": str,
                "exit_code": int,
                "duration": float
            }
        """
        pass
```

**Safety Features:**
- **Dry-run mode** - Show what would happen without executing
- **Approval required** - User must approve before execution
- **Sandboxing** - Run in isolated environment when possible
- **Logging** - Record all executed commands

#### 4.2 Kubernetes Operations
```python
class K8sOperations:
    """
    Interact with Kubernetes clusters.
    """
    def apply_manifest(
        self,
        manifest: str,
        namespace: str = "default",
        dry_run: bool = True
    ):
        """Apply Kubernetes manifest."""
        pass
    
    def get_pods(
        self,
        namespace: str = "default",
        label_selector: str = None
    ) -> List[Dict]:
        """Get pod information."""
        pass
```

**Supported Operations:**
- **Deployment** - Deploy, update, rollback
- **Scaling** - HPA configuration, manual scaling
- **Debugging** - Logs, describe, exec into pods
- **Monitoring** - Resource usage, health checks

## 🔄 Request Flow

### Typical Query Flow

```
1. User Query
   ↓
2. Query Analysis
   • Intent classification
   • Entity extraction
   • Complexity assessment
   ↓
3. Context Retrieval
   • Generate query embedding
   • Search vector store
   • Rank results by relevance
   ↓
4. Prompt Construction
   • Select prompt template
   • Inject retrieved context
   • Add system instructions
   ↓
5. LLM Generation
   • Send to LLM API
   • Stream response
   • Parse output
   ↓
6. Response Enhancement
   • Add code syntax highlighting
   • Include source citations
   • Format for display
   ↓
7. Action Extraction (if applicable)
   • Identify executable commands
   • Request user approval
   • Execute with safety checks
   ↓
8. Result Presentation
   • Display to user
   • Store in conversation history
   • Update feedback loop
```

## 🗂️ Data Flow

### Document Indexing Pipeline

```
Raw Documents
    ↓
[Parser] → Structured Documents
    ↓
[Chunker] → Text Chunks (512 tokens)
    ↓
[Embedder] → Vector Embeddings (1536 dims)
    ↓
[Vector Store] → Indexed & Searchable
```

### Query Processing Pipeline

```
User Query
    ↓
[Embedder] → Query Embedding
    ↓
[Vector Store] → Top-K Docs (k=10)
    ↓
[Reranker] → Filtered Results (k=5)
    ↓
[Prompt Builder] → Contextualized Prompt
    ↓
[LLM] → Generated Response
    ↓
User
```

## 💾 Data Models

### Document Schema
```python
@dataclass
class Document:
    """Representation of a document chunk."""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    
    # Metadata fields
    source: str          # File path or URL
    type: str            # markdown, code, yaml, log
    timestamp: datetime  # When indexed
    chunk_index: int     # Position in original doc
    token_count: int     # Tokens in content
    tags: List[str]      # Classification tags
```

### Conversation Schema
```python
@dataclass
class Message:
    """Single message in conversation."""
    role: str           # user, assistant, system
    content: str
    timestamp: datetime
    sources: List[str]  # Documents used for response
    
@dataclass
class Conversation:
    """Complete conversation thread."""
    id: str
    messages: List[Message]
    context: Dict[str, Any]  # Persistent context
    created_at: datetime
    updated_at: datetime
```

## ⚙️ Configuration

### System Configuration
```yaml
# config.yaml
llm:
  provider: openai
  model: gpt-4
  temperature: 0.7
  max_tokens: 1000

embeddings:
  model: text-embedding-ada-002
  batch_size: 100

vector_store:
  type: chromadb
  persist_directory: ./data/chromadb
  collection_name: logician_docs

rag:
  chunk_size: 512
  chunk_overlap: 128
  top_k: 10
  rerank: true
  
safety:
  require_approval: true
  dry_run_default: true
  timeout_seconds: 300
```

## 🔒 Security Considerations

### Authentication & Authorization
- API keys stored in environment variables (never committed)
- Role-based access control for multi-user deployments
- Audit logging of all actions

### Command Execution Safety
- Whitelist of allowed commands
- Sandboxed execution when possible
- User approval required for destructive operations
- Logging of all executed commands

### Data Privacy
- No sensitive data in embeddings (PII, credentials)
- Option for local-only LLMs (Ollama)
- Conversation history can be disabled

## 📊 Performance Characteristics

### Latency Breakdown (typical query)
- **Embedding generation**: ~50ms
- **Vector search**: ~100ms
- **LLM generation**: ~2-5s (depending on model)
- **Total**: ~2-5s end-to-end

### Scalability
- **Document capacity**: 100K+ documents with ChromaDB
- **Concurrent users**: 10-50 (depends on LLM rate limits)
- **Query throughput**: ~10-20 queries/minute (LLM bottleneck)

### Resource Requirements
- **Memory**: 2-4 GB (vector store + embeddings)
- **Storage**: 1-5 GB (documents + vectors)
- **CPU**: 2-4 cores for parallel processing

## 🔮 Future Enhancements

### Planned Improvements
1. **Multi-modal RAG** - Support for images, diagrams
2. **Graph-based retrieval** - Relationship-aware context
3. **Active learning** - Improve from user feedback
4. **Tool use** - LLM can call external APIs directly
5. **Multi-agent** - Specialized agents for different tasks

### Architecture Evolution
```
Current: Simple RAG
    ↓
Next: Hybrid search (vector + keyword)
    ↓
Future: Graph RAG with entity linking
    ↓
Ultimate: Multi-agent orchestration
```

## 📚 References

**Papers:**
- [Retrieval-Augmented Generation (RAG)](https://arxiv.org/abs/2005.11401)
- [Dense Passage Retrieval](https://arxiv.org/abs/2004.04906)
- [ColBERT: Efficient and Effective Passage Search](https://arxiv.org/abs/2004.12832)

**Tools:**
- [LangChain](https://python.langchain.com/) - RAG framework
- [LlamaIndex](https://www.llamaindex.ai/) - Data framework for LLMs
- [ChromaDB](https://www.trychroma.com/) - Vector store
- [Sentence Transformers](https://www.sbert.net/) - Embedding models

---

**This architecture is designed for flexibility and evolution. Start simple, scale as needed.**
