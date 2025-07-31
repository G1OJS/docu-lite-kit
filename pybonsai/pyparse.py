class files:
    def __init__(self, filepath):
        self.lines = ""
        self.lines = self._read(filepath)
        
    def _read(self, filepath):
        with open(filepath) as f:
            return f.readlines()

class pbNode:
    def __init__(self, first_line_number, line, object_pattern, doc_ord):
        self.first_line_number = first_line_number
        self.line_indent = self._line_indent(line)
        self.object_pattern = object_pattern
        self.last_line_number = 0
        self.doc_ord = doc_ord
        self.twigs = []
        
    def _line_indent(self, line):
        line = line.rstrip()
        if(len(line.strip()) == 0):
            return 1000
        else:
            return len(line) - len(line.lstrip())

class pbList:
    """
        Uses the docu-lite method of reading all lines sequentially to generate a flat list of objects where
        docstring and non-docstring content are counted as objects alongside object_pattern objects. The purpose of
        doing this is to ensure that nothing is missed, and this list is organised into a tree later
    """
    def __init__(self, doc_objects, doclines, object_patterns = ['def', 'class']):
        self.object_patterns = object_patterns
        self.objects = doc_objects
        ancestry = pbNode(0,"","",0)
        in_docstring = False
        for line_no, line in enumerate(doclines):
            object_pattern_found = self._has_object_pattern(line)
            if (object_pattern_found):
                self.objects.append(pbNode(line_no, line, object_pattern_found, len(self.objects)))
            docstring_closure = self._has_docstring_delimeter(line)
            if(docstring_closure):
                if(not in_docstring):
                    self.objects.append(pbNode(line_no, line, 'docstring',  len(self.objects)))
                    in_docstring = True
                else:
                    self.objects[-1].last_line_number = line_no
                    in_docstring = False

    def _has_object_pattern(self, line):
        l = line.strip()
        for pat in self.object_patterns:
            if (l.startswith(pat) and line.endswith(':\n')):
                return line.split()[0]
        return False

    def _has_docstring_delimeter(self,line):
        for delim in ['"""',"'''"]:
            if(line.strip().startswith(delim) or line.strip().endswith(delim)):
                return delim
        return False


class pbTree:
    """
        Uses pbList to get flat list if one doesn't already exist, and packages this into a tree structure based
        on the indent level of each object
    """
    def __init__(self, doc_objects):
        self.objects = doc_objects
        self.root = pbNode(0,"","",0)
        ancestry = [self.root]
        to_remove = []
        # this loop needs work - it's not appending twigs to the twigs?
        for pbN in self.objects:
            if(pbN.line_indent > ancestry[-1].line_indent):
                ancestry[-1].twigs.append(pbN)
                to_remove.append(pbNode)
        for pbN in to_remove:
            self.objects.remove(pbN)

    def print_pb(pbNode):
        # is this print loop correct?
        indent_str = "    " * pbNode.line_indent + "|"
        print(f"{indent_str} line {pbNode.first_line_number + 1} info: {pbNode.object_pattern}'\n")
        for pbTwig in pbNode.twigs:
            print_pb(pbTwig)

class test:
    # where to set last line number - naturally when making tree?
    def __init__(self, pyfile):
        doc_objects = []
        pylines = files(pyfile).lines
        doc_objects = pbList(doc_objects, pylines, ['def','class']).objects
        scopelist = []
        for pbNode in doc_objects:
            scopelist.append((pbNode.first_line_number, pbNode.last_line_number, pbNode.object_pattern))            
        for lno, line in enumerate(pylines):
            dline = f"{lno:4g}: {line.strip()[0:20]:<20}| "
            for s in scopelist:
                fl,ll,pat = s
                if(lno==fl):
                    dline += pat + " ->" + str(ll)
            print(dline) 
            indent_str = ">" * pbNode.line_indent + "|"

        tree = pbTree(doc_objects)
        pbTree.print_pb(tree.root)





class pbBrowser:
    """
        Generates HTML for expandable node list representing the document tree
    """


    
    def _format_docstring(self, docstring_lines):
        lines = [line.rstrip().replace(docstring_delimeter, '') for line in docstring_lines]


class pbUserguide:
    """
        Generates HTML for user guide
    """
    def dummy():
        a=1


class pbListAPI:
    """
        Generates text list representing API functions only
    """
    def dummy2():
        a=1


t = test("./pyparse.py")
