import re
from astropy.coordinates import frame_transform_graph
from astropy.coordinates.transformations import trans_to_color
from graphviz import Source

raw_src = frame_transform_graph.to_dot_graph(priorities=False,
                                             color_edges=False)

# Remove the short names / aliases
pattr = re.compile(r'\\n`[a-z0-9]+`')
raw_src = pattr.sub('', raw_src)

dot = Source(raw_src, engine='neato')
dot.render('coordinates_graph', cleanup=True)
