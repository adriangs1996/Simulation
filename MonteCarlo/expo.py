#! /usr/bin/python3

from scipy.integrate import quad
from integral import integral
from argparse import ArgumentParser
from math import e, inf
import progressbar.progressbar as progress
from time import sleep
from statistics import stdev, mean

parser = ArgumentParser()
parser.add_argument('--iterations',
                    type=int,
                    help="number of iterations for Monte Carlo.")
parser.add_argument('--verbose',
                    action="store_true",
                    help="Add more verbose output.")
parser.add_argument('--samples', type=int, help="Number of simulations.")
parser.add_argument("--standard-deviation",
                    action='store_true',
                    help="Calculate standard deviation of simulated values.")
parser.add_argument("--mean",
                    action='store_true',
                    help="Calculate mean of simulated values")
args = parser.parse_args()

i = args.iterations if args.iterations else 10000
samples = args.samples if args.samples else 1
exp0_1_simulations = []
exp_inf_simulations = []

if args.verbose:
    print("[+] Calculating integral of e^-(x^2) by Monte Carlo.")
    print("[+] Running algorithm %d times" % samples)

pro = progress.ProgressBar()
for _ in pro(range(samples)):
    exp0_1_simulations.append(integral(0, 1, lambda x: e**-(x**2), i))
    exp_inf_simulations.append(integral(-inf, inf, lambda x: e**-(x**2), i))
    sleep(0.00001)

m01 = mean(exp0_1_simulations)
minf = mean(exp_inf_simulations)

if args.standard_deviation:
    sd01 = stdev(exp0_1_simulations)
    sdinf = stdev(exp_inf_simulations)

scipy_int01 = quad(lambda x: e**-(x**2), 0, 1)[0]
scipy_inf = quad(lambda x: e**-(x**2), -inf, +inf)[0]

if args.verbose:
    print("\t\t=======  Stats ========")
    print("Simulation in [0,1]")
    print("-------------------")
    print("Result: %.5f\tScipy: %.5f" % (exp0_1_simulations[0], scipy_int01))
    if args.mean:
        print("Mean: %.5f" % m01)
    if args.standard_deviation:
        print("SD: %.5f" % sd01)
    print("Simulation in [-inf, +inf]")
    print("--------------------------")
    print("Result: %.5f\tScipy: %.5f" % (exp_inf_simulations[0], scipy_inf))
    if args.mean:
        print("Mean: %.5f" % minf)
    if args.standard_deviation:
        print("SD: %.5f" % sdinf)

else:
    print("[0,1] ->> %.5f" % m01 if args.mean else exp0_1_simulations[0])
    print("[-inf, +inf] ->> %.5f" %
          minf if args.mean else exp_inf_simulations[0])
