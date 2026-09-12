"""Export frozen analysis figures through BytesIO for portable PNG writes.

Some mounted filesystems truncate Pillow's direct file-descriptor PNG output.
This changes only byte delivery; the frozen plotting function is reused intact.
"""
import io
import json
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from analyze_e1 import plot

original = Figure.savefig


def buffered_save(self, target, *args, **kwargs):
    target = Path(target)
    buffer = io.BytesIO()
    original(self, buffer, *args, format=target.suffix.lstrip('.'), **kwargs)
    target.write_bytes(buffer.getvalue())


if __name__ == '__main__':
    Figure.savefig = buffered_save
    for arg in sys.argv[1:]:
        root = Path(arg)
        plot(root, json.loads((root / 'summary.json').read_text()))
        from PIL import Image
        with Image.open(root / 'E1_RESULTS.png') as im:
            im.verify()
        print(f'{arg}: PNG byte integrity verified')
