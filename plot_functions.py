"""
Plotting functions for figures.

Created on Fri Oct  2 17:48:14 2026

@author: claireguepin
"""

import numpy as np
from typing import Any, Optional
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt


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
