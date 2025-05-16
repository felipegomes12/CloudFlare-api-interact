#!/bin/bash

# Caminho do diretório do script
PROJECT_DIR="/opt/cloudflare_dns"
VENV="$PROJECT_DIR/venv"

# Cria o venv se não existir
if [ ! -d "$VENV" ]; then
  echo "Criando ambiente virtual em $VENV..."
  python3 -m venv "$VENV"
fi

# Ativa o venv
source "$VENV/bin/activate"

# Instala as dependências se requirements.txt existir
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
  echo "Instalando dependências..."
  pip install --upgrade pip
  pip install -r "$PROJECT_DIR/requirements.txt"
fi

# Executa conforme argumento
case "$1" in
  "setup")
    python "$PROJECT_DIR/main.py" setup
    ;;
  "list")
    python "$PROJECT_DIR/main.py" list
    ;;
  "create-a")
    python "$PROJECT_DIR/main.py" create-a
    ;;
  "create-srv")
    python "$PROJECT_DIR/main.py" create-srv
    ;;
  "all")
    python "$PROJECT_DIR/main.py" setup
    python "$PROJECT_DIR/main.py" create-a
    python "$PROJECT_DIR/main.py" create-srv
    ;;
  *)
    echo "Uso: $0 {setup|list|create-a|create-srv|all}"
    ;;
esac
