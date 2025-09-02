import matplotlib.pyplot as plt
import scipy.signal as signal
import cothread
from cothread.catools import *
import numpy as np
import time
import sys


def get_sa_data(psc_prefix):
    # Create PV list for DieTemp and all 4 channels
    sa_pv = []

    # Die temperature (only one instance)
    sa_pv.append(psc_prefix + "DieTemp-I")

    # Add PVs for Chan1 through Chan4
    for chan in range(1, 5):
        chan_prefix = f"{psc_prefix}Chan{chan}:"
        sa_pv.extend([
            chan_prefix + "DCCT1-I",
            chan_prefix + "DCCT2-I",
            chan_prefix + "DAC-I",
            chan_prefix + "Volt-I",
            chan_prefix + "Gnd-I",
            chan_prefix + "Spare-I",
            chan_prefix + "Reg-I",
            chan_prefix + "Error-I"
        ])

    # Collect SA data points
    waveform = np.asarray(caget(sa_pv), dtype=np.float32)
    return waveform


def main():
    print("Total arguments passed:", len(sys.argv))
    if len(sys.argv) != 4:
        print("Usage: %s [psc name] [num pts] [output filename]" % (sys.argv[0]))
        exit()

    psc = sys.argv[1]
    numpts = int(sys.argv[2]) + 1
    filename = sys.argv[3]

    with open(filename, 'w', buffering=1) as outfile:
        for i in range(1, numpts):
            ts = caget(psc + "TS-S-I")
            data = get_sa_data(psc)

            # Print to terminal
            print(f"{i:8d}:\t{ts:10d}\t", end="")
            print("\t".join(f"{d:2.6f}" for d in data))

            # Print to output file
            print(f"{ts:10d}\t", end="", file=outfile)
            print("\t".join(f"{d:2.6f}" for d in data), file=outfile)

            # Wait for new timestamp before next read
            while ts == caget(psc + "TS-S-I"):
                time.sleep(0.1)


if __name__ == "__main__":
    main()

