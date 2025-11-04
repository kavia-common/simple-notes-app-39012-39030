# simple-notes-app-39012-39030

Simple Notes Application - Backend (FastAPI)

This container exposes a REST API for managing notes with CRUD operations using in-memory storage.

- Docs: visit /docs on the running service (e.g., https://vscode-internal-21908-qa.qa01.cloud.kavia.ai:3001/docs)
- OpenAPI JSON: /openapi.json

Health
- GET /
  Response: {"status":"ok"}

Endpoints
- GET /notes
  Query params:
    - q: optional case-insensitive search across title and content
    - skip: default 0
    - limit: default 50 (max 200)
  Response: { items: Note[], total: number, skip: number, limit: number }

- POST /notes
  Body: { "title": "My title", "content": "Optional content" }
  Response: Note (201 Created)

- GET /notes/{id}
  Response: Note or 404

- PUT /notes/{id}
  Body: { "title": "New title", "content": "New content" } (either field optional)
  Response: Note or 404

- DELETE /notes/{id}
  Response: 204 No Content or 404

Data Model
- Note fields:
  - id: UUID (server-generated)
  - title: string (required)
  - content: string (optional)
  - created_at: ISO8601 UTC timestamp
  - updated_at: ISO8601 UTC timestamp

Example curl commands
- Health
  curl -s https://vscode-internal-21908-qa.qa01.cloud.kavia.ai:3001/

- Create
  curl -s -X POST https://vscode-internal-21908-qa.qa01.cloud.kavia.ai:3001/notes \
    -H "Content-Type: application/json" \
    -d '{"title":"First note","content":"Hello"}'

- List
  curl -s "https://vscode-internal-21908-qa.qa01.cloud.kavia.ai:3001/notes?skip=0&limit=50"

- Search
  curl -s "https://vscode-internal-21908-qa.qa01.cloud.kavia.ai:3001/notes?q=first"

- Get by id
  curl -s https://vscode-internal-21908-qa.qa01.cloud.kavia.ai:3001/notes/{uuid}

- Update
  curl -s -X PUT https://vscode-internal-21908-qa.qa01.cloud.kavia.ai:3001/notes/{uuid} \
    -H "Content-Type: application/json" \
    -d '{"title":"Updated title"}'

- Delete
  curl -s -X DELETE https://vscode-internal-21908-qa.qa01.cloud.kavia.ai:3001/notes/{uuid} -i

Notes
- This backend uses in-memory storage; data resets when the service restarts.
- CORS is enabled for all origins to simplify local development.