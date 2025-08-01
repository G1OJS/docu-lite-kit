"""
    Pyparse
    Works well but misses file-level docstring
"""

class pbBlock:
    def __init__(self, first_line_number, doclines, pattern_list):
        self.pattern_list = pattern_list
        self.first_line_text = doclines[first_line_number]
        self.indent_spaces = len(self.first_line_text) - len(self.first_line_text.lstrip())
        self.indent_level = 0
        self.signature = ""
        self.icon = ""
        self.docstring = ""
        self.body = ""
        # if no pattern on first line, exit early with self.pattern = False
        self.pattern = self._has_pattern(self.first_line_text)
        if(self.pattern == False):
            return

        self._fill_signature(doclines, first_line_number)
        self._fill_content(doclines, first_line_number)

    def _has_pattern(self, line):
        l = line.strip()
        for pat in self.pattern_list:
            if (l.startswith(pat) and line.endswith(':\n')):
                return line.split()[0]
        return False

    def _fill_signature(self, doclines, first_line_number):
        if("(" in self.first_line_text):
            lno = first_line_number
            sigtext = ""
            while not (')' in sigtext):
                sigtext += doclines[lno].strip()
                lno += 1
            self.signature =  sigtext[:sigtext.find(')')+1].replace(self.pattern,'')
        else:
            self.signature = "".join(self.first_line_text.split()[1:])

    def _fill_content(self, doclines, first_line_number):
        content_start = first_line_number + 1
        content_end = len(doclines)-1
        docstring_start = -1
        docstring_end = -1
        line_no = first_line_number + 1
        while( line_no <= content_end):
            line  = doclines[line_no].replace("'''",'"""').strip()
            if(line.startswith('"""')):
                if(docstring_start<0):
                    docstring_start = line_no
                else:
                    docstring_end = line_no
            if(line.replace('"""','').endswith('"""')):
                docstring_end = line_no
            if(self._has_pattern(doclines[line_no])):
                content_end = line_no -1
            line_no +=1
        if(docstring_start>=0):
            self.docstring = doclines[docstring_start:docstring_end + 1]
            content_start = docstring_end + 1
        self.body = doclines[content_start:content_end]
        
class pbBlocks:
    def __init__(self, doclines, patterns):
        self.blocks = []

        # get all blocks in a flat list
        for line_no, line in enumerate(doclines):
            block = pbBlock(line_no, doclines, patterns)
            if(block.pattern):
                self.blocks.append(block)
                print(f"{line_no} {block.first_line_text}")

        # tell each object what its indent level is within the document
        indents =[0]
        for pbB in self.blocks:
            if(pbB.indent_spaces > indents[-1]):
                indents.append(pbB.indent_spaces)
            pbB.indent_level = indents.index(pbB.indent_spaces)

class pbBrowser:
    """
        Generates HTML for expandable node list representing the document tree
    """
    def __init__(self, blocks):
        style_sheet_file = "docu-lite-style.css"
        self.html =  f"<!DOCTYPE html><html lang='en'>\n<head>\n<title></title>"
        self.html += f"<link rel='stylesheet' href='./{style_sheet_file}' />"
        prev_indent = 0
        count = 0
        for pbB in blocks:
            self.html += self._signature_html(pbB.pattern, pbB.signature, True)
            if(pbB.docstring != ""):
                self.html += self._content_html('docstring', pbB.docstring)   
            self.html += self._content_html(pbB.pattern, pbB.body)
            self.html += self._close_details(pbB.indent_level-prev_indent+1 )
            prev_indent = pbB.indent_level
            count +=1
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


def main():
    input_file = r"C:\Users\drala\Documents\Projects\GitHub\NECBOL\necbol\modeller.py"
    output_html_file = "test.html"

    with open(input_file) as f:
        lines = f.readlines()
    blocks = pbBlocks(lines, ['def', 'class']).blocks
    
    htm = pbBrowser(blocks).html
    with open(output_html_file, "w", encoding="utf-8") as f:
        f.write(htm)
            
if __name__ == "__main__":
    main()
