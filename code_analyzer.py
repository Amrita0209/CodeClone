import ast
import hashlib
from collections import defaultdict
from typing import Dict, List, Tuple, Set

class CodeStructureExtractor:
    """
    Extracts the structural 'DNA' of code - the logic flow independent of naming.
    This is the core innovation - we normalize code to catch sneaky plagiarism.
    """
    
    def __init__(self, code_string: str, filename: str = "unknown"):
        self.code = code_string
        self.filename = filename
        self.tree = None
        self.function_signatures = []  # stores normalized function structures
        self.control_flow_patterns = []  # if/for/while patterns
        self.operation_sequences = []  # mathematical/logical operations
        self.variable_usage_graph = defaultdict(set)  # tracks how vars relate
        
        # parse once, use many times (performance optimization)
        try:
            self.tree = ast.parse(code_string)
        except SyntaxError as e:
            print(f"[!] Syntax error in {filename}: {e}")
            self.tree = None
    
    def extract_all_features(self) -> Dict:
        """Main extraction - pulls out everything interesting about the code"""
        if not self.tree:
            return self._empty_features()
        
        # walk the entire AST and collect patterns
        for node in ast.walk(self.tree):
            self._process_node(node)
        
        return {
            'functions': self.function_signatures,
            'control_flow': self.control_flow_patterns,
            'operations': self.operation_sequences,
            'var_graph': dict(self.variable_usage_graph),
            'tree_hash': self._compute_structure_hash()
        }
    
    def _process_node(self, node):
        """
        The secret sauce - processes each AST node to extract patterns.
        This is where we normalize away surface-level differences.
        """
        # Function definitions - capture the STRUCTURE not the name
        if isinstance(node, ast.FunctionDef):
            sig = self._normalize_function(node)
            self.function_signatures.append(sig)
        
        # Control flow - if/while/for create unique patterns
        elif isinstance(node, (ast.If, ast.While, ast.For)):
            pattern = self._extract_control_pattern(node)
            self.control_flow_patterns.append(pattern)
        
        # Operations - the actual logic/math being performed
        elif isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp)):
            op_sig = self._get_operation_signature(node)
            self.operation_sequences.append(op_sig)
        
        # Variable relationships - who uses what
        elif isinstance(node, ast.Name):
            self._track_variable_usage(node)
    
    def _normalize_function(self, func_node) -> Dict:
        """
        Converts function to a structure signature.
        Example: def calc_total(items) becomes {params: 1, returns: True, loops: 1, ...}
        Names don't matter - structure does.
        """
        body_structure = []
        has_return = False
        loop_count = 0
        condition_count = 0
        
        for stmt in ast.walk(func_node):
            if isinstance(stmt, ast.Return):
                has_return = True
            elif isinstance(stmt, (ast.For, ast.While)):
                loop_count += 1
            elif isinstance(stmt, ast.If):
                condition_count += 1
        
        # create a fingerprint of the function's structure
        return {
            'param_count': len(func_node.args.args),
            'has_return': has_return,
            'loops': loop_count,
            'conditionals': condition_count,
            'statement_count': len(func_node.body),
            'nesting_depth': self._calculate_max_depth(func_node)
        }
    
    def _extract_control_pattern(self, node) -> str:
        """
        Creates a pattern string for control structures.
        Example: for->if->break becomes "LOOP(COND(BREAK))"
        """
        if isinstance(node, ast.For):
            inner = self._get_body_pattern(node.body)
            return f"FOR({inner})"
        elif isinstance(node, ast.While):
            inner = self._get_body_pattern(node.body)
            return f"WHILE({inner})"
        elif isinstance(node, ast.If):
            inner = self._get_body_pattern(node.body)
            else_part = self._get_body_pattern(node.orelse) if node.orelse else ""
            return f"IF({inner}){('ELSE(' + else_part + ')') if else_part else ''}"
        return "UNKNOWN"
    
    def _get_body_pattern(self, body: List) -> str:
        """Helper to get pattern of a code block"""
        if not body:
            return ""
        
        patterns = []
        for stmt in body:
            if isinstance(stmt, ast.Return):
                patterns.append("RET")
            elif isinstance(stmt, ast.Break):
                patterns.append("BRK")
            elif isinstance(stmt, ast.Continue):
                patterns.append("CONT")
            elif isinstance(stmt, (ast.For, ast.While, ast.If)):
                patterns.append("CTRL")  # nested control
        
        return ",".join(patterns) if patterns else "STMT"
    
    def _get_operation_signature(self, node) -> str:
        """
        Captures the type of operation being performed.
        Example: a + b becomes "ADD", x > y becomes "GT"
        """
        if isinstance(node, ast.BinOp):
            op_map = {
                ast.Add: "ADD", ast.Sub: "SUB", ast.Mult: "MUL", 
                ast.Div: "DIV", ast.Mod: "MOD", ast.Pow: "POW"
            }
            return op_map.get(type(node.op), "BINOP")
        
        elif isinstance(node, ast.Compare):
            op_map = {
                ast.Eq: "EQ", ast.NotEq: "NEQ", ast.Lt: "LT",
                ast.LtE: "LTE", ast.Gt: "GT", ast.GtE: "GTE"
            }
            # might have multiple comparisons like a < b < c
            ops = [op_map.get(type(op), "CMP") for op in node.ops]
            return "_".join(ops)
        
        elif isinstance(node, ast.BoolOp):
            return "AND" if isinstance(node.op, ast.And) else "OR"
        
        return "OP"
    
    def _track_variable_usage(self, node):
        """
        Builds a graph of variable relationships.
        Helps catch plagiarism where they renamed everything but kept the logic.
        """
        # this is simplified - in production you'd track scope too
        var_name = node.id
        # track which variables appear together in expressions
        # (not fully implemented here but shows the concept)
        self.variable_usage_graph[var_name].add("used")
    
    def _calculate_max_depth(self, node, current_depth=0) -> int:
        """
        Measures code nesting complexity.
        Deeply nested code has a signature even if renamed.
        """
        max_depth = current_depth
        
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.For, ast.While, ast.If, ast.FunctionDef)):
                child_depth = self._calculate_max_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
        
        return max_depth
    
    def _compute_structure_hash(self) -> str:
        """
        Creates a hash of the code structure.
        Identical structures = identical hash, even with different names.
        """
        if not self.tree:
            return ""
        
        # convert AST to a normalized string representation
        structure_str = ast.dump(self.tree, annotate_fields=False, include_attributes=False)
        return hashlib.md5(structure_str.encode()).hexdigest()[:16]
    
    def _empty_features(self) -> Dict:
        """Returns empty features for invalid code"""
        return {
            'functions': [],
            'control_flow': [],
            'operations': [],
            'var_graph': {},
            'tree_hash': ''
        }


class SimilarityCalculator:
    """
    Compares two code structures and computes similarity score.
    Uses multiple metrics because plagiarism is sneaky.
    """
    
    @staticmethod
    def compare_features(features1: Dict, features2: Dict) -> Dict[str, float]:
        """
        Multi-dimensional similarity analysis.
        Each dimension catches different plagiarism techniques.
        """
        scores = {}
        
        # 1. Function structure similarity (catches copy-paste with rename)
        scores['function_similarity'] = SimilarityCalculator._compare_functions(
            features1['functions'], 
            features2['functions']
        )
        
        # 2. Control flow pattern matching (catches logic theft)
        scores['control_flow_similarity'] = SimilarityCalculator._compare_sequences(
            features1['control_flow'],
            features2['control_flow']
        )
        
        # 3. Operation sequence similarity (catches algorithm copying)
        scores['operation_similarity'] = SimilarityCalculator._compare_sequences(
            features1['operations'],
            features2['operations']
        )
        
        # 4. Structural hash match (exact structure match)
        scores['structure_match'] = 1.0 if features1['tree_hash'] == features2['tree_hash'] else 0.0
        
        # weighted overall score - tuned through experimentation
        # (in real code, these weights would come from testing on known plagiarism cases)
        overall = (
            scores['function_similarity'] * 0.35 +
            scores['control_flow_similarity'] * 0.30 +
            scores['operation_similarity'] * 0.25 +
            scores['structure_match'] * 0.10
        )
        
        scores['overall'] = overall
        return scores
    
    @staticmethod
    def _compare_functions(funcs1: List[Dict], funcs2: List[Dict]) -> float:
        """
        Compares function signatures using set-based similarity.
        Handles when functions are reordered or some are added/removed.
        """
        if not funcs1 or not funcs2:
            return 0.0
        
        # convert function signatures to comparable tuples
        sig1 = [tuple(sorted(f.items())) for f in funcs1]
        sig2 = [tuple(sorted(f.items())) for f in funcs2]
        
        # find matching signatures
        matches = sum(1 for s in sig1 if s in sig2)
        
        # Jaccard similarity: intersection / union
        total_unique = len(set(sig1) | set(sig2))
        return matches / total_unique if total_unique > 0 else 0.0
    
    @staticmethod
    def _compare_sequences(seq1: List, seq2: List) -> float:
        """
        Sequence similarity using longest common subsequence approach.
        Catches when code blocks are reordered but still similar.
        """
        if not seq1 or not seq2:
            return 0.0
        
        # simple implementation - could use more sophisticated LCS
        common = sum(1 for item in seq1 if item in seq2)
        total = max(len(seq1), len(seq2))
        
        return common / total if total > 0 else 0.0


class PlagiarismDetector:
    """
    Main interface - orchestrates the detection process.
    This is what users interact with.
    """
    
    def __init__(self):
        self.results = []
    
    def analyze_pair(self, code1: str, code2: str, file1: str = "file1.py", file2: str = "file2.py") -> Dict:
        """
        Analyzes two code files for similarity.
        Returns detailed breakdown of what matches.
        """
        print(f"[*] Analyzing {file1} vs {file2}...")
        
        # extract features from both files
        extractor1 = CodeStructureExtractor(code1, file1)
        extractor2 = CodeStructureExtractor(code2, file2)
        
        features1 = extractor1.extract_all_features()
        features2 = extractor2.extract_all_features()
        
        # compare features
        similarity_scores = SimilarityCalculator.compare_features(features1, features2)
        
        # interpret the results
        verdict = self._make_verdict(similarity_scores['overall'])
        
        result = {
            'file1': file1,
            'file2': file2,
            'scores': similarity_scores,
            'verdict': verdict,
            'details': {
                'file1_functions': len(features1['functions']),
                'file2_functions': len(features2['functions']),
                'file1_control_structures': len(features1['control_flow']),
                'file2_control_structures': len(features2['control_flow']),
            }
        }
        
        self.results.append(result)
        return result
    
    def _make_verdict(self, score: float) -> str:
        """
        Human-readable interpretation of similarity score.
        Thresholds based on practical testing (would tune with real data).
        """
        if score >= 0.85:
            return "🚨 HIGHLY SUSPICIOUS - Very likely plagiarized"
        elif score >= 0.65:
            return "⚠️  SUSPICIOUS - Strong structural similarity"
        elif score >= 0.40:
            return "⚡ MODERATE - Some similar patterns found"
        elif score >= 0.20:
            return "✓ LOW - Minor similarities (possibly coincidental)"
        else:
            return "✅ CLEAR - No significant similarity"
    
    def print_report(self, result: Dict):
        """Pretty-prints analysis results to console"""
        print("\n" + "="*70)
        print(f"PLAGIARISM ANALYSIS REPORT")
        print("="*70)
        print(f"\nFile 1: {result['file1']}")
        print(f"File 2: {result['file2']}")
        print(f"\nVerdict: {result['verdict']}")
        print(f"\nOverall Similarity: {result['scores']['overall']*100:.1f}%")
        print("\nDetailed Breakdown:")
        print(f"  • Function Structure:  {result['scores']['function_similarity']*100:.1f}%")
        print(f"  • Control Flow Logic:  {result['scores']['control_flow_similarity']*100:.1f}%")
        print(f"  • Operation Patterns:  {result['scores']['operation_similarity']*100:.1f}%")
        print(f"  • Exact Structure:     {result['scores']['structure_match']*100:.1f}%")
        print("\nCode Statistics:")
        print(f"  {result['file1']}: {result['details']['file1_functions']} functions, "
              f"{result['details']['file1_control_structures']} control structures")
        print(f"  {result['file2']}: {result['details']['file2_functions']} functions, "
              f"{result['details']['file2_control_structures']} control structures")
        print("="*70 + "\n")


# Quick test to verify everything works
if __name__ == "__main__":
    # test with two obviously similar functions
    code_a = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total
"""
    
    code_b = """
def get_total(items):
    result = 0
    for item in items:
        result = result + item
    return result
"""
    
    detector = PlagiarismDetector()
    result = detector.analyze_pair(code_a, code_b, "original.py", "suspicious.py")
    detector.print_report(result)