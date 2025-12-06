# VoiceNot
Un modulador de voz el cual busca ser una opcion gratuita o muy asequible que busca competir algun dia con programas mas profesionales.
# 🎤 Voice Modifier Pro - Documentación Completa

## 📋 Índice Rápido
1. [Instalación](#instalación)
2. [Uso Básico](#uso-básico)
3. [Editor de Nodos](#editor-de-nodos)
4. [Presets](#presets)
5. [Efectos Disponibles](#efectos-disponibles)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🚀 Instalación

### Requisitos
- Windows 10 o superior
- Python 3.8+

### Pasos

```cmd
# 1. Instalar dependencias
pip install numpy scipy sounddevice soundfile

# 2. Ejecutar aplicación
python main_app_sounddevice.py
```

### Verificar Instalación
```cmd
python test_app.py
```

---

## 🎮 Uso Básico

### Inicio Rápido (3 pasos)

1. **Cargar Preset**
   - Ve a pestaña "💾 Presets"
   - Haz clic en cualquier preset (ej: "🐻 Voz Grave Cómica")
   - Los nodos se cargan automáticamente

2. **Configurar Audio**
   - Ve a "🎤 Control de Audio"
   - Selecciona tu micrófono
   - Selecciona tus auriculares/altavoces

3. **Iniciar**
   - Haz clic en "▶ INICIAR PROCESAMIENTO"

---

## 🎛️ Editor de Nodos

### Conceptos Básicos

**Nodos:** Bloques que representan efectos de audio
**Conexiones:** Líneas que conectan nodos (flujo de audio)

### Añadir Nodos

1. Usa el menú desplegable "Añadir Nodo"
2. Selecciona un efecto
3. Haz clic en "➕ Añadir" (o presiona Enter)
4. El nodo aparece en el centro del canvas

### Conectar Nodos

1. Haz clic en el **punto blanco derecho** de un nodo
2. Arrastra hasta el **punto blanco izquierdo** del siguiente nodo
3. Suelta para crear la conexión

### Editar Parámetros

1. Haz clic en cualquier nodo
2. Aparece un **panel flotante** en la esquina superior derecha
3. Ajusta los sliders
4. Los cambios se aplican en tiempo real
5. Arrastra el panel desde el header para moverlo
6. Haz clic en ✕ para cerrar

### Organizar Nodos

- **Mover:** Haz clic y arrastra el nodo
- **Eliminar:** Clic derecho en el nodo
- **Limpiar todo:** Botón "🗑️ Limpiar"

### Guardar/Cargar

- **Guardar:** Botón "💾 Guardar" → Elige nombre → Guarda .json
- **Cargar:** Botón "📂 Cargar" → Selecciona archivo .json

---

## 💾 Presets

### Presets Incluidos

1. **🐻 Voz Grave Cómica**
   - Pitch -5 semitonos
   - Graves aumentados
   - Perfecto para: Monstruos, gigantes

2. **🐿️ Voz de Ardilla**
   - Pitch +7 semitonos
   - Agudos aumentados
   - Perfecto para: Personajes animados

3. **🤖 Robot Clásico**
   - Pitch -2 + Distorsión + Eco
   - Perfecto para: Robots, IA

4. **👻 Voz Fantasmal**
   - Pitch -8 + Reverb intenso
   - Perfecto para: Fantasmas, terror

5. **📻 Radio Antiguo**
   - EQ limitado + Distorsión
   - Perfecto para: Radio AM, vintage

6. **🎸 Rockstar**
   - Distorsión + Eco + EQ potente
   - Perfecto para: Rock, metal

7. **🌊 Bajo el Agua**
   - Graves altos + Reverb + Pitch bajo
   - Perfecto para: Escenas submarinas

8. **👾 Videojuego 8-bit**
   - Distorsión alta + Pitch alto
   - Perfecto para: Retro gaming

### Cómo Usar Presets

1. Clic en preset → Nodos se crean automáticamente
2. Ve a "Editor de Nodos" para ver la cadena
3. Personaliza ajustando parámetros
4. Guarda tu versión modificada

---

## 🔊 Efectos Disponibles

### 🎤 Entrada
- Captura audio del micrófono
- Sin parámetros configurables
- Debe ser el primer nodo

### 🔊 Salida
- Envía audio procesado
- Sin parámetros configurables
- Debe ser el último nodo

### 🎚️ Ecualizador (3 bandas)
- **Graves** (-12 a +12 dB): 0-250 Hz
- **Medios** (-12 a +12 dB): 250-4000 Hz
- **Agudos** (-12 a +12 dB): 4000+ Hz

**Uso:** Ajustar balance de frecuencias

### 🔉 Eco
- **Retardo** (0.1-1.0 s): Tiempo entre repeticiones
- **Retroalimentación** (0-100%): Intensidad del eco
- **Mezcla** (0-100%): Balance original/eco

**Uso:** Añadir profundidad espacial

### 🌊 Reverb
- **Tamaño Sala** (0-100%): Tamaño del espacio
- **Amortiguación** (0-100%): Absorción de agudos
- **Mezcla** (0-100%): Cantidad de reverb

**Uso:** Simular diferentes espacios

### 🎵 Pitch Shifter
- **Semitonos** (-12 a +12): Cambio de tono musical
- **Ajuste Fino** (-100 a +100 cents): Ajuste preciso

**Uso:** Cambiar tono de voz (grave/agudo)

### 📢 Distorsión
- **Intensidad** (0-100%): Cantidad de distorsión
- **Tono** (0-100%): Filtro de frecuencia
- **Mezcla** (0-100%): Balance original/distorsionado

**Uso:** Añadir carácter y saturación

### 🔇 Compresor
- **Umbral** (-60 a 0 dB): Nivel de activación
- **Ratio** (1-20:1): Intensidad de compresión
- **Ataque** (0.001-0.1 s): Rapidez de respuesta
- **Liberación** (0.01-1 s): Tiempo de recuperación

**Uso:** Controlar rango dinámico

### 🎛️ Ganancia
- **Volumen** (0-2x): Multiplicador de volumen

**Uso:** Ajustar volumen final

---

## 🎨 Ejemplos de Cadenas

### Voz Profesional de Radio
```
🎤 → 🔇 Compresor → 🎚️ EQ → 🎛️ Ganancia → 🔊
```
- Compresor: Threshold -20, Ratio 6
- EQ: Graves +3, Medios +4, Agudos -2
- Ganancia: 1.2x

### Voz de Demonio
```
🎤 → 🎵 Pitch (-8) → 📢 Distorsión → 🌊 Reverb → 🔊
```
- Pitch: -8 semitonos
- Distorsión: Drive 50%, Mix 40%
- Reverb: Room 90%, Mix 70%

### Voz Espacial
```
🎤 → 🎚️ EQ → 🔉 Eco → 🌊 Reverb → 🔊
```
- EQ: Graves -4, Medios +2, Agudos +6
- Eco: Delay 0.4s, Feedback 40%
- Reverb: Room 70%, Mix 50%

---

## 🆘 Solución de Problemas

### No se detecta el micrófono
- Verifica que esté conectado
- Haz clic en "🔄 Actualizar Dispositivos"
- Dale permisos de micrófono a Python

### Escucho eco/feedback
- **Usa auriculares**, no altavoces
- Reduce el volumen del micrófono
- Aleja el micrófono de los altavoces

### La voz suena cortada
- Cierra otras apps que usen el micrófono
- Reduce la cantidad de efectos en la cadena
- Reinicia la aplicación

### Error al instalar PyAudio
**Solución:** Usa la versión con SoundDevice (recomendada)
```cmd
python main_app_sounddevice.py
```

Si necesitas PyAudio:
1. Descarga wheel desde: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Instala: `pip install PyAudio-0.2.14-cp3XX-cp3XX-win_amd64.whl`

### El panel flotante no aparece
- Asegúrate de hacer clic en un nodo (no en el canvas vacío)
- Verifica que el nodo tenga parámetros editables
- Los nodos Entrada/Salida no tienen parámetros

### No se escucha audio procesado
- Verifica que los dispositivos correctos estén seleccionados
- Asegúrate de que el audio esté iniciado (botón verde)
- Revisa que los nodos estén conectados correctamente

---

## 💡 Tips y Mejores Prácticas

### Para Principiantes
1. Empieza con presets
2. Experimenta ajustando un parámetro a la vez
3. Guarda tus configuraciones favoritas
4. Usa auriculares siempre

### Para Crear Voces Graves
- Pitch negativo (-3 a -8 semitonos)
- Aumenta graves en EQ (+4 a +8 dB)
- Reduce agudos (-2 a -6 dB)

### Para Crear Voces Agudas
- Pitch positivo (+4 a +10 semitonos)
- Reduce graves (-4 a -8 dB)
- Aumenta agudos (+2 a +6 dB)

### Para Efectos Espaciales
- Usa Reverb con Room Size alto (70-90%)
- Añade Eco con Delay largo (0.3-0.5s)
- Ajusta Mix para controlar intensidad

### Orden Recomendado de Efectos
```
1. 🎤 Entrada (siempre primero)
2. 🔇 Compresor (controla dinámicas)
3. 🎵 Pitch (cambia tono)
4. 🎚️ EQ (ajusta frecuencias)
5. 📢 Distorsión (añade carácter)
6. 🔉 Eco (añade repeticiones)
7. 🌊 Reverb (añade espacio)
8. 🎛️ Ganancia (ajusta volumen final)
9. 🔊 Salida (siempre último)
```

---

## 🎯 Usar en Otras Aplicaciones

### Discord, Zoom, Teams, etc.

**Necesitas un cable de audio virtual:**

1. **Instala VB-Audio Virtual Cable** (gratis)
   - Descarga: https://vb-audio.com/Cable/

2. **En Voice Modifier Pro:**
   - Entrada: Tu micrófono real
   - Salida: CABLE Input (VB-Audio)

3. **En Discord/Zoom:**
   - Micrófono: CABLE Output (VB-Audio)

4. **Inicia procesamiento** en Voice Modifier Pro

5. **Habla** → Tu voz modificada se escuchará en Discord/Zoom

---

## 📦 Crear Ejecutable

```cmd
# 1. Instalar PyInstaller
pip install pyinstaller

# 2. Compilar
python build_exe.py

# 3. El .exe estará en dist/VoiceModifierPro.exe
```

---

## 🎓 Atajos y Trucos

### Atajos de Teclado
- **Clic derecho** en nodo → Elimina nodo
- **Arrastrar header** del panel → Mueve panel

### Trucos Útiles
- **Doble clic** en canvas → (futuro: añadir nodo rápido)
- **Shift + Arrastrar** → (futuro: selección múltiple)
- **Ctrl + S** → (futuro: guardar rápido)

### Personalización
- Edita `audio_processor.py` para crear nuevos efectos
- Edita `node_editor.py` para cambiar colores
- Añade presets en `main_app_sounddevice.py`

---

## 📊 Especificaciones Técnicas

### Audio
- **Tasa de muestreo:** 44.1 kHz
- **Canales:** Mono (1)
- **Buffer:** 1024 samples
- **Latencia:** ~23ms
- **Formato:** int16


### Compatibilidad
- **OS:** Windows 10/11
- **Python:** 3.8+
- **Dependencias:** numpy, scipy, sounddevice

---

### Verificar Instalación
```cmd
python test_app.py
```

### Archivos Importantes
- `main_app_sounddevice.py` - Aplicación principal
- `node_editor.py` - Editor de nodos
- `audio_processor.py` - Motor de efectos
- `test_app.py` - Verificador

### Documentación
- `README.md` - Información general
- `DOCUMENTACION_COMPLETA.md` - Este archivo
- `CHANGELOG.md` - Historial de cambios
- `SOLUCION_PYAUDIO.md` - Problemas con PyAudio

---

**¡Diviértete creando voces únicas!** 🎤✨

---
