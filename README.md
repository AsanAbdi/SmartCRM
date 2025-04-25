# SmartCRM — Minimalist CRM with ML Predictions

SmartCRM is a lightweight CRM system for small businesses to manage clients, track interactions, and predict future behavior using machine learning. Built with FastAPI and SQLModel, it features async background processing and ML-powered decision support.

## 🚀 Features

- 🔐 JWT-secured REST API (FastAPI)
- 👥 Client, deal, and activity management (CRUD)
- ⚙️ Asynchronous task handling via Celery + Redis
- 🤖 ML model for:
  - Purchase probability
  - Churn risk
  - Upsell potential
- 📈 Metrics API for visualization
- 📄 Swagger documentation and Postman collection
- 🧪 Unit testing with pytest
- 📦 Dockerized for easy deployment

## 🧠 ML Integration

A lightweight ML model (Logistic Regression or Random Forest) is trained on synthetic behavioral data. Every activity triggers a background inference task to update predictions.

## 🔧 Tech Stack

- **Backend:** FastAPI · SQLModel · PostgreSQL
- **Async Tasks:** Celery · Redis
- **ML:** PyTorch
- **DevOps:** Docker · Railway
- **Optional:** Telegram Bot · FastAPI Admin · Plotly

## 🛠️ Setup

```bash
git clone https://github.com/your-username/smartcrm.git
cd SmartCRM
docker-compose up --build
