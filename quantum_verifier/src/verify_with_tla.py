"""
Verification Bridge: Python <-> TLA+
Compares Python's quantum extraction with TLA+'s mathematical model
"""

import sys
sys.path.append('.')

from circuit_generator import QuantumStateExtractor
import numpy as np

class VerificationBridge:
    """
    Bridges the gap between Python's Qiskit simulation
    and TLA+'s formal specification
    """
    
    def __init__(self):
        self.extractor = QuantumStateExtractor()
        self.verification_results = []
    
    def verify_bell_state(self):
        """Verify Bell state matches TLA+ expected properties"""
        print("\n" + "="*60)
        print("VERIFYING BELL STATE (Python vs TLA+ Model)")
        print("="*60)
        
        # Get Python/Qiskit's answer
        bell_circuit = self.extractor.create_bell_state()
        bell_state = self.extractor.extract_statevector(bell_circuit)
        
        # These are the values TLA+'s BellStateProperty checks
        # TLA+ says: amp[1] > 0.7, amp[2] = 0, amp[3] = 0, amp[4] > 0.7
        
        checks = {
            "|00⟩ amplitude ≈ 0.7071": abs(bell_state[0].real - 0.7071) < 0.001,
            "|01⟩ amplitude = 0": abs(bell_state[1]) < 1e-10,
            "|10⟩ amplitude = 0": abs(bell_state[2]) < 1e-10,
            "|11⟩ amplitude ≈ 0.7071": abs(bell_state[3].real - 0.7071) < 0.001,
        }
        
        all_passed = True
        for check, passed in checks.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status}: {check}")
            if not passed:
                all_passed = False
        
        self.verification_results.append({
            "test": "Bell State Verification",
            "passed": all_passed,
            "details": checks
        })
        
        return all_passed
    
    def verify_normalization(self):
        """Verify the quantum state is normalized (sum of probabilities = 1)"""
        print("\n" + "="*60)
        print("VERIFYING NORMALIZATION (TLA+ Invariant)")
        print("="*60)
        
        bell_circuit = self.extractor.create_bell_state()
        bell_state = self.extractor.extract_statevector(bell_circuit)
        probabilities = self.extractor.extract_probabilities(bell_state)
        total_probability = np.sum(probabilities)
        
        # TLA+ NormalizationInvariant says: total must be within tolerance of 1
        tolerance = 1e-10
        normalized = abs(total_probability - 1.0) < tolerance
        
        print(f"   Total probability: {total_probability:.10f}")
        print(f"   Expected: 1.0 ± {tolerance}")
        print(f"   {'✅ PASS' if normalized else '❌ FAIL'}: Normalization holds")
        
        self.verification_results.append({
            "test": "Normalization Invariant",
            "passed": normalized,
            "details": {"total_probability": total_probability}
        })
        
        return normalized
    
    def generate_report(self):
        """Generate a verification report"""
        print("\n" + "="*60)
        print("FINAL VERIFICATION REPORT")
        print("="*60)
        
        total_tests = len(self.verification_results)
        passed_tests = sum(1 for r in self.verification_results if r["passed"])
        
        print(f"\n   Total tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {total_tests - passed_tests}")
        
        if passed_tests == total_tests:
            print("\nALL VERIFICATIONS PASSED")
            print("   The quantum simulator is behaving correctly!")
        else:
            print("\n⚠️ SOME VERIFICATIONS FAILED")
            print("   Investigation required.")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    bridge = VerificationBridge()
    bridge.verify_bell_state()
    bridge.verify_normalization()
    bridge.generate_report()