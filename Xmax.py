"""
Plot xmax moments.

Created on Thu Jan 22 18:18:18 2026

@author: claireguepin
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

from plot_functions import read_xmax_file, draw_with_errorbars_xmax
from plot_styles import get_plot_styles_xmax

# =============================================================================
# PARAMETERS

moment = "sigma"  # mean or sigma

# =============================================================================
# HADRONIC INTERACTION MODELS DATA

had_dir = 'CRDB_Data/hadronic_data/'
line_p_s_mean = np.loadtxt(
    had_dir + "Sibyll23d_p.csv", skiprows=1, delimiter=',')
line_fe_s_mean = np.loadtxt(
    had_dir + "Sibyll23d_fe.csv", skiprows=1, delimiter=',')
line_p_q_mean = np.loadtxt(
    had_dir + "QGSJet-II04_p.csv", skiprows=1, delimiter=',')
line_fe_q_mean = np.loadtxt(
    had_dir + "QGSJet-II04_fe.csv", skiprows=1, delimiter=',')
line_p_e_mean = np.loadtxt(
    had_dir + "EPOSLHC_p.csv", skiprows=1, delimiter=',')
line_fe_e_mean = np.loadtxt(
    had_dir + "EPOSLHC_fe.csv", skiprows=1, delimiter=',')

line_p_s_sigma = np.loadtxt(
    had_dir + "Sibyll23d_sigma_p.csv", skiprows=1, delimiter=',')
line_fe_s_sigma = np.loadtxt(
    had_dir + "Sibyll23d_sigma_fe.csv", skiprows=1, delimiter=',')
line_p_q_sigma = np.loadtxt(
    had_dir + "QGSJet-II04_sigma_p.csv", skiprows=1, delimiter=',')
line_fe_q_sigma = np.loadtxt(
    had_dir + "QGSJet-II04_sigma_fe.csv", skiprows=1, delimiter=',')
line_p_e_sigma = np.loadtxt(
    had_dir + "EPOSLHC_sigma_p.csv", skiprows=1, delimiter=',')
line_fe_e_sigma = np.loadtxt(
    had_dir + "EPOSLHC_sigma_fe.csv", skiprows=1, delimiter=',')

# =============================================================================
# XMAX DATA

expedir = "./Xmax_Data/DataFiles/dat/"
expetab = np.array([
    "Auger_AERA_ICRC21_XmaxMoments",
    "Auger_Delta_PRD2017_ICRC19_XmaxMoments",
    "Auger_FD_ICRC2019_XmaxMoments",
    "LOFAR_PRD2021_XmaxMoments",
    "TA_ApJ2018_XmaxMoments_unbias",
    "TA_ApJ2018_XmaxMoments",
    "TALE_unbiased_EPOSLHC_ApJ2021_XmaxMoments",
    "Tunka-133_PhysAtNucl2021_XmaxMoments",
    "TunkaRex_PRD2018_XmaxMoments",
    "Yakutsk_ASR2019_XmaxMoments",
    "Yakutsk_RD_ICRC2019_XmaxMoments"
])

# Initialize DataFrame
df_test = pd.DataFrame(
    data=np.ones((len(expetab), 3)),
    index=expetab,
    columns=["color", "marker", "label"],
)

# Get styles from the config file
color_map, marker_map, label_map = get_plot_styles_xmax()

# Apply styles using .loc to avoid SettingWithCopyWarning
for key, value in color_map.items():
    if key in df_test.index:
        df_test.loc[key, "color"] = value

for key, value in marker_map.items():
    if key in df_test.index:
        df_test.loc[key, "marker"] = value


for key, value in label_map.items():
    if key in df_test.index:
        df_test.loc[key, "label"] = value

# =============================================================================
# FIGURES

fig, ax = plt.subplots(1, 1, figsize=(10, 7))
plt.subplots_adjust(left=0.08, bottom=0.1, right=0.95)
handles = []

i = 0

for fname in expetab:
    # if (fname != expetab[5] and fname != expetab[9] and fname != expetab[10]):
    if (fname != expetab[5] and fname != expetab[10]):
        # if (fname == expetab[0] or fname == expetab[1] or fname == expetab[2]):
        print(fname)

        x, y, ystat, ysys_up, ysys_dn = read_xmax_file(
            expedir + fname + '.dat', "mean")
        # There is a mistake with the signs in the TA data
        if fname == expetab[4]:
            for ii in range(len(ysys_dn)):
                if ysys_dn[ii] < 0:
                    ysys_dn[ii] *= -1

        if y is None:
            print(
                f"File {fname} does not contain the requested moment; skipping")
            continue

        handle = draw_with_errorbars_xmax(
            x=10**x/1e9,
            y=y,
            ysta=ystat,
            ysys=np.vstack([ysys_dn, ysys_up]),
            color=df_test["color"][fname],
            marker=df_test["marker"][fname],
            label=df_test["label"][fname],
            ax=ax
        )
        handles.append(handle)
        i += 1


leg1 = ax.legend(handles=handles, fontsize=14, loc="upper left",
                 frameon=False, ncols=2)
ax.add_artist(leg1)

# line_p_s = np.loadtxt("Sibyll23d_p.csv", skiprows=1, delimiter=',')
# line_fe_s = np.loadtxt("Sibyll23d_fe.csv", skiprows=1, delimiter=',')

# plt.plot(10**line_p_s[:, 0]/1e9, line_p_s[:, 1], color='r')
# plt.plot(10**line_fe_s[:, 0]/1e9, line_fe_s[:, 1], color='b')

plt.plot(10**line_p_s_mean[:, 0]/1e9, line_p_s_mean[:, 1],
         color='grey', ls='--')
plt.plot(10**line_fe_s_mean[:, 0]/1e9, line_fe_s_mean[:, 1],
         color='grey',  ls='--')
plt.plot(10**line_p_q_mean[:, 0]/1e9, line_p_q_mean[:, 1],
         color='grey', ls=':')
plt.plot(10**line_fe_q_mean[:, 0]/1e9, line_fe_q_mean[:, 1],
         color='grey',  ls=':')
plt.plot(10**line_p_e_mean[:, 0]/1e9, line_p_e_mean[:, 1],
         color='grey', ls='-')
plt.plot(10**line_fe_e_mean[:, 0]/1e9, line_fe_e_mean[:, 1],
         color='grey',  ls='-')


# legend_lines = []
# for model in HadModel:
#     model_name = model.name
#     linestyle = MODEL_LINESTYLE[model_name]
#     legend_lines.append(Line2D([0], [0],
#                                color="gray", ls=linestyle, lw=2))
legend_labels = ['QGSJet-II.04', 'EPOS-LHC', 'Sibyll2.3d']
legend_ls = [':', '-', '--']
ax.legend(legend_ls, legend_labels, frameon=False,
          fontsize=14, loc="lower right")

# plot_model_rails(ax, moment="mean", bool_legend=True, loc="lower right")
ax.text(3e10, 860, r'proton', color='grey', rotation=20, fontsize=14)
ax.text(3e10, 705, r'iron', color='grey', rotation=20, fontsize=14)
ax.set_xlim(1e15/1e9, 2e20/1e9)
ax.set_xscale('log')
ax.set_ylim(420, 900)
ax.set_xlabel(r"$E\,[\rm{GeV}]$")
ax.set_ylabel(r"$\langle X_{\max} \rangle\,[\mathrm{g\,cm^{-2}}]$")

# plt.tight_layout()
plt.savefig('Xmax_mean_ExpData.pdf')

fig, ax = plt.subplots(1, 1, figsize=(10, 7))
plt.subplots_adjust(left=0.08, bottom=0.1, right=0.95)
handles = []

i = 0
# for fname in expetab[0:3]:
for fname in expetab:
    # if (fname != expetab[5] and fname != expetab[9] and fname != expetab[10]
    #     and (fname != expetab[7] or moment != "sigma")):
    if (fname != expetab[5] and fname != expetab[10]
            and (fname != expetab[7] or moment != "sigma")):
        print(fname)

        x, y, ystat, ysys_up, ysys_dn = read_xmax_file(
            expedir + fname + '.dat', moment)
        # There is a mistake with the signs in the TA data
        if fname == expetab[4]:
            for ii in range(len(ysys_dn)):
                if ysys_dn[ii] < 0:
                    ysys_dn[ii] *= -1

        if y is None:
            print(
                f"File {fname} does not contain the requested moment; skipping")
            continue

        handle = draw_with_errorbars_xmax(
            x=10**x/1e9,
            y=y,
            ysta=ystat,
            ysys=np.vstack([ysys_dn, ysys_up]),
            color=df_test["color"][fname],
            marker=df_test["marker"][fname],
            label=df_test["label"][fname],
            ax=ax
        )
        handles.append(handle)
        i += 1

leg1 = ax.legend(handles=handles, fontsize=14, loc="upper left",
                 frameon=False, ncols=2)
ax.add_artist(leg1)


def lissage(y, fenetre):
    box = np.ones(fenetre) / fenetre
    return np.convolve(y, box, mode='same')


y_lisse = lissage(line_fe_e_sigma[:, 1], fenetre=3)


plt.plot(10**line_p_s_sigma[:, 0]/1e9, line_p_s_sigma[:, 1],
         color='grey', ls='--')
plt.plot(10**line_fe_s_sigma[:, 0]/1e9, line_fe_s_sigma[:, 1],
         color='grey',  ls='--')
plt.plot(10**line_p_q_sigma[:, 0]/1e9, line_p_q_sigma[:, 1],
         color='grey', ls=':')
plt.plot(10**line_fe_q_sigma[:, 0]/1e9, line_fe_q_sigma[:, 1],
         color='grey',  ls=':')
plt.plot(10**line_p_e_sigma[:, 0]/1e9, line_p_e_sigma[:, 1],
         color='grey', ls='-')
plt.plot(10**line_fe_e_sigma[:, 0]/1e9, line_fe_e_sigma[:, 1],
         color='grey',  ls='-')

# legend_lines = []
# legend_labels = ['QGSJet-II.04', 'EPOS-LHC', 'Sibyll2.3d']
# for model in HadModel:
#     model_name = model.name
#     linestyle = MODEL_LINESTYLE[model_name]
#     legend_lines.append(Line2D([0], [0],
#                                color="gray", ls=linestyle, lw=2))
# ax.legend(legend_lines, legend_labels, frameon=False,
#           fontsize=14, loc="lower left")

legend_labels = ['QGSJet-II.04', 'EPOS-LHC', 'Sibyll2.3d']
legend_ls = [':', '-', '--']
ax.legend(legend_ls, legend_labels, frameon=False,
          fontsize=14, loc="lower left")

# plot_model_rails(ax, moment="sigma", bool_legend=True, loc="lower left")
ax.text(3e10, 62, r'proton', color='grey', fontsize=14)
ax.text(3e10, 13, r'iron', color='grey', fontsize=14)
ax.set_xlim(2e7, 1e20/1e9)
ax.set_xscale('log')
ax.set_ylim(0, 100)
ax.set_xlabel(r"$E\,[\rm{GeV}]$")
ax.set_ylabel(r"$\sigma(X_{\max})\,[\mathrm{g\,cm^{-2}}]$")

# plt.tight_layout()
plt.savefig('Xmax_sigma_ExpData.pdf')
