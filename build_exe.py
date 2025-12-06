"""
Script para crear el ejecutable .exe
Ejecuta: python build_exe.py
"""
import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main_app.py',
    '--name=VoiceModifierPro',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--hidden-import=scipy.special._cdflib',
    '--hidden-import=scipy.signal',
    '--hidden-import=numpy',
    '--hidden-import=pyaudio',
    '--hidden-import=tkinter',
])
