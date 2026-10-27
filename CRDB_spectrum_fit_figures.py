"""
Figures cosmic rays spectral features.

Created on Tue Dec 2 2025

@author: claireguepin
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pandas
from typing import Any, Optional
from matplotlib.lines import Line2D

plt.rcParams["font.family"] = "STIXGeneral"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams['font.size'] = 16
plt.rcParams['xtick.labelsize'] = 16
plt.rcParams['ytick.labelsize'] = 16
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True

arr = pandas.read_csv("figures/spectral_fits/Spectrum_features.csv")
# arr.set_index('Experiment', inplace=True)


# GENERAL VALUES

Eknee = 4e-3
Econcave = 2e-2
Eknee_2 = 0.1
E12_TA = 5.
E23_TA = 14.
E34_TA = 68.

# =============================================================================
# FIGURES similar to Hubble constant estimates comparisons

# colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
colors = np.array(['C0', 'C6', 'C4', 'C0', 'C3', 'C7', 'C9', 'C0', 'C1',
                   'C5', 'C2'])

# ENERGIES low

fig, ax = plt.subplots(1, 1, figsize=(12, 4))
fig.subplots_adjust(left=0.13, bottom=0.2, right=0.95, top=0.9)
axi = ax
plt.sca(axi)
# ax.loglog()
ax.set_xscale("log")
ax.set_xlabel(r"$E$ [EeV]")
ax.set_ylabel(r"Experiments")
ax.set_xlim(3e-3, 3e-1)

arr_labels = np.array([])

for i in range(1, len(arr["Eknee"])-2):
    # if not np.isnan(arr["Eknee"][i]):
    ind = i
    plt.errorbar(arr["Eknee"][i], ind, yerr=None, xerr=arr["Eknee err"][i], marker='|', ms=12, lw=3, color=colors[i])
    arr_labels = np.concatenate((arr_labels, np.array([arr["Experiment"][i]])))

for i in range(1, len(arr["Econcave"])-2):
    # if not np.isnan(arr["Eknee"][i]):
    ind = i
    plt.errorbar(arr["Econcave"][i], ind, yerr=None, xerr=arr["Econcave err"][i], marker='|', ms=12, lw=3, color=colors[i])

for i in range(1, len(arr["Eknee2"])-2):
    # if not np.isnan(arr["Eknee"][i]):
    ind = i
    plt.errorbar(arr["Eknee2"][i], ind, yerr=None, xerr=arr["Eknee2 err"][i], marker='|', ms=12, lw=3, color=colors[i])

# TEXT
plt.text(Eknee, 1.02, "Knee", fontsize=14,
         transform=ax.get_xaxis_transform(), ha='center', va='bottom')
plt.text(Econcave, 1.02, "Hardening", fontsize=14,
         transform=ax.get_xaxis_transform(), ha='center', va='bottom')
plt.text(Eknee_2, 1.02, "Second Knee", fontsize=14,
         transform=ax.get_xaxis_transform(), ha='center', va='bottom')

ax.set_yticks(np.arange(1, len(arr_labels)+1, 1), labels=arr_labels,
              fontsize=10)
ax.set_ylim(0, len(arr_labels)+1)

# ax.legend(frameon=False, ncol=2, loc=3, fontsize=10)
plt.savefig("figures/spectral_fits/Comparison_Experiments_Energy_low.pdf")
plt.show()

# ENERGIES High

fig, ax = plt.subplots(1, 1, figsize=(12, 3))
fig.subplots_adjust(left=0.13, bottom=0.2, right=0.95, top=0.9)
axi = ax
plt.sca(axi)
# ax.loglog()
ax.set_xscale("log")
ax.set_xlabel(r"$E$ [EeV]")
ax.set_ylabel(r"Experiments")
ax.set_xlim(2e0, 2e2)

arr_labels = np.array([])

for i in range(len(arr["Eankle"])):
    if not np.isnan(arr["Eankle"][i]):
        arr_labels = np.concatenate((arr_labels, np.array([arr["Experiment"][i]])))

ind = 1
for i in range(len(arr["Eankle"])):
    if not np.isnan(arr["Eankle"][i]):
        plt.errorbar(arr["Eankle"][i], ind, yerr=None, xerr=arr["Eankle err"][i], marker='|', ms=12, lw=3, color=colors[i])
        ind += 1

ind = 1
for i in range(len(arr["Einstep"])):
    if not np.isnan(arr["Eankle"][i]):
        plt.errorbar(arr["Einstep"][i], ind, yerr=None, xerr=arr["Einstep err"][i], marker='|', ms=12, lw=3, color=colors[i])
        ind += 1

ind = 1
for i in range(len(arr["Esuppression"])):
    if not np.isnan(arr["Eankle"][i]):
        plt.errorbar(arr["Esuppression"][i], ind, yerr=None, xerr=arr["Esuppression err"][i], marker='|', ms=12, lw=3, color=colors[i])
        ind += 1

# TEXT
plt.text(E12_TA, 1.02, "Ankle", fontsize=14,
         transform=ax.get_xaxis_transform(), ha='center', va='bottom')
plt.text(E23_TA, 1.02, "Instep", fontsize=14,
         transform=ax.get_xaxis_transform(), ha='center', va='bottom')
plt.text(E34_TA, 1.02, "Suppression", fontsize=14,
         transform=ax.get_xaxis_transform(), ha='center', va='bottom')

ax.set_yticks(np.arange(1, len(arr_labels)+1, 1), labels=arr_labels,
              fontsize=10)
ax.set_ylim(0, len(arr_labels)+1)

# ax.legend(frameon=False, ncol=2, loc=3, fontsize=10)
plt.savefig("figures/spectral_fits/Comparison_Experiments_Energy_high.pdf")
plt.show()

# INDICES low

plt.rcParams['xtick.top'] = False

fig, ax = plt.subplots(1, 4, figsize=(12, 4), sharey=True)
fig.subplots_adjust(left=0.13, bottom=0.2, right=0.95, top=0.9, wspace=0.12)

fig.text(0.5, 0.04, r'Spectral index', ha='center')
ax[0].set_ylabel(r"Experiments")

arr_labels = np.array([])

for i in range(1, len(arr["gamma1_knee"])-2):
    ind = i
    ax[0].errorbar(-arr["gamma1_knee"][i], ind, yerr=None, xerr=arr["gamma1_knee err"][i], marker='|', ms=12, lw=3, color=colors[i])
    arr_labels = np.concatenate((arr_labels, np.array([arr["Experiment"][i]])))

for i in range(1, len(arr["gamma2_knee"])-2):
    ind = i
    ax[1].errorbar(-arr["gamma2_knee"][i], ind, yerr=None, xerr=arr["gamma2_knee err"][i], marker='|', ms=12, lw=3, color=colors[i])

for i in range(1, len(arr["gamma1_knee2"])-2):
    ind = i
    ax[2].errorbar(-arr["gamma1_knee2"][i], ind, yerr=None, xerr=arr["gamma1_knee2 err"][i], marker='|', ms=12, lw=3, color=colors[i])

for i in range(1, len(arr["gamma2_knee2"])-2):
    ind = i
    ax[3].errorbar(-arr["gamma2_knee2"][i], ind, yerr=None, xerr=arr["gamma2_knee2 err"][i], marker='|', ms=12, lw=3, color=colors[i])

# TEXT
plt.text(0.31, 0.92, "Knee", fontsize=14, transform=plt.gcf().transFigure)
plt.text(0.5, 0.92, "Hardening", fontsize=14, transform=plt.gcf().transFigure)
plt.text(0.71, 0.92, "Second Knee", fontsize=14, transform=plt.gcf().transFigure)

ax[0].set_yticks(np.arange(1, len(arr_labels)+1, 1), labels=arr_labels,
              fontsize=10)
ax[0].set_ylim(0, len(arr_labels)+1)

ax[0].set_xticks(np.arange(2.6, 3.0, 0.1))
ax[1].set_xticks(np.arange(3.0, 3.5, 0.1))
ax[2].set_xticks(np.arange(2.7, 3.1, 0.1))
ax[3].set_xticks(np.arange(3.0, 3.8, 0.2))

plt.savefig("figures/spectral_fits/Comparison_Experiments_Index_low.pdf")
plt.show()

# INDICES high

plt.rcParams['xtick.top'] = False

fig, ax = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
fig.subplots_adjust(left=0.13, bottom=0.2, right=0.95, top=0.9, wspace=0.12)

fig.text(0.5, 0.04, r'Spectral index', ha='center')
ax[0].set_ylabel(r"Experiments")

arr_labels = np.array([])

for i in range(len(arr["gamma1_ankle"])):
    if not np.isnan(arr["gamma1_ankle"][i]):
        arr_labels = np.concatenate((arr_labels, np.array([arr["Experiment"][i]])))

ind = 1
for i in range(len(arr["gamma1_ankle"])):
    if not np.isnan(arr["gamma1_ankle"][i]):
        ax[0].errorbar(-arr["gamma1_ankle"][i], ind, yerr=None, xerr=arr["gamma1_ankle err"][i], marker='|', ms=12, lw=3, color=colors[i])
        ind += 1

ind = 1
for i in range(len(arr["gamma2_ankle"])):
    if not np.isnan(arr["gamma1_ankle"][i]):
        ax[1].errorbar(-arr["gamma2_ankle"][i], ind, yerr=None, xerr=arr["gamma2_ankle err"][i], marker='|', ms=12, lw=3, color=colors[i])
        ind += 1


ind = 1
for i in range(len(arr["gamma1_suppression"])):
    if not np.isnan(arr["gamma1_ankle"][i]):
        ax[2].errorbar(-arr["gamma1_suppression"][i], ind, yerr=None, xerr=arr["gamma1_suppression err"][i], marker='|', ms=12, lw=3, color=colors[i])
        ind += 1


ind = 1
for i in range(len(arr["gamma2_suppression"])):
    if not np.isnan(arr["gamma1_ankle"][i]):
        ax[3].errorbar(-arr["gamma2_suppression"][i], ind, yerr=None, xerr=arr["gamma2_suppression err"][i], marker='|', ms=12, lw=3, color=colors[i])
        ind += 1

# TEXT
plt.text(0.31, 0.92, "Ankle", fontsize=14, transform=plt.gcf().transFigure)
plt.text(0.52, 0.92, "Instep", fontsize=14, transform=plt.gcf().transFigure)
plt.text(0.71, 0.92, "Suppression", fontsize=14, transform=plt.gcf().transFigure)

ax[0].set_yticks(np.arange(1, len(arr_labels)+1, 1), labels=arr_labels,
              fontsize=10)
ax[0].set_ylim(0, len(arr_labels)+1)

# ax[0].set_xticks(np.arange(2.6, 3.0, 0.1))
# ax[1].set_xticks(np.arange(3.0, 3.5, 0.1))
# ax[2].set_xticks(np.arange(2.7, 3.1, 0.1))
# ax[3].set_xticks(np.arange(3.0, 3.8, 0.2))

plt.savefig("figures/spectral_fits/Comparison_Experiments_Index_high.pdf")
plt.show()
