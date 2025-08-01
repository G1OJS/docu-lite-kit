
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
