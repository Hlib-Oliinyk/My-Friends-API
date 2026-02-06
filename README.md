# My Friends API

**FastAPI backend for managing friends, friend groups, and user relationships. Features async SQLAlchemy + PostgreSQL, JWT authentication with cookies, full CRUD operations, and Docker deployment.**

[![SQLAlchemy Async](https://img.shields.io/badge/SQLAlchemy-Async-0074D9)](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-AsyncPG-336791)](https://www.asyncpg.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](https://docs.docker.com/compose/)

## ✨ Features

- 🛡️ **JWT authentication** with HTTP-only cookies
- 👥 **Friends system** - add/update/delete with pagination
- 👥👥 **Friend groups** - organize friends into custom groups
- 👤 **User management** - registration, login/logout
- 🏗️ **Auto table creation** on app startup
- 🐳 **Docker ready** with PostgreSQL
- 🚀 **Production ready** - deployed on Render

## 🏗️ Project Structure

```
├── main.py                    # FastAPI app + lifespan (auto tables)
├── app/
│   ├── api/v1/               # API routers
│   │   ├── users.py          # User CRUD
│   │   ├── authorization.py  # JWT auth
│   │   ├── friends.py        # Friends CRUD + pagination
│   │   ├── friend_groups.py  # Friend groups
│   │   └── friend_group_members.py  # Group members
│   ├── db/                   # Async SQLAlchemy models + engine
│   ├── schemas/              # Pydantic schemas
│   └── services/             # Business logic
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🚀 Quick Start

### 1. Docker (Recommended)
```bash
git clone <your-repo>
cd project
docker-compose up -d
```

**API ready at:** `http://localhost:8000/api/docs`

### 2. Local Development
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt
uvicorn main:app --reload --port 9000
```

## 🔧 Environment Variables

Create `.env`:
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/dbname
SECRET_KEY=your-super-secret-jwt-key-change-in-production
ALGORITHM=HS256
```

## 📋 API Endpoints

### **Users** `/api/users`
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | List all users | - |
| `GET` | `/{user_id}` | Get user | - |
| `DELETE` | `/{user_id}` | Delete user | - |

### **Auth** `/api/auth`
| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| `POST` | `/register` | Register user | `{"email": "...", "username": "...", "password": "..."}` |
| `POST` | `/login` | Login → JWT cookie | `{"email": "...", "password": "..."}` |
| `POST` | `/logout` | Clear cookie | - |

### **Friends** `/api/friends` ✨
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | List friends (paginated) | ✅ |
| `GET` | `/{friend_id}` | Get friend | ✅ |
| `POST` | `/` | Add friend `{"friend_id": 2}` | ✅ |
| `PUT` | `/{friend_id}` | Update friend | ✅ |
| `DELETE` | `/{friend_id}` | Delete friend | ✅ |

### **Friend Groups** `/api/friendgroups` 👥
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| `GET` | `/` | User groups | ✅ |
| `GET` | `/{group_id}` | Get group | ✅ |
| `POST` | `/` | Create `{"name": "Family"}` | ✅ |
| `PUT` | `/{group_id}` | Update group | ✅ |
| `DELETE` | `/{group_id}` | Delete group | ✅ |

### **Group Members** `/api/friendgroupmembers`
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/{group_id}` | List members |
| `POST` | `/` | Add `{"friendgroup_id": 1, "friend_id": 2}` |
| `DELETE` | `/{group_id}?friend_id=2` | Remove member |

## 🐳 Docker Compose

**Full stack (App + PostgreSQL):**
```yaml
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/friends_db
    depends_on:
      - db
  
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: friends_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
```

**Commands:**
```bash
docker-compose up -d           # Start
docker-compose logs app        # Logs
docker-compose down -v         # Stop + cleanup
```

## ☁️ Production Deployment (Render)

1. **Connect GitHub repo**
2. **Environment Variables:**
   ```
   DATABASE_URL=postgresql+asyncpg://... (Render PostgreSQL)
   SECRET_KEY=your-super-secret-key
   ALGORITHM=HS256
   ```
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 9000`


## 🛠️ Tech Stack

```
Frontend: FastAPI + Pydantic v2 (schemas)
Backend: SQLAlchemy 2.0 Async + asyncpg
Database: PostgreSQL 16
Auth: JWT (PyJWT) + HTTP-only cookies
DevOps: Docker, docker-compose
Deploy: Render (Web Service + PostgreSQL)
```

## 📚 Interactive Documentation

- **Swagger UI:** `http://localhost:8000/api/docs`
- **OnRender:** `https://my-friends-api.onrender.com/api/docs`
- **Root:** `http://localhost:8000/` → API info

**All endpoints fully documented with request/response models!**

## 🔄 Development Workflow

```bash
# Install dev deps
pip install -r requirements.txt

# Run with reload
uvicorn main:app --reload --port 8000

# Test endpoints
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"123"}'
```

## 🤝 Contributing

1. Fork the project
2. `docker-compose up` for testing
3. Create feature branch `git checkout -b feature/amazing-feature`
4. Commit changes `git commit -m 'Add amazing feature'`
5. Push & PR


**📚 API Docs:** `/api/docs`
