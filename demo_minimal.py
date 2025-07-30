"""
    standard file-level docstring
    with two lines
"""
def func_one():
    """ one-line docstring """
    pass

class some_class:
    """ this is a dummy class """
    def func_two():
        """ docstring with text on start line and standard close
                and the closing line has an extra indent
        """

    def func_three():
        """
            standard docstring with text on closing line
            here's the closing line """

def func_four():
    """
        standard docstring with a blank line in the middle
        
        here's the end line
    """
    
def func_five():
    """ docstring with text on start line and end line
        here's the end line """


import pybonsai

def print_lines(file):
    with open(file,"r") as f:
        for lno, line in enumerate(f.readlines()):
            print(f"{lno+1}: {line.replace('\n','')}")

def print_pb(pbNode, types):
    if(len(pbNode.signature)>0):
        if(pbNode.signature[0] in types):
            indent_str = "    " * pbNode.indent + "|"
            docstring_indented = "\n" + "\n".join(f"{indent_str} {line}" for line in pbNode.docstring) if (len(pbNode.docstring)>0) else ""
            print(f"{indent_str} line {pbNode.first_line_number + 1} info: {pbNode.signature} docstring:'{docstring_indented}'\n")
    for pbTwig in pbNode.twigs:
        print_pb(pbTwig, types)


def main():
    """
        docstring for main
    """
    
    file = r"./demo_minimal.py"
    print(f"Simple listing of test file {file}\n")
    print_lines(file)
    print(f"\nExample listing of pybonsai tree:\n")
    pbTree = pybonsai.pbTree(file)
    print_pb(pbTree.pbRoot, ['def', 'class'])

if __name__ == "__main__":
    main()

