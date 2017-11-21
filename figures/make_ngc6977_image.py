from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
from astropy.visualization import make_lupton_rgb

# load the data
g_name = get_pkg_data_filename('visualization/reprojected_sdss_g.fits.bz2')
r_name = get_pkg_data_filename('visualization/reprojected_sdss_r.fits.bz2')
i_name = get_pkg_data_filename('visualization/reprojected_sdss_i.fits.bz2')
g = fits.open(g_name)[0].data
r = fits.open(r_name)[0].data
i = fits.open(i_name)[0].data

# extract a smaller region around the Hickson 88 group
slc = (slice(0, 285), slice(33, 318))
gp = g[slc]
rp = r[slc]
ip = i[slc]

# make the figure
rgb = make_lupton_rgb(ip*0.8, rp, gp*1.3, Q=10, stretch=0.4,
                      filename='ngc6977.png')
