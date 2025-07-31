class files:
    def __init__(self, filepath):
        self.lines = ""
        self.lines = self._read(filepath)
        
    def _read(self, filepath):
        with open(filepath) as f:
            return f.readlines()

class pbNode:
    def __init__(self, first_line_number, doclines, pattern):
        self.first_line_number = first_line_number
        self.line_indent = 10000
        self.pattern = pattern
        self.signature = ""
        self.last_line_number = 0
        self.twigs = []

        line = doclines[self.first_line_number].rstrip()
        if(len(line.strip()) != 0):
            self.line_indent = len(line) - len(line.lstrip())

class pbTree:
    """
        Uses the docu-lite method of reading all lines sequentially to generate a flat list of blocks where
        docstring and non-docstring content are counted as blocks alongside pattern blocks. The purpose of
        doing this is to ensure that nothing is missed, and this list is organised into a tree later
    """
    def __init__(self, doclines, patterns = ['def', 'class']):
        self.patterns = patterns
        self.block_list = []
        self.root = pbNode(0, "root()", "root")
        self.block_tree =[self.root]

        # get all blocks in a flat list
        in_docstring = False
        for line_no, line in enumerate(doclines):
            pattern_found = self._has_pattern(line)
            if(pattern_found):
                self.block_list.append(pbNode(line_no, doclines, pattern_found))
            else:
                docstring_closure = self._has_docstring_delimeter(line)
                if(docstring_closure):
                    if(not in_docstring):
                        self.block_list.append(pbNode(line_no, doclines, 'docstring'))
                        in_docstring = not self._has_docstring_delimeter(line.replace(docstring_closure,'',1))
                    else:
                        in_docstring = False
     
        # set object signatures
        for block in self.block_list[1:]:
            if(block.pattern == 'docstring'):
                continue
            first_line = doclines[block.first_line_number]
            if("(" in first_line):
                lno = block.first_line_number
                sigtext = ""
                while not (')' in sigtext):
                    sigtext += doclines[lno].strip()
                    lno += 1
                block.signature = sigtext[:sigtext.find(')')+1].replace(block.pattern,'')
            else:
                block.signature = first_line.split()[1:]

        # make the document tree
        ancestry = [self.root]
        for pbN in self.block_list:
            # Find parent by comparing indentation
            while len(ancestry)>1 and pbN.line_indent < ancestry[-1].line_indent:
                ancestry.pop()
            ancestry[-1].twigs.append(pbN)
            ancestry.append(pbN)

    def _has_pattern(self, line):
        l = line.strip()
        for pat in self.patterns:
            if (l.startswith(pat) and line.endswith(':\n')):
                return line.split()[0]
        return False

    def _has_docstring_delimeter(self, line):
        """ finds lines with three quotes at the beginning and/or end of a line """
        for delim in ['"""',"'''"]:
            if(line.strip().startswith(delim) or line.strip().endswith(delim)):
                return delim
        return False


class test:
    def __init__(self, pyfile):
        pylines = files(pyfile).lines
        graphs = pbTree(pylines, ['def', 'class'])
        doc_blocks = graphs.block_list

        list_lines = self._pbList_lines(doc_blocks)
        tree_lines = self._pbTree_lines(graphs.root)

        print(f"{'Line':<5} | {'Python source':<25} | {'Block list':<25} | {'Block tree':<25}")
        print("-" * 89)
        for lno, line in enumerate(pylines):
            src = line.rstrip()
            block_info = list_lines[lno] if lno in list_lines else f"src: {src}"
            tree_info = tree_lines[lno] if lno in tree_lines else f"src: {src}"
            print(f"{lno+1:<5} | {src[:25]:<25} | {block_info[:25]:<25} | {tree_info[:25]:<25}")

    def _pbList_lines(self, doc_blocks):
        output_lines = {}
        for pbNode in doc_blocks:
            output_lines[pbNode.first_line_number] = self._fString(pbNode)
        return output_lines

    def _pbTree_lines(self, pbNode, output_lines=None):
        output_lines = {} if output_lines is None else output_lines
        if pbNode.pattern:
            output_lines[pbNode.first_line_number] =  self._fString(pbNode)
        for twig in pbNode.twigs:
            self._pbTree_lines(twig, output_lines)

        return output_lines

    def _fString(self, pbNode):
        indent_str = ">" * pbNode.line_indent
        return f"{indent_str} {pbNode.pattern} {pbNode.signature}"



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

def main():
    t = test("./pyparse.py")


if __name__ == "__main__":
    main()
