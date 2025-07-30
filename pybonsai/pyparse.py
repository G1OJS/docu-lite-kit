class pbNode:
    def __init__(self, first_line_number, doclines):
        self.indent = self._line_indent(doclines[first_line_number])
        self.signature = doclines[first_line_number].split()
        self.first_line_number = first_line_number
        self.docstring = ""
        self.twigs = []

        docstring_lines = None
        line_no = first_line_number - 1
        while (line_no  < len(doclines) - 1):
            line_no += 1
            if(docstring_lines is None):
                docstring_delimeter = self._has_docstring_delimeter(doclines[line_no])
                if(docstring_delimeter):        
                    docstring_lines = []
                    doclines[line_no] = doclines[line_no].replace(docstring_delimeter,'',1)
            if(docstring_lines is not None):
                docstring_lines.append(doclines[line_no])
                if(docstring_delimeter in doclines[line_no]):
                    self.docstring = [line.rstrip().replace(docstring_delimeter, '').replace('\n','') for line in docstring_lines]
                    self.docstring = [line for cnt,line in enumerate(self.docstring) if line.strip() or (cnt !=0 and cnt != len(self.docstring)-1)]
                    docstring_lines = None
            if(line_no < len(doclines) -1):
                if(doclines[line_no+1].rstrip().endswith(':')):
                    break
            
    def _line_indent(self, line):
        line = line.rstrip()
        if(len(line.strip()) == 0):
            return 1000
        else:
            return len(line) - len(line.lstrip())

    def _has_docstring_delimeter(self,line):
        for delim in ['"""',"'''"]:
            if(delim in line):
                return delim
        return False

    def _format_docstring(self, docstring_lines):
        lines = [line.rstrip().replace(docstring_delimeter, '') for line in docstring_lines]

class pbTree:

    def __init__(self,filepath):
        with open(filepath) as f:
            doclines = f.readlines()
        self.pbRoot = pbNode(0, doclines)
        self.pbNodes = [self.pbRoot]
        ancestry = [self.pbRoot]
        while (self.pbNodes[-1].first_line_number < len(doclines) -1):
            self.pbNodes.append(pbNode(self.pbNodes[-1].first_line_number+1, doclines))
            while ancestry and self.pbNodes[-1].indent < ancestry[-1].indent:
                ancestry.pop()
            ancestry[-1].twigs.append(self.pbNodes[-1])
            ancestry.append(self.pbNodes[-1])
            


