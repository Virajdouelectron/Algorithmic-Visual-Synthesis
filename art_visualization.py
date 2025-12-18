"""
Art Visualization System - Step 3
Converts numerical matrices into artistic images using Matplotlib.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from typing import Optional, List, Tuple, Dict, Union
import os
from pathlib import Path


class ArtVisualizer:
    """
    Converts numerical matrices into artistic images using Matplotlib colormaps.
    """
    
    def __init__(self, dpi: int = 150, figsize: Tuple[int, int] = (10, 10)):
        """
        Initialize the visualizer.
        
        Args:
            dpi: Resolution for saved images
            figsize: Figure size (width, height) in inches
        """
        self.dpi = dpi
        self.figsize = figsize
        
        # Available colormaps (artistic and standard)
        self.colormaps = {
            'artistic': [
                'viridis', 'plasma', 'inferno', 'magma', 'cividis',
                'turbo', 'rainbow', 'hsv', 'twilight', 'twilight_shifted'
            ],
            'diverging': [
                'RdBu', 'RdYlBu', 'Spectral', 'coolwarm', 'seismic',
                'PiYG', 'PRGn', 'BrBG', 'RdGy', 'PuOr'
            ],
            'sequential': [
                'Blues', 'Greens', 'Reds', 'Oranges', 'Purples',
                'Greys', 'YlOrRd', 'YlGnBu', 'hot', 'cool'
            ],
            'custom': self._create_custom_colormaps()
        }
    
    def _create_custom_colormaps(self) -> Dict[str, ListedColormap]:
        """Create custom artistic colormaps."""
        custom = {}
        
        # Sunset gradient
        colors_sunset = ['#1a1a2e', '#16213e', '#0f3460', '#533483', '#e94560', '#ff6b6b', '#ffa500', '#ffd700']
        custom['sunset'] = LinearSegmentedColormap.from_list('sunset', colors_sunset, N=256)
        
        # Ocean depth
        colors_ocean = ['#000428', '#004e92', '#009ffd', '#2a2a72', '#009ffd', '#00d2ff', '#3a7bd5']
        custom['ocean'] = LinearSegmentedColormap.from_list('ocean', colors_ocean, N=256)
        
        # Forest
        colors_forest = ['#0a0e27', '#1a3a2a', '#2d5016', '#3d6b14', '#5a9214', '#7fb347', '#a8d5ba']
        custom['forest'] = LinearSegmentedColormap.from_list('forest', colors_forest, N=256)
        
        # Fire
        colors_fire = ['#000000', '#330000', '#660000', '#990000', '#cc0000', '#ff3300', '#ff6600', '#ff9900', '#ffcc00']
        custom['fire'] = LinearSegmentedColormap.from_list('fire', colors_fire, N=256)
        
        # Aurora
        colors_aurora = ['#000000', '#001122', '#003344', '#0066aa', '#00aaff', '#00ffaa', '#aaff00', '#ffff00']
        custom['aurora'] = LinearSegmentedColormap.from_list('aurora', colors_aurora, N=256)
        
        # Neon
        colors_neon = ['#000000', '#1a0033', '#330066', '#6600cc', '#9900ff', '#cc66ff', '#ff99ff', '#ffccff']
        custom['neon'] = LinearSegmentedColormap.from_list('neon', colors_neon, N=256)
        
        # Vintage
        colors_vintage = ['#2c1810', '#4a2c1a', '#6b4423', '#8b6914', '#a0822d', '#c4a574', '#e6d5b8', '#f5e6d3']
        custom['vintage'] = LinearSegmentedColormap.from_list('vintage', colors_vintage, N=256)
        
        # Cyberpunk
        colors_cyber = ['#000000', '#1a0033', '#330066', '#0000ff', '#00ffff', '#00ff00', '#ffff00', '#ff00ff']
        custom['cyberpunk'] = LinearSegmentedColormap.from_list('cyberpunk', colors_cyber, N=256)
        
        return custom
    
    def visualize_pattern(self, pattern: np.ndarray, 
                          colormap: Union[str, ListedColormap] = 'viridis',
                          title: Optional[str] = None,
                          show_axis: bool = False,
                          save_path: Optional[str] = None,
                          **kwargs) -> plt.Figure:
        """
        Visualize a single pattern as an image.
        
        Args:
            pattern: 2D numpy array (intensity values)
            colormap: Colormap name or colormap object
            title: Optional title for the image
            show_axis: Whether to show axis labels
            save_path: Optional path to save the image
            **kwargs: Additional arguments for imshow
        
        Returns:
            Matplotlib figure object
        """
        # Get colormap
        if isinstance(colormap, str):
            if colormap in self.colormaps['custom']:
                cmap = self.colormaps['custom'][colormap]
            else:
                cmap = plt.get_cmap(colormap)
        else:
            cmap = colormap
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Display image
        im = ax.imshow(pattern, cmap=cmap, origin='lower', **kwargs)
        
        # Customize appearance
        if not show_axis:
            ax.axis('off')
        
        if title:
            ax.set_title(title, fontsize=16, pad=20, color='white' if colormap in ['inferno', 'magma', 'viridis'] else 'black')
        
        # Add colorbar
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        
        plt.tight_layout()
        
        # Save if path provided
        if save_path:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight', facecolor='black' if colormap in ['inferno', 'magma'] else 'white')
            print(f"Saved image to: {save_path}")
        
        return fig
    
    def visualize_rgb(self, rgb_pattern: np.ndarray,
                     title: Optional[str] = None,
                     show_axis: bool = False,
                     save_path: Optional[str] = None) -> plt.Figure:
        """
        Visualize an RGB pattern (3D array with R, G, B channels).
        
        Args:
            rgb_pattern: 3D numpy array (height, width, 3) with RGB values [0, 1]
            title: Optional title
            show_axis: Whether to show axis labels
            save_path: Optional path to save
        
        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        # Ensure values are in [0, 1] range
        rgb_clipped = np.clip(rgb_pattern, 0, 1)
        
        ax.imshow(rgb_clipped, origin='lower')
        
        if not show_axis:
            ax.axis('off')
        
        if title:
            ax.set_title(title, fontsize=16, pad=20)
        
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved RGB image to: {save_path}")
        
        return fig
    
    def create_gallery(self, patterns: List[np.ndarray],
                      titles: Optional[List[str]] = None,
                      colormap: Union[str, ListedColormap] = 'viridis',
                      n_cols: int = 3,
                      save_path: Optional[str] = None,
                      figsize: Optional[Tuple[int, int]] = None) -> plt.Figure:
        """
        Create a gallery of multiple patterns.
        
        Args:
            patterns: List of 2D pattern arrays
            titles: Optional list of titles for each pattern
            colormap: Colormap to use
            n_cols: Number of columns in the gallery
            save_path: Optional path to save
            figsize: Optional figure size (auto-calculated if None)
        
        Returns:
            Matplotlib figure object
        """
        n_patterns = len(patterns)
        n_rows = (n_patterns + n_cols - 1) // n_cols
        
        if figsize is None:
            figsize = (n_cols * 4, n_rows * 4)
        
        # Get colormap
        if isinstance(colormap, str):
            if colormap in self.colormaps['custom']:
                cmap = self.colormaps['custom'][colormap]
            else:
                cmap = plt.get_cmap(colormap)
        else:
            cmap = colormap
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize, dpi=self.dpi)
        
        # Handle different subplot configurations
        if n_rows == 1 and n_cols == 1:
            axes = np.array([[axes]])
        elif n_rows == 1:
            axes = axes.reshape(1, -1)
        elif n_cols == 1:
            axes = axes.reshape(-1, 1)
        else:
            axes = axes.reshape(n_rows, n_cols)
        
        for i, pattern in enumerate(patterns):
            row = i // n_cols
            col = i % n_cols
            if n_rows == 1 and n_cols == 1:
                ax = axes[0, 0]
            elif n_rows == 1:
                ax = axes[0, col]
            elif n_cols == 1:
                ax = axes[row, 0]
            else:
                ax = axes[row, col]
            
            ax.imshow(pattern, cmap=cmap, origin='lower')
            ax.axis('off')
            
            if titles and i < len(titles):
                ax.set_title(titles[i], fontsize=10, pad=10)
        
        # Hide unused subplots
        for i in range(n_patterns, n_rows * n_cols):
            row = i // n_cols
            col = i % n_cols
            if n_rows == 1 and n_cols == 1:
                ax = axes[0, 0]
            elif n_rows == 1:
                ax = axes[0, col]
            elif n_cols == 1:
                ax = axes[row, 0]
            else:
                ax = axes[row, col]
            ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved gallery to: {save_path}")
        
        return fig
    
    def create_multi_colormap_gallery(self, pattern: np.ndarray,
                                     colormaps: Optional[List[str]] = None,
                                     save_path: Optional[str] = None) -> plt.Figure:
        """
        Show the same pattern with different colormaps.
        
        Args:
            pattern: 2D pattern array
            colormaps: List of colormap names (uses default if None)
            save_path: Optional path to save
        
        Returns:
            Matplotlib figure object
        """
        if colormaps is None:
            colormaps = ['viridis', 'plasma', 'inferno', 'magma', 'turbo', 'rainbow']
        
        n_cols = 3
        n_rows = (len(colormaps) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5), dpi=self.dpi)
        
        if n_rows == 1:
            axes = axes.reshape(1, -1)
        
        for i, cmap_name in enumerate(colormaps):
            row = i // n_cols
            col = i % n_cols
            ax = axes[row, col] if n_rows > 1 else axes[col]
            
            # Get colormap
            if cmap_name in self.colormaps['custom']:
                cmap = self.colormaps['custom'][cmap_name]
            else:
                cmap = plt.get_cmap(cmap_name)
            
            im = ax.imshow(pattern, cmap=cmap, origin='lower')
            ax.set_title(cmap_name, fontsize=12, pad=10)
            ax.axis('off')
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        
        # Hide unused subplots
        for i in range(len(colormaps), n_rows * n_cols):
            row = i // n_cols
            col = i % n_cols
            ax = axes[row, col] if n_rows > 1 else axes[col]
            ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else '.', exist_ok=True)
            fig.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            print(f"Saved multi-colormap gallery to: {save_path}")
        
        return fig
    
    def list_colormaps(self) -> Dict[str, List[str]]:
        """List all available colormaps."""
        all_maps = {}
        all_maps.update(self.colormaps)
        all_maps['all_standard'] = (
            self.colormaps['artistic'] + 
            self.colormaps['diverging'] + 
            self.colormaps['sequential']
        )
        return all_maps
    
    def display(self, pattern: np.ndarray, colormap: str = 'viridis', **kwargs):
        """
        Display a pattern interactively.
        
        Args:
            pattern: 2D pattern array
            colormap: Colormap name
            **kwargs: Additional arguments
        """
        self.visualize_pattern(pattern, colormap=colormap, **kwargs)
        plt.show()


def load_pattern_from_csv(csv_path: str, pattern_name: Optional[str] = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
    """
    Load a pattern from CSV file (from Step 1).
    
    Args:
        csv_path: Path to CSV file
        pattern_name: Optional pattern name to filter
    
    Returns:
        Tuple of (intensity_pattern, rgb_pattern)
    """
    import pandas as pd
    
    df = pd.read_csv(csv_path)
    
    if pattern_name:
        df = df[df['pattern_type'] == pattern_name]
    
    if len(df) == 0:
        raise ValueError(f"No pattern found with name: {pattern_name}")
    
    # Get dimensions
    width = df['x'].max() + 1
    height = df['y'].max() + 1
    
    # Reshape intensity
    intensity = df['intensity'].values.reshape(height, width)
    
    # Reshape RGB if available
    rgb = None
    if 'r' in df.columns and 'g' in df.columns and 'b' in df.columns:
        rgb = np.stack([
            df['r'].values.reshape(height, width),
            df['g'].values.reshape(height, width),
            df['b'].values.reshape(height, width)
        ], axis=-1)
    
    return intensity, rgb


def batch_visualize_from_csv(csv_path: str, output_dir: str = 'output/images',
                            colormaps: Optional[List[str]] = None,
                            pattern_limit: Optional[int] = None):
    """
    Batch visualize all patterns from a CSV file.
    
    Args:
        csv_path: Path to CSV file
        output_dir: Output directory for images
        colormaps: List of colormaps to use (uses default if None)
        pattern_limit: Limit number of patterns to process
    """
    import pandas as pd
    
    df = pd.read_csv(csv_path)
    pattern_names = df['pattern_type'].unique()
    
    if pattern_limit:
        pattern_names = pattern_names[:pattern_limit]
    
    if colormaps is None:
        colormaps = ['viridis', 'plasma', 'inferno', 'magma', 'turbo']
    
    visualizer = ArtVisualizer()
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Processing {len(pattern_names)} patterns...")
    
    for i, pattern_name in enumerate(pattern_names):
        print(f"Processing {i+1}/{len(pattern_names)}: {pattern_name}")
        
        try:
            intensity, rgb = load_pattern_from_csv(csv_path, pattern_name)
            
            # Save with different colormaps
            for cmap in colormaps:
                filename = f"{pattern_name.replace(' ', '_')}_{cmap}.png"
                filepath = os.path.join(output_dir, filename)
                visualizer.visualize_pattern(
                    intensity, 
                    colormap=cmap,
                    title=pattern_name,
                    save_path=filepath
                )
                plt.close()
            
            # Also save RGB version if available
            if rgb is not None:
                filename = f"{pattern_name.replace(' ', '_')}_rgb.png"
                filepath = os.path.join(output_dir, filename)
                visualizer.visualize_rgb(rgb, title=pattern_name, save_path=filepath)
                plt.close()
        
        except Exception as e:
            print(f"Error processing {pattern_name}: {e}")
    
    print(f"\nCompleted! Images saved to: {output_dir}")

