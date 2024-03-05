cd /workspaces/llama_game_demo/output/python
pip install build
python -m build --outdir dist .
pip install dist/llamagame-1.0.0-py3-none-any.whl --upgrade --no-deps --force-reinstall
