# 📝 Registro de Cambios - Voice Modifier Pro

## [Versión 1.1] - Diciembre 2025

### ✨ Nuevas Funcionalidades

#### Ventana Flotante de Propiedades ⭐ NUEVO
- **Antes**: Panel fijo a la derecha ocupando 30% de la pantalla
- **Ahora**: Ventana flotante que aparece solo cuando haces clic en un nodo
- **Beneficios**:
  - 30% más espacio para el canvas
  - Interfaz más limpia (aparece bajo demanda)
  - Ventana movible y siempre visible (topmost)
  - Header con color del nodo para identificación rápida
  - Scroll automático para nodos con muchos parámetros
  - Indicador visual (borde amarillo) en el nodo siendo editado
  - Botón de cerrar integrado

#### Menú Desplegable para Nodos
- **Antes**: Barra de herramientas con 9 botones individuales para cada tipo de nodo
- **Ahora**: Menú desplegable limpio y organizado con botón "➕ Añadir"
- **Beneficios**:
  - Interfaz más limpia y profesional
  - Más espacio en la barra de herramientas
  - Mejor organización visual
  - Feedback visual al seleccionar (botón cambia de color)
  - Atajo de teclado: presiona Enter después de seleccionar

#### Mejoras en la Interfaz
- Añadido separador visual entre secciones
- Añadido label informativo con tips en la barra de herramientas
- Mejores colores de hover en botones (activebackground)
- Cursores de mano (hand2) en botones interactivos
- Feedback visual al añadir nodo (flash verde en canvas)

#### Carga Automática de Presets
- Los presets ahora cargan automáticamente los nodos visuales en el editor
- Puedes ver, editar y personalizar cualquier preset
- Los parámetros se configuran automáticamente según el preset
- Mensaje informativo en el panel de propiedades al cargar

### 🔧 Mejoras Técnicas

- Método `load_chain_from_preset()` en NodeEditor
- Parámetro `update_chain` en `add_node()` para optimización
- Mejor manejo de posicionamiento de nodos
- Reseteo automático del combobox después de añadir

### 📚 Documentación Actualizada

- GUIA_EDITOR_NODOS.md - Actualizada con nuevo método de añadir nodos
- COMO_USAR_PRESETS.md - Actualizada con instrucciones del menú desplegable
- INICIO_RAPIDO.md - Actualizada con nueva interfaz
- CHANGELOG.md - Nuevo archivo de registro de cambios

---

## [Versión 1.0] - Diciembre 2025

### 🎉 Lanzamiento Inicial

#### Características Principales

**Editor Visual de Nodos**
- Sistema de nodos drag & drop
- Conexiones visuales entre efectos
- Panel de propiedades en tiempo real
- Sistema de guardar/cargar configuraciones (.json)

**9 Tipos de Nodos**
- 🎤 Entrada - Captura de micrófono
- 🔊 Salida - Salida de audio
- 🎚️ Ecualizador - 3 bandas (graves, medios, agudos)
- 🔉 Eco - Delay con feedback
- 🌊 Reverb - Reverberación de sala
- 🎵 Pitch Shifter - Cambio de tono (±12 semitonos)
- 📢 Distorsión - Saturación y carácter
- 🔇 Compresor - Control dinámico
- 🎛️ Ganancia - Control de volumen

**8 Presets Predefinidos**
- 🐻 Voz Grave Cómica
- 🐿️ Voz de Ardilla
- 🤖 Robot Clásico
- 👻 Voz Fantasmal
- 📻 Radio Antiguo
- 🎸 Rockstar
- 🌊 Bajo el Agua
- 👾 Videojuego 8-bit

**Procesamiento de Audio**
- Procesamiento en tiempo real (latencia ~23ms)
- Soporte para múltiples dispositivos de audio
- Tasa de muestreo: 44.1kHz
- Buffer: 1024 samples

**Dos Versiones**
- main_app.py - Versión con PyAudio
- main_app_sounddevice.py - Versión con SoundDevice (recomendada)

**Documentación Completa**
- README.md - Documentación general
- START_HERE.md - Punto de inicio
- INICIO_RAPIDO.md - Guía rápida
- GUIA_EDITOR_NODOS.md - Guía del editor
- PRESETS_EXPLICADOS.md - Explicación de presets
- COMO_USAR_PRESETS.md - Tutorial de presets
- SOLUCION_PYAUDIO.md - Solución de problemas
- RESUMEN_FUNCIONALIDADES.md - Resumen técnico

**Scripts de Utilidad**
- install.bat - Instalador automático
- test_app.py - Verificador de módulos
- build_exe.py - Compilador a .exe

---

## 🔮 Próximas Versiones (Planeadas)

### Versión 1.2 (Futuro)
- [ ] Visualizador de forma de onda en tiempo real
- [ ] Medidor de nivel de audio (VU meter)
- [ ] Más efectos (chorus, flanger, phaser)
- [ ] Temas de color personalizables

### Versión 1.3 (Futuro)
- [ ] Automatización de parámetros
- [ ] Grabación de audio procesado
- [ ] Atajos de teclado personalizables
- [ ] Modo "performance" con menor latencia

### Versión 2.0 (Futuro)
- [ ] Soporte para VST plugins
- [ ] Procesamiento multi-hilo
- [ ] Presets compartibles en la nube
- [ ] Interfaz con temas personalizables

---

## 📊 Estadísticas

**Versión 1.1**
- Archivos de código: 5
- Líneas de código: ~2,500
- Archivos de documentación: 11
- Presets incluidos: 8
- Tipos de efectos: 9

---

## 🙏 Agradecimientos

Gracias por usar Voice Modifier Pro. Si tienes sugerencias o encuentras bugs, no dudes en reportarlos.

---

**Nota**: Este proyecto está en desarrollo activo. Las versiones futuras pueden incluir cambios significativos en la API y la interfaz.
