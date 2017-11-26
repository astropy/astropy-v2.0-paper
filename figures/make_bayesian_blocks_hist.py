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
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
hist_kwds = dict(histtype='stepfilled', alpha=0.5, normed=True)

fig.subplots_adjust(left=0.05, right=0.98, bottom=0.15, wspace=0.25)

ax[0].hist(t, **hist_kwds)
ax[0].set(xlabel='t', ylabel='P(t)')
ax[0].set_title('plt.hist(t)', fontdict=dict(family='monospace'))

ax[1].hist(t, bins='auto', **hist_kwds)
ax[1].set(xlabel='t', ylabel='P(t)')
ax[1].set_title('plt.hist(t, bins="auto")', fontdict=dict(family='monospace'))

hist(t, bins='blocks', ax=ax[2], **hist_kwds)
ax[2].set_xlabel('t')
ax[2].set_ylabel('P(t)')
ax[2].set_title('hist(t, bins="blocks")', fontdict=dict(family='monospace'))

plt.savefig('bayesian_blocks_hist.pdf')
