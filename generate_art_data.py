"""
Generative Art Data Generator
Generates pixel-level data using mathematical functions for visual synthesis.
"""

import numpy as np
import pandas as pd
import math
from typing import Tuple, List
import os


class ArtDataGenerator:
    """Generates art data using various mathematical functions."""
    
    def __init__(self, width: int = 512, height: int = 512):
        """
        Initialize the generator.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels
        """
        self.width = width
        self.height = height
        self.x_coords, self.y_coords = np.meshgrid(
            np.arange(width), np.arange(height)
        )
    
    def normalize_coords(self) -> Tuple[np.ndarray, np.ndarray]:
        """Normalize coordinates to [-1, 1] range."""
        x_norm = (self.x_coords / self.width) * 2 - 1
        y_norm = (self.y_coords / self.height) * 2 - 1
        return x_norm, y_norm
    
    def sine_wave(self, frequency: float = 5.0, phase: float = 0.0) -> np.ndarray:
        """Generate sine wave pattern."""
        x_norm, y_norm = self.normalize_coords()
        intensity = np.sin(2 * np.pi * frequency * (x_norm + y_norm) + phase)
        return (intensity + 1) / 2  # Normalize to [0, 1]
    
    def cosine_wave(self, frequency: float = 5.0, phase: float = 0.0) -> np.ndarray:
        """Generate cosine wave pattern."""
        x_norm, y_norm = self.normalize_coords()
        intensity = np.cos(2 * np.pi * frequency * (x_norm + y_norm) + phase)
        return (intensity + 1) / 2  # Normalize to [0, 1]
    
    def spiral(self, turns: float = 5.0, tightness: float = 1.0) -> np.ndarray:
        """Generate spiral pattern."""
        x_norm, y_norm = self.normalize_coords()
        center_x, center_y = 0, 0
        
        # Calculate distance and angle from center
        dx = x_norm - center_x
        dy = y_norm - center_y
        distance = np.sqrt(dx**2 + dy**2)
        angle = np.arctan2(dy, dx)
        
        # Create spiral pattern
        spiral_value = np.sin(turns * angle + tightness * distance * 10)
        return (spiral_value + 1) / 2  # Normalize to [0, 1]
    
    def wave_interference(self, freq1: float = 3.0, freq2: float = 5.0) -> np.ndarray:
        """Generate wave interference pattern."""
        x_norm, y_norm = self.normalize_coords()
        wave1 = np.sin(2 * np.pi * freq1 * x_norm)
        wave2 = np.sin(2 * np.pi * freq2 * y_norm)
        intensity = wave1 * wave2
        return (intensity + 1) / 2  # Normalize to [0, 1]
    
    def random_noise(self, seed: int = None) -> np.ndarray:
        """Generate random noise pattern."""
        if seed is not None:
            np.random.seed(seed)
        return np.random.rand(self.height, self.width)
    
    def perlin_like_noise(self, octaves: int = 4, scale: float = 0.1) -> np.ndarray:
        """Generate Perlin-like noise using multiple octaves."""
        x_norm, y_norm = self.normalize_coords()
        noise = np.zeros((self.height, self.width))
        
        for i in range(octaves):
            freq = 2 ** i
            amplitude = 0.5 ** i
            noise += amplitude * np.sin(
                2 * np.pi * freq * scale * (x_norm + np.random.rand() * 10)
            ) * np.cos(
                2 * np.pi * freq * scale * (y_norm + np.random.rand() * 10)
            )
        
        return (noise - noise.min()) / (noise.max() - noise.min())
    
    def radial_gradient(self, center_x: float = 0.0, center_y: float = 0.0) -> np.ndarray:
        """Generate radial gradient pattern."""
        x_norm, y_norm = self.normalize_coords()
        dx = x_norm - center_x
        dy = y_norm - center_y
        distance = np.sqrt(dx**2 + dy**2)
        intensity = 1 - np.clip(distance, 0, 1)
        return intensity
    
    def combine_patterns(self, patterns: List[np.ndarray], weights: List[float] = None) -> np.ndarray:
        """Combine multiple patterns with optional weights."""
        if weights is None:
            weights = [1.0] * len(patterns)
        
        combined = np.zeros((self.height, self.width))
        total_weight = sum(weights)
        
        for pattern, weight in zip(patterns, weights):
            combined += pattern * weight
        
        combined /= total_weight
        return np.clip(combined, 0, 1)
    
    def generate_rgb_data(self, intensity: np.ndarray, color_scheme: str = 'grayscale') -> np.ndarray:
        """
        Convert intensity to RGB values.
        
        Args:
            intensity: 2D array of intensity values [0, 1]
            color_scheme: 'grayscale', 'red', 'blue', 'green', 'rainbow', 'warm', 'cool'
        """
        height, width = intensity.shape
        rgb = np.zeros((height, width, 3))
        
        if color_scheme == 'grayscale':
            rgb[:, :, 0] = intensity
            rgb[:, :, 1] = intensity
            rgb[:, :, 2] = intensity
        elif color_scheme == 'red':
            rgb[:, :, 0] = intensity
        elif color_scheme == 'green':
            rgb[:, :, 1] = intensity
        elif color_scheme == 'blue':
            rgb[:, :, 2] = intensity
        elif color_scheme == 'rainbow':
            # Create rainbow effect based on intensity
            rgb[:, :, 0] = np.sin(intensity * np.pi)
            rgb[:, :, 1] = np.sin(intensity * np.pi + 2 * np.pi / 3)
            rgb[:, :, 2] = np.sin(intensity * np.pi + 4 * np.pi / 3)
            rgb = (rgb + 1) / 2
        elif color_scheme == 'warm':
            rgb[:, :, 0] = intensity
            rgb[:, :, 1] = intensity * 0.7
            rgb[:, :, 2] = intensity * 0.3
        elif color_scheme == 'cool':
            rgb[:, :, 0] = intensity * 0.3
            rgb[:, :, 1] = intensity * 0.7
            rgb[:, :, 2] = intensity
        
        return np.clip(rgb, 0, 1)
    
    def to_dataframe(self, pattern: np.ndarray, rgb: np.ndarray = None, 
                     pattern_name: str = 'pattern') -> pd.DataFrame:
        """
        Convert pattern to DataFrame with pixel-level data.
        
        Args:
            pattern: 2D intensity array
            rgb: Optional 3D RGB array
            pattern_name: Name identifier for the pattern
        """
        data = []
        
        for y in range(self.height):
            for x in range(self.width):
                row = {
                    'x': x,
                    'y': y,
                    'intensity': pattern[y, x],
                    'pattern_type': pattern_name
                }
                
                if rgb is not None:
                    row['r'] = rgb[y, x, 0]
                    row['g'] = rgb[y, x, 1]
                    row['b'] = rgb[y, x, 2]
                
                data.append(row)
        
        return pd.DataFrame(data)


def generate_dataset(output_dir: str = 'data', num_samples: int = 10, 
                     width: int = 512, height: int = 512):
    """
    Generate a complete dataset with multiple patterns.
    
    Args:
        output_dir: Directory to save CSV files
        num_samples: Number of samples per pattern type
        width: Image width in pixels
        height: Image height in pixels
    """
    os.makedirs(output_dir, exist_ok=True)
    
    generator = ArtDataGenerator(width=width, height=height)
    all_dataframes = []
    
    # Generate different pattern types
    pattern_configs = [
        ('sine_wave', lambda: generator.sine_wave(frequency=np.random.uniform(2, 8))),
        ('cosine_wave', lambda: generator.cosine_wave(frequency=np.random.uniform(2, 8))),
        ('spiral', lambda: generator.spiral(turns=np.random.uniform(3, 8))),
        ('wave_interference', lambda: generator.wave_interference(
            freq1=np.random.uniform(2, 6),
            freq2=np.random.uniform(4, 8)
        )),
        ('random_noise', lambda: generator.random_noise(seed=np.random.randint(0, 10000))),
        ('perlin_noise', lambda: generator.perlin_like_noise(
            octaves=np.random.randint(3, 6),
            scale=np.random.uniform(0.05, 0.2)
        )),
        ('radial_gradient', lambda: generator.radial_gradient(
            center_x=np.random.uniform(-0.5, 0.5),
            center_y=np.random.uniform(-0.5, 0.5)
        )),
    ]
    
    color_schemes = ['grayscale', 'red', 'blue', 'green', 'rainbow', 'warm', 'cool']
    
    print(f"Generating {num_samples} samples per pattern type...")
    
    for pattern_name, pattern_func in pattern_configs:
        for i in range(num_samples):
            # Generate pattern
            intensity = pattern_func()
            
            # Randomly select color scheme
            color_scheme = np.random.choice(color_schemes)
            rgb = generator.generate_rgb_data(intensity, color_scheme=color_scheme)
            
            # Create unique pattern identifier
            unique_name = f"{pattern_name}_{color_scheme}_{i:03d}"
            
            # Convert to DataFrame
            df = generator.to_dataframe(intensity, rgb, pattern_name=unique_name)
            all_dataframes.append(df)
            
            print(f"Generated: {unique_name}")
    
    # Combine all dataframes
    print("\nCombining all data...")
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Save to CSV
    output_file = os.path.join(output_dir, 'art_dataset.csv')
    print(f"\nSaving to {output_file}...")
    combined_df.to_csv(output_file, index=False)
    
    print(f"\nDataset generated successfully!")
    print(f"Total pixels: {len(combined_df):,}")
    print(f"Unique patterns: {combined_df['pattern_type'].nunique()}")
    print(f"File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
    
    # Also save a sample (first pattern) for quick inspection
    sample_df = all_dataframes[0]
    sample_file = os.path.join(output_dir, 'art_dataset_sample.csv')
    sample_df.to_csv(sample_file, index=False)
    print(f"Sample saved to: {sample_file}")
    
    return combined_df


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate art dataset for visual synthesis')
    parser.add_argument('--samples', type=int, default=10,
                        help='Number of samples per pattern type (default: 10)')
    parser.add_argument('--width', type=int, default=512,
                        help='Image width in pixels (default: 512)')
    parser.add_argument('--height', type=int, default=512,
                        help='Image height in pixels (default: 512)')
    parser.add_argument('--output-dir', type=str, default='data',
                        help='Output directory for CSV files (default: data)')
    
    args = parser.parse_args()
    
    print(f"Configuration:")
    print(f"  Samples per pattern: {args.samples}")
    print(f"  Image size: {args.width}x{args.height}")
    print(f"  Output directory: {args.output_dir}")
    print()
    
    # Generate the dataset
    df = generate_dataset(output_dir=args.output_dir, num_samples=args.samples,
                          width=args.width, height=args.height)
    
    # Display summary statistics
    print("\n" + "="*50)
    print("Dataset Summary")
    print("="*50)
    print(df.head())
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nNote: Large datasets may take time to upload to Kaggle.")
    print(f"Consider using --samples 5 or fewer for initial testing.")

