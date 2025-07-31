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


import pybonsai
def main():
    """
        docstring for main
    """
    t = pybonsai.test("./demo_minimal.py")

if __name__ == "__main__":
    main()
