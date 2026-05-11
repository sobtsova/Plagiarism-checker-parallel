import sys

from tests.unit_tests import run_manual_unit_tests
from tests.parallel_tests import run_parallel_unit_tests
from tests.file_verification import run_file_comparison_test
from tests.stress_test import run_stress_test
from benchmarks.speed_test import run_benchmarks
from benchmarks.parallel_speed_test import run_parallel_benchmarks
from benchmarks.k_test import run_k_benchmark

def main():
    while True:
        print("\n" + "="*50)
        print("   PLAGIARISM CHECKER: PARALLEL COMPUTING STUDY   ")
        print("="*50)
        print("1. [Correctness] Sequential Unit Tests")
        print("2. [Correctness] Parallel Unit Tests")
        print("3. [Correctness] File Comparison Test")
        print("4. [Correctness] Stress Test (1M words)")
        print("-" * 50)
        print("5. [Performance] Sequential Benchmarks")
        print("6. [Performance] Parallel Benchmarks (P=1-20)")
        print("7. [Performance] Shingle Size (k) Influence Study")
        print("0. Exit")
        
        choice = input("\nSelect an option to run: ")

        if choice == "1": run_manual_unit_tests()
        elif choice == "2": run_parallel_unit_tests()
        elif choice == "3": run_file_comparison_test()
        elif choice == "4": run_stress_test()
        elif choice == "5": run_benchmarks()
        elif choice == "6": run_parallel_benchmarks()
        elif choice == "7": run_k_benchmark()
        elif choice == "0": break
        else: print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()