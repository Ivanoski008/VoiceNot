import tkinter as tk
from tkinter import ttk, messagebox
import pyaudio
from voice_filter import VoiceFilter
import threading

class VoiceFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filtro de Voz - Voice Modifier")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        self.voice_filter = VoiceFilter()
        self.audio_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Título
        title_label = tk.Label(
            self.root, 
            text="🎤 Modificador de Voz", 
            font=("Arial", 18, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Frame para controles
        control_frame = tk.Frame(self.root, pady=10)
        control_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Selector de dispositivo de entrada
        tk.Label(control_frame, text="Micrófono:", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        self.input_device_combo = ttk.Combobox(control_frame, state="readonly")
        self.input_device_combo.pack(fill=tk.X, pady=5)
        
        # Selector de dispositivo de salida
        tk.Label(control_frame, text="Salida de Audio:", font=("Arial", 10)).pack(anchor=tk.W, pady=5)
        self.output_device_combo = ttk.Combobox(control_frame, state="readonly")
        self.output_device_combo.pack(fill=tk.X, pady=5)
        
        # Botón para actualizar dispositivos
        refresh_btn = tk.Button(
            control_frame, 
            text="🔄 Actualizar Dispositivos",
            command=self.refresh_devices
        )
        refresh_btn.pack(pady=10)
        
        # Selector de filtro
        tk.Label(control_frame, text="Filtro de Voz:", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        filters = [
            ("Normal (Sin filtro)", "normal"),
            ("Voz Grave (Cómica)", "deep"),
            ("Voz Aguda (Ardilla)", "high"),
            ("Voz Robótica", "robot"),
            ("Eco", "echo")
        ]
        
        self.filter_var = tk.StringVar(value="normal")
        
        for filter_name, filter_value in filters:
            rb = tk.Radiobutton(
                control_frame,
                text=filter_name,
                variable=self.filter_var,
                value=filter_value,
                font=("Arial", 10),
                command=self.change_filter
            )
            rb.pack(anchor=tk.W, pady=2)
        
        # Botones de control
        button_frame = tk.Frame(self.root, pady=20)
        button_frame.pack()
        
        self.start_btn = tk.Button(
            button_frame,
            text="▶ Iniciar",
            command=self.start_filter,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            width=10,
            height=2
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⏹ Detener",
            command=self.stop_filter,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            width=10,
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Estado
        self.status_label = tk.Label(
            self.root,
            text="Estado: Detenido",
            font=("Arial", 10),
            fg="red"
        )
        self.status_label.pack(pady=10)
        
        # Cargar dispositivos
        self.refresh_devices()

    def refresh_devices(self):
        """Actualiza la lista de dispositivos de audio"""
        input_devices = []
        output_devices = []
        
        for i in range(self.voice_filter.p.get_device_count()):
            info = self.voice_filter.p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices.append((i, info['name']))
            if info['maxOutputChannels'] > 0:
                output_devices.append((i, info['name']))
        
        self.input_device_combo['values'] = [name for _, name in input_devices]
        self.output_device_combo['values'] = [name for _, name in output_devices]
        
        if input_devices:
            self.input_device_combo.current(0)
        if output_devices:
            self.output_device_combo.current(0)
        
        self.input_devices = input_devices
        self.output_devices = output_devices
    
    def change_filter(self):
        """Cambia el filtro de voz"""
        self.voice_filter.filter_type = self.filter_var.get()
    
    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback para procesar audio en tiempo real"""
        if self.voice_filter.running:
            processed_data = self.voice_filter.process_audio(in_data)
            return (processed_data, pyaudio.paContinue)
        return (in_data, pyaudio.paComplete)
    
    def start_filter(self):
        """Inicia el filtro de voz"""
        try:
            input_idx = self.input_device_combo.current()
            output_idx = self.output_device_combo.current()
            
            if input_idx < 0 or output_idx < 0:
                messagebox.showerror("Error", "Selecciona dispositivos de entrada y salida")
                return
            
            input_device_id = self.input_devices[input_idx][0]
            output_device_id = self.output_devices[output_idx][0]
            
            self.voice_filter.running = True
            
            self.voice_filter.stream = self.voice_filter.p.open(
                format=self.voice_filter.FORMAT,
                channels=self.voice_filter.CHANNELS,
                rate=self.voice_filter.RATE,
                input=True,
                output=True,
                input_device_index=input_device_id,
                output_device_index=output_device_id,
                frames_per_buffer=self.voice_filter.CHUNK,
                stream_callback=self.audio_callback
            )
            
            self.voice_filter.stream.start_stream()
            
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Estado: Activo", fg="green")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el filtro:\n{str(e)}")
            self.voice_filter.running = False
    
    def stop_filter(self):
        """Detiene el filtro de voz"""
        self.voice_filter.running = False
        
        if self.voice_filter.stream:
            self.voice_filter.stream.stop_stream()
            self.voice_filter.stream.close()
            self.voice_filter.stream = None
        
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Estado: Detenido", fg="red")
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if self.voice_filter.running:
            self.stop_filter()
        self.voice_filter.p.terminate()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceFilterApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
