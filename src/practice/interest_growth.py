import sys
import numpy as np


def simple_compound(principal, rate, time, compound_per_cycle=1):
    rate = float(rate)
    principal = float(principal)
    time = int(time)
    compound_per_cycle = float(compound_per_cycle)
    return principal*(1 + rate / compound_per_cycle)**(time*compound_per_cycle)


def simple_compound_solve(total, rate, time, compound_per_cycle=1.0):
    rate = float(rate)
    total = float(total)
    time = int(time)
    compound_per_cycle = float(compound_per_cycle)
    return total / (1 + (rate / compound_per_cycle))**(time*compound_per_cycle)


def annual_additions(principal, rate, time, additions):
    rate = float(rate)
    if rate < 1:
        rate += 1
    principal = float(principal)
    time = int(time)
    additions = float(additions)
    additions_compound_factor = sum([rate**n for n in range(1, time + 1)])
    return principal*rate**time + additions*additions_compound_factor


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: \n"
              "interest_growth.py -s PRINCIPAL APR TIME_PERIODS --> Compound Interest")
        print("interest_growth.py -c PRINCIPAL APR TIME_PERIODS MONTHLY_ADDITIONS--> Total Contributions Savings")
        print("interest_growth.py -sc TOTAL APR TIME_PERIODS --> Compound Interest")
        print("interest_growth.py ")

    elif sys.argv[1] == "-s":
        print("Principal = ${0}, Rate = {1}, time periods = {2}".format(*sys.argv[2:]))
        print(f"Total amount is $ {round(simple_compound(*sys.argv[2:]), 2)}")

    elif sys.argv[1] == "-c":
        print("Principal = ${0}, Rate = {1}, time periods = {2}, annual contribution = ${3}".format(*sys.argv[2:]))
        print(f"Total amount is $ {round(annual_additions(*sys.argv[2:]),2)}")

    elif sys.argv[1] == "-ss":
        print("Total = ${0}, Rate = {1}, time periods = {2}".format(*sys.argv[2:]))
        print(f"Principal Amount needed is $ {round(simple_compound_solve(*sys.argv[2:]), 2)}")

    else:
        pass




