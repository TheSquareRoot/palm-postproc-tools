import os

import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
from numpy.typing import NDArray


def xz_streamlines(
    u: NDArray,
    w: NDArray,
    x: NDArray,
    z: NDArray,
) -> None:
    # Create grid
    X, Z = np.meshgrid(x, z)
    nt = u.shape[0]

    # Store image paths to assemble GIF later
    image_paths = []

    for t in range(nt):
        fig, ax = plt.subplots(figsize=(8, 8))

        ax.streamplot(
            X,
            Z,
            u[t, :, :],
            w[t, :, :],
            color="black",
            density=8,
            linewidth=0.5,
            broken_streamlines=True,
        )

        ax.set_xlim(-0.5, 0.5)
        ax.set_ylim(0.0, 1.0)

        ax.set_title(f"Streamlines at t = {t}")
        ax.set_xlabel("x/W")
        ax.set_ylabel("z/H")

        fig.tight_layout()

        filename = f"./figs/streamlines_t{t:03d}.png"
        fig.savefig(filename, dpi=300)
        image_paths.append(filename)
        plt.close(fig)


def xy_streamlines(
    u: NDArray,
    v: NDArray,
    x: NDArray,
    y: NDArray,
    background: str = "sign",
) -> None:
    # Create grid
    X, Y = np.meshgrid(x, y)

    if background == "sign":
        field = np.sign(u)
        levels = [-1.5, -0.5, 0.5, 1.5]  # threshold between signs
    elif background == "mag":
        field = np.sign(u) * np.sqrt(u**2 + v**2)
        levels = 60

    vmin, vmax = field.min(), field.max()

    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot background: red for u < 0, blue for u > 0
    ax.contourf(
        X,
        Y,
        field,
        vmin=vmin,
        vmax=vmax,
        levels=levels,
        cmap="bwr_r",
        alpha=0.5,
    )

    ax.streamplot(
        X,
        Y,
        u,
        v,
        color="black",
        density=8,
        linewidth=0.5,
        broken_streamlines=True,
    )

    ax.set_aspect("equal")

    fig.tight_layout()
    fig.savefig("./figs/streamlines_xy.png", dpi=300)
    plt.close(fig)


def main() -> None:
    # Domain lims
    xmin, xmax = 50, 150
    ycut = 80
    zmax = 100
    # Set file path
    path = "./data/canyon_dust_HW1_R100_DP01_3d.001.nc"

    # Open file and extract relevant fields
    with Dataset(path, "r") as f:
        x = f.variables["x"][xmin:xmax]
        zu = f.variables["zu_3d"][:zmax]
        y = f.variables["y"][:-1]
        u_xz = f.variables["u"][:, :zmax, ycut, xmin : xmax + 1]
        w_xz = f.variables["w"][:, :zmax, ycut, xmin:xmax]
        u_xy = f.variables["u"][:, 1, :-1, xmin : xmax + 1]
        v_xy = f.variables["v"][:, 1, :, xmin:xmax]

    # Variables processing
    u_xz = u_xz.filled(0.0)
    w_xz = w_xz.filled(0.0)

    x = x / 10 - 1
    y = y / 10 - 1
    zu = zu[1:] / 10

    # Interpolation
    u_xz = (u_xz[:, 1:, :-1] + u_xz[:, 1:, 1:]) / 2
    w_xz = (w_xz[:, :-1, :] + w_xz[:, 1:, :]) / 2

    u_xy = (u_xy[:, :, :-1] + u_xy[:, :, 1:]) / 2
    v_xy = (v_xy[:, 1:, :] + v_xy[:, :-1, :]) / 2

    t = 0
    # xz_streamlines(u_xz, w_xz, x, zu)
    xy_streamlines(u_xy[t, :, :], v_xy[t, :, :], x, y, background="mag")


if __name__ == "__main__":
    main()
