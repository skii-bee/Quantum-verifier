from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
import time

print("Attempting optimized NVIDIA cuStateVec GPU pathway...")

qc = QuantumCircuit(25)
qc.h(range(25))
qc.measure_all()

# CPU Benchmark
cpu = AerSimulator(method="statevector", device="CPU")
start = time.time(); cpu.run(qc, shots=1024).result(); cpu_time = time.time() - start
print(f"CPU Time: {cpu_time:.4f}s")

# GPU with explicit settings
try:
    gpu = AerSimulator(
        method="statevector", 
        device="GPU",
        cuStateVec_enable=True,
        blocking_enable=True,
        blocking_qubits=20  # Force GPU for anything over 20 qubits
    )
    start = time.time(); gpu.run(qc, shots=1024).result(); gpu_time = time.time() - start
    print(f"GPU Time: {gpu_time:.4f}s")
    print(f"GPU Speedup: {cpu_time/gpu_time:.2f}x")
    print("SUCCESS: Your RTX 3050 is now a Quantum Simulator.")
except Exception as e:
    print(f"GPU still failed: {e}")
    print("But do not worry, your CPU is still incredibly fast for Phase 1.")