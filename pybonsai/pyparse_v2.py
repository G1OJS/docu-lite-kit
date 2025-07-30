class doc_object:
    def __init__(self, first_line_number, doclines):
        first_line_text = doclines[first_line_number]
        first_line_text_words = first_line_text.split()
        self.type = "" if len(first_line_text_words) == 0 else first_line_text_words[0]
        self.definition = "" if (len(first_line_text_words) == 0) else first_line_text_words[1:]
        self.first_line_number = first_line_number
        self.last_line_number = len(doclines) - 1
        self.indent = self._line_indent(first_line_text)
        self.docstring = ""
        self.children = []

        docstring_lines = None
        line_no = first_line_number - 1
        while (line_no  < len(doclines) - 1):
            line_no += 1
            if(docstring_lines is None):
                docstring_delimeter = self._has_delimeter(doclines[line_no])
                if(docstring_delimeter):        
                    docstring_lines = []
                    doclines[line_no] = doclines[line_no].replace(docstring_delimeter,'',1)
            if(docstring_lines is not None):
                docstring_lines.append(doclines[line_no])
                if(docstring_delimeter in doclines[line_no]):
                    self.docstring = "\n".join(line.rstrip() for line in docstring_lines).replace(docstring_delimeter, '').strip()
                    docstring_lines = None
            if(line_no < len(doclines) -1):
                new_block = doclines[line_no+1].endswith(':')
                dedent = ( (docstring_lines is None) and self._line_indent(doclines[line_no+1]) <= self.indent )
                if(new_block or dedent):
                    self.last_line_number = line_no
                    break
                
    def __repr__(self):
        return f"<line {self.first_line_number + 1} to {self.last_line_number + 1}: {self.type} {self.definition} , indent={self.indent}, docstring = '{self.docstring}'>"
            
    def _line_indent(self, line):
        return  len(line) - len(line.lstrip())

    def _has_delimeter(self,line):
        for delim in ['"""',"'''"]:
            if(delim in line):
                return delim
        return False

class doc_object_tree:

    def __init__(self,filepath):
        with open(filepath) as f:
            doclines = f.readlines()
        self.blocks = [doc_object(0, doclines)]
        self.blocks[0].indent = -1
        while (self.blocks[-1].last_line_number < len(doclines) -2):
            self.blocks.append(doc_object(self.blocks[-1].last_line_number+1, doclines))

        stack = [self.blocks[0]]
        for b in self.blocks[1:]:
            while stack and b.indent < stack[-1].indent:
                stack.pop()
            stack[-1].children.append(b)
            stack.append(b)

    def print(self, node = None, indent=0):
        if node is None:
            node = self.blocks[0]
        print(node)
        for child in node.children:
            self.print(child, indent + 1)

    def print_flat(self):
        for b in self.blocks:
            print(b)
