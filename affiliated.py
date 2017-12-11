import json
import re


with open('registry.json') as data_file:
    data = json.load(data_file)

with open('bib_mapping.json') as data_file:
    bib_map = json.load(data_file)

package_list = sorted(data['packages'], key=lambda k: k['name'].lower())

stable_dict = {False: 'No', True: 'Yes'}

row = ('\\href{{{0}}}{{{1}}} & {2} & '
       '\\href{{https://pypi.python.org/pypi/{3}}}{{{3}}} & {4} & {5} \\\\\n')

with open("registry.tex", "w") as f1, open("registry_prov.tex", "w") as f2:
    for item in package_list:

        citealt = ("\\citealt{{{0}}}".format(bib_map[item["name"]])
                   if item["name"] in bib_map
                   else "")

        if not item['provisional']:
            f1.write(row.format(item["repo_url"], item["name"],
                                stable_dict[item["stable"]], item['pypi_name'],
                                re.sub(' <.*?>', '', item["maintainer"]),
                                citealt
                               ))
        else:
            f2.write(row.format(item["repo_url"], 
                                re.sub('_', '\_', item["name"]),
                                stable_dict[item["stable"]], item['pypi_name'],
                                re.sub(' <.*?>', '', item["maintainer"]),
                                citealt
                               ))
