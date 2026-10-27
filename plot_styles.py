"""
Plotting styles for figures.

Created on Fri Oct  2 17:48:14 2026

@author: claireguepin
"""
import matplotlib.pyplot as plt


def get_plot_styles():
    """Return dictionaries for E_rescaling, color, and marker styles."""
    # Define general plotting styles
    plt.rcParams["font.family"] = "STIXGeneral"
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams["font.size"] = 16
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    plt.rcParams["xtick.top"] = True
    plt.rcParams["ytick.right"] = True

    e_rescaling = {
        'HAWC (2016/06-2017/02) QGSJet-II-03': 0.940,
        'HAWC (2018-2019) QGSJet-II-04': 0.940,
        'Tunka-133 (2009/10-2012/04) QGSJet01': 0.955,
        'Auger Hybrid (2004/01-2016/12) QGSJet-II-04+EPOS-LHC+SIBYLL2.3': 1.,
        'Auger SD750 (2014/01-2018/08)': 1.,
        'Auger SD750+SD1500 (2014/01-2018/08)': 1.,
        'Auger (2004/01-2007/08)': 1.,
        'Auger (2005/11-2008/05)': 1.,
        'Auger Hybrid (2004/01-2014/12)': 1.,
        'IceTop (2016/05-2017/04) QGSJet-II-04': 0.980,
        'IceTop (2016/05-2017/04) SIBYLL2.1': 0.980,
        'IceTop (2010/06-2013/05)': 0.980,
        'IceTop (2010/06-2011/05) SIBYLL2.1': 0.980,
        'IceCube+IceTop (2010/06-2013/05) SIBYLL2.1': 0.960,
        'IceCube + IceTop (2010/06-2013/05) SIBYLL2.1': 0.960,
        'KASCADE (1996/10-2002/01) QGSJet01': 0.980,
        'KASCADE (1996/10-2002/01) SIBYLL 2.1': 0.980,
        'KASCADE-Grande (2003/01-2009/03) QGSJet-II-04': 1.,
        'KASCADE-Grande (2003/12-2009/03) QGSJet-II-2': 1.,
        'KASCADE-Grande (2003/12-2011/10) SIBYLL2.3': 1.,
        'KASCADE-Grande (2004/03-2010/12) QGSJet-II-3': 1.,
        'KASCADE-Grande (2004/03-2012/05) QGSJet-II-2': 1.,
        'KASCADE-Grande EPOS-LHC': 1.08,
        'KASCADE-Grande (2003/01-2006/08) QGSJet-II.04': 1.08,
        'TALE (2014/06/-2016/03) QGSJet-II-03': 1.,  # 0.99
        'Telescope Array Hybrid (2008/01-2015/05)': 0.945,
        'Telescope Array SD (2008/05 - 2024/05)': 0.945,
        'TA SD (2008/05-2019/05)': 0.945,
        'NUCLEON-KLEM (2015/07-2017/06)': 0.92,
        'EAS-TOP (1992/01-1999/12) QGSJet': 0.92,
        'TAIGA-HiScore (2017/01-2018/12)': 0.96,
        'LHAASO-KM2A (2021/09-2022/12) EPOS-LHC': 1.0
    }

    colors = {
        'NUCLEON-KLEM (2015/07-2017/06)': '#1f77b4',
        'HAWC (2016/06-2017/02) QGSJet-II-03': '#ff7f0e',
        'HAWC (2018-2019) QGSJet-II-04': '#2ca02c',
        'TAIGA-HiScore (2017/01-2018/12)': '#d62728',
        'LHAASO EPOS-LHC': "C6",
        "LHAASO-KM2A (2021/09-2022/12) EPOS-LHC": "C6",
        'EAS-TOP (1992/01-1999/12) QGSJet': '#9467bd',
        'Maket-ANI (1997-2004) QGSJet-II-01': '#8c564b',
        'DICE (1994/07-1996/03)': '#e377c2',
        'HEGRA (1987-1998) QGSJet': '#7f7f7f',
        'IceTop (2016/05-2017/04) QGSJet-II-04': '#bcbd22',
        'IceCube Hybrid (2010/06-2013/05) SIBYLL2.1': '#ff7f0e',
        'IceCube+IceTop (2010/06-2013/05) SIBYLL2.1': '#1f77b4',
        'IceTop (2010/06-2013/05)': '#ff7f0e',
        "IceTop (2016/05-2017/04) SIBYLL2.1": "#17becf",
        'KASCADE (1996/10-2002/01) QGSJet01': '#2ca02c',
        'KASCADE (1996/10-2002/01) SIBYLL 2.1': '#d62728',
        'KASCADE-Grande (2003/01-2009/03) QGSJet-II-04': '#9467bd',
        'KASCADE-Grande (2003/12-2009/03) QGSJet-II-2': '#8c564b',
        'KASCADE-Grande (2003/12-2011/10) SIBYLL2.3': '#e377c2',
        'KASCADE-Grande (2004/03-2010/12) QGSJet-II-3': '#7f7f7f',
        'KASCADE-Grande (2004/03-2012/05) QGSJet-II-2': '#bcbd22',
        'KASCADE-Grande EPOS-LHC': "#7f7f7f",
        "KASCADE-Grande (2003/01-2006/08) QGSJet-II.04": "#7f7f7f",
        'GAMMA (2003/01-2007/12) SIBYLL': '#17becf',
        'Tunka-133 (2009/10-2012/04) QGSJet01': '#1f77b4',
        'TALE (2014/06/-2016/03) QGSJet-II-03': '#ff7f0e',
        'Telescope Array Hybrid (2008/01-2015/05)': '#2ca02c',
        'Telescope Array SD (2008/05 - 2024/05)': '#2ca02c',
        "TA SD (2008/05-2019/05)": "#2ca02c",
        'Auger FD (2004/12-2012/12) EPOS-LHC': '#d62728',
        'Auger FD (2004/12-2012/12) QGSJet-II-04': '#9467bd',
        'Auger FD (2004/12-2012/12) SIBYLL2.1': '#8c564b',
        "Auger SD750+SD1500 (2014/01-2018/08)": "#8c564b",
        'Yakutsk (1995/01-2008/12) QGSJet01': '#e377c2',
        "Fly's Eye (1988/06-1992/07)": '#7f7f7f',
        'AGASA (1993/12-2002/12)': '#bcbd22',
        'NUCLEON-IC (2015/07-2017/06)': '#17becf',
        'SOKOL (1984/03-1986/01)': '#1f77b4',
        'RUNJOB (1995+1996)': '#ff7f0e',
        'RUNJOB (1995+1996+1997+1999)': '#2ca02c',
        'Mount Norikura (1976/01-1995/12)': '#d62728',
        'GAMMA (2004/01-2006/12) SIBYLL': '#9467bd',
        'Haverah Park (1974/01-1987/12) QGSJet98': '#8c564b',
        'JACEE (1979+1980+1982+1983+1984+1986+1987+1988+1990+1994+1995)': '#e377c2',
        'Auger (2004/01-2007/08)': '#7f7f7f',
        'Auger (2005/11-2008/05)': '#bcbd22',
        'Auger Hybrid (2004/01-2014/12)': '#17becf',
        'IceTop (2010/06-2011/05) SIBYLL2.1': '#1f77b4',
        'IceCube + IceTop (2010/06-2013/05) SIBYLL2.1': '#ff7f0e'
        }

    markers = {
        'NUCLEON-KLEM (2015/07-2017/06)': 'o',
        'HAWC (2016/06-2017/02) QGSJet-II-03': 'o',
        'HAWC (2018-2019) QGSJet-II-04': 'o',
        'TAIGA-HiScore (2017/01-2018/12)': 'o',
        'LHAASO EPOS-LHC': "o",
        "LHAASO-KM2A (2021/09-2022/12) EPOS-LHC": "o",
        'EAS-TOP (1992/01-1999/12) QGSJet': 'o',
        'Maket-ANI (1997-2004) QGSJet-II-01': 'o',
        'DICE (1994/07-1996/03)': 'o',
        'HEGRA (1987-1998) QGSJet': 'o',
        'IceTop (2016/05-2017/04) QGSJet-II-04': 'o',
        'IceTop (2016/05-2017/04) SIBYLL2.1': 'o',
        'IceCube Hybrid (2010/06-2013/05) SIBYLL2.1': 'D',
        'IceCube+IceTop (2010/06-2013/05) SIBYLL2.1': 'D',
        'IceTop (2010/06-2013/05)': 'D',
        'KASCADE (1996/10-2002/01) QGSJet01': 'D',
        'KASCADE (1996/10-2002/01) SIBYLL 2.1': 'D',
        'KASCADE-Grande (2003/01-2009/03) QGSJet-II-04': 'D',
        'KASCADE-Grande (2003/12-2009/03) QGSJet-II-2': 'D',
        'KASCADE-Grande (2003/12-2011/10) SIBYLL2.3': 'D',
        'KASCADE-Grande (2004/03-2010/12) QGSJet-II-3': 'D',
        'KASCADE-Grande (2004/03-2012/05) QGSJet-II-2': 'D',
        'KASCADE-Grande EPOS-LHC': 'D',
        "KASCADE-Grande (2003/01-2006/08) QGSJet-II.04": 'D',
        'GAMMA (2003/01-2007/12) SIBYLL': 'D',
        'Tunka-133 (2009/10-2012/04) QGSJet01': 'x',
        'TALE (2014/06/-2016/03) QGSJet-II-03': 'x',
        'Telescope Array Hybrid (2008/01-2015/05)': 'x',
        'Telescope Array SD (2008/05 - 2024/05)': '^',
        "TA SD (2008/05-2019/05)": "^",
        'Auger FD (2004/12-2012/12) EPOS-LHC': 'x',
        'Auger FD (2004/12-2012/12) QGSJet-II-04': 'x',
        'Auger FD (2004/12-2012/12) SIBYLL2.1': 'x',
        "Auger SD750+SD1500 (2014/01-2018/08)": "x",
        'Yakutsk (1995/01-2008/12) QGSJet01': 'x',
        "Fly's Eye (1988/06-1992/07)": 'x',
        'AGASA (1993/12-2002/12)': 'x',
        'NUCLEON-IC (2015/07-2017/06)': 'x',
        'SOKOL (1984/03-1986/01)': 'v',
        'RUNJOB (1995+1996)': 'v',
        'RUNJOB (1995+1996+1997+1999)': 'v',
        'Mount Norikura (1976/01-1995/12)': 'v',
        'GAMMA (2004/01-2006/12) SIBYLL': 'v',
        'Haverah Park (1974/01-1987/12) QGSJet98': 'v',
        'JACEE (1979+1980+1982+1983+1984+1986+1987+1988+1990+1994+1995)': 'v',
        'Auger (2004/01-2007/08)': 'v',
        'Auger (2005/11-2008/05)': 'v',
        'Auger Hybrid (2004/01-2014/12)': 'v',
        'IceTop (2010/06-2011/05) SIBYLL2.1': '^',
        'IceCube + IceTop (2010/06-2013/05) SIBYLL2.1': '^'
        }
    return e_rescaling, colors, markers
