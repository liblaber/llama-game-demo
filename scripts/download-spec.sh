curl http://localhost:8000/openapi.json -o spec.json
python -m json.tool spec.json spec.json