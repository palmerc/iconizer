#!/usr/bin/env python3

import json
import pathlib
import gi
import cairo
import argparse

gi.require_version('Rsvg', '2.0')

from gi.repository import Rsvg


def svg_to_png(svg_path, png_path, width, height):
    svg = Rsvg.Handle().new_from_file(svg_path.as_posix())
    unscaled_width = svg.props.width
    unscaled_height = svg.props.height

    svg_surface = cairo.SVGSurface(None, width, height)
    svg_context = cairo.Context(svg_surface)
    svg_context.save()
    svg_context.scale(width / unscaled_width, height / unscaled_height)
    svg.render_cairo(svg_context)
    svg_context.restore()

    svg_surface.write_to_png(png_path.as_posix())
    svg_surface.finish()


def render(svg_path, json_file, output_path):
    with open(json_file) as f:
        data = json.load(f)

    output_path.mkdir(exist_ok=True)
    output_json_path = output_path.joinpath('Contents.json')
    for image in data['images']:
        idiom = image['idiom']
        size = image['size']
        scale = image['scale'].strip('x')
        (width, height) = size.split('x')
        filename = svg_path.stem.lower()
        if scale == '1':
            png_filename = '%s-%s-%s.png' % (filename, idiom, width)
        else:
            png_filename = '%s-%s-%s@%s.png' % (filename, idiom, width, scale)
        png_width = float(width) * float(scale)
        png_height = float(height) * float(scale)
        png_path = output_path.joinpath(png_filename)
        print('{} {}'.format(png_width, png_height))
        svg_to_png(svg_path, png_path, png_width, png_height)
        image['filename'] = png_filename

        with open(output_json_path, 'w+') as f:
            json.dump(data, f)


def main():
    parser = argparse.ArgumentParser(description='Create icons from SVG')
    parser.add_argument('--svg', dest='svg',
                        help='path to .svg', required=True)
    parser.add_argument('-j', '--contents-json', dest='contents_json',
                        help='the Contents.json file', required=True)
    parser.add_argument('-o', '--output', dest='output',
                        help='the output path', required=True)
    args = parser.parse_args()

    render(pathlib.Path(args.svg), pathlib.Path(args.contents_json), pathlib.Path(args.output).resolve())


if __name__ == '__main__':
    main()

