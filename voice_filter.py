import pyaudio
import numpy as np
from scipy import signal
import tkinter as tk
from tkinter import ttk
import threading

class VoiceFilter:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.running = False
        self.filter_type = "normal"
        self.pitch_shift = 1.0
        
        self.p = pyaudio.PyAudio()
        self.stream = None
        
    def apply_pitch_shift(self, audio_data, shift_factor):
        """Cambia el tono de la voz"""
        if shift_factor == 1.0:
            return audio_data
        
        # Resample para cambiar el pitch
        indices = np.round(np.arange(0, len(audio_data), shift_factor))
        indices = indices[indices < len(audio_data)].astype(int)
        return audio_data[indices]
    
    def apply_deep_voice(self, audio_data):
        """Aplica efecto de voz grave"""
        return self.apply_pitch_shift(audio_data, 1.5)
    
    def apply_high_voice(self, audio_data):
        """Aplica efecto de voz aguda"""
        return self.apply_pitch_shift(audio_data, 0.7)
    
    def apply_robot_voice(self, audio_data):
        """Aplica efecto de voz robótica"""
        # Añade distorsión y modulación
        modulation = np.sin(2 * np.pi * 10 * np.arange(len(audio_data)) / self.RATE)
        return (audio_data * (0.5 + 0.5 * modulation)).astype(np.int16)
    
    def apply_echo(self, audio_data):
        """Aplica efecto de eco"""
        delay_samples = int(0.2 * self.RATE)
        echo = np.zeros(len(audio_data) + delay_samples)
        echo[:len(audio_data)] = audio_data
        echo[delay_samples:delay_samples + len(audio_data)] += audio_data * 0.5
        return echo[:len(audio_data)].astype(np.int16)
    
    def process_audio(self, in_data):
        """Procesa el audio según el filtro seleccionado"""
        audio_array = np.frombuffer(in_data, dtype=np.int16).astype(np.float32)
        
        if self.filter_type == "deep":
            audio_array = self.apply_deep_voice(audio_array)
        elif self.filter_type == "high":
            audio_array = self.apply_high_voice(audio_array)
        elif self.filter_type == "robot":
            audio_array = self.apply_robot_voice(audio_array)
        elif self.filter_type == "echo":
            audio_array = self.apply_echo(audio_array)
        
        # Normalizar y convertir de vuelta a int16
        audio_array = np.clip(audio_array, -32768, 32767).astype(np.int16)
        return audio_array.tobytes()
