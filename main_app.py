import tkinter as tk
from tkinter import ttk, messagebox
import pyaudio
import threading
from node_editor import NodeEditor
from audio_processor import AudioProcessor

class VoiceModifierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Voice Modifier Pro - Editor de Nodos")
        self.root.geometry("1200x700")
        
        # Audio
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        self.processor = AudioProcessor(sample_rate=44100)
        
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        
        self.setup_ui()
        
    def setup_ui(self):
        # Notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña 1: Editor de Nodos
        editor_frame = tk.Frame(notebook)
        notebook.add(editor_frame, text="🎛️ Editor de Nodos")
        
        self.node_editor = NodeEditor(editor_frame, on_chain_update=self.on_chain_update)
        
        # Pestaña 2: Control de Audio
        control_frame = tk.Frame(notebook, bg="#f5f5f5")
        notebook.add(control_frame, text="🎤 Control de Audio")
        
        self.setup_audio_controls(control_frame)
        
        # Pestaña 3: Presets
        preset_frame = tk.Frame(notebook, bg="#f5f5f5")
        notebook.add(preset_frame, text="💾 Presets")
        
        self.setup_presets(preset_frame)
        
    def setup_audio_controls(self, parent):
        """Configura los controles de audio"""
        container = tk.Frame(parent, bg="#f5f5f5")
        container.pack(expand=True)
        
        tk.Label(
            container,
            text="🎤 Control de Audio",
            font=("Arial", 20, "bold"),
            bg="#f5f5f5"
        ).pack(pady=20)
        
        # Dispositivos
        device_frame = tk.LabelFrame(
            container,
            text="Dispositivos de Audio",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            padx=20,
            pady=20
        )
        device_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(device_frame, text="Micrófono de Entrada:", 
                font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_combo = ttk.Combobox(device_frame, state="readonly", width=40)
        self.input_combo.grid(row=0, column=1, pady=5, padx=10)
        
        tk.Label(device_frame, text="Salida de Audio:", 
                font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_combo = ttk.Combobox(device_frame, state="readonly", width=40)
        self.output_combo.grid(row=1, column=1, pady=5, padx=10)
        
        tk.Button(
            device_frame,
            text="🔄 Actualizar Dispositivos",
            command=self.refresh_devices,
            font=("Arial", 10),
            bg="#2196f3",
            fg="white",
            padx=20,
            pady=5
        ).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Controles
        control_frame = tk.Frame(container, bg="#f5f5f5")
        control_frame.pack(pady=30)
        
        self.start_btn = tk.Button(
            control_frame,
            text="▶ INICIAR PROCESAMIENTO",
            command=self.start_processing,
            font=("Arial", 14, "bold"),
            bg="#4caf50",
            fg="white",
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=3
        )
        self.start_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ DETENER",
            command=self.stop_processing,
            font=("Arial", 14, "bold"),
            bg="#f44336",
            fg="white",
            padx=30,
            pady=15,
            relief=tk.RAISED,
            bd=3,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # Estado
        self.status_label = tk.Label(
            container,
            text="⚫ Estado: Detenido",
            font=("Arial", 12, "bold"),
            bg="#f5f5f5",
            fg="#f44336"
        )
        self.status_label.pack(pady=20)
        
        # Info
        info_text = """
        ℹ️ INSTRUCCIONES:
        
        1. Selecciona tu micrófono y salida de audio
        2. Ve a la pestaña "Editor de Nodos" para crear tu cadena de efectos
        3. Arrastra nodos para organizarlos
        4. Conecta nodos haciendo clic en el punto blanco derecho y arrastrando al punto izquierdo del siguiente nodo
        5. Haz clic en un nodo para ver sus propiedades
        6. Clic derecho en un nodo para eliminarlo
        7. Vuelve aquí y haz clic en "INICIAR PROCESAMIENTO"
        
        ⚠️ Usa auriculares para evitar retroalimentación
        """
        
        tk.Label(
            container,
            text=info_text,
            font=("Arial", 9),
            bg="#f5f5f5",
            fg="#666",
            justify=tk.LEFT
        ).pack(pady=10)
        
        self.refresh_devices()

    def setup_presets(self, parent):
        """Configura la sección de presets"""
        container = tk.Frame(parent, bg="#f5f5f5")
        container.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        tk.Label(
            container,
            text="💾 Presets Predefinidos",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5"
        ).pack(pady=20)
        
        presets = [
            ("🐻 Voz Grave Cómica", "deep_voice"),
            ("🐿️ Voz de Ardilla", "chipmunk"),
            ("🤖 Robot Clásico", "robot"),
            ("👻 Voz Fantasmal", "ghost"),
            ("📻 Radio Antiguo", "radio"),
            ("🎸 Rockstar", "rockstar"),
            ("🌊 Bajo el Agua", "underwater"),
            ("👾 Videojuego 8-bit", "8bit")
        ]
        
        preset_frame = tk.Frame(container, bg="#f5f5f5")
        preset_frame.pack(pady=10)
        
        for i, (name, preset_id) in enumerate(presets):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                preset_frame,
                text=name,
                command=lambda p=preset_id: self.load_builtin_preset(p),
                font=("Arial", 11),
                bg="#673ab7",
                fg="white",
                padx=20,
                pady=15,
                width=25,
                relief=tk.RAISED,
                bd=2
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
        
        tk.Label(
            container,
            text="Los presets cargarán automáticamente una configuración de nodos",
            font=("Arial", 9),
            bg="#f5f5f5",
            fg="#666"
        ).pack(pady=20)
    
    def load_builtin_preset(self, preset_id):
        """Carga un preset predefinido"""
        presets = {
            "deep_voice": [
                {"type": "pitch", "params": {"semitones": -5, "fine": 0}},
                {"type": "equalizer", "params": {"low": 6, "mid": -2, "high": -4}},
                {"type": "gain", "params": {"volume": 1.2}}
            ],
            "chipmunk": [
                {"type": "pitch", "params": {"semitones": 7, "fine": 0}},
                {"type": "equalizer", "params": {"low": -6, "mid": 2, "high": 4}},
                {"type": "compressor", "params": {"threshold": -15, "ratio": 6, "attack": 0.001, "release": 0.05}}
            ],
            "robot": [
                {"type": "pitch", "params": {"semitones": -2, "fine": 0}},
                {"type": "distortion", "params": {"drive": 0.3, "tone": 0.3, "mix": 0.4}},
                {"type": "echo", "params": {"delay": 0.1, "feedback": 0.3, "mix": 0.2}}
            ],
            "ghost": [
                {"type": "pitch", "params": {"semitones": -8, "fine": 0}},
                {"type": "reverb", "params": {"room_size": 0.9, "damping": 0.3, "mix": 0.7}},
                {"type": "equalizer", "params": {"low": -8, "mid": 4, "high": -6}}
            ],
            "radio": [
                {"type": "equalizer", "params": {"low": -10, "mid": 6, "high": -8}},
                {"type": "distortion", "params": {"drive": 0.2, "tone": 0.4, "mix": 0.3}},
                {"type": "compressor", "params": {"threshold": -20, "ratio": 8, "attack": 0.005, "release": 0.1}}
            ],
            "rockstar": [
                {"type": "distortion", "params": {"drive": 0.6, "tone": 0.6, "mix": 0.5}},
                {"type": "echo", "params": {"delay": 0.25, "feedback": 0.4, "mix": 0.3}},
                {"type": "equalizer", "params": {"low": 4, "mid": 2, "high": 3}},
                {"type": "gain", "params": {"volume": 1.3}}
            ],
            "underwater": [
                {"type": "equalizer", "params": {"low": 8, "mid": -6, "high": -10}},
                {"type": "reverb", "params": {"room_size": 0.8, "damping": 0.7, "mix": 0.6}},
                {"type": "pitch", "params": {"semitones": -3, "fine": 0}}
            ],
            "8bit": [
                {"type": "distortion", "params": {"drive": 0.8, "tone": 0.2, "mix": 0.7}},
                {"type": "pitch", "params": {"semitones": 4, "fine": 0}},
                {"type": "equalizer", "params": {"low": -4, "mid": 8, "high": -6}}
            ]
        }
        
        if preset_id in presets:
            chain = presets[preset_id]
            # Cargar en el procesador
            self.processor.set_chain(chain)
            # Cargar nodos visuales en el editor
            self.node_editor.load_chain_from_preset(chain)
            messagebox.showinfo("Preset Cargado", 
                f"Preset cargado con éxito!\n\nVe a la pestaña 'Editor de Nodos' para ver y editar los efectos.\nO ve a 'Control de Audio' para iniciar el procesamiento.")
    
    def refresh_devices(self):
        """Actualiza la lista de dispositivos"""
        input_devices = []
        output_devices = []
        
        for i in range(self.audio.get_device_count()):
            info = self.audio.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append((i, info['name']))
            if info['maxOutputChannels'] > 0:
                output_devices.append((i, info['name']))
        
        self.input_combo['values'] = [name for _, name in input_devices]
        self.output_combo['values'] = [name for _, name in output_devices]
        
        if input_devices:
            self.input_combo.current(0)
        if output_devices:
            self.output_combo.current(0)
        
        self.input_devices = input_devices
        self.output_devices = output_devices
    
    def on_chain_update(self, chain):
        """Callback cuando se actualiza la cadena de nodos"""
        self.processor.set_chain(chain)
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback de audio en tiempo real"""
        if self.running:
            try:
                processed = self.processor.process(in_data)
                return (processed, pyaudio.paContinue)
            except Exception as e:
                print(f"Error procesando audio: {e}")
                return (in_data, pyaudio.paContinue)
        return (in_data, pyaudio.paComplete)
    
    def start_processing(self):
        """Inicia el procesamiento de audio"""
        try:
            input_idx = self.input_combo.current()
            output_idx = self.output_combo.current()
            
            if input_idx < 0 or output_idx < 0:
                messagebox.showerror("Error", "Selecciona dispositivos de entrada y salida")
                return
            
            input_device = self.input_devices[input_idx][0]
            output_device = self.output_devices[output_idx][0]
            
            self.running = True
            
            self.stream = self.audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                output=True,
                input_device_index=input_device,
                output_device_index=output_device,
                frames_per_buffer=self.CHUNK,
                stream_callback=self.audio_callback
            )
            
            self.stream.start_stream()
            
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="🟢 Estado: Procesando Audio", fg="#4caf50")
            
            messagebox.showinfo("Iniciado", 
                "Procesamiento de audio iniciado.\n¡Habla por el micrófono!")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar:\n{str(e)}")
            self.running = False
    
    def stop_processing(self):
        """Detiene el procesamiento"""
        self.running = False
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="⚫ Estado: Detenido", fg="#f44336")
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if self.running:
            self.stop_processing()
        self.audio.terminate()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceModifierApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
