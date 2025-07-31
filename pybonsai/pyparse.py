"""
    file-level docstring
"""

class files:
    def __init__(self, filepath):
        self.lines = ""
        self.lines = self._read(filepath)
        
    def _read(self, filepath):
        with open(filepath) as f:
            return f.readlines()

class pbBlock:
    def __init__(self, first_line_number, doclines, pattern):
        self.first_line_number = first_line_number
        self.last_line_number = len(doclines) - 1
        self.indent_spaces = 10000
        self.indent_level = 0
        self.pattern = pattern
        self.signature = ""
        self.icon = ""

        line = doclines[self.first_line_number].rstrip()
        if(len(line.strip()) != 0):
            self.indent_spaces = len(line) - len(line.lstrip())

    # may be much easier to mod this to search forwards from first line, return any docstring and then other content
    # rather than fill in all the end line numbers globally as currently
    def get_content(self, doclines):
        return doclines[self.first_line_number:self.last_line_number+1]
        
class pbBlocks:
    """
        Uses the docu-lite method of reading all lines sequentially to generate a flat list of blocks where
        docstring and non-docstring content are counted as blocks alongside pattern blocks.
    """
    def __init__(self, doclines, patterns = ['def', 'class']):
        self.patterns = patterns
        self.blocks = []

        # get all blocks in a flat list
        in_docstring = False
        for line_no, line in enumerate(doclines):
            pattern_found = self._has_pattern(line)
            if(pattern_found):
                self.blocks.append(pbBlock(line_no, doclines, pattern_found))
            else:
                docstring_closure = self._has_docstring_delimeter(line)
                if(docstring_closure):
                    if(not in_docstring):
                        self.blocks.append(pbBlock(line_no, doclines, 'docstring'))
                        in_docstring = not self._has_docstring_delimeter(line.replace(docstring_closure,'',1))
                    else:
                        in_docstring = False
                        self.blocks[-1].last_line_number = line_no
     
        # set object signatures
        for block in self.blocks[1:]:
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
                block.signature = "".join(first_line.split()[1:])

        # tell each object what its indent level is within the document
        indents =[0]
        for pbB in self.blocks:
            if(pbB.indent_spaces > indents[-1]):
                indents.append(pbB.indent_spaces)
            pbB.indent_level = indents.index(pbB.indent_spaces)

        # find and set last line numbers
        for block_number, block in enumerate(self.blocks[1:]):
            bn = block_number
            while(bn>0):
                if(block.indent_level <= self.blocks[bn].indent_level):
                    potential_last_line_number = block.first_line_number - 1
                    if(potential_last_line_number < self.blocks[bn].last_line_number):
                        self.blocks[bn].last_line_number = potential_last_line_number
                bn -= 1

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
        doc_blocks = pbBlocks(pylines, ['def', 'class']).blocks
        first_line_info = {pb.first_line_number: f"{'>' * pb.indent_level} {pb.first_line_number + 1}-{pb.last_line_number + 1}: {pb.pattern} {pb.signature}" for pb in doc_blocks}
        print(f"{'Line':<5} | {'Python source':<25} | {'Block list':<25}")
        print("-" * 89)
        for lno, line in enumerate(pylines):
            src = line.rstrip()
            block_info = first_line_info[lno] if lno in first_line_info else f"src: {src}"
            print(f"{lno+1:<5} | {src[:25]:<25} | {block_info:<25}")

    def _fString(self, pbBlock):
        indent_str = ">" * pbBlock.indent_spaces
        return f"{indent_str} {pbBlock.pattern} {pbBlock.signature}"

class pbBrowser:
    """
        Generates HTML for expandable node list representing the document tree
    """
    def __init__(self, pyfile):
        self.pylines = files(pyfile).lines
        self.blocks = pbBlocks(self.pylines, ['def', 'class']).blocks
        style_sheet_file = "docu-lite-style.css"
        self.html =  f"<!DOCTYPE html><html lang='en'>\n<head>\n<title></title>"
        self.html += f"<link rel='stylesheet' href='./{style_sheet_file}' />"
        prev_indent = 0
        for pbB in self.blocks:
            self.html += self._signature_html(pbB.pattern, pbB.signature, True)
            self.html += self._content_html(pbB.pattern, pbB.get_content(self.pylines))
            self.html += self._close_details(pbB.indent_level-prev_indent+1 )
            prev_indent = pbB.indent_level
        soft_string = ''
        self.html += f"\n<br><br><span style = 'font-size:0.8em;color:#666;border-top:1px solid #ddd; "
        self.html += f"font-style:italic'>Made with {soft_string}</span></body>\n"

    
    def _signature_html(self, obj_type, obj_signature, open_details = True):
        htm = "<details><summary>" if open_details else "<div>"
        htm += f"<span class ='{obj_type} {'signature'}'>{obj_signature}</span>"
        htm += "</summary>" if open_details else "</div>"
        return htm + "\n"

    def _content_html(self, object_type, content_lines):
        import html
        htm = f"<pre class ='{object_type} content'>"
        for i, line in enumerate(content_lines):
            if(i==0 and len(line.strip()) ==0):
                continue
            htm += f"{html.escape(line)}"
        htm += "</pre>\n"
        return htm

    def _close_details(self, n_times):
        if(n_times <1):
            return ""
        return "</details>\n" * n_times

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
   # t = test("./pyparse.py")
    output_html_file = "test.html"
    htm = pbBrowser(r"C:\Users\drala\Documents\Projects\GitHub\NECBOL\necbol\modeller.py").html
    with open(output_html_file, "w", encoding="utf-8") as f:
        f.write(htm)
            
if __name__ == "__main__":
    main()
