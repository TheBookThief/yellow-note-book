import os
import urllib.request
import numpy as np
from pretty_midi import PrettyMIDI, Instrument, Note
import torch
import torch.nn as nn
import torch.nn.functional as F

# Download SoundFont if not exists - Using a more reliable URL
soundfont_path = "FluidR3_GM.sf2"
if not os.path.exists(soundfont_path):
    print("Downloading SoundFont...")
    url = "https://cdn.jsdelivr.net/gh/FluidSynth/fluidsynth@master/sf2/FluidR3_GM.sf2"
    try:
        urllib.request.urlretrieve(url, soundfont_path)
        print(f"Downloaded SoundFont to {soundfont_path}")
    except Exception as e:
        print(f"Error downloading SoundFont: {e}")
        print("You can manually download the SoundFont from:")
        print("https://musical-artifacts.com/artifacts/Zy/FluidR3_GM.sf2")
        print("and place it in the current directory.")

def generate_polynomial(degree=5):
    return np.random.uniform(-1, 1, size=degree+1).tolist()

def polynomial_to_music(poly_coeffs, num_notes=50):
    midi = PrettyMIDI()
    instrument = Instrument(program=0)  # Piano
    x = np.linspace(-1, 1, num_notes)
    y = np.polyval(poly_coeffs, x)
    for i, value in enumerate(y):
        # Ensure pitch is a valid MIDI pitch (0-127)
        pitch = int(np.clip(60 + (value * 24), 0, 127))
        velocity = int(np.clip(64 + value * 32, 0, 127))
        duration = 0.5
        start = i * duration
        end = start + duration
        note = Note(velocity=velocity, pitch=pitch, start=start, end=end)
        instrument.notes.append(note)
    midi.instruments.append(instrument)
    return midi

class PolyToMusic(nn.Module):
    def __init__(self, poly_degree=5, note_dim=128, hidden_size=64):
        super().__init__()
        self.poly_degree = poly_degree
        self.note_dim = note_dim
        self.hidden_size = hidden_size
        
        self.encoder = nn.Linear(poly_degree+1, hidden_size)
        self.lstm = nn.LSTM(input_size=note_dim, hidden_size=hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, note_dim)
    
    def forward(self, poly, target_sequence):
        # poly shape: [batch_size, poly_degree+1]
        # target_sequence shape: [batch_size, seq_length, note_dim]
        
        # Encode polynomial coefficients
        encoded = self.encoder(poly)  # [batch_size, hidden_size]
        
        # Use encoded polynomial as initial hidden state
        h0 = encoded.unsqueeze(0)  # [1, batch_size, hidden_size]
        c0 = torch.zeros_like(h0)   # [1, batch_size, hidden_size]
        
        # Run LSTM
        outputs, _ = self.lstm(target_sequence, (h0, c0))
        # outputs shape: [batch_size, seq_length, hidden_size]
        
        # Decode to note probabilities
        logits = self.fc(outputs)  # [batch_size, seq_length, note_dim]
        return logits
    
    def generate(self, poly, max_length=50):
        with torch.no_grad():
            # Encode polynomial
            batch_size = poly.size(0)
            encoded = self.encoder(poly)  # [batch_size, hidden_size]
            
            # Initialize hidden state
            h = encoded.unsqueeze(0)  # [1, batch_size, hidden_size]
            c = torch.zeros_like(h)   # [1, batch_size, hidden_size]
            
            # Start with a rest note (pitch 60 = middle C)
            current_note = torch.zeros(batch_size, 1, self.note_dim)
            current_note[:, 0, 60] = 1.0  # Start with middle C
            
            # Generate sequence
            generated_notes = []
            for _ in range(max_length):
                # Get next note probabilities
                output, (h, c) = self.lstm(current_note, (h, c))
                logits = self.fc(output)
                
                # Sample next note
                probs = F.softmax(logits[:, 0], dim=-1)
                next_note = torch.multinomial(probs, 1).squeeze(-1)
                
                # Record the note
                generated_notes.append(next_note.cpu().numpy())
                
                # Prepare input for next step
                current_note = F.one_hot(next_note, num_classes=self.note_dim).float().unsqueeze(1)
            
            return np.array(generated_notes).squeeze()

def notes_to_midi(notes, duration=0.5, velocity=100, program=0):
    midi = PrettyMIDI()
    instrument = Instrument(program=program)
    for i, pitch in enumerate(notes):
        start = i * duration
        end = start + duration
        note = Note(velocity=velocity, pitch=int(pitch), start=start, end=end)
        instrument.notes.append(note)
    midi.instruments.append(instrument)
    return midi

# Hyperparameters - reduced training time for quicker testing
poly_degree = 5
note_dim = 128
hidden_size = 64
seq_length = 50
batch_size = 8
num_epochs = 20  # Reduced for testing

# Initialize model, optimizer, and loss function
model = PolyToMusic(poly_degree, note_dim, hidden_size)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Training loop
print("Starting training...")
for epoch in range(num_epochs):
    epoch_loss = 0
    num_batches = 5  # Reduced for testing
    
    for _ in range(num_batches):
        # Generate a batch of polynomial coefficients
        batch_polys = [generate_polynomial(degree=poly_degree) for _ in range(batch_size)]
        poly_tensor = torch.tensor(batch_polys, dtype=torch.float32)
        
        # Generate corresponding MIDI sequences
        target_notes = []
        for poly in batch_polys:
            midi_obj = polynomial_to_music(poly, num_notes=seq_length)
            notes = [note.pitch for note in midi_obj.instruments[0].notes]
            target_notes.append(notes)
        
        target_tensor = torch.tensor(target_notes, dtype=torch.long)
        
        # Prepare input sequence (teacher forcing)
        # Use a start token (middle C = 60) followed by the target notes except the last one
        start_tokens = torch.full((batch_size, 1), 60, dtype=torch.long)
        input_notes = torch.cat([start_tokens, target_tensor[:, :-1]], dim=1)
        
        # One-hot encode the input notes
        input_sequence = F.one_hot(input_notes, num_classes=note_dim).float()
        
        # Forward pass
        output = model(poly_tensor, input_sequence)
        
        # Calculate loss
        loss = criterion(output.reshape(-1, note_dim), target_tensor.reshape(-1))
        
        # Backward pass and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        epoch_loss += loss.item()
    
    # Print average loss for the epoch
    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss/num_batches:.4f}")

# Save the model
torch.save(model.state_dict(), 'poly_to_music_model.pt')
print("Model saved to poly_to_music_model.pt")

# Generate new notes from a test polynomial
print("Generating music from a test polynomial...")
model.eval()
test_poly = torch.tensor([generate_polynomial(degree=poly_degree)], dtype=torch.float32)
generated_notes = model.generate(test_poly)
generated_midi = notes_to_midi(generated_notes)
output_midi_path = "generated_output.mid"
generated_midi.write(output_midi_path)
print(f"Generated MIDI file: {output_midi_path}")

# Try different methods to convert MIDI to audio
try:
    # Try using midi2audio if available
    print("Attempting to convert MIDI to WAV...")
    try:
        from midi2audio import FluidSynth
        if os.path.exists(soundfont_path):
            print("Using FluidSynth with downloaded SoundFont...")
            fs = FluidSynth(sound_font=soundfont_path)
            output_wav_path = "generated_output.wav"
            fs.midi_to_audio(output_midi_path, output_wav_path)
            print(f"Generated WAV file: {output_wav_path}")
        else:
            print("SoundFont not found, skipping FluidSynth conversion")
    except ImportError:
        print("midi2audio not available, trying alternative methods...")
        
        # Try using TiMidity if available
        import subprocess
        import shutil
        
        if shutil.which("timidity"):
            print("Using TiMidity for conversion...")
            subprocess.run(['timidity', output_midi_path, '-Ow', '-o', 'generated_output.wav'])
            print("Generated WAV file: generated_output.wav")
        else:
            print("TiMidity not found. You can install it with:")
            print("  Ubuntu/Debian: sudo apt-get install timidity")
            print("  macOS: brew install timidity")
            print("  Windows: Download from http://timidity.sourceforge.net/")
            
except Exception as e:
    print(f"\nError during audio conversion: {e}")
    print("\nTo manually convert the MIDI file to audio:")
    print("1. Install FluidSynth or TiMidity")
    print("2. Or use an online converter like https://www.conversion-tool.com/midi/")
    print("3. Or open the MIDI file in a DAW like GarageBand, Audacity, etc.")
    
print("\nProcess complete! The MIDI file was successfully generated.")