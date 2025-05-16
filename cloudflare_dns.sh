#!/bin/bash

# Caminho do diretório do script
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="$DIR/venv"

# Cria o venv se não existir
if [ ! -d "$VENV" ]; then
  echo "Criando ambiente virtual em $VENV..."
  python3 -m venv "$VENV"
fi

# Ativa o venv
source "$VENV/bin/activate"

# Instala as dependências se requirements.txt existir
if [ -f "$DIR/requirements.txt" ]; then
  echo "Instalando dependências..."
  pip install --upgrade pip
  pip install -r "$DIR/requirements.txt"
fi

# Executa conforme argumento
case "$1" in
  "setup")
    python "$DIR/main.py" setup
    ;;
  "list")
    python "$DIR/main.py" list
    ;;
  "create-a")
    python "$DIR/main.py" create-a
    ;;
  "create-srv")
    python "$DIR/main.py" create-srv
    ;;
  "all")
    python "$DIR/main.py" setup
    python "$DIR/main.py" create-a
    python "$DIR/main.py" create-srv
    ;;
  *)
    echo "Uso: $0 {setup|list|create-a|create-srv|all}"
    ;;
esac
