#! /usr/bin/python3
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
                    help="Run the simulator <count> times.")

args = parser.parse_args()

hatches = args.hatches if args.hatches else 5

distribution = [1] * hatches

mapp = {"UP": 1, "DOWN": 0}

if args.distribution:
    assert len(
        args.distribution) <= hatches, "To many arguments for distribution"
    for i, mode in args.distribution:
        distribution[i] = mapp[mode]

count = args.count if args.count else 1

r = [SeaChannel(distribution).run_day() for _ in range(count)]

if count > 1:
    for i in range(1, count + 1):
        print("Simulation %d" % (i - 1))
        print("--------------")
        print("Result: %0.5f minutes\n" % r[i - 1])
    if args.mean:
        print("Mean: %0.5f" % mean(r))

else:
    print("Result: %0.5f" % r[0])
    if args.mean:
        print("Result: %0.5f" % r[0])
