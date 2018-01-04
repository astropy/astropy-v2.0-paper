from astropy.wcs import WCS
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename

import numpy as np
import matplotlib.pyplot as plt

from astropy.visualization import (ManualInterval, SqrtStretch,
                                   ImageNormalize)


# filename = get_pkg_data_filename('galactic_center/gc_msx_e.fits')
filename = 'Cygnus-X_images_mosaics_I4_cygnus_2.4.fits'
hdu = fits.open(filename)[0]
wcs = WCS(hdu.header)

TICK_FONTSIZE=8
AXIS_FONTSIZE=10
AXIS_WEIGHT='bold'

import matplotlib.pyplot as plt

plt.rc('font', family='serif')
plt.rc('text', usetex=True)

ax = plt.axes([0.1, 0.1, 0.8, 0.8], projection=wcs, adjustable='datalim')

norm = ImageNormalize(hdu.data, interval=ManualInterval(22, 140),
                      stretch=SqrtStretch())

image = ax.imshow(hdu.data, origin='lower', cmap=plt.cm.plasma, norm=norm, aspect='equal')

ax.set_xlim(1700, 8200)
ax.set_ylim(3300, 8500)

ax.coords['ra'].set_ticks(color='black')
ax.coords['dec'].set_ticks(color='black')

ax.coords['ra'].set_ticklabel(size=TICK_FONTSIZE)
ax.coords['dec'].set_ticklabel(size=TICK_FONTSIZE)

ax.coords['ra'].set_ticks_position('b')
ax.coords['ra'].set_axislabel_position('b')
ax.coords['dec'].set_ticks_position('l')
ax.coords['dec'].set_axislabel_position('l')

ax.coords['ra'].set_major_formatter('hh:mm')
ax.coords['ra'].set_separator((r'$^h$', r'$^m$', r'$^s$'))

ax.coords['ra'].set_axislabel(r'\textbf{Right Ascension (FK5 J2000)}', size=AXIS_FONTSIZE, weight=AXIS_WEIGHT)
ax.coords['dec'].set_axislabel(r'\textbf{Declination (FK5 J2000)}', size=AXIS_FONTSIZE, weight=AXIS_WEIGHT)

ax.coords.grid(color='yellow', linestyle='solid', alpha=0.5)

overlay = ax.get_coords_overlay('galactic')

overlay[0].set_ticks(color='black')
overlay[1].set_ticks(color='black')

overlay[0].set_ticklabel(size=TICK_FONTSIZE)
overlay[1].set_ticklabel(size=TICK_FONTSIZE)

overlay[0].set_ticks_position('t')
overlay[0].set_axislabel_position('t')
overlay[1].set_ticks_position('r')
overlay[1].set_axislabel_position('r')

overlay[0].set_axislabel(r'\textbf{Galactic Longitude}', size=AXIS_FONTSIZE, weight=AXIS_WEIGHT)
overlay[1].set_axislabel(r'\textbf{Galactic Latitude}', size=AXIS_FONTSIZE, weight=AXIS_WEIGHT)

overlay.grid(color='white', linestyle='solid', alpha=0.5)

cax = plt.axes([0.1, 1.0, 0.8, 0.03])

plt.colorbar(image, orientation='horizontal', cax=cax)

cax.xaxis.set_ticks_position('top')
cax.xaxis.set_label_position('top')

for ticklabel in cax.xaxis.get_ticklabels():
    ticklabel.set_size(TICK_FONTSIZE - 1)

cax.set_xlabel(r'\textbf{Surface brightness (MJy/sr)}', size=AXIS_FONTSIZE-1, weight=AXIS_WEIGHT)

plt.savefig('cygnus_x_spitzer.pdf', dpi=200, bbox_inches='tight')
# plt.savefig('wcsaxes.png', dpi=144, bbox_inches='tight')
