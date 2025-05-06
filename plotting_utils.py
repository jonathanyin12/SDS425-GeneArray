import plotly.graph_objects as go
import seaborn as sns
from matplotlib import pyplot as plt

from constants import FEATURE_COLS


def plot_feature_histograms(df, title=""):
    # Create a 10 by 13 grid of histograms for the 130 features
    fig, axes = plt.subplots(10, 13, figsize=(30, 12))

    # Flatten the axes array for easier iteration
    axes = axes.flatten()

    # Plot each feature in its own subplot
    for i, feature in enumerate(FEATURE_COLS):
        if i < len(axes):  # Ensure we don't exceed the number of subplots
            sns.histplot(df[feature], bins=20, kde=True, ax=axes[i])
            # axes[i].set_title(f"{feature}", fontsize=8)
            axes[i].set_xlabel("")
            axes[i].set_ylabel("")
            # Hide x-axis tick labels
            axes[i].set_xticklabels([])
            axes[i].set_yticklabels([])
            # Remove ticks from both axes
            axes[i].tick_params(axis="both", which="both", length=0)

    # Reduce spacing between subplots
    plt.subplots_adjust(hspace=0.0, wspace=0.0)
    if title:
        plt.suptitle(title, y=0.9)
    plt.show()


def plot_3d_scatter(
    df,
    x_col,
    y_col,
    z_col,
    type_col="type",
    outlier_col=None,
    title="3D Scatter Plot",
    hover_data=None,
    filename=None,
):
    """
    Create a 3D scatter plot colored by type using customdata for hover info.

    Parameters:
    -----------
    df : pandas DataFrame
        The data to plot
    x_col, y_col, z_col : str
        Column names for the x, y, and z axes
    type_col : str, default="type"
        Column name for the categorical variable to color by
    outlier_col : str, default=None
        Column name for the outlier variable to color by
    title : str, default="3D Scatter Plot"
        Title for the plot
    hover_data : list, default=None
        List of column names to include in hover information (e.g., ["row", "col", "well"])
    filename : str, default=None
        Filename to save the plot as HTML
    """
    fig = go.Figure()

    # Default hover data if none provided
    if hover_data is None:
        hover_data = []

    # Always include type_col in hover_data if not already present
    if type_col not in hover_data:
        hover_data = [type_col] + hover_data

    # Construct hovertemplate string dynamically
    ht = ""
    for i, col_name in enumerate(hover_data):
        # Use the corresponding customdata index for each column name
        ht += f"<b>{col_name}</b>: %{{customdata[{i}]}}<br>"
    ht += "<extra></extra>"  # Hide the default trace info box like 'trace 0'

    # Get a consistent color for this type_name
    # Get the default plotly colors
    import plotly.express as px

    # Create a mapping from type to color using Dark2 and Set2 color palettes
    type_names = df[type_col].unique()
    dark2_colors = px.colors.qualitative.Dark2  # For outliers
    set2_colors = px.colors.qualitative.Set2  # For non-outliers

    # Create two color mappings for each type - one for outliers and one for non-outliers
    type_colors = {}
    type_colors_outlier = {}

    for i, t in enumerate(type_names):
        dark2_idx = i % len(dark2_colors)
        set2_idx = i % len(set2_colors)
        type_colors[t] = set2_colors[set2_idx]  # Regular points
        type_colors_outlier[t] = dark2_colors[dark2_idx]  # Outlier points

    # Plot points for each type with different colors
    for type_name in df[type_col].unique():
        if outlier_col is not None:
            # Create separate traces for outliers and non-outliers

            for is_outlier in [True, False]:
                mask = (df[type_col] == type_name) & (df[outlier_col] == is_outlier)
                if mask.any():  # Only create trace if there are points
                    df_filtered = df[mask]
                    customdata_values = df_filtered[hover_data].values

                    name = f"{type_name} (Outlier)" if is_outlier else str(type_name)

                    trace = go.Scatter3d(
                        x=df_filtered[x_col],
                        y=df_filtered[y_col],
                        z=df_filtered[z_col],
                        mode="markers",
                        name=name,
                        marker=dict(
                            size=6,
                            opacity=1 if is_outlier else 0.8,
                            symbol="diamond" if is_outlier else "circle",
                            line=dict(
                                width=1 if is_outlier else 0,
                                color="black",  # Keep border color consistent
                            ),
                            color=type_colors_outlier[type_name]
                            if is_outlier
                            else type_colors[type_name],
                        ),
                        legendgroup=name,  # Group traces by type_name
                        customdata=customdata_values,
                        hovertemplate=ht,
                    )

                    fig.add_trace(trace)
        else:
            # Just create traces by type
            mask = df[type_col] == type_name
            df_filtered = df[mask]
            customdata_values = df_filtered[hover_data].values

            trace = go.Scatter3d(
                x=df_filtered[x_col],
                y=df_filtered[y_col],
                z=df_filtered[z_col],
                mode="markers",
                name=str(type_name),  # Ensure name is a string
                marker=dict(size=6, opacity=0.7),
                customdata=customdata_values,
                hovertemplate=ht,
            )

            fig.add_trace(trace)

    # Update layout
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title=x_col,
            yaxis_title=y_col,
            zaxis_title=z_col,
        ),
        width=1600,
        height=1200,
        showlegend=True,
    )

    if filename:
        fig.write_html(filename + ".html")
        try:
            fig.write_image(filename + ".png")
        except Exception as e:
            print(f"Error writing image: {e}")

    fig.show()
    return fig
