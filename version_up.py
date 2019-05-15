import sys
import re
from jinja2 import Environment, FileSystemLoader


j2_env = Environment(loader=FileSystemLoader('.'))
semantic_version_regex = r'v?(\d+\.\d+\.\d+)'

if len(sys.argv) < 2:
    print("please provide a version number!")
    exit(-1)

version = sys.argv[1]
matchobj = re.match(semantic_version_regex, version)

if matchobj is None:
    print("Semnatic version does not seem to be followed (I check a narrow regex). Please check your version and try again")
    print("(See https://semver.org/ for details -- I only support basic x.y.z patterns, with optional (ignored) support for a preceeding 'v')")
    exit(-1)

version = matchobj.group(1)

template = j2_env.get_template('setup.py.j2')
content = template.render(version=version)

with open('setup.py', 'w') as fh:
    fh.write(content)
