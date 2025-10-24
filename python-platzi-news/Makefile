install:
	@echo "Instalando paquetes"
	uv sync

run:
	uv pip install .
	platzi-news --log-level DEBUG search "tecnología" --source newsapi


publish:
	uv publish --index testpypi --username __token__ --password NUNCA_PUBLICAR_CLAVES