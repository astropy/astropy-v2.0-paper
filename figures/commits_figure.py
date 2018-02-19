"""
This is a subset of the functionality in astropy/astropy-tools in the
visualizations_demographics subdirectory.
"""

from datetime import datetime
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def generate_commit_stats_file(filename='gitlogstats.csv', overwrite=False,
                               astropy_path=None):
    """
    Running this will generate a file in the current directory that stores the
    statistics to make generating lots of plots easier.  Delete the file or
    set `overwrite` to True to always re-generate the statistics.
    """
    if os.path.isfile(filename) and not overwrite:
        df = pd.read_csv(filename)

    else:
        import subprocess
        import tempfile

        # cmd = 'git log --use-mailmap --no-merges --format=format:\"%H\",\"%aI\",\"%aN\",\"%cN\"'.split()
        cmd = 'git log --use-mailmap --format=format:\"%H\",\"%aI\",\"%aN\",\"%cN\"'.split()
        output = subprocess.check_output(cmd, cwd=astropy_path)
        output = output.decode('utf-8')

        with tempfile.NamedTemporaryFile(mode='w+') as f:
            f.write(output)
            f.seek(0)
            df = pd.read_csv(f.name, names=['commit', 'date', 'author',
                                            'committer'])

        print('writing df to file {0}'.format(filename))
        df.to_csv(filename)

    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index(df['date'])

    return df


def commits_plot(astropy_path, ax=None, **hist_kw):

    df = generate_commit_stats_file(astropy_path=astropy_path)
    n_commits = df.groupby('author').size()

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6,5))

    _bins = np.logspace(0, 3.5, 16)
    hist_kw.setdefault('histtype', 'stepfilled')
    ax.hist(n_commits, bins=_bins, **hist_kw)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('number of commits')
    ax.set_ylabel('number of committers')

    ax.plot(_bins, 150*_bins**-0.5, marker='')

    xticks = [1, 10, 100, 1000]
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(tick) for tick in xticks])

    yticks = [1, 10, 100]
    ax.set_yticks(xticks)
    ax.set_yticklabels([str(tick) for tick in yticks])

    ax.set_ylim(0.8, 200)
    ax.set_xlim(_bins.min(), _bins.max())

    ax.text(100, 20, r'$\propto N^{-0.5}$', fontsize=20)


def commits_vs_time(astropy_path, ax=None, **hist_kw):

    df = generate_commit_stats_file(astropy_path=astropy_path)
    # n_commits = df.groupby('date').size()

    date_bins = df.groupby(pd.TimeGrouper('D'))
    commits_per_day = date_bins.size()

    if ax is None:
        fig, ax = plt.subplots(1, 1, figsize=(6,5))

    n_commits = np.cumsum(commits_per_day)
    ax.fill_between(n_commits.index, 0, np.array(n_commits))

    ax.set_xlabel('year')
    ax.set_ylabel('number of commits')

    ax.set_xlim(datetime(2011,6,1), datetime(2018,1,1))
    ax.set_ylim(0, 21000)


def contributors_vs_time(astropy_path, timegrouper_freq='M', ax=None):
    df = generate_commit_stats_file(astropy_path=astropy_path)
    groups = df.groupby(pd.TimeGrouper(freq=timegrouper_freq))
    agg = groups.agg({"author": lambda x: x.nunique()})

    if ax is None:
        fig, ax = plt.subplots(1, 1)

    ax.plot(agg.index, agg['author'], drawstyle='steps-mid', marker='')
    ax.set_xlabel('year')
    ax.set_ylabel('committers per month')
    ax.set_xlim(datetime(2011, 6, 1), datetime(2018, 1, 1))
    ax.set_ylim(0, 35)


if __name__ == "__main__":
    from os import path
    from argparse import ArgumentParser

    # Define parser object
    parser = ArgumentParser(description="")

    parser.add_argument('--astropy-path', dest='astropy_path',
                        required=True, type=str,
                        help='Path to the astropy core package repository.')

    args = parser.parse_args()

    astropy_path = path.abspath(path.expanduser(args.astropy_path))

    fig, axes = plt.subplots(1, 3, figsize=(15, 5.))
    commits_plot(astropy_path, ax=axes[0])
    commits_vs_time(astropy_path, ax=axes[1])
    contributors_vs_time(astropy_path, ax=axes[2])

    fig.tight_layout()
    fig.savefig('commits.pdf')
