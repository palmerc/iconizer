# iconizer
Python script to convert an SVG to a variety of PNG sizes necessary for iOS projects

An iOS project requires a bunch of icons in a variety of sizes. This is generally annoying. So this script takes the Contents.json file and outputs the PNGs necessary from an SVG source

    brew install librsvg

    pip install pycairo
    pip install pyGObject


    ./iconizer.py --svg /path/to/svg -o /where/to/go -j /Contents.json
