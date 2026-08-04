# ☕ Swasthya Coffee AI Assistant

An AI-powered customer support assistant for Swasthya Coffee built using FastAPI, Google's Gemini LLM, Redis, ChromaDB, and WooCommerce.

The assistant can:

- Recommend coffee products
- Answer coffee-related questions using RAG
- Track WooCommerce orders
- Remember user preferences across conversations
- Route requests to specialized AI agents

---

# Features

## Product Discovery
- Search products
- Recommend products
- Product details
- WooCommerce integration

## Coffee Knowledge (RAG)
- ChromaDB vector database
- Gemini Embeddings
- Semantic search
- Coffee blogs
- Brewing guides
- FAQs
- Shipping policy
- Refund policy

## Personalized Recommendations
- Redis-based memory
- Preference extraction
- Multi-turn conversation
- Recommendation workflow

## Order Tracking
- WooCommerce order lookup
- Order status
- Natural language interaction

---

# Tech Stack

Backend

- FastAPI
- Python 3.12
- Pydantic

AI

- Google Gemini
- Function Calling
- Embeddings

Vector Database

- ChromaDB

Memory

- Redis

E-commerce

- WooCommerce REST API

Frontend (Coming Soon)

- React
- Vite

---

# Architecture

```
                FastAPI
                    │
                    ▼
              ChatService
                    │
                    ▼
              RouterAgent
                    │
   ┌────────┬────────┬───────────┬─────────┐
   ▼        ▼        ▼           ▼
Product  Knowledge Recommendation Order
Agent      Agent       Agent      Agent
   │         │           │          │
WooCommerce ChromaDB   Redis    WooCommerce
```

---

# Project Structure

```
app/
│
├── agents/
├── services/
├── tools/
├── routes/
├── registry/
├── knowledge/
├── models/
├── constants/
├── exceptions/
└── main.py
```

---

# AI Workflow

## 1. User sends a message

↓

## 2. ChatService

- Loads conversation
- Updates preferences
- Creates AgentContext

↓

## 3. RouterAgent

Determines which agent should answer.

↓

## 4. Selected Agent

Examples:

- ProductAgent
- KnowledgeAgent
- RecommendationAgent
- OrderAgent

↓

## 5. Gemini Function Calling

Calls appropriate tools.

↓

## 6. Response returned to user

---

# Recommendation Workflow

User

↓

Preference Extraction

↓

Redis Memory

↓

Workflow Service

↓

RecommendationAgent

↓

WooCommerce Products

↓

Gemini

↓

Personalized Recommendation

---

# Knowledge Workflow

Question

↓

Embedding

↓

ChromaDB

↓

Relevant Documents

↓

Gemini

↓

Answer

---

# Order Workflow

Question

↓

OrderAgent

↓

WooCommerce API

↓

Gemini

↓

Order Status

---

# Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=

WOOCOMMERCE_URL=

WOOCOMMERCE_CONSUMER_KEY=

WOOCOMMERCE_CONSUMER_SECRET=

REDIS_HOST=

REDIS_PORT=
```

---

# Installation

```bash
git clone <repo>

cd coffee-ai-assistant

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```

Run Redis

```bash
redis-server
```

Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

# API

## Chat

POST

```
/chat
```

Example

```json
{
    "session_id":"abc123",
    "message":"Recommend me a strong Arabica coffee"
}
```

---

# Future Improvements

- React Chat UI
- Multi-LLM Support
- Streaming Responses
- Authentication
- Conversation Analytics
- Admin Dashboard
- Docker Deployment

---

# Author

**Shabari Prasad H D**

Senior Python Backend Developer
