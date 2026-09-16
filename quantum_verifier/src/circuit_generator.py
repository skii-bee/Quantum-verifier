"""
Quantum Circuit Generator & Extractor
Phase 1: Generates quantum circuits and extracts state information
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

class QuantumStateExtractor:
    """
    Runs quantum circuits and extracts their mathematical state.
    This is the 'source of truth' that TLA+ will verify against.
    """
    
    def __init__(self):
        self.simulator = AerSimulator(method="statevector")
    
    def create_bell_state(self):
        """Creates a Bell state (entanglement)"""
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.save_statevector()
        return qc
    
    def create_hadamard_superposition(self):
        """Creates a single qubit in superposition"""
        qc = QuantumCircuit(1)
        qc.h(0)
        qc.save_statevector()
        return qc
    
    def create_three_qubit_ghz(self):
        """Creates a GHZ state (3-qubit entanglement)"""
        qc = QuantumCircuit(3)
        qc.h(0)
        qc.cx(0, 1)
        qc.cx(0, 2)
        qc.save_statevector()
        return qc
    
    def extract_statevector(self, circuit):
        """Runs the circuit and returns the state vector"""
        result = self.simulator.run(circuit).result()
        return np.array(result.get_statevector())
    
    def extract_probabilities(self, statevector):
        """Converts amplitudes to measurement probabilities"""
        return np.abs(statevector) ** 2
    
    def interpret_state(self, statevector):
        """
        Converts a raw statevector into human-readable information
        Returns: dict with state labels and probabilities
        """
        n_qubits = int(np.log2(len(statevector)))
        probabilities = self.extract_probabilities(statevector)
        
        interpretation = {}
        for i, prob in enumerate(probabilities):
            if prob > 1e-10:  # Only show non-zero probabilities
                # Convert index to binary string (e.g., 2 -> '10')
                state_label = format(i, f'0{n_qubits}b')
                interpretation[state_label] = {
                    'amplitude': statevector[i],
                    'probability': prob
                }
        
        return interpretation

# Test the extractor
if __name__ == "__main__":
    extractor = QuantumStateExtractor()
    
    print("=" * 60)
    print("QUANTUM STATE EXTRACTOR TEST")
    print("=" * 60)
    
    # Test Bell State
    print("\n1. Bell State (2 qubits, entangled):")
    bell = extractor.create_bell_state()
    bell_state = extractor.extract_statevector(bell)
    bell_interpretation = extractor.interpret_state(bell_state)
    for state, info in bell_interpretation.items():
        print(f"   |{state}⟩: amplitude={info['amplitude']:.4f}, probability={info['probability']:.2%}")
    
    # Test GHZ State
    print("\n2. GHZ State (3 qubits, fully entangled):")
    ghz = extractor.create_three_qubit_ghz()
    ghz_state = extractor.extract_statevector(ghz)
    ghz_interpretation = extractor.interpret_state(ghz_state)
    for state, info in ghz_interpretation.items():
        print(f"   |{state}⟩: amplitude={info['amplitude']:.4f}, probability={info['probability']:.2%}")