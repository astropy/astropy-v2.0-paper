import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import hist

# generate some complicated data
rng = np.random.RandomState(0)
t = np.concatenate([-5 + 1.8 * rng.standard_cauchy(500),
                    -4 + 0.8 * rng.standard_cauchy(2000),
                    -1 + 0.3 * rng.standard_cauchy(500),
                    2 + 0.8 * rng.standard_cauchy(1000),
                    4 + 1.5 * rng.standard_cauchy(1000)])

# truncate to a reasonable range
t = t[(t > -15) & (t < 15)]

# draw histograms with two different bin widths
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
hist_kwds = dict(histtype='stepfilled', alpha=0.5, normed=True)

fig.subplots_adjust(left=0.1, right=0.95, bottom=0.15)

ax[0].hist(t, **hist_kwds)
ax[0].set(xlabel='t', ylabel='P(t)')
ax[0].set_title('plt.hist()', fontdict=dict(family='monospace'))

hist(t, bins='blocks', ax=ax[1], **hist_kwds)
ax[1].set_xlabel('t')
ax[1].set_ylabel('P(t)')
ax[1].set_title('hist(t, bins="blocks")', fontdict=dict(family='monospace'))

plt.savefig('bayesian_blocks_hist.pdf')
