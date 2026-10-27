"""
Spectrum cosmic rays.

CRDB, data not show discussed in README

From https://github.com/crdb-project/tutorial/blob/main/gallery.ipynb
Created on Wed Nov 29 16:08:56 2023

@author: claireguepin
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pandas
from typing import Any, Optional
from matplotlib.lines import Line2D
from pathlib import Path
from plot_styles import get_plot_styles
from plot_functions import draw_with_errorbars

plt.rcParams["font.family"] = "STIXGeneral"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.size"] = 16
plt.rcParams["xtick.labelsize"] = 16
plt.rcParams["ytick.labelsize"] = 16
plt.rcParams["xtick.top"] = True
plt.rcParams["ytick.right"] = True

# =============================================================================
# LOAD CUSTOM DATA

# tab = pandas.read_csv('CRDB_Data/Flux_crdb_import_mod.csv',
# tab = pandas.read_csv('CRDB_Data/Flux_crdb_import_mod_new.csv',
#                       header=0, delimiter=',')
tab = pandas.read_csv("./CRDB_Data/Flux_crdb_Sep2026.csv", header=0, delimiter=",")
exp_tab = pandas.unique(tab["SUBEXP-NAME"])

# =============================================================================
# FIGURE OPTIONS
exponents = 3.0
expo = exponents
plot_err_systematic = True
path_fig = Path("./figures/flux")
path_fig.mkdir(parents=True, exist_ok=True)

# =============================================================================
# DETECTORS
expetab = np.array(
    [
        "NUCLEON-KLEM (2015/07-2017/06)",
        "HAWC (2016/06-2017/02) QGSJet-II-03",
        "HAWC (2018-2019) QGSJet-II-04",
        "TAIGA-HiScore (2017/01-2018/12)",

        # 'LHAASO EPOS-LHC',
        "LHAASO-KM2A (2021/09-2022/12) EPOS-LHC",

        "EAS-TOP (1992/01-1999/12) QGSJet",
        "Maket-ANI (1997-2004) QGSJet-II-01",
        "DICE (1994/07-1996/03)",
        "HEGRA (1987-1998) QGSJet",
        "IceTop (2016/05-2017/04) QGSJet-II-04",
        "IceTop (2016/05-2017/04) SIBYLL2.1",
        "IceCube+IceTop (2010/06-2013/05) SIBYLL2.1",
        "IceTop (2010/06-2013/05)",
        "KASCADE (1996/10-2002/01) QGSJet01",
        "KASCADE (1996/10-2002/01) SIBYLL 2.1",
        "KASCADE-Grande (2003/01-2009/03) QGSJet-II-04",
        "KASCADE-Grande (2004/03-2010/12) QGSJet-II-3",
        "KASCADE-Grande (2003/12-2011/10) SIBYLL2.3",
        "KASCADE-Grande (2004/03-2012/05) QGSJet-II-2",

        'KASCADE-Grande EPOS-LHC',
        # "KASCADE-Grande (2003/01-2006/08) QGSJet-II.04",

        "KASCADE-Grande QGSjet-II-04",
        "GAMMA (2003/01-2007/12) SIBYLL",
        "TUNKA-133 Array (2009/10-2012/04) QGSJet01",
        "TALE (2014/06/-2016/03) QGSJet-II-03",
        # 'Telescope Array Hybrid (2008/01-2015/05)',

        'Telescope Array SD (2008/05 - 2024/05)',
        # "TA SD (2008/05-2019/05)",

        "Auger Hybrid (2004/01-2016/12) QGSJet-II-04+EPOS-LHC+SIBYLL2.3",
        "Auger SD750 (2014/01-2018/08)",
        "Auger SD750+SD1500 (2014/01-2018/08)",
        "Yakutsk (1995/01-2008/12) QGSJet01",
        "Fly's Eye (1988/06-1992/07)",
        "AGASA (1993/12-2002/12)",
        "NUCLEON-IC (2015/07-2017/06)",
        "SOKOL (1984/03-1986/01)",
        "RUNJOB (1995+1996)",
        "RUNJOB (1995+1996+1997+1999)",
        "Mount Norikura (1976/01-1995/12)",
        "GAMMA (2004/01-2006/12) SIBYLL",
        "Haverah Park (1974/01-1987/12) QGSJet98",
        "JACEE (1979+1980+1982+1983+1984+1986+1987+1988+1990+1994+1995)",
        "Auger (2004/01-2007/08)",
        "Auger (2005/11-2008/05)",
        "Auger Hybrid (2004/01-2014/12)",
        "IceTop (2010/06-2011/05) SIBYLL2.1",
        "IceCube + IceTop (2010/06-2013/05) SIBYLL2.1",
    ]
)

# =============================================================================
# Dataframe with energy rescaling factor, when available
# Test with values from LHAASO paper 2403.11832

# Initialize DataFrame
df_test = pandas.DataFrame(data=np.ones((len(expetab), 3)),
                           index=expetab,
                           columns=["E_rescaling", "color", "marker"])

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

fig, ax = plt.subplots(1, 1, figsize=(14, 6))
axi = ax
plt.sca(axi)

for exp in expetab:
    # for i in range(0, 1):
    # exp = exp_tab[i]

    if (
        exp != "AGASA (1993/12-2002/12)"
        and exp != "NUCLEON-IC (2015/07-2017/06)"
        and exp != "HAWC (2016/06-2017/02) QGSJet-II-03"  # Keep only one dataset
        and exp != "SOKOL (1984/03-1986/01)"
        and exp != "RUNJOB (1995+1996)"
        and exp != "RUNJOB (1995+1996+1997+1999)"
        and exp != "Mount Norikura (1976/01-1995/12)"
        and exp != "GAMMA (2004/01-2006/12) SIBYLL"
        and exp != "Haverah Park (1974/01-1987/12) QGSJet98"
        and exp != "JACEE (1979+1980+1982+1983+1984+1986+1987+1988+1990+1994+1995)"
        and exp != "Auger (2004/01-2007/08)"
        and exp != "Auger (2005/11-2008/05)"
        and exp != "Auger Hybrid (2004/01-2014/12)"
        and exp != "IceCube + IceTop (2010/06-2013/05) SIBYLL2.1"
        and exp != "IceTop (2010/06-2011/05) SIBYLL2.1"
        and exp != "IceTop (2010/06-2013/05)"  # Keep only one dataset
        and exp != "IceTop (2016/05-2017/04) QGSJet-II-04"  # Keep only one dataset
        and exp != "Yakutsk (1995/01-2008/12) QGSJet01"
        and exp != "Fly's Eye (1988/06-1992/07)"
        and exp != "Auger SD750 (2014/01-2018/08)"
        and exp != "Auger Hybrid (2004/01-2016/12) QGSJet-II-04+EPOS-LHC+SIBYLL2.3"
        and exp != "KASCADE (1996/10-2002/01) QGSJet01"  # Keep only one dataset
        and exp != "KASCADE-Grande (2003/01-2009/03) QGSJet-II-04"  # ICRC
        and exp != "KASCADE-Grande (2003/12-2011/10) SIBYLL2.3"  # ICRC
        and exp != "KASCADE-Grande (2004/03-2010/12) QGSJet-II-3"  # test
        and exp != "KASCADE-Grande (2004/03-2012/05) QGSJet-II-2"  # test
        and exp
        != "DICE (1994/07-1996/03)"  # unsure, but older dataset without syst. uncert.
        and exp
        != "Maket-ANI (1997-2004) QGSJet-II-01"  # unsure, but older dataset without syst. uncert.
        and exp
        != "HEGRA (1987-1998) QGSJet"  # unsure, but older dataset without syst. uncert.
        and exp
        != "KASCADE-Grande QGSjet-II-04"  # Only one set of new KASCADE-Grande data
        and exp != "TAIGA-HiScore (2017/01-2018/12)"  # missing in latest data
        and exp
        != "TUNKA-133 Array (2009/10-2012/04) QGSJet01"  # missing in latest data
    ):

        # if (exp == 'IceTop (2016/05-2017/04) QGSJet-II-04'
        #     or exp == 'IceTop (2016/05-2017/04) SIBYLL2.1'
        #     or exp == 'IceCube+IceTop (2010/06-2013/05) SIBYLL2.1'
        #     or exp == 'IceTop (2010/06-2013/05)'):

        # if (exp == 'KASCADE (1996/10-2002/01) QGSJet01'
        #     or exp == 'KASCADE (1996/10-2002/01) SIBYLL 2.1'):

        # if (exp == 'EAS-TOP (1992/01-1999/12) QGSJet'
        #     or exp == 'HEGRA (1987-1998) QGSJet'
        #     or exp == 'Maket-ANI (1997-2004) QGSJet-II-01'
        #     or exp == 'DICE (1994/07-1996/03)'
        #     or exp == 'TAIGA-HiScore (2017/01-2018/12)'):

        # if (exp == 'GAMMA (2003/01-2007/12) SIBYLL'
        #     or exp == 'TUNKA-133 Array (2009/10-2012/04) QGSJet01'
        #     or exp == 'KASCADE-Grande EPOS-LHC'
        #     or exp == 'KASCADE-Grande (2003/01-2009/03) QGSJet-II-04'
        #     or exp == 'KASCADE-Grande (2004/03-2010/12) QGSJet-II-3'):

        # if (exp == 'TALE (2014/06/-2016/03) QGSJet-II-03'
        #     or exp == 'Telescope Array Hybrid (2008/01-2015/05)'
        #     or exp == 'Auger SD750+SD1500 (2014/01-2018/08)'):

        # if (exp == 'LHAASO EPOS-LHC'):

        print(exp)
        # tabloc = tab[tab['SUB-EXP NAME'] == exp]
        tabloc = tab[tab["SUBEXP-NAME"] == exp]
        # print(np.array(tabloc['ADS URL FOR PAPER REF'])[0])
        print(np.array(tabloc["PUBLI-HTML"])[0])
        # f = np.array(tabloc['Emean'])**expo
        f = np.array(tabloc["DATA-E_MEAN"] * df_test["E_rescaling"][exp]) ** expo
        print(df_test["E_rescaling"][exp])

        fL = np.array(tabloc["DATA-E_BIN_L"]) ** expo
        fU = np.array(tabloc["DATA-E_BIN_U"]) ** expo
        ic = np.argwhere(expetab == exp).item()
        # xdat = np.array(tabloc['Emean'])
        xdat = np.array(tabloc["DATA-E_MEAN"]) * df_test["E_rescaling"][exp]

        # if exp == 'Telescope Array Hybrid (2008/01-2015/05)':
        #     eloc = tabloc['DATA-E_MEAN']\
        #         * (1.-(5.+5./2.*(np.log10(tabloc['DATA-E_MEAN'])-10.))/100.)
        #     print(eloc)
        #     f = np.array(eloc)**expo
        #     xdat = np.array(eloc)

        # ydat = np.array(tabloc['QUANTITY VALUE: [#/sr/s/m2/EAxis] if flux'] * f)
        ydat = np.array(tabloc["DATA-VAL"] * f)
        # ysta = (np.array([tabloc['ERR_STAT-'], tabloc['ERR_STAT+']]) * f)
        ysta = (
            np.array([tabloc["DATA-VAL_ERRSTAT_L"], tabloc["DATA-VAL_ERRSTAT_U"]]) * f
        )
        # ysys = (np.array([tabloc['ERR_SYST-'], tabloc['ERR_SYST+']]) * f)
        ysys = (
            np.array([tabloc["DATA-VAL_ERRSYST_L"], tabloc["DATA-VAL_ERRSYST_U"]]) * f
        )
        # xerr = np.abs(tabloc['EBIN_HIGH'] - x)
        xerr = None
        # is_ul = np.array(tabloc['IS UPPER LIMIT: format = 0 or 1']) == 1
        is_ul = np.array(tabloc["DATA-ISUPPERLIM"]) == 1

        # =====================================================================
        # Play with data: try to overlap
        # if exp == 'DICE (1994/07-1996/03)':
        #     ydat *= 1.4
        # if exp == 'TALE (2014/06/-2016/03) QGSJet-II-03':
        #     ydat *= 1.3
        # if exp == 'Telescope Array Hybrid (2008/01-2015/05)':
        #     ydat *= 1.2
        # if exp == 'GAMMA (2003/01-2007/12) SIBYLL':
        #     ydat *= 1.1
        # if exp == 'KASCADE-Grande (2003/01-2009/03) QGSJet-II-04':
        #     ydat *= 1.5
        # if exp == 'KASCADE-Grande (2003/12-2011/10) SIBYLL2.3':
        #     ydat *= 1.4
        # if exp == 'KASCADE-Grande (2004/03-2010/12) QGSJet-II-3':
        #     ydat *= 1.4
        # if exp == 'Auger Hybrid (2004/01-2016/12) QGSJet-II-04+EPOS-LHC+SIBYLL2.3':
        #     ydat *= 1.4
        # if exp == 'Auger SD750 (2014/01-2018/08)':
        #     ydat *= 1.4
        # if exp == 'Auger SD750+SD1500 (2014/01-2018/08)':
        #     ydat *= 1.4
        # =====================================================================

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
            plot_err_systematic=plot_err_systematic
        )
        # color=colortab[ic],
        # marker=markertab[ic])

# =============================================================================
# Not sure to understant the arrow representation of
# energy-related systematic uncertainties
# Is it supposed to be symmetric?

# ax.annotate(text='', xy=(2e4*(1-0.21), 5e6*(1-0.63)), xytext=(2e4, 5e6), arrowprops=dict(arrowstyle='->'))
# ax.annotate(text='', xy=(2e10, 4e6), xytext=(2e10*(1+0.41), 4e6*(1+1.26)), arrowprops=dict(arrowstyle='<->'))
# ax.scatter([2e10*(1+0.41/2)], [4e6*(1+1.26/2)], marker='o', color='k', zorder=10)
# ax.text(3e10*(1+0.41/2), 4e6*(1+1.26/2), s=r'$\sigma_{E, sys} - TA$')
# plt.annotate(s='', xy=(1,1), xytext=(0,0), arrowprops=dict(arrowstyle='<->'))

# ax.scatter([2e10*(1-0.21)], [4e6*(1-0.63)], marker='o', color='k', zorder=10)
# ax.scatter([2e10], [4e6], marker='o', color='k', zorder=10)
# ax.scatter([2e10*(1+0.21)], [4e6*(1+0.63)], marker='o', color='k', zorder=10)
# =============================================================================

ax.loglog()
ax.set_xlabel(r"$E$ [GeV]")
ax.set_xlim(1e4, 3e11)
ax.set_ylim(1e5, 1e7)

if expo == 1:
    plt.ylabel(r"$E$ d$J$/d$E$ [1/(m$^2$ s sr)]")
else:
    plt.ylabel(f"$E^{{{expo}}}$ d$J$/d$E$ " f"[GeV$^{{{expo - 1}}}$ / (m$^2$ s sr)]")

# draw_logo(0, 0.98, height=0.05)

# tab_TA = 10**np.loadtxt('TA_update.csv', skiprows=1, delimiter=',')
# plt.plot(tab_TA[:, 0]/1e9*0.95, tab_TA[:, 1]/1e18*0.95**3, marker='o', color='r')

ax.legend(frameon=False, ncol=2, loc=3, fontsize=10)
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.94)

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
    transform=ax.get_xaxis_transform(),
    ha="center",
    va="bottom",
)
plt.text(
    Econcave,
    1.02,
    "Hardening",
    fontsize=14,
    transform=ax.get_xaxis_transform(),
    ha="center",
    va="bottom",
)
plt.text(
    Eknee_2,
    1.02,
    "Second Knee",
    fontsize=14,
    transform=ax.get_xaxis_transform(),
    ha="center",
    va="bottom",
)

plt.text(
    E12_TA,
    1.02,
    "Ankle",
    fontsize=14,
    transform=ax.get_xaxis_transform(),
    ha="center",
    va="bottom",
)
plt.text(
    E23_TA,
    1.02,
    "Instep",
    fontsize=14,
    transform=ax.get_xaxis_transform(),
    ha="center",
    va="bottom",
)
plt.text(
    E34_TA,
    1.02,
    "Suppression",
    fontsize=14,
    transform=ax.get_xaxis_transform(),
    ha="center",
    va="bottom",
)

if plot_err_systematic:
    plt.savefig(path_fig / "fluxes_syst.pdf")
else:
    plt.savefig(path_fig / "fluxes.pdf")
