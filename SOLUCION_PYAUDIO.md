# 🔧 Solución para Problemas con PyAudio en Windows

## Problema Común

PyAudio puede fallar al instalarse en Windows porque requiere compilación. Aquí están las soluciones:

## ✅ Solución 1: Usar Wheel Precompilado (RECOMENDADO)

1. **Descarga el archivo wheel apropiado** desde:
   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

2. **Identifica tu versión de Python:**
   ```cmd
   python --version
   ```
   
   Ejemplo: Python 3.14.0

3. **Descarga el archivo correcto:**
   - Para Python 3.14 64-bit: `PyAudio‑0.2.14‑cp314‑cp314‑win_amd64.whl`
   - Para Python 3.14 32-bit: `PyAudio‑0.2.14‑cp314‑cp314‑win32.whl`

4. **Instala el archivo descargado:**
   ```cmd
   python -m pip install ruta\al\archivo\PyAudio-0.2.14-cp314-cp314-win_amd64.whl
   ```

## ✅ Solución 2: Usar pipwin

```cmd
python -m pip install pipwin
pipwin install pyaudio
```

## ✅ Solución 3: Instalar Microsoft C++ Build Tools

Si prefieres compilar desde el código fuente:

1. Descarga **Microsoft C++ Build Tools**:
   https://visualstudio.microsoft.com/visual-cpp-build-tools/

2. Instala con la opción "Desktop development with C++"

3. Reinicia tu terminal

4. Intenta instalar PyAudio nuevamente:
   ```cmd
   python -m pip install pyaudio
   ```

## ⚠️ Si Nada Funciona: Versión Alternativa

Si PyAudio sigue sin funcionar, puedes usar una versión alternativa con `sounddevice`:

1. **Instala sounddevice en lugar de pyaudio:**
   ```cmd
   python -m pip install sounddevice soundfile
   ```

2. **Usa el archivo alternativo** (crearé uno para ti)

## 🧪 Verificar Instalación

Después de instalar, verifica que funciona:

```cmd
python -c "import pyaudio; print('PyAudio instalado correctamente!')"
```

## 📝 Notas

- La mayoría de problemas con PyAudio en Windows se resuelven con el wheel precompilado
- Asegúrate de descargar el archivo que coincida EXACTAMENTE con tu versión de Python
- Si usas Python 3.14 (muy nuevo), puede que aún no haya wheels disponibles. En ese caso, considera usar Python 3.11 o 3.12

## 🆘 Última Opción

Si nada funciona, considera instalar Python 3.11 o 3.12 que tienen mejor soporte:

```cmd
# Desinstala Python 3.14
# Instala Python 3.11 o 3.12 desde python.org
# Vuelve a ejecutar install.bat
```
