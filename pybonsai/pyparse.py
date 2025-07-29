class block:
    
    def __init__(self, first_line, block_type, block_definition, block_indent, block_docstring):
        self.first_line = first_line
        self.type = block_type
        self.definition = block_definition
        self.indent = block_indent
        self.docstring = block_docstring
        self.children = []
        
    def __repr__(self):
        return f"<line {self.first_line}: {self.type} {self.definition} , indent={self.indent}, docstring = {self.docstring}>"

class doc_object_tree:
    def __init__(self, filepath):
        self.filepath = filepath
        self.lines = self._read_file(filepath)
        self.root = self._build_doc_tree()

    def _read_file(self, path):
        with open(path) as f:
            return f.readlines()

    def _get_docstring(self, delimeter, lines, i, block_indent):
        docstring_lines = None
        j = i
        while j < len(lines)-1:
            j += 1
            if (len(lines[j]) - len(lines[j].lstrip()) <= block_indent):
                break
            if(delimeter in lines[j] and docstring_lines is None):
                docstring_lines = []
                lines[j] = lines[j].replace(delimeter,'',1)
            if(docstring_lines is not None):
                docstring_lines.append(lines[j])
                if(delimeter in lines[j]):
                    return " ".join(docstring_lines).replace(delimeter,'')
        return ""

    def _build_doc_tree(self):
        # Find all 'blocks' and record them as a list of block objects
        blocks = []
        for i, line in enumerate(self.lines):
            if not line.strip().endswith(":"):
                continue
            if line.strip().startswith("#") or line.strip().startswith("@"):
                continue
            # we are now on the first line of a valid block of some kind
            line_words = line.split()
            block_indent = len(line) - len(line.lstrip())
            for delim in ['"""', "'''"]:
                docstring = self._get_docstring(delim, self.lines, i, block_indent)
                if(docstring !=""):
                    break
            blocks.append(block(i, line_words[0], line_words[1:], block_indent, docstring))
        # Find parentage by walking back up the indentation levels
        root = block(-1, 'module', ['<root>'], -1, "")
        stack = [root]
        for b in blocks:
            while stack and b.indent <= stack[-1].indent:
                stack.pop()
            stack[-1].children.append(b)
            stack.append(b)
        return root

    def print(self, node = None, indent=0):
        if node is None:
            node = self.root
        print(node)
        for child in node.children:
            self.print(child, indent + 1)




