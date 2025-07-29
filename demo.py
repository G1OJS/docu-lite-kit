from pybonsai import doc_object_tree

#doctree = doc_object_tree("py_file_for_demo.py")
#doctree.print()

doctree = doc_object_tree("py_file_for_demo_no_root_docstring.py")
doctree.print()

