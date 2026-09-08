# ☕ Swasthya Coffee AI Assistant

An AI-powered customer-facing coffee assistant for **Swasthya Coffee**.

The project combines a React/Vite chat interface with a FastAPI backend,
Google Gemini, Redis/Valkey, ChromaDB, and the Swasthya Coffee
WooCommerce store.

## Live services

-   Frontend: `https://swasthya-coffee-ui.onrender.com`
-   Backend API: `https://swasthya-coffee-api.onrender.com`
-   API health/root endpoint: `GET /`

> The live deployment URLs are environment-specific. Do not put API keys
> or WooCommerce secrets in this repository.

## What the assistant can do

-   Answer coffee-related questions.
-   Search the WooCommerce product catalog.
-   Show product cards with image, price, stock status, and product
    link.
-   Guide a customer through a personalized coffee recommendation.
-   Remember recommendation preferences for a session.
-   Search the coffee knowledge base using embeddings and ChromaDB.
-   Check WooCommerce order status when an order number is supplied.
-   Maintain conversation history per browser/session.

## Architecture

``` text
Customer
   │
   ▼
React + Vite UI
   │
   │ POST /chat
   ▼
FastAPI Backend
   │
   ▼
ChatService
   │
   ▼
RouterAgent
   │
   ├── ProductAgent ──────────────► WooCommerce REST API
   │
   ├── RecommendationAgent ──────► Redis/Valkey
   │                                  │
   │                                  └──► WooCommerce tools
   │
   ├── KnowledgeAgent ────────────► Gemini Embeddings
   │                                  │
   │                                  ▼
   │                               ChromaDB
   │
   └── OrderAgent ────────────────► WooCommerce REST API
```

## Backend

### Stack

-   Python 3.x
-   FastAPI
-   Uvicorn
-   Pydantic
-   Google Gemini API
-   Gemini embeddings
-   Redis Python client
-   Render Key Value / Valkey in production
-   ChromaDB
-   WooCommerce REST API

### Main backend flow

1.  React sends `session_id` and `message` to `POST /chat`.
2.  `ChatService` stores the user message.
3.  Conversation history is loaded from Redis.
4.  The active workflow is checked.
5.  `RouterAgent` chooses the appropriate specialized agent.
6.  The selected agent calls Gemini with the appropriate tools.
7.  Tool calls can query WooCommerce or ChromaDB.
8.  The response and relevant products are returned to React.
9.  The assistant response is saved back into Redis.

## Specialized agents

### ProductAgent

Used for:

-   Product search.
-   Product details.
-   Product availability/pricing.
-   Product catalog requests.

Uses:

-   `get_products`
-   `search_products`
-   `get_product`

### RecommendationAgent

Implements a multi-turn recommendation workflow.

It collects:

1.  Bean type --- Arabica / Robusta / Blend.
2.  Brew method --- Filter Coffee / Espresso / French Press.
3.  Strength --- Mild / Medium / Strong.

Preferences are stored in Redis with a 24-hour expiry.

Once enough information is available, Gemini uses product tools and
recommends one product.

### KnowledgeAgent

Used for questions such as:

-   Brewing.
-   Storage.
-   Coffee origins.
-   FAQs.
-   Blog/knowledge content.
-   Shipping/refund information.

It uses the RAG pipeline:

``` text
Question
   ↓
Gemini Embedding
   ↓
ChromaDB similarity search
   ↓
Relevant chunks
   ↓
Gemini
   ↓
Answer
```

### OrderAgent

Used for order-status requests.

It asks for an order number if one has not been provided and then calls
the WooCommerce order API.

## Redis / Valkey

Redis is used as application memory rather than as the product database.

The application stores:

-   Conversation history: `conversation:<session_id>`
-   Preferences: `preference:<session_id>`
-   Active workflow: `workflow:<session_id>`

The configured expiry is:

``` text
24 hours
```

In production, the Render Key Value service is Valkey-compatible and the
backend can connect using `REDIS_URL`.

## ChromaDB / RAG

The knowledge base is built from website content.

The ingestion process:

``` text
WebsiteLoader
    ↓
TextChunker
    ↓
Gemini Embedding
    ↓
ChromaDB
```

Run ingestion locally with:

``` bash
python -m scripts.ingest_knowledge
```

The configured collection is:

``` text
swasthya_coffee
```

The current implementation stores ChromaDB under:

``` text
./vector_db
```

Because this is local persistent storage, production deployment should
be reviewed if the service is expected to restart or scale across
instances. A persistent disk or managed vector database would be the
appropriate next step for a production-grade RAG deployment.

## Frontend

The frontend is a React 19 + Vite application.

Main components:

``` text
src/
├── App.jsx
├── main.jsx
├── components/
│   ├── Header.jsx
│   ├── Message.jsx
│   ├── ChatInput.jsx
│   ├── ProductCard.jsx
│   └── ChatBox.jsx
├── services/
│   └── api.js
├── utils/
│   └── session.js
└── styles/
```

The API base URL is read from:

``` text
VITE_API_URL
```

The frontend sends:

``` json
{
  "session_id": "browser-session-id",
  "message": "Recommend a strong coffee"
}
```

The session ID is generated with `crypto.randomUUID()` and stored in
browser `localStorage`.

## Environment variables

### Backend

``` env
GEMINI_API_KEY=
GEMINI_MODEL=

WOOCOMMERCE_URL=
WOOCOMMERCE_CONSUMER_KEY=
WOOCOMMERCE_CONSUMER_SECRET=
WEBSITE_URL=

REDIS_URL=
```

The backend also supports the local Redis configuration:

``` env
REDIS_HOST=
REDIS_PORT=6379
REDIS_DB=0
```

### Frontend

``` env
VITE_API_URL=
```

Example local frontend value:

``` env
VITE_API_URL=http://localhost:8000
```

Example production value:

``` env
VITE_API_URL=https://swasthya-coffee-api.onrender.com
```

### Important

`.env` files must remain local and must **not** be committed to Git.

Render receives production environment variables through the Render
service configuration.

## Local backend setup

``` bash
git clone <backend-repository>
cd coffee-ai-assistant

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend:

``` text
http://localhost:8000
```

## Local frontend setup

``` bash
git clone <frontend-repository>
cd coffee-ai-ui

npm install
npm run dev
```

Frontend:

``` text
http://localhost:5173
```

Create a local `.env`:

``` env
VITE_API_URL=http://localhost:8000
```

## Production deployment

### Backend

Hosted on Render as a Python web service.

Typical start command:

``` bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend

Hosted on Render as a Static Site.

Build command:

``` bash
npm install; npm run build
```

Publish directory:

``` text
dist
```

### Redis

Hosted as a Render Key Value service using Valkey.

The backend uses the internal Redis/Valkey connection URL through:

``` env
REDIS_URL=
```

### CORS

The backend currently allows:

``` text
http://localhost:5173
https://swasthya-coffee-ui.onrender.com
```

If the frontend URL changes, update the backend CORS configuration.

## Security notes

Never commit:

-   `GEMINI_API_KEY`
-   `WOOCOMMERCE_CONSUMER_KEY`
-   `WOOCOMMERCE_CONSUMER_SECRET`
-   Redis connection credentials
-   `.env` files
-   GitHub personal access tokens

The React application should only receive public configuration such as
the backend API URL. Backend secrets must stay on the backend.

## Repository separation

The project uses two repositories:

``` text
coffee-ai-assistant
    → FastAPI / AI backend

coffee-ai-ui
    → React / Vite frontend
```

This separation allows the frontend and backend to be deployed
independently.

## Useful commands

### Backend

``` bash
uvicorn app.main:app --reload
python -m scripts.ingest_knowledge
```

### Frontend

``` bash
npm install
npm run dev
npm run build
npm run lint
```

### Git

``` bash
git status
git add .
git commit -m "your message"
git push
```

## Current limitations / next improvements

1.  Production ChromaDB persistence needs a deliberate storage strategy.
2.  Authentication is not implemented.
3.  There is no admin/analytics dashboard.
4.  Chat responses are not streamed.
5.  Order support currently focuses on status/tracking rather than full
    order management.
6.  Recommendation logic can be expanded with budget, roast, grind size,
    and other preferences.
7.  Automated tests should be expanded around the complete chat
    workflow.
8.  Production monitoring and structured metrics can be added.
9.  Rate limiting and abuse protection should be added before public
    traffic grows.
10. CORS should ideally be controlled through environment configuration
    rather than hard-coded origins.

## Project documentation

See `PROJECT_DOCUMENTATION.md` for the detailed technical explanation,
architecture, workflows, deployment, environment variables,
troubleshooting, and interview-ready explanation.

## Author

**Shabari Prasad H D**