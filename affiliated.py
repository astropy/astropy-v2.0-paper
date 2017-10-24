import json
import re


with open('registry.json') as data_file:
    data = json.load(data_file)

package_list = sorted(data['packages'], key=lambda k: k['name'].lower()) 

stable_dict = {False: 'No', True: 'Yes'}

with open("registry.tex", "w") as f:
    for item in package_list:
        if not item['provisional']:
            f.write('\\href{{{0}}}{{{1}}} & {2} & '
                    '\\href{{https://pypi.python.org/pypi/{3}}}{{{3}}} & {4} '
                    '\\\\\n'.format(item["repo_url"], item["name"],
                                    stable_dict[item["stable"]],
                                    item['pypi_name'],
                                    re.sub(' <.*?>', '', item["maintainer"])))
