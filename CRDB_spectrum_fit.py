"""
Figure for one cosmic ray spectrum and fit.

From https://github.com/crdb-project/tutorial/blob/main/gallery.ipynb
Created on Wed Nov 29 16:08:56 2023

@author: claireguepin
"""

import datetime
import logging
from pathlib import Path
from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pandas
from matplotlib.lines import Line2D
from scipy.optimize import curve_fit

from plot_functions import draw_with_errorbars
from plot_styles import get_plot_styles

# =============================================================================
# FIGURES OPTIONS
path_fig = Path("./figures/spectral_fits/fig")
path_fig.mkdir(parents=True, exist_ok=True)
path_log = Path("./figures/spectral_fits/log")
path_log.mkdir(parents=True, exist_ok=True)

# Get styles from the config file
e_rescaling, color_map, marker_map = get_plot_styles()

# =============================================================================
# PARAMETERS

# Knee
Emin = 1e5
Emax = 2e7
index_low = -2.7 + 3
index_high = -3.2 + 3

# # Hardening
# Emin = 8e6
# Emax = 1e8
# index_low = -3.2+3
# index_high = -2.7+3

# # Second knee
# Emin = 2e7
# Emax = 1e9
# index_low = -2.7+3
# index_high = -3.2+3


# =============================================================================
# FUNCTION FOR CURVE FITTING


def broken_power_law_logx(log_x, log_A, log_x_break, gamma1, gamma2):
    log_ratio = log_x - log_x_break
    return np.where(
        log_x < log_x_break,
        10 ** (log_A + gamma1 * log_ratio),
        10 ** (log_A + gamma2 * log_ratio),
    )


# =============================================================================
# LOAD CUSTOM DATA

# tab = pandas.read_csv('CRDB_Data/Flux_crdb_import_mod.csv',
# tab = pandas.read_csv('CRDB_Data/Flux_crdb_import_mod_new.csv',
#                       header=0, delimiter=',')
tab = pandas.read_csv("./CRDB_Data/Flux_crdb_Sep2026.csv", header=0, delimiter=",")
exp_tab = pandas.unique(tab["SUBEXP-NAME"])

# FIGURE OPTIONS
exponents = 0.0
expo = exponents
plot_err_systematic = True

# DETECTORS
expetab = np.array(
    [
        # 'TAIGA-HiScore (2017/01-2018/12)',
        # 'EAS-TOP (1992/01-1999/12) QGSJet',
        # 'IceTop (2016/05-2017/04) SIBYLL2.1',
        "IceCube+IceTop (2010/06-2013/05) SIBYLL2.1",
        # 'KASCADE (1996/10-2002/01) SIBYLL 2.1',
        # 'KASCADE-Grande (2004/03-2010/12) QGSJet-II-3',
        # 'KASCADE-Grande EPOS-LHC',
        # 'GAMMA (2003/01-2007/12) SIBYLL',
        # 'TUNKA-133 Array (2009/10-2012/04) QGSJet01',
        # 'TALE (2014/06/-2016/03) QGSJet-II-03',
        # 'Auger SD750+SD1500 (2014/01-2018/08)',
        # 'LHAASO EPOS-LHC',
    ]
)

name = expetab[0].replace(" ", "").replace("(", "_").replace(")", "_").replace("/", "_")

# =============================================================================
# Dataframe with data and figure properties

df_test = pandas.DataFrame(
    data=np.ones((len(expetab), 3)),
    index=expetab,
    columns=["E_rescaling", "color", "marker"],
)
df_test["color"][expetab[0]] = "#d62728"
df_test["marker"][expetab[0]] = "o"

# =============================================================================
# LOGGING

# Define the log file name
log_filename = (
    path_log / f"fit_results_{name}_{datetime.datetime.now().strftime('%Y%m%d')}.log"
)

# Set up the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the logging level

# Clear existing handlers (to avoid duplicate logs)
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Add a new file handler with the updated filename
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)

# Add a console handler (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define the log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# =============================================================================
# FIGURE FOR REVIEW

fig, ax = plt.subplots(1, 1, figsize=(14, 6))
axi = ax
plt.sca(axi)

exp = expetab[0]
logging.info("=" * 50)
logging.info(exp)
logging.info(df_test["E_rescaling"][exp])

tabloc = tab[tab["SUBEXP-NAME"] == exp]
xdat = np.array(tabloc["DATA-E_MEAN"]) * df_test["E_rescaling"][exp]
xdat_relerr = np.array(tabloc["SUBEXP-ESCALE_RELERR"])
f = xdat**expo
ydat = np.array(tabloc["DATA-VAL"] * f)
ysta = np.array([tabloc["DATA-VAL_ERRSTAT_L"], tabloc["DATA-VAL_ERRSTAT_U"]]) * f
ysys = np.array([tabloc["DATA-VAL_ERRSYST_L"], tabloc["DATA-VAL_ERRSYST_U"]]) * f
xerr = None
is_ul = np.array(tabloc["DATA-ISUPPERLIM"]) == 1

# Case for IceCube: add IceTop data
if exp == "IceCube+IceTop (2010/06-2013/05) SIBYLL2.1":
    expetab_low = np.array(["IceTop (2016/05-2017/04) SIBYLL2.1"])
    exp_low = expetab_low[0]
    tabloc = tab[tab["SUBEXP-NAME"] == exp_low]
    xdat_low = np.array(tabloc["DATA-E_MEAN"]) * df_test["E_rescaling"][exp] * 0.97
    xdat_low_relerr = np.array(tabloc["SUBEXP-ESCALE_RELERR"])
    f = xdat_low**expo
    ydat_low = np.array(tabloc["DATA-VAL"] * f)
    ysta_low = (
        np.array([tabloc["DATA-VAL_ERRSTAT_L"], tabloc["DATA-VAL_ERRSTAT_U"]]) * f
    )
    ysys_low = (
        np.array([tabloc["DATA-VAL_ERRSYST_L"], tabloc["DATA-VAL_ERRSYST_U"]]) * f
    )
    xerr_low = None
    is_ul_low = np.array(tabloc["DATA-ISUPPERLIM"]) == 1
    xdat = np.concatenate((xdat_low, xdat))
    ydat = np.concatenate((ydat_low, ydat))
    ysta = np.concatenate((ysta_low, ysta), axis=1)
    ysys = np.concatenate((ysys_low, ysys), axis=1)
    is_ul = np.concatenate((is_ul_low, is_ul))

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
ax.loglog()
ax.set_xlabel(r"$E$ [GeV]")
# ax.set_xlim(1e4, 3e11)
# ax.set_ylim(1e5, 1e7)

if expo == 1:
    plt.ylabel(r"$E$ d$J$/d$E$ [1/(m$^2$ s sr)]")
else:
    plt.ylabel(f"$E^{{{expo}}}$ d$J$/d$E$ " f"[GeV$^{{{expo - 1}}}$ / (m$^2$ s sr)]")

ax.legend(frameon=False, ncol=2, loc=3, fontsize=10)
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.94)
plt.show()

# =============================================================================
# Fit in log space

expo = 3
f = xdat**expo
log_xdat = np.log10(xdat)

# Define energy range for the fit
rangeE = (xdat > Emin) * (xdat < Emax)

# Initial guess in log-space
log_initial_guess = [
    np.log10(np.median((ydat * f)[rangeE])),
    np.log10(np.median(xdat[rangeE])),
    index_low,
    index_high,
]
bounds = ([4, 5, -4, -4], [8, 10, 4, 4])

# # Initial guess in log-space
# log_initial_guess = [
#     np.log10(np.median((ydat*f)[rangeE])),
#     np.log10(np.median(xdat[rangeE])),
#     -2.7+3,
#     -3.1+3,
# ]
# bounds = (
#     [4, 9, -4, -4],
#     [8, 10, 4, 4]
# )

popt, pcov = curve_fit(
    broken_power_law_logx,
    log_xdat[rangeE],
    (ydat * f)[rangeE],
    p0=log_initial_guess,
    sigma=np.mean([(ysta * f)[0][rangeE], (ysta * f)[1][rangeE]], axis=0),
    maxfev=10000,
    bounds=bounds,
)

# Extract and convert back to linear space
log_A_fit, log_x_break_fit, gamma1_fit, gamma2_fit = popt
A_fit = 10**log_A_fit
x_break_fit = 10**log_x_break_fit
logging.info("=" * 50)
logging.info("FITTED PARAMETERS")
logging.info(
    f"Fitted Parameters: A_3={A_fit}, x_break_3={x_break_fit}, gamma1_3={gamma1_fit-3}, gamma2_3={gamma2_fit-3}"
)
logging.info(f"E knee = {x_break_fit*1e-9} EeV")
logging.info(f"Spectral index below = {gamma1_fit-3}")
logging.info(f"Spectral index above = {gamma2_fit-3}")

# Extract parameter uncertainties from the covariance matrix
parameter_errors = np.sqrt(np.diag(pcov))
A_err, x_break_err, gamma1_err, gamma2_err = parameter_errors
logging.info("=" * 50)
logging.info("PARAMETERS UNCERTAINTIES FROM THE COVARIANCE MATRIX")
logging.info(f"E knee err = {x_break_err*1e-9} EeV")
logging.info(
    f"E knee err (based on relative error) = {x_break_fit*1e-9*np.max(xdat_relerr)} EeV"
)
logging.info(f"Spectral index below err = {gamma1_err}")
logging.info(f"Spectral index above err = {gamma2_err}")

# Generate fitted values for plotting
log_x_fit_3 = np.linspace(min(log_xdat), max(log_xdat), 100)
x_fit_3 = 10**log_x_fit_3
y_fit_3 = broken_power_law_logx(log_x_fit_3, *popt)

fig, ax = plt.subplots(1, 1, figsize=(14, 6))
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.94)

draw_with_errorbars(
    xdat,
    ydat * f,
    ysta * f,
    ysys * f,
    xerr,
    is_ul,
    label=exp,
    sys_lw=5,
    color=df_test["color"][exp],
    marker=df_test["marker"][exp],
    plot_err_systematic=plot_err_systematic,
)

plt.plot(x_fit_3, y_fit_3)

# plt.axvline(x=x_fit[np.argmax(y_fit*x_fit**expo)], ls='--')
# plt.plot(x_fit, x_fit**(3+gamma1_fit)/(x_fit[0]**(3+gamma1_fit))*(ydat*f)[0])
# plt.plot(x_fit, x_fit**(3+gamma2_fit)/(x_fit[-1]**(3+gamma2_fit))*(ydat*f)[-1])

ax.loglog()
ax.set_xlim(np.min(xdat), np.max(xdat))
# ax.set_ylim(3e6, 6e6)
ax.set_xlabel(r"$E$ [GeV]")
if expo == 1:
    plt.ylabel(r"$E$ d$J$/d$E$ [1/(m$^2$ s sr)]")
else:
    plt.ylabel(f"$E^{{{expo}}}$ d$J$/d$E$ " f"[GeV$^{{{expo - 1}}}$ / (m$^2$ s sr)]")
filename = f"Spectrum_bestfit_{name}.pdf"
plt.savefig(path_fig / filename)
plt.show

# =============================================================================
# MONTE CARLO TO EVALUATE THE ERROR

# energy to power expo
f = xdat**expo

# Assume x_err is the uncertainty on xdat (e.g., from energy resolution)
x_err = xdat_relerr[0] * xdat

# Number of Monte Carlo iterations
n_iterations = 1000
fitted_params = np.zeros((n_iterations, 4))

# Initial guess in log-space
log_initial_guess = [
    np.log10(np.median((ydat * f)[rangeE])),
    np.log10(np.median(xdat[rangeE])),
    -2.7 + 3,
    -3.2 + 3,
]
bounds = ([4, 5, -4, -4], [8, 10, 4, 4])

fig, ax = plt.subplots(1, 1, figsize=(14, 6))
fig.subplots_adjust(left=0.1, bottom=0.1, right=0.95, top=0.94)
plt.plot(xdat, ydat * f, color="k")
plt.axvline()
ax.loglog()
ax.set_xlim(np.min(xdat), np.max(xdat))
ax.set_ylim(1e6, 1e7)
ax.set_xlabel(r"$E$ [GeV]")
if expo == 1:
    plt.ylabel(r"$E$ d$J$/d$E$ [1/(m$^2$ s sr)]")
else:
    plt.ylabel(f"$E^{{{expo}}}$ d$J$/d$E$ " f"[GeV$^{{{expo - 1}}}$ / (m$^2$ s sr)]")

ysta[0] = np.sqrt(ysta[0] ** 2 + ysys[0] ** 2)
ysta[1] = np.sqrt(ysta[1] ** 2 + ysys[1] ** 2)

for i in range(n_iterations):
    # Perturb xdat and ydat with their uncertainties
    xdat_perturbed = xdat * (1 + np.random.normal(0, xdat_relerr[0]))
    ydat_perturbed = ydat + np.random.normal(0, np.mean([ysta[0], ysta[1]], axis=0))

    plt.plot(xdat_perturbed, ydat_perturbed * xdat**expo)
    # plt.plot(xdat_perturbed, ydat_perturbed*xdat_perturbed**expo)

    # Transform to log-space for x
    log_xdat_perturbed = np.log10(xdat_perturbed)

    # Fit the model
    try:
        popt, _ = curve_fit(
            broken_power_law_logx,
            log_xdat_perturbed[rangeE],
            (ydat_perturbed * xdat**expo)[rangeE],
            # (ydat_perturbed*xdat_perturbed**expo)[rangeE],
            p0=log_initial_guess,
            maxfev=10000,
            bounds=bounds,
        )
        fitted_params[i] = popt
    except RuntimeError:
        # Skip failed fits (optional: handle or retry)
        continue

filename = f"MonteCarlo_spectra_{name}.pdf"
plt.savefig(path_fig / filename)
plt.show

# Compute mean and standard deviation of fitted parameters
param_means = np.nanmean(fitted_params, axis=0)
param_errors = np.nanstd(fitted_params, axis=0)

#  Convert back to linear space for A and x_break
log_A_fit, log_x_break_fit, gamma1_fit, gamma2_fit = param_means
A_fit, x_break_fit = 10**log_A_fit, 10**log_x_break_fit

# Uncertainties in linear space for A and x_break
A_err = A_fit * np.log(10) * param_errors[0]  # Error propagation for log(A)
x_break_err = (
    x_break_fit * np.log(10) * param_errors[1]
)  # Error propagation for log(x_break)

# Uncertainties for gamma1 and gamma2 (already in linear space)
gamma1_err, gamma2_err = param_errors[2], param_errors[3]

logging.info("=" * 50)
logging.info("MONTE CARLO")
logging.info(
    f"Fitted Parameters: A={A_fit} ± {A_err}, x_break={x_break_fit} ± {x_break_err}, gamma1={gamma1_fit-3} ± {gamma1_err}, gamma2={gamma2_fit-3} ± {gamma2_err}"
)

# =============================================================================
# VISUALIZE THE DISTRIBUTIONS

# Extract the fitted parameter samples from Monte Carlo
A_samples = 10 ** fitted_params[:, 0]  # Convert log_A back to linear
x_break_samples = 10 ** fitted_params[:, 1]  # Convert log_x_break back to linear
gamma1_samples = fitted_params[:, 2]
gamma2_samples = fitted_params[:, 3]

# Create a figure with subplots for each parameter
fig, axes = plt.subplots(2, 2, figsize=(12, 7))
fig.suptitle("Monte Carlo Parameter Distributions", fontsize=14)

# Histogram for A
axes[0, 0].hist(A_samples, bins=30, alpha=0.7, color="C0", edgecolor="black")
axes[0, 0].axvline(
    A_fit, color="red", linestyle="--", linewidth=2, label=f"Mean: {A_fit:.2e}"
)
axes[0, 0].set_title("Normalization (A)")
axes[0, 0].set_xlabel("A")
axes[0, 0].legend()

# Histogram for x_break
axes[0, 1].hist(x_break_samples, bins=30, alpha=0.7, color="C1", edgecolor="black")
axes[0, 1].axvline(
    x_break_fit,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Mean: {x_break_fit:.2e}",
)
axes[0, 1].set_title("Break Energy")
axes[0, 1].set_xlabel(r"$x_{\rm break}$ (eV)")
axes[0, 1].legend()

# Histogram for gamma1
axes[1, 0].hist(
    gamma1_samples - 3, bins=30, alpha=0.7, color="C2", edgecolor="black"
)
axes[1, 0].axvline(
    gamma1_fit - 3,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Mean: {gamma1_fit-3:.3f}",
)
axes[1, 0].set_title("Spectral Index 1")
axes[1, 0].set_xlabel(r"$\gamma_1$")
axes[1, 0].legend()

# Histogram for gamma2
axes[1, 1].hist(
    gamma2_samples - 3, bins=30, alpha=0.7, color="C3", edgecolor="black"
)
axes[1, 1].axvline(
    gamma2_fit - 3,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Mean: {gamma2_fit-3:.3f}",
)
axes[1, 1].set_title("Spectral Index 2")
axes[1, 1].set_xlabel(r"$\gamma_2$")
axes[1, 1].legend()

plt.tight_layout()
filename = f"MonteCarlo_histograms_{name}.pdf"
plt.savefig(path_fig / filename)
plt.show()
