#!/usr/bin/env python3

import gi
import cairo

gi.require_version('Rsvg', '2.0')

from gi.repository import Rsvg
import json
import os

def svg_to_png(svg_path, png_path, width, height):
    svg = Rsvg.Handle().new_from_file('/Users/palmerc/Downloads/WSHorse.svg')
    unscaled_width = svg.props.width
    unscaled_height = svg.props.height

    svg_surface = cairo.SVGSurface(None, width, height)
    svg_context = cairo.Context(svg_surface)
    svg_context.save()
    svg_context.scale(width / unscaled_width, height / unscaled_height)
    svg.render_cairo(svg_context)
    svg_context.restore()

    svg_surface.write_to_png(png_path)
    svg_surface.finish()


svg_path = '/Users/palmerc/Downloads/WSHorse.svg'
output_path = '/Users/palmerc/Desktop'
output_json_path = os.path.join(output_path, 'Contents.json')
json_file = open('Assets.xcassets/AppIcon.appiconset/Contents.json')
data = json.load(json_file)

for image in data['images']:
    idiom = image['idiom']
    size = image['size']
    scale = image['scale'].strip('x')
    (width, height) = size.split('x')
    filename = os.path.basename(os.path.normpath(svg_path)).lower().strip('.svg')
    if scale == '1':
        png_filename = '%s-%s-%s.png' % (filename, idiom, width)
    else:
        png_filename = '%s-%s-%s@%s.png' % (filename, idiom, width, scale)
    png_width = float(width) * float(scale)
    png_height = float(height) * float(scale)
    png_path = os.path.join(output_path, png_filename)
    print('{} {}'.format(png_width, png_height))
    svg_to_png(svg_path, png_path, png_width, png_height)
    image['filename'] = png_filename

output_json_file = open(output_json_path, 'w+')
json.dump(data, output_json_file)