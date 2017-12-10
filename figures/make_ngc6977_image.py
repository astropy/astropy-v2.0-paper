from astropy.io import fits
import astropy.units as u
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization import make_lupton_rgb, astropy_mpl_style
from astropy.wcs import WCS
import matplotlib.pyplot as plt
plt.style.use(astropy_mpl_style)

# load the data
g_name = get_pkg_data_filename('visualization/reprojected_sdss_g.fits.bz2')
r_name = get_pkg_data_filename('visualization/reprojected_sdss_r.fits.bz2')
i_name = get_pkg_data_filename('visualization/reprojected_sdss_i.fits.bz2')

g = fits.open(g_name)[0]
r = fits.open(r_name)[0]
i = fits.open(i_name)[0]

# extract a smaller region around the Hickson 88 group
slc = (slice(0, 285), slice(33, 318))
gp = g.data[slc]
rp = r.data[slc]
ip = i.data[slc]

# make the figure - stretch 1
rgb1 = make_lupton_rgb(ip, rp, gp)
rgb2 = make_lupton_rgb(ip*0.8, rp, gp*1.3, Q=10, stretch=0.4)

wcs = WCS(g.header)

fig, axes = plt.subplots(1, 2, figsize=(8, 4),
                         sharex=True, sharey=True,
                         subplot_kw=dict(projection=wcs))

axes[0].imshow(rgb1, origin='lower')
axes[0].set_title('default parameters', fontsize=18)
axes[0].set_adjustable('box-forced')

axes[1].imshow(rgb2, origin='lower')
axes[1].set_title('Q=10, stretch=0.4', fontsize=18)
axes[1].set_adjustable('box-forced')

for i in [0,1]:
    lon, lat = axes[i].coords
    axes[i].coords.grid(True, color='white', ls='solid', alpha=0.4)

    lon.set_axislabel('Right Ascension (ICRS)')

    lon.set_ticks(spacing=1*u.arcmin)
    lat.set_ticks(spacing=1*u.arcmin)

    lon.set_major_formatter('dd:mm')
    lat.set_major_formatter('dd:mm')

axes[0].coords[1].set_axislabel('Declination (ICRS)')
fig.savefig('ngc6977.png')
