import json
import re


with open('registry.json') as data_file:
    data = json.load(data_file)

package_list = sorted(data['packages'], key=lambda k: k['name'].lower()) 

stable_dict = {False: 'No', True: 'Yes'}

row = ('\\href{{{0}}}{{{1}}} & {2} & '
      '\\href{{https://pypi.python.org/pypi/{3}}}{{{3}}} & {4} \\\\\n')

with open("registry.tex", "w") as f1, open("registry_prov.tex", "w") as f2:
    for item in package_list:
        if not item['provisional']:
            f1.write(row.format(item["repo_url"], item["name"],
                                stable_dict[item["stable"]], item['pypi_name'],
                                re.sub(' <.*?>', '', item["maintainer"])))
        else:
            f2.write(row.format(item["repo_url"], 
                                re.sub('_', '\_', item["name"]),
                                stable_dict[item["stable"]], item['pypi_name'],
                                re.sub(' <.*?>', '', item["maintainer"])))
