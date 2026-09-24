#!/usr/bin/env bash
# Prepara o ambiente do transcricao.py: venv com Playwright + Chromium e as bibliotecas de sistema dele.
set -euo pipefail
cd "$(dirname "$0")"

sudo apt-get update
sudo apt-get install -y python3-venv

python3 -m venv .venv
.venv/bin/pip install --upgrade pip playwright
sudo .venv/bin/python -m playwright install-deps chromium
.venv/bin/python -m playwright install chromium

echo
echo "Pronto. Teste com:"
echo "  ferramentas/.venv/bin/python ferramentas/transcricao.py --aulas 15"
