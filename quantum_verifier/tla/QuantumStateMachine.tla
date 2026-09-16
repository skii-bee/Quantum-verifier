-------------------------------- MODULE QuantumStateMachine --------------------------------
(* 
   Project 1: Quantum State Machine Verifier
   Author: Tumelo Tshabalala
   Date: 2026-09-08
   
   This specification models the state transitions of quantum gates.
   It verifies that quantum circuits behave according to the laws
   of linear algebra, independent of the simulator implementation.
*)

EXTENDS Integers, Reals, Sequences, FiniteSets, TLC

RECURSIVE SumRange(_, _)
SumRange(f, n) == IF n = 0 THEN 0 ELSE f[n] + SumRange(f, n - 1)

CONSTANTS
    MaxQubits,
    Tolerance,
    Scale          (* e.g., 10000 *)

VARIABLES
    state

(* ------------------------------------------------------------------------- *)
(* Quantum state representation                                               *)
(*                                                                           *)
(* We represent a quantum state as a record:                                  *)
(*   num_qubits : the number of qubits                                       *)
(*   amplitudes : a sequence of complex numbers (simplified as reals here)   *)
(* ------------------------------------------------------------------------- *)

(* ------------------------------------------------------------------------- *)
(* Helper functions                                                           *)
(* ------------------------------------------------------------------------- *)

(* Returns the number of possible basis states for n qubits *)
NumStates(n) == 2^n

(* Initial state: all qubits in |0...0⟩ *)
(* The statevector is [1, 0, 0, ..., 0] *)
InitialState(n) ==
    [ num_qubits |-> n,
      amplitudes |-> [i \in 1..NumStates(n) |-> IF i = 1 THEN Scale ELSE 0] ]

(* Apply a Hadamard gate to qubit q *)
(* In a real system, this transforms the amplitude vector via matrix mult *)
ApplyHadamard(s, q) ==
    LET n == s.num_qubits
        factor == 7071
        offset == 2^(n-q-1)
    IN
    [ num_qubits |-> n,
      amplitudes |-> [i \in 1..NumStates(n) |->
        LET bit == (i - 1) \div offset % 2
        IN
        IF bit = 0 THEN
            (factor * (s.amplitudes[i] + s.amplitudes[i + offset])) \div Scale
        ELSE
            (factor * (s.amplitudes[i - offset] - s.amplitudes[i])) \div Scale
      ]
    ]

(* Apply a CNOT gate with control qubit c and target qubit t *)
ApplyCNOT(s, c, t) ==
    LET n == s.num_qubits
        cbit(i) == (i - 1) \div (2^(n-c-1)) % 2
        tbit(i) == (i - 1) \div (2^(n-t-1)) % 2
    IN
    [ num_qubits |-> n,
      amplitudes |-> [i \in 1..NumStates(n) |->
        IF cbit(i) = 1 /\ tbit(i) = 0 THEN
            (* Swap amplitudes: |10⟩ <-> |11⟩ *)
            s.amplitudes[i + 2^(n-t-1)]
        ELSE IF cbit(i) = 1 /\ tbit(i) = 1 THEN
            s.amplitudes[i - 2^(n-t-1)]
        ELSE
            s.amplitudes[i]
      ]
    ]

(* ------------------------------------------------------------------------- *)
(* Bell State Specification                                                   *)
(*                                                                           *)
(* The Bell state is the most famous example of quantum entanglement.         *)
(* Circuit: H on qubit 0, then CNOT with control=0, target=1                 *)
(* Expected result: 1/sqrt(2) * [1, 0, 0, 1]                                 *)
(* ------------------------------------------------------------------------- *)

(* The Bell state transition *)
BellStateNext ==
    ApplyCNOT(ApplyHadamard(state, 0), 0, 1)

(* Property: Bell state produces exactly two outcomes *)
BellStateProperty ==
    LET expected == 7071   (* 0.7071 × 10000 *)
    IN
    /\ state.num_qubits = 2
    /\ state.amplitudes[1] > expected - Tolerance
    /\ state.amplitudes[2] = 0
    /\ state.amplitudes[3] = 0
    /\ state.amplitudes[4] > expected - Tolerance

(* ------------------------------------------------------------------------- *)
(* General Verification Properties                                            *)
(*                                                                           *)
(* These are invariants that MUST hold for any valid quantum state.          *)
(* ------------------------------------------------------------------------- *)

(* The sum of all probabilities must equal 1 (normalization) *)
NormalizationInvariant ==
    LET n == NumStates(state.num_qubits)
        squares == [i \in 1..n |-> state.amplitudes[i] * state.amplitudes[i]]
        total == SumRange(squares, n)
        expected == Scale * Scale
        upper == (expected * 105) \div 100
        lower == (expected * 95) \div 100
    IN
    /\ total < upper
    /\ total > lower

(* ------------------------------------------------------------------------- *)
(* The specification                                                          *)
(* ------------------------------------------------------------------------- *)

Init ==
    state = InitialState(2)

Next ==
    \/ state' = BellStateNext
    \/ UNCHANGED state

Spec == Init /\ [][Next]_state

(* ------------------------------------------------------------------------- *)
(* Theorems to check                                                          *)
(* ------------------------------------------------------------------------- *)

(* After applying Bell state transformation, the result must be entangled *)
BellStateTheorem ==
    LET final == ApplyCNOT(ApplyHadamard(InitialState(2), 0), 0, 1)
    IN
    /\ final.num_qubits = 2
    /\ final.amplitudes[1] > 7071 - Tolerance
    /\ final.amplitudes[2] = 0
    /\ final.amplitudes[3] = 0
    /\ final.amplitudes[4] > 7071 - Tolerance

=============================================================================