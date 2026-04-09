import os
import supereeg as se
import hypertools as hyp
import pandas as pd
import numpy as np
import glob as glob
from scipy import stats, signal
import scipy.spatial as spatial
import numpy.matlib as mat
import matplotlib.patches as patches
from scipy.spatial.distance import cdist, pdist
from sklearn.neighbors import NearestNeighbors
from nilearn import plotting as ni_plt
from supereeg.helpers import _log_rbf, _brain_to_nifti, _plot_borderless
from supereeg.helpers import _corr_column, get_rows, known_unknown, _get_corr
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.ticker as mtick
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize, to_hex
import seaborn as sns
from scipy import stats
import math
import torch
from scipy.spatial.distance import cdist
from scipy.interpolate import Rbf
from nilearn import datasets, image
import nibabel as nib
from nilearn.plotting import plot_glass_brain

############## General functions #################

def density(n_by_3_Locs, nearest_n, tau=.2):
    """
        Calculates the density of the nearest n neighbors
        Parameters
        ----------
        n_by_3_Locs : ndarray
            Array of electrode locations - one for each row
        nearest_n : int
            Number of nearest neighbors to consider in density calculation
        Returns
        ----------
        results : ndarray
            Denisity for each electrode location
        """
    nbrs = NearestNeighbors(n_neighbors=nearest_n, algorithm='ball_tree').fit(n_by_3_Locs)
    distances, indices = nbrs.kneighbors(n_by_3_Locs)
    return np.exp(-tau*(distances.sum(axis=1)))


def graph_den_corr_map(locs, corr):
# Define your coordinates
    coordinates = [[-42, 30, 24], [60, -15, 30]]

    # Get bounds that include all coordinates
    coords_array = np.array(coordinates)
    cut_coords = [
        np.mean(coords_array[:, 0]),  # x-axis
        np.mean(coords_array[:, 1]),  # y-axis
        np.mean(coords_array[:, 2])   # z-axis
    ]

    # Create figure and display separately
    fig = plt.figure(figsize=(10, 5))

    # Create display
    display = plot_glass_brain(None, display_mode='ortho',cut_coords=cut_coords,figure=fig)

    # Setup colormap
    cmap = plt.cm.gnuplot
    norm = Normalize(vmin=-1, vmax=1)

    # FIX 1: Convert RGBA to hex color string
    for idx, strength in enumerate(corr):
        coord = locs[idx]
        abs_strength = abs(strength)
    
        # Get RGBA tuple and convert to hex
        rgba = cmap(norm(strength))
        hex_color = to_hex(rgba)
    
        display.add_markers(
            [coord],
            marker_color=hex_color,  # Now it's a single color string
            marker_size=5,
            alpha=.6
        )

    # Add colorbar to figure
    sm = ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])

    # Simple colorbar at the bottom of the figure
    cbar_ax = fig.add_axes([0.2, 0.05, 0.6, 0.02])  # [left, bottom, width, height]
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation='horizontal',
                    label='Correlation (-1 to 1)',
                    ticks=[-1, -0.5, 0, 0.5, 1])

    plt.show()


# After running pipeline pull all correlation and location data into a numpy array
def _get_corr(results_path):
    within_files = glob.glob(os.path.join(results_path, "*within*"))
    all_files = glob.glob(os.path.join(results_path, "*"))
    across_files = [f for f in all_files if "within" not in os.path.basename(f)]


    within_data = np.zeros(len(within_files))
    within_locs = np.zeros((len(within_files),3))
    for i in range(len(within_files)):
        load = np.load(within_files[i])
        if len(load["corrs"]) == 1:
            within_data[i] = load["corrs"].item()
            within_locs[i] = load["coord"]
    
    mask = ~np.isnan(within_data)
    within_data = within_data[mask]
    within_locs = within_locs[mask]
    within_mean = np.mean(within_data)
    within_median = np.median(within_data)
    within_std = np.std(within_data)
    within_var = np.var(within_data)


    across_data = np.zeros(len(across_files))
    across_locs = np.zeros((len(across_files),3))
    for i in range(len(across_files)):
        load = np.load(across_files[i])
        if len(load["corrs"]) == 1:
            across_data[i] = load["corrs"].item()
            across_locs[i] = load["coord"] 

    across_mask = ~np.isnan(across_data)
    across_data = across_data[across_mask]
    across_locs = across_locs[across_mask]
    across_mean = np.mean(across_data)
    across_median = np.median(across_data)
    across_std = np.std(across_data)
    across_var = np.var(across_data)

    data_corr = {"within_corr": within_data, "within_locs":within_locs ,"across_corr":across_data, "across_locs":across_locs}
    data_stats = {"within_mean":within_mean,"within_median":within_median,"within_std":within_std,"within_var":within_var,
                  "across_mean":across_mean,"across_median":across_median,"across_std":across_std,"across_var":across_var}
    
    return data_corr, data_stats

def graph_histo_corr(file_path_corr,graph_title="Electrode Reconstruction Correlation"):
    data, data_stats = _get_corr(file_path_corr)
    fig, (ax_box,ax_hist) = plt.subplots(1,2,figsize=(10,6), gridspec_kw={"width_ratios":[1,4]})

    ax_hist.hist(data["within_corr"],bins=10,density=True,color="grey",alpha=0.7,label=f"Within (μ = {data_stats["within_mean"]:.3f}, σ = {data_stats["within_std"]:.3f}, σ² = {data_stats["within_var"]:.3f})")
    ax_hist.axvline(data_stats["within_median"], color="grey", linestyle="--", linewidth=2, label=f"Within Median = {data_stats["within_median"]:.3f}")
    #ax.plot(x_within,pdf_within,color="grey")
    ax_hist.hist(data["across_corr"], density= True,bins=10,color="black",alpha=0.7,label=f"Across (μ = {data_stats["across_mean"]:.3f}, σ = {data_stats["across_std"]:.3f}, σ² = {data_stats["across_var"]:.3f})")
    ax_hist.axvline(data_stats["across_median"], color="black", linestyle="--", linewidth=2, label=f"Across Median = {data_stats["across_median"]:.3f}")
    #ax.plot(x_across,pdf_across,color="black")

    ax_hist.set_xlabel("Correlation")
    ax_hist.set_ylabel("Electrode Density")
    ax_hist.legend()
    ax_hist.grid()

    ax_box.boxplot(data["across_corr"],positions=[20],widths=.27,label="Across", patch_artist=True, 
           boxprops=dict(facecolor='black', alpha=0.6),
           medianprops=dict(color="red", linewidth=1))
    ax_box.boxplot(data["within_corr"], positions=[20.3] ,widths=.27,label="Within", patch_artist=True,
            boxprops=dict(facecolor='grey', alpha=0.6),
            medianprops=dict(color="red", linewidth=1))

    ax_box.set_ylabel("Correlation")
    ax_box.set_xticklabels([])
    ax_box.grid()
    ax_box.legend()

    plt.suptitle(graph_title)
    plt.tight_layout()
    plt.show()