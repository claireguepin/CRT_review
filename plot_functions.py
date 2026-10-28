"""
Plotting functions for figures.

Created on Fri Oct  2 17:48:14 2026

@author: claireguepin
"""

from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.collections as mc
import pandas as pd


def read_xmax_file(filename, moment="mean"):
    """
    Reads Xmax data from a .dat file and returns arrays for energy, moment values,
    statistical errors, and systematic errors.

    Parameters
    ----------
    filename : str
        Path to the .dat file.
    moment : str
        Which moment to read (e.g., "mean", "sigma"). Default is "mean".

    Returns
    -------
    x : np.ndarray
        Energy array (meanlgE).
    y : np.ndarray or None
        Requested moment values (e.g., meanXmax), or None if missing.
    ystat : np.ndarray or None
        Statistical errors, or None if missing.
    ysys_up : np.ndarray or None
        Upper systematic errors, or None if missing.
    ysys_dn : np.ndarray or None
        Lower systematic errors, or None if missing.
    """
    # Read the .dat file
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Parse header to get column names
    header = lines[0].strip()
    column_names = header.split(' ')

    # Read data rows into a DataFrame
    data = []
    for line in lines[1:]:
        # Skip empty lines and comments
        if line.strip() and not line.strip().startswith('#'):
            values = line.strip().split(' ')
            data.append(values)

    df = pd.DataFrame(data, columns=column_names)

    # Extract the required columns dynamically
    x = df['meanlgE'].astype(float).values

    # Determine the moment columns based on the input
    y_col = f"{moment}Xmax"
    ystat_col = f"{moment}Xmax_staterr"
    ysys_up_col = f"{moment}Xmax_syserr_up"
    ysys_dn_col = f"{moment}Xmax_syserr_dn"

    # Safely extract columns (return None if missing)
    y = df[y_col].astype(float).values if y_col in df.columns else None
    ystat = df[ystat_col].astype(
        float).values if ystat_col in df.columns else None
    ysys_up = df[ysys_up_col].astype(
        float).values if ysys_up_col in df.columns else None
    ysys_dn = df[ysys_dn_col].astype(
        float).values if ysys_dn_col in df.columns else None

    return x, y, ystat, ysys_up, ysys_dn


def draw_with_errorbars(
    x: np.ndarray,
    y: np.ndarray,
    ysta: np.ndarray,
    ysys: np.ndarray,
    xerr: Optional[np.ndarray],
    is_ul: np.ndarray,
    label: Optional[str],
    sys_lw: float,
    color: str,
    marker: str,
    plot_err_systematic: bool,
    **kwargs: Any,
) -> Line2D:
    """Plot data with statistical and systematic errors."""
    ysta = np.abs(ysta)
    ysys = np.abs(ysys)
    if xerr is not None:
        xerr = np.abs(xerr)

    is_pt = ~is_ul
    lines = None

    for mask in (is_pt, is_ul):
        if not np.any(mask):
            continue

        xm = x[mask]
        ym = y[mask]
        ystam = ysta[:, mask]
        ysysm = ysys[:, mask]

        if xerr is None:
            xerrm = None
        else:
            xerrm = xerr[..., mask]

        # for upper limits: shrink stat errors
        if mask is is_ul:
            ystam = 0.2 * ym

        # ----- STATISTICAL ERRORS -----
        lines = plt.errorbar(
            xm,
            ym,
            ystam,
            xerrm,
            color=color,
            marker=marker,
            markersize=6,
            zorder=3,
            uplims=(mask is is_ul),
            ls="none",
            label=label if lines is None else None,
            **kwargs,
        )[0]

        # ----- SYSTEMATIC ERRORS -----
        if plot_err_systematic and (mask is is_pt):
            # draw vertical systematic error bars at each x
            for xi, yi, ylow, yhigh in zip(xm, ym, ysysm[0], ysysm[1]):
                dx = xi * (10**0.02 - 1)  # ~ 2% width
                plt.fill_between(
                    [xi - dx, xi + dx],
                    yi - ylow,
                    yi + yhigh,
                    color=color,
                    alpha=0.5,
                    zorder=1,
                    edgecolor="none",
                )

    return lines


def draw_with_errorbars_xmax(
    x, y,
    ysta=None,
    ysys=None,
    color="k",
    marker="o",
    label=None,
    xw=None,
    alpha_sta=0.8,
    alpha_sys=0.3,
    linewidth_sta=2,
    linewidth_sys=4,
    ax=None
):
    """
    Draw points with statistical and systematic errors, with distinct styles.

    Parameters
    ----------
    x, y : array-like
        Data points
    ysta : array-like, optional
        Statistical errors (symmetric)
    ysys : array-like, shape (2, N), optional
        Systematic errors (asymmetric, [down, up])
    color : str
        Color of points and error bars
    marker : str
        Marker style
    label : str
        Label for legend
    xw : float, optional
        Width of error bar caps. Defaults to 3% of x-range.
    alpha_sta : float
        Transparency of statistical error bars
    alpha_sys : float
        Transparency of systematic error bars
    linewidth_sta : float
        Line width of statistical error bars
    linewidth_sys : float
        Line width of systematic error bars
    ax : matplotlib.axes.Axes, optional
        Axes to draw on. If None, uses current axes.
    """
    print("x length:", len(x))
    print("y length:", len(y) if y is not None else "None")
    print("ystat length:", len(ysta) if ysta is not None else "None")
    print("ysys:", len(ysys) if ysys is not None else "None")

    if ax is None:
        ax = plt.gca()

    x = np.asarray(x)
    y = np.asarray(y)

    print(x)
    # Determine cap width
    if xw is None:
        xw = 0.03 * (np.max(x) - np.min(x))

    lines = []

    # --- Statistical errors (symmetric) ---
    if ysta is not None:
        ysta = np.asarray(ysta)
        for xi, yi, dy in zip(x, y, ysta):
            # # horizontal caps
            # lines.append([(xi - xw, yi + dy), (xi + xw, yi + dy)])
            # lines.append([(xi - xw, yi - dy), (xi + xw, yi - dy)])
            # vertical stems
            lines.append([(xi, yi + dy), (xi, yi - dy)])

        lc_sta = mc.LineCollection(
            lines, colors=color, linewidths=linewidth_sta, alpha=alpha_sta)
        ax.add_collection(lc_sta)
        lines.clear()  # reset for systematic bars

    # --- Systematic errors (asymmetric) ---
    if ysys is not None:
        ysys = np.asarray(ysys)
        ylo, yhi = ysys
        print(ylo)

        # Convert to lists
        ylo = list(ylo) if ylo is not None else []
        yhi = list(yhi) if yhi is not None else []

        # If all entries are None, skip systematic errors
        if all(v is None for v in ylo) and all(v is None for v in yhi):
            ylo = yhi = []

        # Only loop if lengths match x and y
        if len(ylo) == len(yhi) == len(x):
            for xi, yi, lo, hi in zip(x, y, ylo, yhi):
                if lo is None or hi is None:
                    continue  # skip missing
                # # horizontal caps
                # lines.append([(xi - xw, yi + hi), (xi + xw, yi + hi)])
                # lines.append([(xi - xw, yi - lo), (xi + xw, yi - lo)])
                # vertical stems
                lines.append([(xi, yi + hi), (xi, yi - lo)])

        lc_sys = mc.LineCollection(
            lines, colors=color, linewidths=linewidth_sys, alpha=alpha_sys)
        ax.add_collection(lc_sys)

    # Draw markers on top
    scatter = ax.scatter(x, y, color=color, marker=marker, label=label)
    return scatter
