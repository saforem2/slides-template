"""
src/slides/__init__.py
"""
from __future__ import absolute_import, annotations, division, print_function

import os
import logging
import warnings
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
from enrich.style import STYLES
from rich.console import Console
from rich.theme import Theme

console = Console(theme=Theme(STYLES), log_path=False, markup=True)

os.environ['MPLBACKEND'] = ''

warnings.filterwarnings('ignore')

HERE = Path(__file__).parent
ROOT = HERE.parent.parent

COLORS = {
    "blue":     "#2196F3",
    "red":      "#EF5350",
    "green":    "#4CAF50",
    "orange":   "#FFA726",
    "purple":   "#AE81FF",
    "yellow":   "#ffeb3b",
    "pink":     "#EC407A",
    "teal":     "#009688",
    "white":    "#CFCFCF",
    "grey000":   "#111111",
    "grey010":   "#111111",
    "grey020":   "#222222",
    "grey030":   "#333333",
    "grey040":   "#444444",
    "grey050":   "#555555",
    "grey060":   "#666666",
    "grey070":   "#777777",
    "grey080":   "#888888",
    "grey090":   "#999999",
    "grey100":   "#FFFFFF",
}


def get_console() -> Console:
    console = Console(theme=Theme(STYLES), log_path=False, markup=True)
    console.is_jupyter = False
    return console


def set_plot_style(params: Optional[dict] = None):
    import matplotlib.pyplot as plt
    defaults = {
        'axes.facecolor': 'none',
        'figure.facecolor': 'none',
        'savefig.facecolor': 'none',
        'savefig.format': 'svg',
        'axes.edgecolor': 'none',
        'axes.grid': True,
        'axes.labelcolor': '#838383',
        'axes.titlecolor': '#838383',
        'grid.color': '#838383',
        'text.color': '#838383',
        'grid.linestyle': '--',
        'grid.linewidth': 0.5,
        'grid.alpha': 0.4,
        'xtick.color': 'none',
        'ytick.color': 'none',
        'xtick.labelcolor': '#838383',
        'legend.edgecolor': 'none',
        'ytick.labelcolor': '#838383',
        'savefig.transparent': True,
    }
    plt.rcParams['axes.prop_cycle'] = plt.cycler(
        'color', list(COLORS.values())
    )
    plt.rcParams |= defaults
    if params is not None:
        plt.rcParams |= params


def get_logger(
        name: Optional[str] = None,
        level: str = 'INFO',
        rank: int = 0,
        **kwargs,
) -> logging.Logger:
    # logging.basicConfig(stream=DummyTqdmFile(sys.stderr))
    log = logging.getLogger(name)
    from enrich.console import Console, get_theme
    from enrich.logging import RichHandler
    # log.handlers = []
    # from rich.logging import RichHandler
    # from l2hmc.utils.rich import get_console, is_interactive
    theme = get_theme()
    console = Console(theme=theme, log_path=False, markup=True)
    import os

    from rich.console import Console as rConsole
    os.environ['COLORTERM'] = 'truecolor'
    from rich.console import Console as rConsole
    rconsole = rConsole(theme=theme, log_path=False, markup=True)
    if console.is_jupyter:
        console.is_jupyter = False
    log.addHandler(
        RichHandler(
            omit_repeated_times=False,
            level=level,
            console=console,
            show_time=True,
            show_level=True,
            show_path=False,
            # tracebacks_width=120,
            markup=True,
            enable_link_path=True,
            # keywords=['loss=', 'dt=', 'Saving']
        )
    )
    log.setLevel(level)
    if (
            len(log.handlers) > 1
            and all([i == log.handlers[0] for i in log.handlers])
    ):
        log.handlers = [log.handlers[0]]
    return log


log = get_logger('ClimRR')
