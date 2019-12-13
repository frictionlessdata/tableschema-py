import re
import sys
import pdoc

# Module API

def generate_reference(package):
    reference = ''
    with open('%s/__init__.py' % package) as file:
        for line in file:
            match = re.match(r'from \.(\w+) import (\w+)', line)
            if match:
                module, object_name = match.groups()
                def docfilter(object):
                    object.__class__.mro = lambda self: []
                    object.__class__.subclasses = lambda self: []
                    return object.name == object_name
                path = '%s.%s' % (package, module)
                modules = [pdoc.Module(pdoc.import_module(path), docfilter=docfilter)]
                doctext = pdoc._render_template('/pdf.mako', modules=modules)
                doctext = re.sub("\n\n\n+", "\n\n", doctext)
                skip = True
                for docline in doctext.split("\n"):
                    if docline.startswith('--'):
                        skip = True
                        continue
                    if docline.startswith('## '):
                        skip = False
                        continue
                    if skip:
                        continue
                    docline = re.sub(r'{.*}', '', docline)
                    reference += "%s\n" % docline
    return reference


def generate_readme(reference):
    readme = ''
    replace = False
    with open('README.md') as file:
        for docline in file:
            if docline.startswith('## Contributing'):
                replace = False
                readme += reference
            if replace:
                continue
            if docline.startswith('## Reference'):
                replace = True
            readme += docline
    return readme


# Main

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: python readme.py package')
    reference = generate_reference(sys.argv[1])
    readme = generate_readme(reference)
    print(readme)
