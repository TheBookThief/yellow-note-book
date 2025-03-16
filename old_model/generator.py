import numpy as np
from pretty_midi import PrettyMIDI, Instrument, Note

def generate_polynomial(degree=5):
    """Generate a random polynomial with coefficients in [-1, 1]."""
    return np.random.uniform(-1, 1, size=degree+1).tolist()

def polynomial_to_music(poly_coeffs, num_notes=50):
    """Map polynomial features to music notes (simplified example)."""
    midi = PrettyMIDI()
    instrument = Instrument(program=0)  # Piano
    
    x = np.linspace(-1, 1, num_notes)
    y = np.polyval(poly_coeffs, x)  # Evaluate polynomial
    
    for i, value in enumerate(y):
        # Map polynomial output to pitch (48-72 = C3 to C5)
        pitch = int(48 + (value * 12)) % 128  # Mod to valid MIDI range
        velocity = 64 + int(value * 32)
        duration = 0.5  # Fixed duration for simplicity
        
        start = i * 0.5
        end = start + duration
        note = Note(velocity=velocity, pitch=pitch, start=start, end=end)
        instrument.notes.append(note)
    
    midi.instruments.append(instrument)
    return midi

# Example usage:
poly = generate_polynomial(degree=10)
midi = polynomial_to_music(poly)
midi.write("output.mid")