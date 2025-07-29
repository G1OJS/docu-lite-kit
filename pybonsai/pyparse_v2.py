class next_block:

    def __init__(self, first_line_number, doclines):
        first_line_text = doclines[first_line_number]
        
        self.first_line_number = first_line_number
        self.indent = self.line_indent(first_line_text)
        self.type = ""
        self.definition = ""
        self.docstring = ""
        self.children = []

        first_line_text_words = first_line_text.split()
        if(len(first_line_text_words)>0):
            self.type = first_line_text_words[0]
        if(len(first_line_text_words)>1):
            self.definition = first_line_text_words[1:]

        docstring_lines = None
        delimeters = ['"""',"'''"]
        line_no = first_line_number - 1
        while (True):
            line_no += 1
            if(docstring_lines is None):
                docstring_delimeter = self.has_delimeter(doclines[line_no])
                if(docstring_delimeter):        
                    docstring_lines = []
                    doclines[line_no] = doclines[line_no].replace(docstring_delimeter,'',1)
            if(docstring_lines is not None):
                docstring_lines.append(doclines[line_no])
                if(docstring_delimeter in doclines[line_no]):
                    self.docstring = "\n".join(line.rstrip() for line in docstring_lines).replace(docstring_delimeter, '').strip()
                    docstring_lines = None
            end_of_doc = (line_no +1 == len(doclines) - 1)
            new_block = doclines[line_no+1].endswith(':')
            dedent = ( (docstring_lines is None) and self.line_indent(doclines[line_no+1]) <= self.indent )
            if(end_of_doc or new_block or dedent):
                self.last_line_number = line_no
                break
            
    def __repr__(self):
        return f"<line {self.first_line_number + 1} to {self.last_line_number + 1}: {self.type} {self.definition} , indent={self.indent}, docstring = '{self.docstring}'>"

    def line_indent(self, line):
        return  len(line) - len(line.lstrip())

    def has_delimeter(self,line):
        for delim in ['"""',"'''"]:
            if(delim in line):
                return delim
        return False

class doc_object_tree:
    def __init__(self, filepath):
        with open(filepath) as f:
            doclines = f.readlines()
        self.blocks = [next_block(0, doclines)]
        while (self.blocks[-1].last_line_number < len(doclines) -2):
            self.blocks.append(next_block(self.blocks[-1].last_line_number+1, doclines))

    def print(self, node = None, indent=0):
#        if node is None:
#            node = self.root
#        print(node)
#        for child in node.children:
#            self.print(child, indent + 1)
        for b in self.blocks:
            print(b)




