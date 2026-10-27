"""
Composition cosmic rays.

CRDB

Created on Oct 15 2024

@author: claireguepin
"""

from typing import Any, Optional

# from crdb.mpl import draw_logo
import matplotlib.pyplot as plt
import numpy as np
import pandas as pandas
from matplotlib.lines import Line2D

from plot_functions import draw_with_errorbars
from plot_styles import get_plot_styles

# =============================================================================
# LOAD CUSTOM DATA
tab_H = pandas.read_csv("CRDB_Data/composition/H_All.csv", header=0, delimiter=",")
exp_tab_H = pandas.unique(tab_H["SUBEXP-NAME"])

tab_He = pandas.read_csv("CRDB_Data/composition/He_All.csv", header=0, delimiter=",")
exp_tab_He = pandas.unique(tab_He["SUBEXP-NAME"])

tab_O = pandas.read_csv(
    "CRDB_Data/composition/O-group_All.csv", header=0, delimiter=","
)
exp_tab_O = pandas.unique(tab_O["SUBEXP-NAME"])

tab_N = pandas.read_csv(
    "CRDB_Data/composition/N-group_All.csv", header=0, delimiter=","
)
exp_tab_N = pandas.unique(tab_N["SUBEXP-NAME"])

tab_Fe = pandas.read_csv(
    "CRDB_Data/composition/Fe-group_All.csv", header=0, delimiter=","
)
exp_tab_Fe = pandas.unique(tab_Fe["SUBEXP-NAME"])

# =============================================================================
# FIGURE OPTIONS

savefig = True  # set to true to save all the plots below as svg and pdf
plot_err_systematic = True

# =============================================================================
# DETECTORS

expetab = np.array(
    [
        "NUCLEON-IC (2015/07-2017/06)",
        "NUCLEON-KLEM (2015/07-2017/06)",
        "IceCube Hybrid (2010/06-2013/05) SIBYLL2.1",
        "IceCube+IceTop (2010/06-2013/05) SIBYLL2.1",
        "KASCADE (1996/10-2002/01) QGSJet01",
        "KASCADE (1996/10-2002/01) SIBYLL 2.1",
        "KASCADE-Grande (2003/12-2009/03) QGSJet-II-2",
        "KASCADE-Grande (2003/12-2011/10) SIBYLL2.3",
        "GAMMA (2003/01-2007/12) SIBYLL",
        "Tunka-133 (2009/10-2012/04) QGSJet01",
        "Auger FD (2004/12-2012/12) EPOS-LHC",
        "Auger FD (2004/12-2012/12) QGSJet-II-04",
        "Auger FD (2004/12-2012/12) SIBYLL2.1",
    ]
)

# =============================================================================
# Dataframe with energy rescaling factor, when available
# Test with values from LHAASO paper 2403.11832

# Initialize DataFrame
df_test = pandas.DataFrame(
    data=np.ones((len(expetab), 3)),
    index=expetab,
    columns=["E_rescaling", "color", "marker"],
)

# Get styles from the config file
e_rescaling, color_map, marker_map = get_plot_styles()

# Apply styles using .loc to avoid SettingWithCopyWarning
for key, value in e_rescaling.items():
    if key in df_test.index:
        df_test.loc[key, "E_rescaling"] = value

for key, value in color_map.items():
    if key in df_test.index:
        df_test.loc[key, "color"] = value

for key, value in marker_map.items():
    if key in df_test.index:
        df_test.loc[key, "marker"] = value

# =============================================================================
# FIGURE FOR REVIEW
# LOCAL VERSION OF FIGURE


# # =============================================================================
# # LOAD LHAASO DATA TO OVERLAY

# dat = np.loadtxt("./DataLHAASO/AllparticleSpectrum_EPOS-LHC.txt", delimiter=" ",
#                  skiprows=8)
# ene = 10**dat[:, 0]
# flu = dat[:, 1]

# file_path = "DataLHAASO/ProtonSpectrumPRL.txt"
# df = parse_spectrum(file_path)
# # print(df.head())
# # print(df.columns)

# file_path = "DataLHAASO/HeliumSpectrum.txt"
# df_He = parse_spectrum(file_path)

# ene_p = 10**df['EnergyRange'].values*1e6
# flu_p = df['EPOS_Flux']*1e-6

# ene_He = 10**df_He['EnergyRange'].values*1e6
# flu_He = df_He['EPOS_Flux']*1e-6

# ene_comp = ene[ene <= ene_p[-1]]
# flu_comp = flu[ene <= ene_p[-1]]
# flu_p = flu_p[ene_He >= ene[0]]
# flu_He = flu_He[ene_He >= ene[0]]

excluded_experiments = {
    "IceCube Hybrid (2010/06-2013/05) SIBYLL2.1",  # Only keep IceCube+IceTop
    "KASCADE (1996/10-2002/01) QGSJet01",  # Outdated hadronic interaction model
    "KASCADE-Grande (2003/12-2009/03) QGSJet-II-2",  # Outdated hadronic interaction model
}

# =============================================================================
# FIGURE FOR REVIEW

fig, ax = plt.subplots(4, 1, figsize=(14, 14), sharex=True)

# =============================================================================
# H / All particles

plt.sca(ax[0])

for exp in expetab:
    if exp not in excluded_experiments:

        # for exp in exp_tab_H:
        # if (exp.find("Tibet") == 0):
        print(exp)
        print("HEEEEEEERRRRE")
        tabloc = tab_H[tab_H["SUBEXP-NAME"] == exp]
        print(np.array(tabloc["PUBLI-HTML"])[0])
        print(np.argwhere(expetab == exp))
        xdat = np.array(tabloc[" DATA-E_MEAN"])
        ydat = np.array(tabloc["DATA-VAL"])

        ysta = np.array([tabloc["DATA-VAL_ERRSTAT_L"], tabloc["DATA-VAL_ERRSTAT_U"]])
        ysys = np.array([tabloc["DATA-VAL_ERRSYST_L"], tabloc["DATA-VAL_ERRSYST_U"]])
        # xerr = np.abs(tabloc['EBIN_HIGH'] - x)
        xerr = None
        is_ul = np.array(tabloc["DATA-ISUPPERLIM"]) == 1
        draw_with_errorbars(
            xdat,
            ydat,
            ysta,
            ysys,
            xerr,
            is_ul,
            label=exp,
            sys_lw=5,
            color=df_test["color"][exp],
            marker=df_test["marker"][exp],
            plot_err_systematic=plot_err_systematic,
        )

        # # LHAASO
        # plt.plot(ene_comp, flu_p/flu_comp, ls='', marker='o', color='C6')

# =============================================================================
# He / All particles

plt.sca(ax[1])

for exp in expetab:
    if exp not in excluded_experiments:

        try:
            print(exp)
            tabloc = tab_He[tab_He["SUBEXP-NAME"] == exp]
            print(np.array(tabloc["PUBLI-HTML"])[0])
            xdat = np.array(tabloc[" DATA-E_MEAN"])
            ydat = np.array(tabloc["DATA-VAL"])

            ysta = np.array(
                [tabloc["DATA-VAL_ERRSTAT_L"], tabloc["DATA-VAL_ERRSTAT_U"]]
            )
            ysys = np.array(
                [tabloc["DATA-VAL_ERRSYST_L"], tabloc["DATA-VAL_ERRSYST_U"]]
            )
            # xerr = np.abs(tabloc['EBIN_HIGH'] - x)
            xerr = None
            is_ul = np.array(tabloc["DATA-ISUPPERLIM"]) == 1
            draw_with_errorbars(
                xdat,
                ydat,
                ysta,
                ysys,
                xerr,
                is_ul,
                label=exp,
                sys_lw=5,
                color=df_test["color"][exp],
                marker=df_test["marker"][exp],
                plot_err_systematic=plot_err_systematic,
            )
        except:
            print("Data not found")

        # # LHAASO
        # plt.plot(ene_comp, flu_He/flu_comp, ls='', marker='o', color='C6')


# =============================================================================
# O & N / All particles

plt.sca(ax[2])

for exp in expetab:
    if exp not in excluded_experiments:

        try:
            print(exp)
            tabloc = tab_O[tab_O["SUBEXP-NAME"] == exp]
            print(np.array(tabloc["PUBLI-HTML"])[0])
            xdat = np.array(tabloc[" DATA-E_MEAN"])
            ydat = np.array(tabloc["DATA-VAL"])

            ysta = np.array(
                [tabloc["DATA-VAL_ERRSTAT_L"], tabloc["DATA-VAL_ERRSTAT_U"]]
            )
            ysys = np.array(
                [tabloc["DATA-VAL_ERRSYST_L"], tabloc["DATA-VAL_ERRSYST_U"]]
            )
            # xerr = np.abs(tabloc['EBIN_HIGH'] - x)
            xerr = None
            is_ul = np.array(tabloc["DATA-ISUPPERLIM"]) == 1
            draw_with_errorbars(
                xdat,
                ydat,
                ysta,
                ysys,
                xerr,
                is_ul,
                label=exp,
                sys_lw=5,
                color=df_test["color"][exp],
                marker=df_test["marker"][exp],
                plot_err_systematic=plot_err_systematic,
            )
        except:
            print("Data not found")

for exp in expetab:
    if exp not in excluded_experiments:
        try:
            print(exp)
            tabloc = tab_N[tab_N["SUBEXP-NAME"] == exp]
            print(np.array(tabloc["PUBLI-HTML"])[0])
            xdat = np.array(tabloc[" DATA-E_MEAN"])
            ydat = np.array(tabloc["DATA-VAL"])

            ysta = np.array(
                [tabloc["DATA-VAL_ERRSTAT_L"], tabloc["DATA-VAL_ERRSTAT_U"]]
            )
            ysys = np.array(
                [tabloc["DATA-VAL_ERRSYST_L"], tabloc["DATA-VAL_ERRSYST_U"]]
            )
            # xerr = np.abs(tabloc['EBIN_HIGH'] - x)
            xerr = None
            is_ul = np.array(tabloc["DATA-ISUPPERLIM"]) == 1
            draw_with_errorbars(
                xdat,
                ydat,
                ysta,
                ysys,
                xerr,
                is_ul,
                label=exp,
                sys_lw=5,
                color=df_test["color"][exp],
                marker=df_test["marker"][exp],
                plot_err_systematic=plot_err_systematic,
            )
        except:
            print("Data not found")

# =============================================================================
# Fe / All particles

plt.sca(ax[3])

for exp in expetab:
    if exp not in excluded_experiments:
        try:
            print(exp)
            tabloc = tab_Fe[tab_Fe["SUBEXP-NAME"] == exp]
            print(np.array(tabloc["PUBLI-HTML"])[0])
            xdat = np.array(tabloc[" DATA-E_MEAN"])
            ydat = np.array(tabloc["DATA-VAL"])

            ysta = np.array(
                [tabloc["DATA-VAL_ERRSTAT_L"], tabloc["DATA-VAL_ERRSTAT_U"]]
            )
            ysys = np.array(
                [tabloc["DATA-VAL_ERRSYST_L"], tabloc["DATA-VAL_ERRSYST_U"]]
            )
            # xerr = np.abs(tabloc['EBIN_HIGH'] - x)
            xerr = None
            is_ul = np.array(tabloc["DATA-ISUPPERLIM"]) == 1
            draw_with_errorbars(
                xdat,
                ydat,
                ysta,
                ysys,
                xerr,
                is_ul,
                label=exp,
                sys_lw=5,
                color=df_test["color"][exp],
                marker=df_test["marker"][exp],
                plot_err_systematic=plot_err_systematic,
            )
        except:
            print("Data not found")

plt.sca(ax[0])
ax[0].set_xlim(1e4, 5e10)
ax[0].set_ylim([0, 1])
ax[0].set_ylabel(r"H / All particles")

plt.sca(ax[1])
ax[1].set_xlim(1e4, 5e10)
ax[1].set_ylim([0, 1])
ax[1].set_ylabel(r"He / All particles")

ax[2].set_ylim([0, 1])
ax[2].set_ylabel(r"O- and N-group / All particles")

ax[3].set_ylim([0, 1])
ax[3].set_ylabel(r"Fe-group / All particles")

plt.xscale("log")
ax[2].set_xlabel(r"$E$ [GeV]")
ax[3].set_xlabel(r"$E$ [GeV]")

# ax[0].set_yticks(np.arange(0, 1, step=0.2))
# ax[1].set_yticks(np.arange(0, 1, step=0.2))
# ax[2].set_yticks(np.arange(0, 1, step=0.2))
# ax[3].set_yticks(np.arange(0, 1, step=0.2))

# draw_logo(-0.01, 0.13)

# handles, labels = ax[0, 0].get_legend_handles_labels()
# fig.legend(handles, labels, fontsize=10, frameon=False, loc='upper right',
#            bbox_to_anchor=(0, 0, 0.98, 0.9))
# plt.subplots_adjust(left=0.08, bottom=0.1, right=0.7, top=0.9,
#                     wspace=0.3, hspace=0.3)

# fig.legend(handles, labels, fontsize=10, frameon=False, loc='center right')
# plt.subplots_adjust(left=0.08, bottom=0.1, right=0.9, top=0.9,
#                     wspace=0.3, hspace=0.3)

handles, labels = ax[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    fontsize=10,
    frameon=False,
    loc="lower left",
    bbox_to_anchor=(0.1, 0, 0.9, 0.8),
    ncols=3,
)

fig.subplots_adjust(left=0.1, bottom=0.12, right=0.95, top=0.95, wspace=0.2, hspace=0.2)


# GENERAL VALUES
Eknee = 4e-3 * 1e9
Econcave = 2e-2 * 1e9
Eknee_2 = 0.1 * 1e9
E12_TA = 5.0 * 1e9
E23_TA = 14.0 * 1e9
E34_TA = 68.0 * 1e9

# TEXT
plt.text(
    Eknee,
    1.02,
    "Knee",
    fontsize=14,
    transform=ax[0].get_xaxis_transform(),
    ha="center",
    va="bottom",
)
plt.text(
    Econcave,
    1.02,
    "Hardening",
    fontsize=14,
    transform=ax[0].get_xaxis_transform(),
    ha="center",
    va="bottom",
)
plt.text(
    Eknee_2,
    1.02,
    "Second Knee",
    fontsize=14,
    transform=ax[0].get_xaxis_transform(),
    ha="center",
    va="bottom",
)

plt.text(
    E12_TA,
    1.02,
    "Ankle",
    fontsize=14,
    transform=ax[0].get_xaxis_transform(),
    ha="center",
    va="bottom",
)
plt.text(
    E23_TA,
    1.02,
    "Instep",
    fontsize=14,
    transform=ax[0].get_xaxis_transform(),
    ha="center",
    va="bottom",
)
# plt.text(E34_TA, 1.02, "Suppression", fontsize=14,
#          transform=ax[0].get_xaxis_transform(), ha='center', va='bottom')

if plot_err_systematic:
    plt.savefig("Figures/composition_syst.pdf")
else:
    plt.savefig("Figures/composition.pdf")
