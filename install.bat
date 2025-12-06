@echo off
echo ========================================
echo Instalando Voice Modifier Pro
echo ========================================
echo.

echo [1/5] Actualizando pip y setuptools...
python -m pip install --upgrade pip setuptools wheel
echo.

echo [2/5] Instalando numpy...
python -m pip install numpy
echo.

echo [3/5] Instalando scipy...
python -m pip install scipy
echo.

echo [4/5] Instalando PyAudio...
echo NOTA: Si PyAudio falla, descarga el wheel desde:
echo https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
python -m pip install pyaudio
echo.

echo [5/5] Verificando instalacion...
python -c "import numpy; import scipy; import pyaudio; print('Todas las dependencias instaladas correctamente!')"
echo.

echo ========================================
echo Instalacion completada!
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo   python main_app.py
echo.
pause
