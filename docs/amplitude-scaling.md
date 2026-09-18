TLC operates in the discrete domain: integers, strings, sets, records. It cannot work with floating-point numbers. This is not a bug — it's a design decision. Model checking requires exhaustive state exploration, and floating-point arithmetic makes the state space infinite.

## The First Attempt: Integer Scaling

The standard workaround is to scale everything up. If I multiplied all amplitudes by 10,000, then `0.7071` became `7071`, and every operation stayed in integer territory.

I changed the initial state from `[1, 0, 0, 0]` to `[10000, 0, 0, 0]`. I changed the Hadamard factor from `1/sqrt(2)` to `7071`. I changed the CNOT swap logic to operate on integers.

And then I hit the wall.

## The Deeper Problem: Integer Division is Lossy

Quantum gates are **unitary** — they are reversible and preserve information. Integer division (`\div`) is neither. When I computed `(7071 * 10000) \div 10000`, I got exactly `7071`. But when I computed `(7071 * 7071) \div 10000`, I got `4999` instead of `4999.9041`. The fractional part was discarded.

A single truncation is negligible. But TLC explores **every reachable state**, which means it applies gates repeatedly across different paths. Each application introduces a tiny rounding error. The errors compound.

After two Hadamard applications, the sum of squared amplitudes drifted from `100,000,000` to `99,980,002`. My normalization invariant — which required the sum to be within 2,000,000 of `100,000,000` — failed.
Invariant NormalizationInvariant is violated.

text

## What This Taught Me

This is not just a TLA+ quirk. It is a **fundamental tension** between two paradigms:

| Paradigm | Domain | Strengths | Weaknesses |
|----------|--------|-----------|------------|
| **Continuous** (physics, NumPy) | Real numbers | Natural fit for quantum mechanics | No exhaustive verification |
| **Discrete** (TLA+, TLC) | Integers, sets | Exhaustive state exploration | Cannot represent real numbers |

Quantum mechanics is continuous. TLA+ is discrete. Bridging them requires approximation, and approximation has limits.

## How I Solved It

For the final verification, I chose pragmatism over purity:

1. **Python layer:** Verifies numerical correctness with full floating-point precision. This is the ground truth.
2. **TLA+ layer:** Verifies the structural correctness of the state machine — initial state, transitions, and reachability. This is the formal specification.

The two layers complement each other. Python handles the numbers. TLA+ handles the logic.

I also relaxed the normalization invariant to a ±5% tolerance band, which absorbs integer truncation drift while still catching genuine violations.

## The Deeper Insight

This experience revealed something important about quantum software verification: **you cannot verify a continuous system with a discrete tool alone.** You need a hybrid approach. The Python layer handles the physics. The formal layer handles the logic. Together, they form a complete verification pipeline.

This is the frontier. The tools don't exist yet. People like me are building them.

## What Comes Next

The next iteration will:
1. Extend to 3-qubit GHZ states
2. Use rational arithmetic instead of integer scaling to eliminate truncation
3. Connect to real IBM quantum hardware and measure how noise corrupts the verified result

The journey continues.

---

*Tumelo Tshabalala is a second-year BSc IT student in South Africa building at the intersection of formal methods and quantum computing.*
