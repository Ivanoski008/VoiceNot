import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import json
import uuid

class AudioNode:
    """Representa un nodo de efecto de audio"""
    def __init__(self, node_id, node_type, x, y, params=None):
        self.id = node_id
        self.type = node_type
        self.x = x
        self.y = y
        self.params = params or {}
        self.connections = []  # Lista de IDs de nodos conectados
        
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'x': self.x,
            'y': self.y,
            'params': self.params,
            'connections': self.connections
        }

class NodeEditor:
    """Editor visual de nodos para crear cadenas de efectos"""
    def __init__(self, parent, on_chain_update=None):
        self.parent = parent
        self.on_chain_update = on_chain_update
        
        self.nodes = {}
        self.selected_node = None
        self.dragging_node = None
        self.connecting_from = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar = tk.Frame(main_frame, bg="#2b2b2b", height=60)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Frame izquierdo para título y añadir nodos
        left_frame = tk.Frame(toolbar, bg="#2b2b2b")
        left_frame.pack(side=tk.LEFT, padx=15, pady=10)
        
        tk.Label(left_frame, text="🎛️ Editor de Nodos", 
                font=("Arial", 12, "bold"), bg="#2b2b2b", fg="white").pack(side=tk.LEFT, padx=(0, 20))
        
        # Separador vertical
        separator = tk.Frame(left_frame, bg="#555", width=2, height=30)
        separator.pack(side=tk.LEFT, padx=10)
        
        # Menú desplegable para añadir nodos
        add_frame = tk.Frame(left_frame, bg="#2b2b2b")
        add_frame.pack(side=tk.LEFT)
        
        tk.Label(add_frame, text="Añadir Nodo:", 
                font=("Arial", 9), bg="#2b2b2b", fg="#aaa").pack(side=tk.LEFT, padx=(0, 8))
        
        self.node_type_var = tk.StringVar(value="Selecciona un efecto...")
        
        node_options = [
            "🎤 Entrada",
            "🔊 Salida",
            "🎚️ Ecualizador",
            "🔉 Eco",
            "🌊 Reverb",
            "🎵 Pitch Shifter",
            "📢 Distorsión",
            "🔇 Compresor",
            "🎛️ Ganancia"
        ]
        
        self.node_combo = ttk.Combobox(
            add_frame,
            textvariable=self.node_type_var,
            values=node_options,
            state="readonly",
            width=22,
            font=("Arial", 9)
        )
        self.node_combo.pack(side=tk.LEFT, padx=5)
        self.node_combo.bind("<<ComboboxSelected>>", self.on_node_selected)
        self.node_combo.bind("<Return>", lambda e: self.add_selected_node())
        
        # Botón de añadir
        self.add_btn = tk.Button(
            add_frame,
            text="➕ Añadir",
            command=self.add_selected_node,
            bg="#4caf50",
            fg="white",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            font=("Arial", 9, "bold"),
            cursor="hand2",
            activebackground="#45a049"
        )
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        # Frame central con info
        center_frame = tk.Frame(toolbar, bg="#2b2b2b")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20)
        
        info_label = tk.Label(
            center_frame,
            text="💡 Tip: Arrastra nodos para moverlos | Clic derecho para eliminar | Conecta puntos blancos",
            font=("Arial", 8),
            bg="#2b2b2b",
            fg="#666"
        )
        info_label.pack(side=tk.LEFT)
        
        # Botones de acción (derecha)
        action_frame = tk.Frame(toolbar, bg="#2b2b2b")
        action_frame.pack(side=tk.RIGHT, padx=15, pady=10)
        
        tk.Button(action_frame, text="🗑️ Limpiar", command=self.clear_all,
                 bg="#d32f2f", fg="white", relief=tk.FLAT, padx=12, pady=6,
                 font=("Arial", 9), cursor="hand2", activebackground="#b71c1c").pack(side=tk.LEFT, padx=3)
        tk.Button(action_frame, text="💾 Guardar", command=self.save_preset,
                 bg="#1976d2", fg="white", relief=tk.FLAT, padx=12, pady=6,
                 font=("Arial", 9), cursor="hand2", activebackground="#1565c0").pack(side=tk.LEFT, padx=3)
        tk.Button(action_frame, text="📂 Cargar", command=self.load_preset,
                 bg="#388e3c", fg="white", relief=tk.FLAT, padx=12, pady=6,
                 font=("Arial", 9), cursor="hand2", activebackground="#2e7d32").pack(side=tk.LEFT, padx=3)
        
        # Canvas para dibujar nodos
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Panel de propiedades flotante (dentro del canvas)
        self.props_panel = None  # Panel flotante de propiedades
        self.current_editing_node = None  # Nodo que se está editando
        
        # Eventos del canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        self.canvas.bind("<Button-3>", self.on_right_click)
        
        # Crear nodos por defecto
        self.create_default_chain()
        
    def create_default_chain(self):
        """Crea una cadena básica: Entrada -> Salida"""
        input_node = self.add_node("input", 100, 200)
        output_node = self.add_node("output", 600, 200)
    
    def on_node_selected(self, event=None):
        """Callback cuando se selecciona un tipo de nodo"""
        # Cambiar el color del botón para indicar que hay algo seleccionado
        if self.node_type_var.get() != "Selecciona un efecto...":
            self.add_btn.config(bg="#66bb6a")  # Verde más brillante
        else:
            self.add_btn.config(bg="#4caf50")  # Verde normal
    
    def add_selected_node(self):
        """Añade el nodo seleccionado en el combobox"""
        selected = self.node_type_var.get()
        
        if selected == "Selecciona un efecto...":
            messagebox.showwarning("Selección requerida", 
                "Por favor selecciona un tipo de nodo del menú desplegable")
            return
        
        # Mapear la selección al tipo de nodo
        node_map = {
            "🎤 Entrada": "input",
            "🔊 Salida": "output",
            "🎚️ Ecualizador": "equalizer",
            "🔉 Eco": "echo",
            "🌊 Reverb": "reverb",
            "🎵 Pitch Shifter": "pitch",
            "📢 Distorsión": "distortion",
            "🔇 Compresor": "compressor",
            "🎛️ Ganancia": "gain"
        }
        
        node_type = node_map.get(selected)
        if node_type:
            # Añadir el nodo en el centro del canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            # Si el canvas aún no tiene tamaño, usar valores por defecto
            x = canvas_width // 2 if canvas_width > 1 else 400
            y = canvas_height // 2 if canvas_height > 1 else 250
            
            self.add_node(node_type, x, y)
            
            # Resetear el combobox
            self.node_type_var.set("Selecciona un efecto...")
            
            # Feedback visual
            self.canvas.config(bg="#1e3a1e")  # Flash verde
            self.canvas.after(100, lambda: self.canvas.config(bg="#1e1e1e"))
        
    def add_node(self, node_type, x=None, y=None, update_chain=True):
        """Añade un nuevo nodo al canvas"""
        if x is None:
            x = 300
        if y is None:
            y = 200
            
        node_id = str(uuid.uuid4())[:8]
        
        # Parámetros por defecto según el tipo
        params = self.get_default_params(node_type)
        
        node = AudioNode(node_id, node_type, x, y, params)
        self.nodes[node_id] = node
        
        self.draw_node(node)
        
        if update_chain:
            self.update_chain()
        
        return node_id

    def get_default_params(self, node_type):
        """Retorna parámetros por defecto para cada tipo de nodo"""
        defaults = {
            "input": {},
            "output": {},
            "equalizer": {
                "low": 0,      # -12 a +12 dB
                "mid": 0,
                "high": 0
            },
            "echo": {
                "delay": 0.3,   # segundos
                "feedback": 0.5, # 0-1
                "mix": 0.5      # 0-1
            },
            "reverb": {
                "room_size": 0.5,  # 0-1
                "damping": 0.5,    # 0-1
                "mix": 0.3         # 0-1
            },
            "pitch": {
                "semitones": 0,  # -12 a +12
                "fine": 0        # -100 a +100 cents
            },
            "distortion": {
                "drive": 0.5,    # 0-1
                "tone": 0.5,     # 0-1
                "mix": 0.5       # 0-1
            },
            "compressor": {
                "threshold": -20,  # dB
                "ratio": 4,        # 1-20
                "attack": 0.01,    # segundos
                "release": 0.1     # segundos
            },
            "gain": {
                "volume": 1.0    # 0-2
            }
        }
        return defaults.get(node_type, {})
    
    def get_node_color(self, node_type):
        """Retorna el color del nodo según su tipo"""
        colors = {
            "input": "#4caf50",
            "output": "#f44336",
            "equalizer": "#2196f3",
            "echo": "#9c27b0",
            "reverb": "#673ab7",
            "pitch": "#ff9800",
            "distortion": "#e91e63",
            "compressor": "#00bcd4",
            "gain": "#8bc34a"
        }
        return colors.get(node_type, "#757575")
    
    def get_node_label(self, node_type):
        """Retorna la etiqueta del nodo"""
        labels = {
            "input": "🎤 Entrada",
            "output": "🔊 Salida",
            "equalizer": "🎚️ EQ",
            "echo": "🔉 Eco",
            "reverb": "🌊 Reverb",
            "pitch": "🎵 Pitch",
            "distortion": "📢 Distorsión",
            "compressor": "🔇 Compresor",
            "gain": "🎛️ Ganancia"
        }
        return labels.get(node_type, node_type)
    
    def draw_node(self, node):
        """Dibuja un nodo en el canvas"""
        x, y = node.x, node.y
        width, height = 120, 60
        
        color = self.get_node_color(node.type)
        label = self.get_node_label(node.type)
        
        # Borde especial si es el nodo que se está editando
        outline_color = "#ffeb3b" if node.id == self.current_editing_node else "white"
        outline_width = 3 if node.id == self.current_editing_node else 2
        
        # Rectángulo del nodo
        rect = self.canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=color, outline=outline_color, width=outline_width,
            tags=("node", node.id)
        )
        
        # Texto del nodo
        text = self.canvas.create_text(
            x + width/2, y + height/2 - 5,
            text=label, fill="white", font=("Arial", 10, "bold"),
            tags=("node", node.id)
        )
        
        # Indicador de propiedades editables (excepto entrada/salida)
        if node.type not in ["input", "output"]:
            self.canvas.create_text(
                x + width/2, y + height - 12,
                text="⚙️ Clic para editar",
                fill="white", font=("Arial", 7),
                tags=("node", node.id)
            )
        
        # Puntos de conexión
        # Entrada (izquierda)
        if node.type != "input":
            self.canvas.create_oval(
                x - 5, y + height/2 - 5,
                x + 5, y + height/2 + 5,
                fill="white", outline=color, width=2,
                tags=("input_port", node.id)
            )
        
        # Salida (derecha)
        if node.type != "output":
            self.canvas.create_oval(
                x + width - 5, y + height/2 - 5,
                x + width + 5, y + height/2 + 5,
                fill="white", outline=color, width=2,
                tags=("output_port", node.id)
            )
    
    def redraw_all(self):
        """Redibuja todos los nodos y conexiones"""
        self.canvas.delete("all")
        
        # Dibujar conexiones primero
        for node_id, node in self.nodes.items():
            for target_id in node.connections:
                if target_id in self.nodes:
                    self.draw_connection(node_id, target_id)
        
        # Dibujar nodos
        for node in self.nodes.values():
            self.draw_node(node)
    
    def draw_connection(self, from_id, to_id):
        """Dibuja una línea de conexión entre dos nodos"""
        from_node = self.nodes[from_id]
        to_node = self.nodes[to_id]
        
        x1 = from_node.x + 120
        y1 = from_node.y + 30
        x2 = to_node.x
        y2 = to_node.y + 30
        
        # Línea curva
        self.canvas.create_line(
            x1, y1, x2, y2,
            fill="#ffeb3b", width=3, smooth=True,
            tags=("connection", f"{from_id}-{to_id}")
        )
    
    def on_canvas_click(self, event):
        """Maneja el clic en el canvas"""
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        
        if "output_port" in tags:
            # Iniciar conexión
            node_id = tags[1]
            self.connecting_from = node_id
            self.canvas.config(cursor="crosshair")
        elif "node" in tags:
            # Seleccionar nodo para arrastrar
            node_id = tags[1]
            self.selected_node = node_id
            self.dragging_node = node_id
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            self.show_properties(node_id)
    
    def on_canvas_drag(self, event):
        """Maneja el arrastre en el canvas"""
        if self.dragging_node:
            node = self.nodes[self.dragging_node]
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            
            node.x += dx
            node.y += dy
            
            self.drag_start_x = event.x
            self.drag_start_y = event.y
            
            self.redraw_all()
    
    def on_canvas_release(self, event):
        """Maneja la liberación del clic"""
        if self.connecting_from:
            # Finalizar conexión
            item = self.canvas.find_closest(event.x, event.y)[0]
            tags = self.canvas.gettags(item)
            
            if "input_port" in tags:
                to_node_id = tags[1]
                from_node = self.nodes[self.connecting_from]
                
                if to_node_id not in from_node.connections:
                    from_node.connections.append(to_node_id)
                    self.redraw_all()
                    self.update_chain()
            
            self.connecting_from = None
            self.canvas.config(cursor="")
        
        self.dragging_node = None
    
    def on_right_click(self, event):
        """Maneja el clic derecho (eliminar nodo)"""
        item = self.canvas.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item)
        
        if "node" in tags:
            node_id = tags[1]
            node = self.nodes[node_id]
            
            # No permitir eliminar entrada/salida si son los únicos
            if node.type in ["input", "output"]:
                count = sum(1 for n in self.nodes.values() if n.type == node.type)
                if count <= 1:
                    messagebox.showwarning("Advertencia", 
                        f"Debe haber al menos un nodo de {node.type}")
                    return
            
            # Cerrar panel de propiedades si es el nodo que se está editando
            if node_id == self.current_editing_node:
                self.close_properties()
            
            # Eliminar conexiones
            for other_node in self.nodes.values():
                if node_id in other_node.connections:
                    other_node.connections.remove(node_id)
            
            del self.nodes[node_id]
            self.redraw_all()
            self.update_chain()

    def show_properties(self, node_id):
        """Muestra las propiedades del nodo en un panel flotante dentro del canvas"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        self.current_editing_node = node_id
        
        # Si ya hay un panel abierto, destruirlo
        if self.props_panel:
            self.props_panel.destroy()
        
        # Crear panel flotante sobre el canvas
        self.props_panel = tk.Frame(
            self.canvas,
            bg="#1a1a1a",
            relief=tk.RAISED,
            borderwidth=0,
            highlightbackground="#ffeb3b",
            highlightthickness=2
        )
        
        # Posicionar el panel en la esquina superior derecha
        panel_width = 280  # Más compacto
        panel_height = 350  # Más pequeño
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Si el canvas aún no tiene tamaño, usar valores por defecto
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 600
        
        x = canvas_width - panel_width - 20
        y = 20
        
        # Crear ventana en el canvas
        self.canvas_window = self.canvas.create_window(
            x, y,
            window=self.props_panel,
            anchor="nw",
            tags="props_panel"
        )
        
        # Header con color del nodo y botón cerrar (más compacto)
        header = tk.Frame(self.props_panel, bg=self.get_node_color(node.type), height=40)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Título (arrastrable) - más compacto
        title_label = tk.Label(
            header,
            text=self.get_node_label(node.type),
            font=("Arial", 10, "bold"),
            bg=self.get_node_color(node.type),
            fg="white",
            cursor="fleur"  # Cursor de mover (compatible con Windows)
        )
        title_label.pack(side=tk.LEFT, padx=8, expand=True)
        
        # Hacer el header arrastrable
        self.drag_data = {"x": 0, "y": 0}
        
        def start_drag(event):
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
        
        def do_drag(event):
            # Calcular nueva posición
            coords = self.canvas.coords(self.canvas_window)
            new_x = coords[0] + (event.x - self.drag_data["x"])
            new_y = coords[1] + (event.y - self.drag_data["y"])
            
            # Limitar a los bordes del canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if new_x < 0:
                new_x = 0
            if new_y < 0:
                new_y = 0
            if new_x > canvas_width - panel_width:
                new_x = canvas_width - panel_width
            if new_y > canvas_height - panel_height:
                new_y = canvas_height - panel_height
            
            self.canvas.coords(self.canvas_window, new_x, new_y)
        
        header.bind("<Button-1>", start_drag)
        header.bind("<B1-Motion>", do_drag)
        title_label.bind("<Button-1>", start_drag)
        title_label.bind("<B1-Motion>", do_drag)
        
        # Botón cerrar (más pequeño)
        close_btn = tk.Button(
            header,
            text="✕",
            command=self.close_properties,
            bg=self.get_node_color(node.type),
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=8
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Contenedor de propiedades con scroll (más compacto)
        canvas_container = tk.Frame(self.props_panel, bg="#2b2b2b", width=panel_width, height=panel_height-40)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        canvas_container.pack_propagate(False)
        
        # Canvas para scroll
        props_canvas = tk.Canvas(canvas_container, bg="#2b2b2b", highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=props_canvas.yview)
        
        self.props_container = tk.Frame(props_canvas, bg="#2b2b2b")
        
        props_canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        props_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        canvas_window = props_canvas.create_window((0, 0), window=self.props_container, anchor="nw")
        
        def configure_scroll(event):
            props_canvas.configure(scrollregion=props_canvas.bbox("all"))
            props_canvas.itemconfig(canvas_window, width=event.width - 20)
        
        self.props_container.bind("<Configure>", configure_scroll)
        props_canvas.bind("<Configure>", lambda e: props_canvas.itemconfig(canvas_window, width=e.width - 20))
        
        # Hacer que el panel esté siempre al frente
        self.canvas.tag_raise("props_panel")
        
        # Separador (más delgado)
        tk.Frame(self.props_container, bg="#555", height=1).pack(fill=tk.X, pady=5)
        
        # Crear controles según el tipo de nodo
        if node.type == "input" or node.type == "output":
            tk.Label(
                self.props_container,
                text="Sin parámetros configurables",
                font=("Arial", 8),
                bg="#2b2b2b", fg="#999",
                wraplength=250,
                justify=tk.CENTER
            ).pack(pady=15)
        
        elif node.type == "equalizer":
            self.create_slider(node, "low", "Graves", -12, 12, "dB")
            self.create_slider(node, "mid", "Medios", -12, 12, "dB")
            self.create_slider(node, "high", "Agudos", -12, 12, "dB")
        
        elif node.type == "echo":
            self.create_slider(node, "delay", "Retardo", 0.1, 1.0, "s", 0.01)
            self.create_slider(node, "feedback", "Retroalimentación", 0, 1, "%", 0.01)
            self.create_slider(node, "mix", "Mezcla", 0, 1, "%", 0.01)
        
        elif node.type == "reverb":
            self.create_slider(node, "room_size", "Tamaño Sala", 0, 1, "", 0.01)
            self.create_slider(node, "damping", "Amortiguación", 0, 1, "", 0.01)
            self.create_slider(node, "mix", "Mezcla", 0, 1, "%", 0.01)
        
        elif node.type == "pitch":
            self.create_slider(node, "semitones", "Semitonos", -12, 12, "st")
            self.create_slider(node, "fine", "Ajuste Fino", -100, 100, "¢")
        
        elif node.type == "distortion":
            self.create_slider(node, "drive", "Intensidad", 0, 1, "", 0.01)
            self.create_slider(node, "tone", "Tono", 0, 1, "", 0.01)
            self.create_slider(node, "mix", "Mezcla", 0, 1, "%", 0.01)
        
        elif node.type == "compressor":
            self.create_slider(node, "threshold", "Umbral", -60, 0, "dB")
            self.create_slider(node, "ratio", "Ratio", 1, 20, ":1")
            self.create_slider(node, "attack", "Ataque", 0.001, 0.1, "s", 0.001)
            self.create_slider(node, "release", "Liberación", 0.01, 1, "s", 0.01)
        
        elif node.type == "gain":
            self.create_slider(node, "volume", "Volumen", 0, 2, "x", 0.01)
        
        # Espacio al final (más pequeño)
        tk.Frame(self.props_container, bg="#2b2b2b", height=10).pack()
    
    def close_properties(self):
        """Cierra el panel de propiedades"""
        if self.props_panel:
            self.props_panel.destroy()
            self.props_panel = None
        self.current_editing_node = None
        self.redraw_all()
    
    def create_slider(self, node, param_name, label, min_val, max_val, unit, resolution=1):
        """Crea un slider para un parámetro (versión compacta)"""
        frame = tk.Frame(self.props_container, bg="#2b2b2b")
        frame.pack(fill=tk.X, pady=3, padx=8)
        
        value_var = tk.DoubleVar(value=node.params.get(param_name, 0))
        
        label_frame = tk.Frame(frame, bg="#2b2b2b")
        label_frame.pack(fill=tk.X)
        
        tk.Label(
            label_frame,
            text=label,
            bg="#2b2b2b", fg="white",
            font=("Arial", 8)
        ).pack(side=tk.LEFT)
        
        value_label = tk.Label(
            label_frame,
            text=f"{value_var.get():.2f}{unit}",
            bg="#2b2b2b", fg="#ffeb3b",
            font=("Arial", 8, "bold")
        )
        value_label.pack(side=tk.RIGHT)
        
        def on_change(val):
            node.params[param_name] = float(val)
            value_label.config(text=f"{float(val):.2f}{unit}")
            self.update_chain()
        
        slider = tk.Scale(
            frame,
            from_=min_val, to=max_val,
            orient=tk.HORIZONTAL,
            resolution=resolution,
            variable=value_var,
            command=on_change,
            bg="#404040", fg="white",
            highlightthickness=0,
            troughcolor="#1e1e1e",
            activebackground="#ffeb3b",
            showvalue=False,
            length=240  # Ancho del slider
        )
        slider.pack(fill=tk.X, pady=2)
    
    def update_chain(self):
        """Actualiza la cadena de procesamiento"""
        if self.on_chain_update:
            chain = self.build_processing_chain()
            self.on_chain_update(chain)
    
    def build_processing_chain(self):
        """Construye la cadena de procesamiento ordenada"""
        # Encontrar nodo de entrada
        input_nodes = [n for n in self.nodes.values() if n.type == "input"]
        if not input_nodes:
            return []
        
        chain = []
        visited = set()
        
        def traverse(node_id):
            if node_id in visited or node_id not in self.nodes:
                return
            
            visited.add(node_id)
            node = self.nodes[node_id]
            
            if node.type != "input":
                chain.append({
                    'type': node.type,
                    'params': node.params.copy()
                })
            
            for next_id in node.connections:
                traverse(next_id)
        
        traverse(input_nodes[0].id)
        return chain
    
    def clear_all(self):
        """Limpia todos los nodos"""
        if messagebox.askyesno("Confirmar", "¿Eliminar todos los nodos?"):
            self.nodes.clear()
            self.redraw_all()
            self.create_default_chain()
    
    def load_chain_from_preset(self, chain):
        """Carga una cadena de efectos y crea los nodos visuales"""
        # Limpiar nodos existentes
        self.nodes.clear()
        
        # Limpiar panel de propiedades
        for widget in self.props_container.winfo_children():
            widget.destroy()
        
        # Crear nodo de entrada
        x_pos = 100
        y_pos = 250
        spacing = 180
        
        input_id = self.add_node("input", x_pos, y_pos, update_chain=False)
        prev_id = input_id
        x_pos += spacing
        
        # Crear nodos para cada efecto en la cadena
        for effect in chain:
            effect_type = effect['type']
            params = effect['params']
            
            # Crear el nodo sin actualizar la cadena aún
            node_id = self.add_node(effect_type, x_pos, y_pos, update_chain=False)
            
            # Establecer parámetros
            if node_id in self.nodes:
                self.nodes[node_id].params = params.copy()
            
            # Conectar con el nodo anterior
            if prev_id in self.nodes:
                self.nodes[prev_id].connections.append(node_id)
            
            prev_id = node_id
            x_pos += spacing
        
        # Crear nodo de salida
        output_id = self.add_node("output", x_pos, y_pos, update_chain=False)
        
        # Conectar último efecto con salida
        if prev_id in self.nodes and prev_id != input_id:
            self.nodes[prev_id].connections.append(output_id)
        elif prev_id == input_id:
            # Si no hay efectos, conectar entrada directamente a salida
            self.nodes[input_id].connections.append(output_id)
        
        # Redibujar todo
        self.redraw_all()
        
        # Actualizar la cadena una sola vez al final
        self.update_chain()
        
        # Mostrar mensaje de confirmación (opcional)
        # Ya no necesitamos mostrar en panel de propiedades porque ahora es flotante
    
    def save_preset(self):
        """Guarda el preset actual"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            data = {
                'nodes': [node.to_dict() for node in self.nodes.values()]
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            
            messagebox.showinfo("Éxito", "Preset guardado correctamente")
    
    def load_preset(self):
        """Carga un preset"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                self.nodes.clear()
                
                for node_data in data['nodes']:
                    node = AudioNode(
                        node_data['id'],
                        node_data['type'],
                        node_data['x'],
                        node_data['y'],
                        node_data['params']
                    )
                    node.connections = node_data['connections']
                    self.nodes[node.id] = node
                
                self.redraw_all()
                self.update_chain()
                
                messagebox.showinfo("Éxito", "Preset cargado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el preset:\n{str(e)}")
