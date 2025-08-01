"""
    Everything in this demo file is 'dummy code' for the parser to parse,
    except the section indicated at the bottom
"""
def func_one():
    """ one-line docstring """
    pass

class some_class:
    """ this is a dummy class """
    a=1
    b=2
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

# Here's the actual code that runs:
import dlk
if __name__ == "__main__":
    
    input_file = r"./demo_minimal.py"
    # parse the doc looking for objects matching a,b,c,d:
    # parser = dlk.dlkIO(input_file, [ pattern_list =  [a,b,c,d] ])
    # For the pattern list, docstring and body are implied & don't need to be mentioned.
    # The pattern list itself is optional and defaults to ['class', 'def']
    parser = dlk.dlkIO(input_file)

    # print out the result including the elements a,b,c,d:
    # parser.dlkPrint([a,b,c,d])
    # This time 'docstring' and 'body' do need to be explicitly mentioned if wanted in the printout
    # However pattern list is optional and defaults to ['class', 'def', 'docstring']
    # parser.dlkPrint( pattern_list = ['def', 'class', 'docstring', 'body'])
    parser.dlkPrint(['def', 'class', 'docstring', 'body'])

    # Similar to dlkPrint, this dumps the output to a JSON file:
    # parser.dlkDumpJSON(self, JSON_file = 'dlk.json', pattern_list = ['def', 'class', 'docstring'])
    parser.dlkDumpJSON()
    

