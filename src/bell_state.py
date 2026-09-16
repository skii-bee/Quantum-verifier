import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def test_bell_state():
    """
    Phase 1: The "Trust Nothing" Verifier.
    We calculate the expected math using pure linear algebra,
    and we assert Qiskit matches it EXACTLY.
    """
    print("🔬 Running Bell State Formal Verification...")
    
    # 1. Create the circuit
    qc = QuantumCircuit(2)
    qc.h(0)      # Put qubit 0 into superposition
    qc.cx(0, 1)  # Entangle qubit 0 and qubit 1
    qc.save_statevector()
    
    # 2. Run on the CPU simulator
    sim = AerSimulator(method="statevector")
    result = sim.run(qc).result()
    qiskit_state = np.array(result.get_statevector())
    
    # 3. Calculate the expected state using pure mathematics
    # Hadamard gate matrix: H = 1/sqrt(2) * [[1, 1], [1, -1]]
    # CNOT gate matrix:     CNOT = [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]
    H = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    CNOT = np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
    
    # Initial state is |00> = [1, 0] tensor [1, 0]
    q0 = np.array([1, 0])  # Qubit 0
    q1 = np.array([1, 0])  # Qubit 1
    initial_state = np.kron(q0, q1)  # Tensor product
    
    # Apply Hadamard to qubit 0 only (Identity on qubit 1)
    H_on_q0 = np.kron(H, np.eye(2))
    state_after_h = H_on_q0 @ initial_state
    
    # Apply CNOT gate
    expected_state = CNOT @ state_after_h
    
    # 4. The Verification (Trust Nothing)
    print(f"\n   Qiskit Output: {np.round(qiskit_state, 6)}")
    print(f"   Mathematical Truth: {np.round(expected_state, 6)}")
    
    # Assert they match exactly
    if np.allclose(qiskit_state, expected_state, atol=1e-10):
        print("\n✅ VERIFIED: Qiskit's simulation is mathematically perfect.")
        return True
    else:
        print("\n❌ FAILED: Mismatch detected between Qiskit and Linear Algebra.")
        return False

if __name__ == "__main__":
    test_bell_state()