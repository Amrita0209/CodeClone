\# CodeClone - Intelligent Code Plagiarism Detector



\*\*Author:\*\* Amrita Nag 

\*\*Purpose\*\* Personal Project



\## What It Does



CodeClone detects code plagiarism by analyzing the \*\*structural DNA\*\* of code rather than surface-level text matching. It catches plagiarism even when students/developers:



\- Rename all variables and functions

\- Reorder code blocks

\- Change comments and formatting

\- Modify code style



\## The Problem



Traditional plagiarism detectors fail when code is superficially modified. Students can easily fool text-based tools by renaming variables. We need structural analysis.



\## The Solution



CodeClone uses \*\*Abstract Syntax Tree (AST) analysis\*\* to extract the underlying logic patterns:



1\. \*\*Function Structure Fingerprinting\*\* - Captures parameter count, return patterns, nesting depth

2\. \*\*Control Flow Pattern Matching\*\* - Analyzes if/for/while structures independent of naming

3\. \*\*Operation Sequence Analysis\*\* - Tracks mathematical/logical operations (ADD, MULTIPLY, COMPARE)

4\. \*\*Variable Relationship Graphs\*\* - Maps how variables interact regardless of names



\### Key Innovation



The `CodeStructureExtractor` class normalizes code to its structural essence. For example:

```python

