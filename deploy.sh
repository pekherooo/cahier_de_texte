#!/bin/bash

echo "========== NETTOYAGE DES CACHES PYTHON =========="
find . -name "__pycache__" -exec rm -rf {} +

echo "========== STATUS GIT =========="
git status

echo "========== AJOUT DES MODIFICATIONS =========="
git add .

echo "========== COMMIT =========="
git commit -m "🟢 Déploiement production Render"

echo "========== PUSH VERS GITHUB =========="
git push origin main

echo "========== 🚀 PRÊT À DÉPLOYER SUR RENDER =========="
