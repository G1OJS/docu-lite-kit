"""
    to show what can be done with ast
"""

import sys
import ast

FILTER_TYPES = (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)

def _format(node, level=0):
    indent = "   "
    if isinstance(node, ast.AST):
        lines = []

        if isinstance(node, FILTER_TYPES):
            name = getattr(node, "name", None)
            lineno = getattr(node, "lineno", None)
            doc = ast.get_docstring(node)
            lines.append(f"{indent*level}{node.__class__.__name__}(name={name}, lineno={lineno})")
            if doc:
                # Optional: format the docstring on its own line, indented
                for line in doc.strip().splitlines():
                    lines.append(f"{indent*(level+1)}{line.strip()}")

        # Always recurse into children regardless of node type
        for field in node._fields:
            value = getattr(node, field, None)
            if isinstance(value, list):
                for item in value:
                    lines.append(_format(item, level+1))
            elif isinstance(value, ast.AST):
                lines.append(_format(value, level+1))

        return '\n'.join(line for line in lines if line)

    return ''


if __name__ == '__main__':
    import sys, tokenize
    filename=r"C:\Users\drala\Documents\Projects\GitHub\NECBOL\necbol\modeller.py"
    print('=' * 50)
    print('AST tree for', filename)
    print('=' * 50)
    with tokenize.open(filename) as f:
        fstr = f.read()

    tree = ast.parse(fstr)
    print(_format(tree))



