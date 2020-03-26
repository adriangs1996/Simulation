from seachannel import SeaChannel
from statistics import mean, stdev
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument(
    "--hatches",
    type=int,
    help="Numbers of hatches for the Sea Channel. Default to 5.")
parser.add_argument("-d",
                    "--distribution",
                    nargs="+",
                    help="""Specify the distribution of the hatches.
                    Every hatch can either go UP or DOWN to conform the
                    transport layer of the Sea Channel. The list must not
                    exced the number of hatches. Every Hatch is default to UP.
                    """,
                    choices={"UP", "DOWN"})
