pyinstaller src/__main__.py --clean --additional-hooks-dir=hooks --runtime-hook=runtime-hook.py --windowed --onefile --name=SeeLevelViz
./dist/SeeLevelViz