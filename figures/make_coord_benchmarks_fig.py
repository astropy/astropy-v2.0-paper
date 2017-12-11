"""
Originally contributed by @dpshelio
"""

import matplotlib.pyplot as plt
import numpy as np

cc = [[0, 0], [0, 0]]
ap = [[0.218, 0.196], [0.249, 0.056]]  # astropy - palpy
ae = [[0.459, 0.458], [0.860, 0.231]]  # astropy - pyephem
pe = [[0.563, 0.570], [1.012, 0.253]]  # palpy - pyephem
data = {'astropy-astropy':   cc,
        'astropy-kapteyn':   cc, 'kapteyn-astropy':  cc,
        'astropy-pytpm':     cc, 'pytpm-astropy':    cc,
        'astropy-palpy':     ap, 'palpy-astropy':    ap,
        'astropy-pyast':     ap, 'pyast-astropy':    ap,
        'astropy-pyslalib':  ap, 'pyslalib-astropy': ap,
        'astropy-pyephem':   ae, 'pyephem-astropy':  ae,
        'kapteyn-kapteyn':   cc,
        'kapteyn-pytpm':     cc, 'pytpm-kapteyn':    cc,
        'kapteyn-palpy':     ap, 'palpy-kapteyn':    ap,
        'kapteyn-pyast':     ap, 'pyast-kapteyn':    ap,
        'kapteyn-pyslalib':  ap, 'pyslalib-kapteyn': ap,
        'kapteyn-pyephem':   ae, 'pyephem-kapteyn':  ae,
        'pytpm-pytpm':       cc,
        'pytpm-palpy':       ap, 'palpy-pytpm':      ap,
        'pytpm-pyast':       ap, 'pyast-pytpm':      ap,
        'pytpm-pyslalib':    ap, 'pyslalib-pytpm':   ap,
        'pytpm-pyephem':     ae, 'pyephem-pytpm':    ae,
        'palpy-palpy':       cc,
        'palpy-pyast':       cc, 'pyast-palpy':      cc,
        'palpy-pyslalib':    cc, 'pyslalib-palpy':   cc,
        'palpy-pyephem':     pe, 'pyephem-palpy':    pe,
        'pyast-pyast':       cc,
        'pyast-pyslalib':    cc, 'pyslalib-pyast':   cc,
        'pyast-pyephem':     pe, 'pyephem-pyast':    pe,
        'pyslalib-pyslalib': cc,
        'pyslalib-pyephem':  pe, 'pyephem-pyslalib': pe,
        'pyephem-pyephem':   cc}

names = ['astropy', 'kapteyn', 'pytpm', 'palpy', 'pyast', 'pyslalib', 'pyephem']
n = len(names)

# Fill a single 2D array with the data to visualize
M = np.zeros((2*n, 2*n))
for i in range(n):
    for j in range(n):
        if 2*i < 2*j:
            M[2*j:2*j+2, 2*i:2*i+2] = np.nan
        else:
            M[2*j:2*j+2, 2*i:2*i+2] = np.array(data["{}-{}".format(names[j], names[i])])


fig, ax = plt.subplots(1, 1, figsize=(7.5,6))

c = ax.imshow(M, cmap='YlOrBr', zorder=1)

maj_ticks = np.arange(0, 2*n, 2) + 0.5

ax.set_xticks(maj_ticks)
ax.set_yticks(maj_ticks)
ax.set_xticklabels(names, fontsize=12)
ax.set_yticklabels(names, fontsize=12)
ax.set_xlim(2*n-0.5, -0.5)

ax.xaxis.tick_top()

ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)

grid_style = dict(marker='', linewidth=1, zorder=8)
for i in range(-1, 2*n+1, 2):
    ax.plot([i-1.5, 2*n], [i+0.5, i+0.5], color='#333333', alpha=0.5,
            **grid_style)
    if i < 2*n-1:
        ax.plot([i+0.5, i+0.5], [-0.5, i+2.5], color='#333333', alpha=0.5,
                **grid_style)

for i in range(0, 2*n):
    ax.plot([np.ceil(i-1.5)+0.5, 2*n], [i+0.5, i+0.5], color='#888888', alpha=0.25,
            **grid_style)
    if i < 2*n-1:
        ax.plot([i+0.5, i+0.5], [-0.5, np.floor(i+2.5)-0.5], color='#888888', alpha=0.25,
                **grid_style)

fig.colorbar(c)
fig.savefig('coordinates-benchmark.pdf')
