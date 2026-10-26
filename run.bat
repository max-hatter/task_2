@echo off
REM Скрипт запуска инструмента визуализации (Вариант 27)
cd /d "%~dp0"
python -m src.main -p requests -r https://github.com/psf/requests -m url -v 2.31.0 -o output.png -a
pause