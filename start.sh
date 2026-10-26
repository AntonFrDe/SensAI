#!/usr/bin/env bash
# Installe ce qui manque (Ollama, modèles, venv, node_modules) puis lance l'API et le frontend.
set -euo pipefail
cd "$(dirname "$0")"

OLLAMA_URL=$(python3 -c 'import json; print(json.load(open("config.json"))["ollama_url"])')
MODELS=$(python3 -c 'import json; c = json.load(open("config.json")); print(c["model"], c.get("opponent_model", ""))')

if ! command -v ollama >/dev/null; then
    echo "Installation d'Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

if ! curl -sf "$OLLAMA_URL/api/version" >/dev/null; then
    echo "Démarrage d'Ollama..."
    ollama serve >/dev/null 2>&1 &
    for _ in $(seq 30); do curl -sf "$OLLAMA_URL/api/version" >/dev/null && break; sleep 1; done
fi

for m in $MODELS; do
    ollama show "$m" >/dev/null 2>&1 || ollama pull "$m"
done

if [ ! -x .venv/bin/python ]; then
    python3 -m venv .venv
    .venv/bin/pip install -q -r requirements.txt
fi

# Vite veut Node >= 20.19 : sinon, Node local dans .node/ (sans sudo)
NODE_VERSION=v22.14.0
node_ok() { node -e 'const [a, b] = process.versions.node.split(".").map(Number); process.exit(a > 20 || (a === 20 && b >= 19) ? 0 : 1)' 2>/dev/null; }
export PATH="$PWD/.node/bin:$PATH"
if ! node_ok; then
    echo "Installation de Node $NODE_VERSION dans .node/..."
    mkdir -p .node
    curl -fsSL "https://nodejs.org/dist/$NODE_VERSION/node-$NODE_VERSION-linux-x64.tar.xz" | tar -xJ -C .node --strip-components=1
fi
if ! (cd frontend && npm ls --depth=0 >/dev/null 2>&1); then
    echo "Installation des dépendances du frontend..."
    (cd frontend && npm install --package-lock=false)
fi

if curl -sf http://127.0.0.1:8000/api/status >/dev/null; then
    echo "API déjà lancée sur http://localhost:8000"
elif (echo >/dev/tcp/127.0.0.1/8000) >/dev/null 2>&1; then
    echo "Erreur : le port 8000 est déjà utilisé par un autre service." >&2
    exit 1
else
    .venv/bin/python server.py &
    API_PID=$!
    trap 'kill $API_PID 2>/dev/null' EXIT
fi

(sleep 3 && xdg-open http://localhost:5173 >/dev/null 2>&1 || true) &
cd frontend && npm run dev
