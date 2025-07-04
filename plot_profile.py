import matplotlib.pyplot as plt
import numpy as np
from matplotlib import ticker

from load import load_3d


def main() -> None:
    # Load data
    path = "./data/canyon_dust_HW1_R100_DP01_av_3d.001.nc"

    # Define variables to extract
    varlist = [
        "u",
    ]

    # Define slices
    tlims = slice(None)
    xlims = slice(50, 150)
    ylims = slice(None)
    zlims = slice(None)

    # Load data
    data = load_3d(path, varlist, tlims=tlims, xlims=xlims, ylims=ylims, zlims=zlims)

    z = data["z"]
    u = np.mean(data["u"][-1, :, :, 50], axis=1)
    uref = np.mean(u[100:152])

    # Plot
    fig, ax = plt.subplots()

    ax.plot(u / uref, z / 10, color="r")

    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(0.0, 1.5)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))

    ax.grid(
        axis="both",
        linestyle=":",
    )

    ax.set_aspect(4.2)

    fig.tight_layout()
    fig.savefig("./figs/u_profile.png", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
