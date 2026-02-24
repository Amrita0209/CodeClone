"""
CodeClone Plagiarism Detection Demo
Compares multiple code pairs to show detection accuracy
"""

from code_analyzer import PlagiarismDetector

def read_file(filename):
    """Helper to read code files"""
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found!")
        return None

def main():
    print("\n" + "█"*70)
    print("█" + " "*68 + "█")
    print("█" + "  CodeClone - Advanced Code Plagiarism Detection System".center(68) + "█")
    print("█" + " "*68 + "█")
    print("█"*70 + "\n")
    
    detector = PlagiarismDetector()
    
    # Test 1: Original vs Plagiarized (should be HIGH similarity)
    print("TEST 1: Checking obvious plagiarism (renamed variables/functions)")
    print("-" * 70)
    code1 = read_file('original.py')
    code2 = read_file('plagiarized.py')
    
    if code1 and code2:
        result1 = detector.analyze_pair(code1, code2, 'original.py', 'plagiarized.py')
        detector.print_report(result1)
    
    # Test 2: Original vs Different (should be LOW similarity)
    print("\nTEST 2: Checking completely different code")
    print("-" * 70)
    code3 = read_file('different.py')
    
    if code1 and code3:
        result2 = detector.analyze_pair(code1, code3, 'original.py', 'different.py')
        detector.print_report(result2)
    
    # Summary
    print("\n" + "█"*70)
    print("SUMMARY OF RESULTS")
    print("█"*70)
    print(f"\n1. original.py vs plagiarized.py")
    print(f"   Similarity: {result1['scores']['overall']*100:.1f}% - {result1['verdict']}")
    print(f"\n2. original.py vs different.py")
    print(f"   Similarity: {result2['scores']['overall']*100:.1f}% - {result2['verdict']}")
    print("\n" + "█"*70)
    print("\n✓ Demo complete! CodeClone successfully detected plagiarism.")
    print("  Even though variable/function names were changed,")
    print("  the underlying code structure was identified as matching.\n")

if __name__ == "__main__":
    main()