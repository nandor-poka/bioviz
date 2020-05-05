import sys
import parser
from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid, Range1d
from bokeh.models.glyphs import Text
from bokeh.io import show, output_file
from bokeh.transform import factor_cmap
from bokeh.layouts import column
import math


# Colour themes
def colorswitcher(argument):
    switcher = {
        'clustalColorMap': {
            "A": "red",
            "C": "blue",
            "G": "orange",
            "T": "green",
        },
        'macCladeColorMap': {
            "A": "red",
            "C": "green",
            "G": "yellow",
            "T": "blue",
        },
        'gcatColorMap': {
            "A": "red",
            "C": "orange",
            "G": "orange",
            "T": "red",
        },
        'purinePyrimidineColorMap': {
            "A": "pink",
            "C": "blue",
            "G": "pink",
            "T": "blue",
        },
        'translationColorMap': {
            "A": "red",
            "C": "red",
            "G": "red",
            "T": "green",
        },
        'annotationColorMap': {
            "A": "yellow",
            "C": "yellow",
            "G": "black",
            "T": "green",
        }
    }
    return switcher.get(argument, "Invalid color theme")


plot_width = 100


def main(argv):
    parsed_sequences = parser.main(argv)
    output_file(argv[2])

    actualColorMap = colorswitcher(argv[3])

    sequence_count = len(parsed_sequences)
    seq_lengths = [parsed_sequences[i].get('seq_length') for i in range(0, sequence_count)]
    max_seq_length = max(seq_lengths)

    # Each subplot should be plot_width letter 'long' at max.
    subplot_count = math.ceil(max_seq_length / plot_width)
    plots = []

    # Create subplots.
    for k in range(0, subplot_count):
        x_start = 1 + plot_width * k
        x_end = plot_width + 1 + plot_width * k

        # X has the values of the X axis of the plot - same for every sequence
        # Y has the values of the Y axis of the plot - different for every sequence
        x = range(x_start, x_end)

        subplot = Plot(title=None, plot_width=10 * plot_width, plot_height=30 * sequence_count,
                       x_range=Range1d(start=x_start, end=x_end),
                       y_range=Range1d(start=0, end=sequence_count),
                       min_border=0, toolbar_location=None)

        # Add sequences to the plot.
        for i in range(0, sequence_count):
            y_seq = []
            # The y value for the i. sequence will be i for all letters.
            for j in range(x_start, x_end):
                y_seq.append(i + 1)

            seq = list(parsed_sequences[i].get('seq'))[x_start-1:x_end-1]
            source_seq = ColumnDataSource(dict(x=x, y=y_seq, text=seq))

            glyph_seq = Text(x="x", y="y", text="text",
                             text_color=factor_cmap('text', palette=list(actualColorMap.values()),
                                                    factors=list(actualColorMap.keys())),
                             text_font_size="9pt",
                             text_line_height=0.8,
                             text_baseline="top")
            subplot.add_glyph(source_seq, glyph_seq)

            print(i, y_seq[0], seq)

        xaxis = LinearAxis(axis_label="Position")
        subplot.add_layout(xaxis, 'below')

        subplot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
        plots.append(subplot)

    show(column(plots))


main(sys.argv)
