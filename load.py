from netCDF4 import Dataset
from numpy.typing import NDArray


def interpolate(var: NDArray, dims: list[str]) -> NDArray:
    if dims[3] == "xu":
        print("xu")
        var = (var[:, :, :, 1:] + var[:, :, :, :-1]) / 2

    if dims[2] == "yv":
        print("yv")
        var = (var[:, :, 1:, :] + var[:, :, :-1, :]) / 2

    if dims[1] == "zw_3d":
        print("zw_3d")
        var = (var[:, 1:, :, :] + var[:, :-1, :, :]) / 2

    return var


def load_3d(
    path: str,
    varlist: list[str],
    tlims: slice | None = None,
    xlims: slice | None = None,
    ylims: slice | None = None,
    zlims: slice | None = None,
) -> dict[NDArray]:
    # If slices are not set the whole arrays are taken
    tlims = tlims or slice(None)
    xlims = xlims or slice(None)
    ylims = ylims or slice(None)
    zlims = zlims or slice(None)

    data = {}

    # Open the file and extract data
    with Dataset(path, "r") as f:
        # Dimensions
        data["t"] = f.variables["time"][tlims]
        data["x"] = f.variables["x"][xlims]
        data["y"] = f.variables["y"][ylims]
        data["z"] = f.variables["zu_3d"][zlims]

        # Iterate over all variables and saves the defined ones
        for name, var in f.variables.items():
            if name in varlist:
                print(f"Processing {name}")
                print(f"{name} has dimensions: {var.dimensions}")
                # Interpolate on the x, y, zu grid
                tmp = var[tlims, zlims, ylims, xlims].filled(0)
                data[name] = interpolate(
                    tmp,
                    var.dimensions,
                )

        return data
