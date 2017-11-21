import re
from astropy.coordinates import frame_transform_graph
from astropy.coordinates.transformations import trans_to_color
from graphviz import Source

legend = """rankdir=LR
node [shape=plaintext margin=0]
  subgraph cluster_01 {
    key [label=<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">
      <tr><td align="right" port="i1">AffineTransform</td></tr>
      <tr><td align="right" port="i2">FunctionTransformWithFiniteDifference</td></tr>
      <tr><td align="right" port="i3">StaticMatrixTransform</td></tr>
      <tr><td align="right" port="i4">DynamicMatrixTransform</td></tr>
      </table>>]
    key2 [label=<<table border="0" cellpadding="2" cellspacing="0" cellborder="0">
      <tr><td port="i1">&nbsp;</td></tr>
      <tr><td port="i2">&nbsp;</td></tr>
      <tr><td port="i3">&nbsp;</td></tr>
      <tr><td port="i4">&nbsp;</td></tr>
      </table>>]
    key:i1:e -> key2:i1:w [color="#555555"]
    key:i2:e -> key2:i2:w [color="#d95f02"]
    key:i3:e -> key2:i3:w [color="#7570b3"]
    key:i4:e -> key2:i4:w [color="#1b9e77"]
  }
"""

raw_src = frame_transform_graph.to_dot_graph(priorities=False)

# Remove the short names / aliases
pattr = re.compile(r'\\n`[a-z0-9]+`')
raw_src = pattr.sub('', raw_src)
raw_src = raw_src[:-1] + '\nsplines=true\n' + legend + '}'

dot = Source(raw_src, engine='neato')
dot.render('coordinates_graph', cleanup=True)
