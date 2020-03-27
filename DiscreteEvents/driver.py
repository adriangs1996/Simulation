#! /usr/bin/python3
from seachannel import SeaChannel
from channelships import MultiShipsSeaChannel
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
                    Every hatch can either go UP(U) or DOWN(D) to conform the
                    transport layer of the Sea Channel. The list must not
                    exced the number of hatches. Every Hatch is default to UP.
                    """,
                    choices={"U", "D"})
parser.add_argument(
    '-m',
    '--mean',
    action='store_true',
    help=
    "Calculate the mean of runned simulations.This is best used toghether with -c option."
)
parser.add_argument('-c',
                    "--count",
                    type=int,
                    help="Run the simulator COUNT times.")
parser.add_argument(
    '-i',
    '--independent-arrivals',
    action='store_true',
    help=
    "Simulate the channel recreating the arrivals of the ships for every size. It means that more ships travels through the channel at every hour."
)

parser.add_argument(
    '-g',
    '--debug',
    action='store_true',
    help="Add debug information and interactive behavior to the simulator")

args = parser.parse_args()

hatches = args.hatches if args.hatches else 5

distribution = [1] * hatches

mapp = {"U": 1, "D": 2}

if args.distribution:
    assert len(
        args.distribution) <= hatches, "To many arguments for distribution"
    for i, mode in enumerate(args.distribution):
        distribution[i] = mapp[mode]

count = args.count if args.count else 1

if not args.debug:
    if not args.independent_arrivals:
        r = [SeaChannel(distribution).run_day() for _ in range(count)]
    else:
        r = [
            MultiShipsSeaChannel(distribution).run_day() for _ in range(count)
        ]
else:
    if not args.independent_arrivals:
        r = [
            SeaChannel(distribution, debug=True).run_day()
            for _ in range(count)
        ]
    else:
        r = [
            MultiShipsSeaChannel(distribution, debug=True).run_day()
            for _ in range(count)
        ]

if count > 1:
    for i in range(1, count + 1):
        print("Simulation %d" % (i - 1))
        print("--------------")
        print("Result: %0.2f minutes\n" % r[i - 1])
    if args.mean:
        print("Mean: %0.2f" % mean(r))

else:
    print("Result: %0.2f" % r[0])
    if args.mean:
        print("Result: %0.2f" % r[0])
