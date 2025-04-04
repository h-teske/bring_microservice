# 🧱 Bring! Microservice

A lightweight Python microservice to manage your Bring! shopping list via REST API.

---

## 🚀 Features

- Login to Bring! using email and password
- Fetch all lists (`GET /lists`)
- Manage list items:
  - Get items (`GET /items`)
  - Add item (`POST /items`)
  - Delete item (`DELETE /items`)
- Lookup list UUID by name (`GET /list-uuid/{list_name}`)
- Deployable via Docker and Portainer

---

## ⚙️ Tech Stack

- FastAPI
- Docker + Docker Compose
- bring-api Python wrapper (https://github.com/miaucl/bring-api)

---

## 📦 Local Setup

```bash
# Create a .env file
echo "BRING_EMAIL=you@example.com" > .env
echo "BRING_PASSWORD=yourPassword" >> .env

# Install and run locally
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 🐳 Docker / Portainer Deployment

### Docker CLI:

```bash
docker build -t bring-microservice .
docker run -p 8000:8000 --env-file .env bring-microservice
```

### Portainer (Git-based stack):

1. Go to **Stacks → Add Stack**
2. Select **Git repository**
3. Set `Repository URL` and use `docker-compose.yml`
4. Add environment variables (`BRING_EMAIL`, `BRING_PASSWORD`)
5. Click **Deploy the stack**

---

## 🛣 API Endpoints

| Endpoint                      | Method | Description               |
|------------------------------|--------|---------------------------|
| `/`                          | GET    | Service status            |
| `/lists`                     | GET    | Get all Bring! lists      |
| `/items`                     | GET    | Get items in a list       |
| `/items`                     | POST   | Add item to a list        |
| `/items`                     | DELETE | Remove item from a list   |
| `/list-uuid/{list_name}`     | GET    | Find list UUID by name    |

---

## 📄 License

MIT – Free to use and modify