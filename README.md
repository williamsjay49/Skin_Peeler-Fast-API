## Skin_Peeler-Fast-API

Prerequisites: Docker, Docker Compose, Python 3.10
Clone Repo:
bashgit clone https://github.com/yourusername/shark-peeler-python.git
cd shark-peeler-python

## Set Environment Variables:
Create a .env file with:
DATABASE_URL=postgresql://dicomuser:dicompass@localhost/dicomdb
SECRET_KEY=---

Build and Run:
docker-compose up --build

Access FastAPI at http://localhost:8000, Swagger UI at http://localhost:8000/docs.

Shortcuts

Run in Detached Mode:
docker-compose up --build -d

Stop:
docker-compose down

View Containers:
docker ps
