AIDPA: AI-Integrated Decentralized Personal Assistant
AIDPA is a full-stack personal assistant application that leverages AI, blockchain, and modern DevOps practices to manage tasks, health, finances, and habits. Built with FastAPI, Next.js, Kubernetes, and Solidity, it showcases a decentralized, AI-driven approach to personal productivity.
Features

Task Management: Create, update, and prioritize tasks with NLP and blockchain storage (IPFS + Ethereum).
Health Analysis: Analyze health metrics using LSTM models with anomaly detection.
Finance Tracking: Log income/expenses and view AI-driven forecasts.
Voice Chat: Interact with the assistant via speech-to-text and text-to-speech.
Habit Learning: Reinforcement learning for personalized habit recommendations.
Real-Time Dashboard: View recent interactions with the assistant.
Decentralized Storage: Tasks stored on IPFS and Ethereum (Anvil).

Tech Stack

Backend: FastAPI, SQLModel, MongoDB, PostgreSQL, LangChain, PyTorch
Frontend: Next.js, TypeScript, Tailwind CSS, Web Speech API
Blockchain: Solidity, Foundry, Anvil
Infrastructure: Kubernetes, Docker, NGINX Ingress
AI/ML: LSTM for health analysis, Q-learning for habit learning

Setup Instructions
Prerequisites

Docker, Docker Compose
Kubernetes (e.g., Minikube)
Node.js 18+, Python 3.10+
Foundry (for Solidity)

Local Development

Clone the repository:git clone <your-repo-url>
cd aidpa


Start backend and frontend with Docker Compose:cd infra
docker-compose up -d


Deploy TaskStorage.sol:cd aidpa-chain
forge script script/Deploy.s.sol --rpc-url http://localhost:8545 --private-key $PRIVATE_KEY --broadcast


Update .env with TASK_STORAGE_ADDRESS and secrets.
Train LSTM model:cd backend
python scripts/train_health_lstm.py


Access the app at http://localhost:3000.

Kubernetes Deployment

Start Minikube:minikube start
minikube addons enable ingress


Apply Kubernetes manifests:kubectl apply -f infra/k8s/


Add aidpa.local to /etc/hosts:echo "127.0.0.1 aidpa.local" | sudo tee -a /etc/hosts


Access the app at http://aidpa.local.

Screenshots
(Add screenshots of Tasks, Health, Finance, and Assistant pages)
Contributing
Feel free to submit issues or PRs to improve AIDPA!
License
MIT