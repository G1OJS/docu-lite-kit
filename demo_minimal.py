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
        a=1

    def func_three():
        """
            standard docstring with text on closing line
            here's the closing line """
        a=1

def func_four():
    """
        standard docstring with a blank line in the middle
        
        here's the end line
    """
    
def func_five():
    """ docstring with text on start line and end line
        here's the end line """


import pybonsai # is included in func_five in error

def print_lines(file):
    """
    test
    """
    with open(file,"r") as f:
        for lno, line in enumerate(f.readlines()):
            print(f"{lno+1}: {line.replace('\n','')}")

def print_pb(pbNode, types):
    if(len(pbNode.signature)>0):
        if(pbNode.signature[0] in types):
            indent_str = "    " * pbNode.indent + "|"
            docstring = "\n" + "\n".join(f"{indent_str} {line}" for line in pbNode.docstring) if (len(pbNode.docstring)>0) else ""
            contentstring = "\n" + "\n".join(f"{indent_str} {line}" for line in pbNode.content) if (len(pbNode.content)>0) else ""
            print(f" line {pbNode.first_line_number + 1} to {pbNode.last_line_number + 1} info: {pbNode.signature}")
            print(f"{indent_str} docstring:'{docstring}'")
            print(f"{indent_str} content:'{contentstring}'")
            print("")
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

def dummy():
    """
    dummy
    """
    a=1
