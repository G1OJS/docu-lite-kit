"""
    Compiles a flat list of blocks of type 'class', 'def' and 'docstring'
    Where class and def blocks include strings representing internal docstrincs and body content
"""
class pbBlock:
    def __init__(self, first_line_number, doclines, pattern_list):
        self.first_line_number = first_line_number
        self.pattern_list = pattern_list
        self.first_line_text = doclines[first_line_number]
        self.indent_spaces = len(self.first_line_text) - len(self.first_line_text.lstrip())
        self.indent_level = 0
        self.signature = ""
        self.icon = ""
        self.docstring = ""
        self.body = ""
        # if no pattern on first line, exit early with self.pattern = False
        if(pattern_list != 'docstring'):
            self.pattern = self._has_pattern(self.first_line_text)
            if(self.pattern == False):
                return
        else:
            self.pattern = 'docstring'

        self._fill_signature(doclines, first_line_number)
        self._fill_content(doclines, first_line_number)

    def to_dict(self):
        return {
            "type": self.pattern,
            "line_number": self.first_line_number,
            "signature": self.signature.strip(),
            "indent_level": self.indent_level,
            "docstring": [l.strip('\n') for l in self.docstring] if self.docstring else [],
            "body": [l.strip('\n') for l in self.body] if self.body else []
        }

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
            self.signature =  sigtext[:sigtext.find(')')+1].replace(self.pattern,'').lstrip()
        else:
            self.signature = "".join(self.first_line_text.split()[1:])

    def _fill_content(self, doclines, first_line_number):
        content_start = first_line_number + 1
        content_end = len(doclines)-1
        docstring_start = -1
        docstring_end = -1
        line_no = first_line_number + 1 if self.pattern !='docstring' else first_line_number
        while( line_no <= content_end):
            line  = doclines[line_no].replace("'''",'"""').strip()
            if('"""' in line):
                if(docstring_start<0):
                    docstring_start = line_no
                else:
                    docstring_end = line_no
            if('"""' in line.replace('"""','',1)):
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
            elif len(self.blocks) == 0 and '"""' in line.replace("'''",'"""'):
                self.blocks.append(pbBlock(line_no, doclines, 'docstring'))
                
        # tell each object what its indent level is within the document
        indents =[0]
        for pbB in self.blocks:
            if(pbB.indent_spaces > indents[-1]):
                indents.append(pbB.indent_spaces)
            pbB.indent_level = indents.index(pbB.indent_spaces)

class pbPrint:
    def __init__(self, blocks, pattern_list = ['def', 'class']):
        for block in blocks:
            if(block.pattern not in pattern_list):
                continue
            print(f"{block.first_line_number+1}: {block.pattern} {block.signature}")
            if('docstring' in pattern_list and block.docstring !=""):
                for l in block.docstring:
                    print(f"{l.replace('\n','')}")
            if('body' in pattern_list and block.body !=""):
                for l in block.body:
                    print(f"{l.replace('\n','')}")

import json

def main():
    input_file = r"C:\Users\drala\Documents\Projects\GitHub\NECBOL\necbol\modeller.py"
    output_json_file = "parsed_blocks.json"

    with open(input_file) as f:
        lines = f.readlines()

    blocks = pbBlocks(lines, ['def', 'class']).blocks
    pbPrint(blocks, ['def', 'class', 'docstring'])

    block_dicts = [b.to_dict() for b in blocks]
    
    with open(output_json_file, 'w') as f:
        json.dump(block_dicts, f, indent=2)

            
if __name__ == "__main__":
    main()
