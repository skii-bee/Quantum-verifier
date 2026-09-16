# Quantum State Machine Verifier

> Formal verification of quantum circuits using TLA+ and Qiskit

[![TLA+](https://img.shields.io/badge/TLA+-verified-blue)]()
[![Qiskit](https://img.shields.io/badge/Qiskit-2.5.2-purple)]()
[![Python](https://img.shields.io/badge/Python-3.11-green)]()

## What This Is

A two-layer verification system that proves a quantum simulator's output is mathematically correct. The Python layer extracts quantum statevectors and validates them against pure linear algebra. The TLA+ layer formally specifies the quantum state machine and verifies it exhaustively with the TLC model checker.

## Why This Matters

Quantum computers are noisy. Even simulators can have bugs. Before trusting a quantum algorithm's output, we need mathematical proof that it is correct. This project builds that proof.

## Architecture
┌─────────────────────────────────────────────────────┐
│ Layer 3: Verification Bridge (verify_with_tla.py) │
│ Compares Python output against expected math │
└─────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ Layer 2: TLA+ Spec (QuantumStateMachine.tla) │
│ Formal model of quantum state transitions │
│ Verified by TLC: Success, 22,366 states explored │
└─────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ Layer 1: Circuit Generator (circuit_generator.py) │
│ Runs Qiskit circuits, extracts statevectors │
└─────────────────────────────────────────────────────┘
## Results

### Python Verification
Total tests: 2
Passed: 2
Failed: 0

ALL VERIFICATIONS PASSED
The quantum simulator is behaving correctly!
### TLA+ Model Check
Status: Success
Fingerprint collision probability: 2.7E-11
Distinct states found: 22,366
Total states generated: 44,733

## The Physics

The Bell state is the canonical example of quantum entanglement. Starting from `|00⟩`, a Hadamard gate on qubit 0 creates superposition, and a CNOT gate entangles the two qubits:
|00⟩ ──H──●── (|00⟩ + |11⟩)/√2
│
|00⟩ ─────X──

The final statevector is `[0.7071, 0, 0, 0.7071]`. The qubits are now correlated: measuring one instantly determines the other. This is impossible in classical computing.

## What Was Verified

| Property | Method | Result |
|----------|--------|--------|
| Bell state amplitudes | NumPy linear algebra | PASS |
| Normalization (Σ\|ψ\|² = 1) | Python + TLA+ | PASS |
| State machine validity | TLC model checker | PASS |

## The Hard Lesson: Integer Scaling in TLA+

TLC (the TLA+ model checker) cannot handle real numbers. To verify quantum amplitudes, we scaled them by 10,000, turning `0.7071` into `7071`. This introduced a subtle problem: integer division (`\div`) truncates, and repeated gate applications compound the error.

This is a fundamental tension between discrete verification tools and continuous physical models. The full analysis is documented in `docs/amplitude-scaling.md`.

## Repository Structure
quantum_verifier/
├── src/
│ ├── circuit_generator.py # Qiskit circuit creation & extraction
│ └── verify_with_tla.py # Verification bridge
├── tla/
│ ├── QuantumStateMachine.tla # Formal specification
│ └── QuantumStateMachine.cfg # TLC configuration
├── docs/
│ └── amplitude-scaling.md # The integer scaling insight
└── README.md

## Setup
bash
# Create environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run Python verification
python src/verify_with_tla.py

# Run TLA+ model check
# Open tla/QuantumStateMachine.tla in VSCode with TLA+ extension
# Right-click → "TLA+: Check model with TLC"
Author
Tumelo Tshabalala — South Africa

Building at the intersection of formal methods and quantum computing.

License
MIT
