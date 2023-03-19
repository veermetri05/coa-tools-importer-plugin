import xml.etree.ElementTree as ET
import sys
import json
from PIL import Image
import os
from pathlib import Path

def pxToUnit(root, px):
    width = float(root.attrib['width'])
    viewBox = root.attrib['view-box'].split()
    areaWidth = abs(float(viewBox[0])) + abs(float(viewBox[2]))
    return px / (width / areaWidth) 

def unitToPx(root, unit):
    width = float(root.attrib['width'])
    viewBox = root.attrib['view-box'].split()
    areaWidth = abs(float(viewBox[0])) + abs(float(viewBox[2]))
    return unit * (width / areaWidth)

# a function that accepts list of layers and returns a switch layer
def createSwitchLayer(canvasChildren: list[ET.Element], desc = ""):
  switchLayerXML = '''
    <layer type="switch" active="true" exclude_from_rendering="false" version="0.0">
    <param name="z_depth">
      <real value="0.0000000000"/>
    </param>
    <param name="amount">
      <real value="1.0000000000"/>
    </param>
    <param name="blend_method">
      <integer value="0" static="true"/>
    </param>
    <param name="origin">
      <vector>
        <x>0</x>
        <y>0</y>
      </vector>
    </param>
    <param name="transformation">
      <composite type="transformation">
        <offset>
          <vector>
            <x>0</x>
            <y>0</y>
          </vector>
        </offset>
        <angle>
          <angle value="0.000000"/>
        </angle>
        <skew_angle>
          <angle value="0.000000"/>
        </skew_angle>
        <scale>
          <vector>
            <x>1.0000000000</x>
            <y>1.0000000000</y>
          </vector>
        </scale>
      </composite>
    </param>
    <param name="canvas">
    </param>
    <param name="time_dilation">
      <real value="1.0000000000"/>
    </param>
    <param name="time_offset">
      <time value="0s"/>
    </param>
    <param name="children_lock">
      <bool value="true" static="true"/>
    </param>
    <param name="outline_grow">
      <real value="0.0000000000"/>
    </param>
    <param name="layer_name">
      <string></string>
    </param>
    <param name="layer_depth">
      <integer value="0"/>
    </param>
  </layer>
  '''
  switchLayer = ET.fromstring(switchLayerXML)
  switchLayer.attrib['desc'] = desc
  ET.SubElement(switchLayer[5], 'canvas')
  switchLayer[5][0].extend(canvasChildren)
  return switchLayer

# a function to draw a rectangle
def createMaskingRectangle(topLeft, bottomRight, desc = "mask"):
  rectangleLayerXML = '''
                <layer type="rectangle" active="true" exclude_from_rendering="false" version="0.2" desc="Rectangle063">
                <param name="z_depth">
                  <real value="0.0000000000"/>
                </param>
                <param name="amount">
                  <real value="1.0000000000"/>
                </param>
                <param name="blend_method">
                  <integer value="19"/>
                </param>
                <param name="color">
                  <color>
                    <r>1.000000</r>
                    <g>1.000000</g>
                    <b>1.000000</b>
                    <a>1.000000</a>
                  </color>
                </param>
                <param name="point1">
                  <vector>
                    <x>1.3395836353</x>
                    <y>0.0088319331</y>
                  </vector>
                </param>
                <param name="point2">
                  <vector>
                    <x>2.5993628502</x>
                    <y>-0.9216493368</y>
                  </vector>
                </param>
                <param name="expand">
                  <real value="0.0000000000"/>
                </param>
                <param name="invert">
                  <bool value="true"/>
                </param>
                <param name="feather_x">
                  <real value="0.0000000000"/>
                </param>
                <param name="feather_y">
                  <real value="0.0000000000"/>
                </param>
                <param name="bevel">
                  <real value="0.0000000000"/>
                </param>
                <param name="bevCircle">
                  <bool value="true"/>
                </param>
              </layer>
  '''
  rectangleLayer = ET.fromstring(rectangleLayerXML)
  rectangleLayer.attrib['desc'] = desc
  rectangleLayer[4][0][1].text = str(pxToUnit(root, topLeft[1]))
  rectangleLayer[4][0][0].text = str(pxToUnit(root, topLeft[0]))
  rectangleLayer[5][0][0].text = str(pxToUnit(root, bottomRight[0]))
  rectangleLayer[5][0][1].text = str(pxToUnit(root, bottomRight[1]))
  return rectangleLayer

# a function that adjusts coordinates to suit the canvas
def adjustForCanvasOrigin(coordinates: list[float, float], canvasRoot):
  return [coordinates[0], -coordinates[1]]

# a function that accpets a list of coordinates and returns a modified list of coordinates with necessary adjustments to suit the canvas
def adjustCoordinates(coordinates: list[float, float], canvasRoot):
  return [coordinates[0] + -1920/2, -coordinates[1] + 1080/2]

def createGroup(canvasChildren: list[ET.Element], desc = "", origin = [0.0, 0.0], offset = [0.0, 0.0]):
    parent = ET.fromstring(''' 
 <layer type="group" active="true" exclude_from_rendering="false" version="0.3">
    <param name="z_depth">
      <real value="0.0000000000"/>
    </param>
    <param name="amount">
      <real value="1.0000000000"/>
    </param>
    <param name="blend_method">
      <integer value="0" static="true"/>
    </param>
    <param name="origin">
      <vector>
        <x>0.0000000000</x>
        <y>0.0000000000</y>
      </vector>
    </param>
    <param name="transformation">
      <composite type="transformation">
        <offset>
          <vector>
            <x>0.0000000000</x>
            <y>0.0000000000</y>
          </vector>
        </offset>
        <angle>
          <angle value="0.000000"/>
        </angle>
        <skew_angle>
          <angle value="0.000000"/>
        </skew_angle>
        <scale>
          <vector>
            <x>1.0000000000</x>
            <y>1.0000000000</y>
          </vector>
        </scale>
      </composite>
    </param>
    <param name="canvas">
    </param>
    <param name="time_dilation">
      <real value="1.0000000000"/>
    </param>
    <param name="time_offset">
      <time value="0s"/>
    </param>
    <param name="children_lock">
      <bool value="true" static="true"/>
    </param>
    <param name="outline_grow">
      <real value="0.0000000000"/>
    </param>
    <param name="z_range">
      <bool value="false" static="true"/>
    </param>
    <param name="z_range_position">
      <real value="0.0000000000"/>
    </param>
    <param name="z_range_depth">
      <real value="0.0000000000"/>
    </param>
    <param name="z_range_blur">
      <real value="0.0000000000"/>
    </param>
</layer>
  ''')
    parent.attrib['desc'] = desc
    parent[3][0][0].text = str(pxToUnit(root, origin[0]))
    parent[3][0][1].text = str(pxToUnit(root, origin[1]))
    parent[4][0][0][0][0].text = str(pxToUnit(root, offset[0]))
    parent[4][0][0][0][1].text = str(pxToUnit(root, offset[1]))
    ET.SubElement(parent[5], 'canvas')
    parent[5][0].extend(canvasChildren)
    return parent

def createImage(desc, imagePath ):
    image = ET.fromstring('''    
        <layer type="import" active="true" exclude_from_rendering="false" version="0.1" desc="">
            <param name="z_depth">
                <real value="0.0000000000"/>
            </param>
            <param name="amount">
                <real value="1.0000000000"/>
            </param>
            <param name="blend_method">
                <integer value="0" static="true"/>
            </param>
            <param name="tl">
                <vector>
                    <x></x>
                    <y></y>
                </vector>
            </param>
            <param name="br">
                <vector>
                    <x></x>
                    <y></y>
                </vector>
            </param>
            <param name="c">
                <integer value="1" static="true"/>
            </param>
            <param name="gamma_adjust">
                <real value="1.0000000000"/>
            </param>
            <param name="filename">
                <string></string>
            </param>
            <param name="time_offset">
            <time value="0s"/>
            </param>
        </layer>
        ''')
    image.attrib['desc'] = desc 
    image[7][0].text = imagePath
    with Image.open(imagePath) as img:
        width, height = img.size
    # print(width, height)
    image[3][0][0].text = str(0)
    image[3][0][1].text = str(0)
    image[4][0][0].text = str(pxToUnit(root, width))
    image[4][0][1].text = str(-(pxToUnit(root, height)))

    return image

def createImageGroup(desc ,imagePath, adjustedPositionOffset = [0.0, 0.0], origin = [0.0, 0.0]):
    image = createImage(desc, imagePath)
    parent = createGroup([image], desc, origin)
    parent[4][0][0][0][0].text = str(pxToUnit(root, adjustedPositionOffset[0]))
    parent[4][0][0][0][1].text = str(pxToUnit(root, adjustedPositionOffset[1]))
    return parent

# a function that accepts name, imagePath, positionOffset, offset, tiles_x, tiles_y and returns a group which contains switch layer
def createSwitchGroup(name, imagePath, positionOffset, offset, tiles_x, tiles_y):
  parentCanvas = []
  with Image.open(imagePath) as img:
    width, height = img.size
  baseCenter = [( positionOffset[0] - ((width / tiles_x) / 2)), ( positionOffset[1] - ( (height / tiles_y) / 2)) ]
  print(baseCenter)
  print(positionOffset)
  for i in range(0, tiles_x):
    topLeft = [None] * 2
    bottomRight = [None] * 2

    adjustedCoordinates = adjustCoordinates(positionOffset, root)

    topLeft[0] = adjustedCoordinates[0] + (i * width/tiles_x)
    bottomRight[0] = adjustedCoordinates[0] + ((i + 1) * width/tiles_x)

    for j in range(0, tiles_y):
      canvas = []

      topLeft[1] = (adjustedCoordinates[1] - (j * height/tiles_y))
      bottomRight[1] = (adjustedCoordinates[1] - ((j + 1) * height/tiles_y))

      # reposition the positionOffset by substracting the inverse of topLeft

      adjustedPositionOffset = adjustCoordinates(positionOffset, root)

      parentOffset = [adjustedPositionOffset[0] - topLeft[0], adjustedPositionOffset[1] - topLeft[1]] 

      imageGroup = createImageGroup(name + str((i+1)*(j+1)), imagePath, adjustedPositionOffset)

      maskingRectangle = createMaskingRectangle(topLeft , bottomRight)
      canvas.append(imageGroup)
      canvas.append(maskingRectangle)
      parentCanvas.append(createGroup(canvas, name + str((i+1)+(j+1)), offset=parentOffset))
  parentCanvas.reverse()
  print(parentCanvas)
  return createSwitchLayer(parentCanvas, name)

if os.path.isfile(sys.argv[2]):
  print("File exists")
else:
  f = open(sys.argv[2], "a")
  f.write('''<?xml version="1.0" encoding="UTF-8"?>
    <canvas version="1.2" width="1920" height="1080" xres="2834.645669" yres="2834.645669" gamma-r="1.000000" gamma-g="1.000000" gamma-b="1.000000" view-box="-4.000000 2.250000 4.000000 -2.250000" antialias="1" fps="24.000" begin-time="0f" end-time="5s" bgcolor="0.500000 0.500000 0.500000 1.000000">
      <name>tempTest.sif</name> 
      <meta name="background_first_color" content="0.880000 0.880000 0.880000"/>
      <meta name="background_rendering" content="0"/>
      <meta name="background_second_color" content="0.650000 0.650000 0.650000"/>
      <meta name="background_size" content="15.000000 15.000000"/>
      <meta name="grid_color" content="0.623529 0.623529 0.623529"/>
      <meta name="grid_show" content="0"/>
      <meta name="grid_size" content="0.250000 0.250000"/>
      <meta name="grid_snap" content="0"/>
      <meta name="guide_color" content="0.435294 0.435294 1.000000"/>
      <meta name="guide_show" content="1"/>
      <meta name="guide_snap" content="0"/>
      <meta name="jack_offset" content="0.000000"/>
      <meta name="onion_skin" content="0"/>
      <meta name="onion_skin_future" content="0"/>
      <meta name="onion_skin_keyframes" content="1"/>
      <meta name="onion_skin_past" content="1"/>
      <keyframe time="0f" active="true"/>
    </canvas>''')
  f.close()

f = open(sys.argv[1])
spriteInfo = json.load(f)
tree = ET.parse(sys.argv[2])
root = tree.getroot()
layers = []
path = Path(sys.argv[1])
parent = path.parent.absolute()
spriteInfo['nodes'] = sorted(spriteInfo['nodes'], key=lambda d: d['z']) 

for item in spriteInfo['nodes']:
  if(item['tiles_x'] == 1 and item['tiles_y'] == 1):
    layers.insert(0, createImageGroup(item['name'], os.path.join(parent, Path(item['resource_path'])), item['position'], item['offset']))
  else:
    layers.insert(0, createSwitchGroup(item['name'], os.path.join(parent, Path(item['resource_path'])), item['position'], item['offset'], item['tiles_x'], item['tiles_y']))

layers.reverse()
root.extend(layers)
tr2ee = ET.ElementTree(root)
with open(sys.argv[2], "wb") as fh:
    tr2ee.write(fh, encoding="utf-8", xml_declaration=True)