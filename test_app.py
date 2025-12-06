"""
Script de prueba rápida para verificar que los módulos funcionan
"""

print("🧪 Probando módulos...")

try:
    import tkinter as tk
    print("✅ tkinter - OK")
except Exception as e:
    print(f"❌ tkinter - ERROR: {e}")

try:
    import numpy as np
    print("✅ numpy - OK")
except Exception as e:
    print(f"❌ numpy - ERROR: {e}")

try:
    import scipy
    print("✅ scipy - OK")
except Exception as e:
    print(f"❌ scipy - ERROR: {e}")

try:
    import sounddevice as sd
    print("✅ sounddevice - OK")
    print(f"   Dispositivos de audio encontrados: {len(sd.query_devices())}")
except Exception as e:
    print(f"❌ sounddevice - ERROR: {e}")

try:
    from node_editor import NodeEditor
    print("✅ node_editor - OK")
except Exception as e:
    print(f"❌ node_editor - ERROR: {e}")

try:
    from audio_processor import AudioProcessor
    print("✅ audio_processor - OK")
except Exception as e:
    print(f"❌ audio_processor - ERROR: {e}")

print("\n" + "="*50)
print("Resumen:")
print("="*50)

try:
    import sounddevice as sd
    devices = sd.query_devices()
    
    print("\n📱 Dispositivos de Audio Disponibles:")
    print("-" * 50)
    
    for i, device in enumerate(devices):
        device_type = []
        if device['max_input_channels'] > 0:
            device_type.append("🎤 Entrada")
        if device['max_output_channels'] > 0:
            device_type.append("🔊 Salida")
        
        if device_type:
            print(f"{i}: {device['name']}")
            print(f"   Tipo: {' | '.join(device_type)}")
            print()
    
except Exception as e:
    print(f"No se pudieron listar dispositivos: {e}")

print("\n✨ Si todos los módulos están OK, ejecuta:")
print("   python main_app_sounddevice.py")
print("\n💡 Si falta algún módulo, instálalo con:")
print("   python -m pip install <nombre_modulo>")
