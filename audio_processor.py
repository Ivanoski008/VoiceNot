import numpy as np
from scipy import signal
from collections import deque

class AudioProcessor:
    """Procesa audio aplicando una cadena de efectos"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.chain = []
        
        # Buffers para efectos con memoria
        self.echo_buffer = deque(maxlen=int(sample_rate * 2))  # 2 segundos max
        self.reverb_buffer = deque(maxlen=int(sample_rate * 1))  # 1 segundo
        
    def set_chain(self, chain):
        """Establece la cadena de procesamiento"""
        self.chain = chain
        
    def process(self, audio_data):
        """Procesa el audio a través de la cadena de efectos"""
        if len(audio_data) == 0:
            return audio_data
        
        audio = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32)
        
        for effect in self.chain:
            effect_type = effect['type']
            params = effect['params']
            
            if effect_type == 'equalizer':
                audio = self.apply_equalizer(audio, params)
            elif effect_type == 'echo':
                audio = self.apply_echo(audio, params)
            elif effect_type == 'reverb':
                audio = self.apply_reverb(audio, params)
            elif effect_type == 'pitch':
                audio = self.apply_pitch(audio, params)
            elif effect_type == 'distortion':
                audio = self.apply_distortion(audio, params)
            elif effect_type == 'compressor':
                audio = self.apply_compressor(audio, params)
            elif effect_type == 'gain':
                audio = self.apply_gain(audio, params)
        
        # Normalizar y convertir de vuelta
        audio = np.clip(audio, -32768, 32767).astype(np.int16)
        return audio.tobytes()
    
    def apply_equalizer(self, audio, params):
        """Aplica ecualización de 3 bandas"""
        low_gain = params.get('low', 0)
        mid_gain = params.get('mid', 0)
        high_gain = params.get('high', 0)
        
        # Filtros de banda
        # Graves: 0-250 Hz
        if low_gain != 0:
            sos_low = signal.butter(2, 250, 'lp', fs=self.sample_rate, output='sos')
            low_band = signal.sosfilt(sos_low, audio)
            audio = audio + low_band * (10 ** (low_gain / 20) - 1)
        
        # Medios: 250-4000 Hz
        if mid_gain != 0:
            sos_mid = signal.butter(2, [250, 4000], 'bp', fs=self.sample_rate, output='sos')
            mid_band = signal.sosfilt(sos_mid, audio)
            audio = audio + mid_band * (10 ** (mid_gain / 20) - 1)
        
        # Agudos: 4000+ Hz
        if high_gain != 0:
            sos_high = signal.butter(2, 4000, 'hp', fs=self.sample_rate, output='sos')
            high_band = signal.sosfilt(sos_high, audio)
            audio = audio + high_band * (10 ** (high_gain / 20) - 1)
        
        return audio
    
    def apply_echo(self, audio, params):
        """Aplica efecto de eco"""
        delay = params.get('delay', 0.3)
        feedback = params.get('feedback', 0.5)
        mix = params.get('mix', 0.5)
        
        delay_samples = int(delay * self.sample_rate)
        
        # Añadir al buffer
        for sample in audio:
            self.echo_buffer.append(sample)
        
        # Crear eco
        output = audio.copy()
        buffer_list = list(self.echo_buffer)
        
        if len(buffer_list) >= delay_samples:
            delayed = np.array(buffer_list[-len(audio)-delay_samples:-delay_samples])
            if len(delayed) == len(audio):
                output = audio * (1 - mix) + delayed * feedback * mix
        
        return output
    
    def apply_reverb(self, audio, params):
        """Aplica efecto de reverberación"""
        room_size = params.get('room_size', 0.5)
        damping = params.get('damping', 0.5)
        mix = params.get('mix', 0.3)
        
        # Reverb simple con múltiples delays
        delays = [int(room_size * self.sample_rate * d) for d in [0.029, 0.037, 0.041, 0.043]]
        gains = [0.7, 0.6, 0.5, 0.4]
        
        reverb = np.zeros_like(audio)
        
        for delay, gain in zip(delays, gains):
            if delay < len(audio):
                delayed = np.pad(audio, (delay, 0), mode='constant')[:len(audio)]
                reverb += delayed * gain * (1 - damping)
        
        return audio * (1 - mix) + reverb * mix
    
    def apply_pitch(self, audio, params):
        """Cambia el pitch del audio"""
        semitones = params.get('semitones', 0)
        fine = params.get('fine', 0)
        
        # Calcular factor de pitch
        total_cents = semitones * 100 + fine
        pitch_factor = 2 ** (total_cents / 1200)
        
        if pitch_factor == 1.0:
            return audio
        
        # Resample para cambiar pitch
        indices = np.round(np.arange(0, len(audio), pitch_factor))
        indices = indices[indices < len(audio)].astype(int)
        
        return audio[indices]
    
    def apply_distortion(self, audio, params):
        """Aplica distorsión al audio"""
        drive = params.get('drive', 0.5)
        tone = params.get('tone', 0.5)
        mix = params.get('mix', 0.5)
        
        # Normalizar
        audio_norm = audio / 32768.0
        
        # Aplicar distorsión (soft clipping)
        driven = audio_norm * (1 + drive * 10)
        distorted = np.tanh(driven) * 32768.0
        
        # Filtro de tono
        if tone < 0.5:
            # Más graves
            cutoff = 1000 + tone * 6000
            sos = signal.butter(2, cutoff, 'lp', fs=self.sample_rate, output='sos')
            distorted = signal.sosfilt(sos, distorted)
        else:
            # Más agudos
            cutoff = 500 + (tone - 0.5) * 4000
            sos = signal.butter(2, cutoff, 'hp', fs=self.sample_rate, output='sos')
            distorted = signal.sosfilt(sos, distorted)
        
        return audio * (1 - mix) + distorted * mix
    
    def apply_compressor(self, audio, params):
        """Aplica compresión dinámica"""
        threshold = params.get('threshold', -20)
        ratio = params.get('ratio', 4)
        attack = params.get('attack', 0.01)
        release = params.get('release', 0.1)
        
        # Convertir a dB
        audio_db = 20 * np.log10(np.abs(audio) / 32768.0 + 1e-10)
        
        # Aplicar compresión
        gain_reduction = np.zeros_like(audio_db)
        mask = audio_db > threshold
        gain_reduction[mask] = (audio_db[mask] - threshold) * (1 - 1/ratio)
        
        # Aplicar ganancia
        gain_linear = 10 ** (-gain_reduction / 20)
        compressed = audio * gain_linear
        
        return compressed
    
    def apply_gain(self, audio, params):
        """Aplica ganancia simple"""
        volume = params.get('volume', 1.0)
        return audio * volume
