from astropy.io import fits
import astropy.units as u
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization import make_lupton_rgb, astropy_mpl_style
from astropy.wcs import WCS
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)
plt.rcParams['font.family'] = plt.rcParamsDefault['font.family']
plt.rcParams['lines.marker'] = ''
from reproject import reproject_interp
import numpy as np

# load the data
# g_name = get_pkg_data_filename('visualization/reprojected_sdss_g.fits.bz2')
# r_name = get_pkg_data_filename('visualization/reprojected_sdss_r.fits.bz2')
# i_name = get_pkg_data_filename('visualization/reprojected_sdss_i.fits.bz2')
g_name = get_pkg_data_filename('hash/fb425fccf6326e34f4566711d8910364')
r_name = get_pkg_data_filename('hash/e6670142bc3c83936d84bd5d5d331d6a')
i_name = get_pkg_data_filename('hash/ed6e4146ea0a1d2af0f005dd8ba79282')

g = fits.open(g_name)[0]
r = fits.open(r_name)[0]
i = fits.open(i_name)[0]

# Rotate the images
ang = np.deg2rad(-90)
wcs = WCS(g.header)
wcs.wcs.cd = wcs.wcs.cd @ np.array([[np.cos(ang),-np.sin(ang)],[np.sin(ang),np.cos(ang)]])
wcs.wcs.crpix = tuple([x/2. for x in g.data.shape])

imgs = []
for img in [g,r,i]:
    hdr = img.header
    hdr = hdr.copy()

    arr, footprint = reproject_interp(img, wcs.to_header(),
                                      shape_out=(g.header['NAXIS1'], g.header['NAXIS2']))
    imgs.append(arr)

# extract a smaller region around the Hickson 88 group
slc = (slice(None, 400), slice(None))
gp = imgs[0][slc]
rp = imgs[1][slc]
ip = imgs[2][slc]

# make the figure - 2 sets of stretch parameters
rgb1 = make_lupton_rgb(ip, rp, gp)
rgb2 = make_lupton_rgb(ip*0.8, rp, gp*1.3, Q=10, stretch=0.4)

fig, axes = plt.subplots(1, 2, figsize=(10, 4),
                         sharex=True, sharey=True,
                         subplot_kw=dict(projection=wcs))

axes[0].imshow(rgb1, origin='lower')
axes[0].set_title('default parameters', fontsize=14)
axes[0].set_adjustable('box-forced')

axes[1].imshow(rgb2, origin='lower')
axes[1].set_title('Q=10, stretch=0.4', fontsize=14)
axes[1].set_adjustable('box-forced')

for j in [0,1]:
    lon, lat = axes[j].coords
    axes[j].coords.grid(True, color='white', ls='solid', alpha=0.4)

    lon.set_axislabel('Right Ascension (ICRS)')

    lon.set_ticks(spacing=2*u.arcmin)
    lat.set_ticks(spacing=2*u.arcmin)

    lon.set_major_formatter('dd:mm')
    lat.set_major_formatter('dd:mm')

axes[0].coords[1].set_axislabel('Declination (ICRS)')
fig.savefig('ngc6977.pdf')
