"""
Automation System - Step 4
Runs the generator multiple times with different random seeds to produce unique artworks.
"""

import numpy as np
import os
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import time

from generate_art_data import ArtDataGenerator
from generative_models import VariationalAutoEncoder, GenerativeAdversarialNetwork
from art_visualization import ArtVisualizer


class ArtAutomation:
    """
    Automated art generation system with seed management.
    """
    
    def __init__(self, output_dir: str = 'output/automated', 
                 width: int = 512, height: int = 512):
        """
        Initialize the automation system.
        
        Args:
            output_dir: Base output directory
            width: Image width
            height: Image height
        """
        self.output_dir = output_dir
        self.width = width
        self.height = height
        
        # Initialize generators
        self.data_generator = ArtDataGenerator(width, height)
        self.vae = VariationalAutoEncoder(latent_dim=16)
        self.gan = GenerativeAdversarialNetwork(width, height)
        self.visualizer = ArtVisualizer(dpi=150, figsize=(10, 10))
        
        # Create output directories
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(f"{output_dir}/images", exist_ok=True)
        os.makedirs(f"{output_dir}/data", exist_ok=True)
        os.makedirs(f"{output_dir}/metadata", exist_ok=True)
        
        # Track generated artworks
        self.generated_artworks = []
    
    def generate_with_seed(self, seed: int, 
                          pattern_type: Optional[str] = None,
                          colormap: str = 'viridis',
                          use_vae: bool = False,
                          use_gan: bool = False,
                          quality_threshold: float = 0.5) -> Dict:
        """
        Generate a single artwork with a specific seed.
        
        Args:
            seed: Random seed
            pattern_type: Optional specific pattern type (random if None)
            colormap: Colormap to use
            use_vae: Whether to use VAE generation
            use_gan: Whether to use GAN filtering
            quality_threshold: Quality threshold for GAN
        
        Returns:
            Dictionary with artwork metadata
        """
        np.random.seed(seed)
        
        # Determine pattern type
        if pattern_type is None:
            pattern_types = [
                'sine_wave', 'cosine_wave', 'spiral', 'wave_interference',
                'random_noise', 'perlin_noise', 'radial_gradient'
            ]
            pattern_type = np.random.choice(pattern_types)
        
        # Generate pattern
        if use_vae:
            pattern = self.vae.generate(pattern_type, self.data_generator, seed=seed)
            generation_method = 'vae'
        elif use_gan:
            # Generate with GAN
            patterns = self.gan.generate_art(n=1, quality_threshold=quality_threshold, seed=seed)
            if patterns:
                pattern, ptype, params, score = patterns[0]
                pattern_type = ptype
                generation_method = 'gan'
            else:
                # Fallback to regular generation
                pattern = self._generate_pattern(pattern_type, seed)
                generation_method = 'standard'
        else:
            pattern = self._generate_pattern(pattern_type, seed)
            generation_method = 'standard'
        
        # Select colormap if random
        if colormap == 'random':
            all_colormaps = (
                self.visualizer.colormaps['artistic'] +
                list(self.visualizer.colormaps['custom'].keys())
            )
            colormap = np.random.choice(all_colormaps)
        
        # Generate RGB
        color_schemes = ['grayscale', 'red', 'blue', 'green', 'rainbow', 'warm', 'cool']
        color_scheme = np.random.choice(color_schemes)
        rgb = self.data_generator.generate_rgb_data(pattern, color_scheme=color_scheme)
        
        # Create metadata
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        artwork_id = f"art_{seed}_{timestamp}"
        
        metadata = {
            'id': artwork_id,
            'seed': seed,
            'pattern_type': pattern_type,
            'colormap': colormap,
            'color_scheme': color_scheme,
            'generation_method': generation_method,
            'width': self.width,
            'height': self.height,
            'timestamp': timestamp,
            'pattern_shape': pattern.shape
        }
        
        # Add GAN score if applicable
        if use_gan and generation_method == 'gan':
            metadata['quality_score'] = float(score)
        
        # Save image
        image_path = f"{self.output_dir}/images/{artwork_id}.png"
        self.visualizer.visualize_pattern(
            pattern,
            colormap=colormap,
            title=f"{pattern_type} (Seed: {seed})",
            save_path=image_path
        )
        metadata['image_path'] = image_path
        
        # Save RGB image
        rgb_path = f"{self.output_dir}/images/{artwork_id}_rgb.png"
        self.visualizer.visualize_rgb(
            rgb,
            title=f"{pattern_type} RGB (Seed: {seed})",
            save_path=rgb_path
        )
        metadata['rgb_path'] = rgb_path
        
        # Save pattern data
        data_path = f"{self.output_dir}/data/{artwork_id}.csv"
        df = self.data_generator.to_dataframe(pattern, rgb, artwork_id)
        df.to_csv(data_path, index=False)
        metadata['data_path'] = data_path
        
        # Save metadata
        metadata_path = f"{self.output_dir}/metadata/{artwork_id}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        metadata['metadata_path'] = metadata_path
        
        self.generated_artworks.append(metadata)
        
        return metadata
    
    def _generate_pattern(self, pattern_type: str, seed: int) -> np.ndarray:
        """Generate a pattern using the data generator."""
        np.random.seed(seed)
        
        if pattern_type == 'sine_wave':
            return self.data_generator.sine_wave(
                frequency=np.random.uniform(2, 8),
                phase=np.random.uniform(0, 2 * np.pi)
            )
        elif pattern_type == 'cosine_wave':
            return self.data_generator.cosine_wave(
                frequency=np.random.uniform(2, 8),
                phase=np.random.uniform(0, 2 * np.pi)
            )
        elif pattern_type == 'spiral':
            return self.data_generator.spiral(
                turns=np.random.uniform(3, 8),
                tightness=np.random.uniform(0.5, 2.0)
            )
        elif pattern_type == 'wave_interference':
            return self.data_generator.wave_interference(
                freq1=np.random.uniform(2, 6),
                freq2=np.random.uniform(4, 8)
            )
        elif pattern_type == 'perlin_noise':
            return self.data_generator.perlin_like_noise(
                octaves=np.random.randint(3, 6),
                scale=np.random.uniform(0.05, 0.2)
            )
        elif pattern_type == 'radial_gradient':
            return self.data_generator.radial_gradient(
                center_x=np.random.uniform(-0.5, 0.5),
                center_y=np.random.uniform(-0.5, 0.5)
            )
        else:
            return self.data_generator.random_noise(seed=seed)
    
    def batch_generate(self, n_artworks: int,
                      seed_start: Optional[int] = None,
                      pattern_types: Optional[List[str]] = None,
                      colormaps: Optional[List[str]] = None,
                      use_vae: bool = False,
                      use_gan: bool = False,
                      quality_threshold: float = 0.5,
                      progress_callback: Optional[callable] = None) -> List[Dict]:
        """
        Generate multiple artworks with different seeds.
        
        Args:
            n_artworks: Number of artworks to generate
            seed_start: Starting seed (random if None)
            pattern_types: List of pattern types to use (random if None)
            colormaps: List of colormaps to use (random if None)
            use_vae: Whether to use VAE generation
            use_gan: Whether to use GAN filtering
            quality_threshold: Quality threshold for GAN
            progress_callback: Optional callback function(current, total, metadata)
        
        Returns:
            List of artwork metadata dictionaries
        """
        if seed_start is None:
            seed_start = np.random.randint(0, 1000000)
        
        print(f"Starting batch generation of {n_artworks} artworks...")
        print(f"Starting seed: {seed_start}")
        print(f"Output directory: {self.output_dir}")
        print("-" * 60)
        
        start_time = time.time()
        self.generated_artworks = []
        
        for i in range(n_artworks):
            seed = seed_start + i
            
            # Select pattern type
            pattern_type = None
            if pattern_types:
                pattern_type = np.random.choice(pattern_types)
            
            # Select colormap
            colormap = 'random'
            if colormaps:
                colormap = np.random.choice(colormaps)
            
            try:
                metadata = self.generate_with_seed(
                    seed=seed,
                    pattern_type=pattern_type,
                    colormap=colormap,
                    use_vae=use_vae,
                    use_gan=use_gan,
                    quality_threshold=quality_threshold
                )
                
                elapsed = time.time() - start_time
                avg_time = elapsed / (i + 1)
                remaining = (n_artworks - i - 1) * avg_time
                
                print(f"[{i+1}/{n_artworks}] Seed {seed}: {metadata['pattern_type']} "
                      f"({metadata['colormap']}) - {metadata['generation_method']} "
                      f"[ETA: {remaining:.1f}s]")
                
                if progress_callback:
                    progress_callback(i + 1, n_artworks, metadata)
                
                # Close matplotlib figures to save memory
                import matplotlib.pyplot as plt
                plt.close('all')
                
            except Exception as e:
                print(f"[{i+1}/{n_artworks}] Error with seed {seed}: {e}")
                continue
        
        total_time = time.time() - start_time
        print("-" * 60)
        print(f"Batch generation complete!")
        print(f"Total time: {total_time:.2f}s")
        print(f"Average time per artwork: {total_time/n_artworks:.2f}s")
        print(f"Generated {len(self.generated_artworks)} artworks")
        
        # Save batch summary
        self.save_batch_summary(seed_start, n_artworks)
        
        return self.generated_artworks
    
    def save_batch_summary(self, seed_start: int, n_artworks: int):
        """Save a summary of the batch generation."""
        summary = {
            'seed_start': seed_start,
            'n_artworks': n_artworks,
            'n_generated': len(self.generated_artworks),
            'timestamp': datetime.now().isoformat(),
            'artworks': self.generated_artworks
        }
        
        summary_path = f"{self.output_dir}/batch_summary_{seed_start}_{seed_start+n_artworks-1}.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Batch summary saved to: {summary_path}")
    
    def create_gallery_from_batch(self, colormap: str = 'viridis', 
                                 n_cols: int = 4) -> str:
        """
        Create a gallery from the generated artworks.
        
        Args:
            colormap: Colormap for gallery
            n_cols: Number of columns
        
        Returns:
            Path to saved gallery
        """
        if not self.generated_artworks:
            print("No artworks to create gallery from. Run batch_generate first.")
            return None
        
        print(f"Creating gallery from {len(self.generated_artworks)} artworks...")
        
        # Load patterns
        patterns = []
        titles = []
        
        for metadata in self.generated_artworks:
            # Load from CSV
            import pandas as pd
            df = pd.read_csv(metadata['data_path'])
            width = df['x'].max() + 1
            height = df['y'].max() + 1
            pattern = df['intensity'].values.reshape(height, width)
            
            patterns.append(pattern)
            titles.append(f"{metadata['pattern_type']}\nSeed: {metadata['seed']}")
        
        # Create gallery
        gallery_path = f"{self.output_dir}/gallery_batch.png"
        self.visualizer.create_gallery(
            patterns,
            titles=titles,
            colormap=colormap,
            n_cols=n_cols,
            save_path=gallery_path
        )
        
        print(f"Gallery saved to: {gallery_path}")
        return gallery_path
    
    def generate_diverse_collection(self, n_artworks: int = 20,
                                   seed_start: Optional[int] = None) -> List[Dict]:
        """
        Generate a diverse collection using all methods.
        
        Args:
            n_artworks: Number of artworks
            seed_start: Starting seed
        
        Returns:
            List of artwork metadata
        """
        if seed_start is None:
            seed_start = np.random.randint(0, 1000000)
        
        print("Generating diverse art collection...")
        print("=" * 60)
        
        all_artworks = []
        
        # Standard generation
        n_standard = n_artworks // 3
        print(f"\n1. Generating {n_standard} standard artworks...")
        artworks = self.batch_generate(
            n_artworks=n_standard,
            seed_start=seed_start,
            use_vae=False,
            use_gan=False
        )
        all_artworks.extend(artworks)
        
        # VAE generation
        n_vae = n_artworks // 3
        print(f"\n2. Generating {n_vae} VAE artworks...")
        artworks = self.batch_generate(
            n_artworks=n_vae,
            seed_start=seed_start + n_standard,
            use_vae=True,
            use_gan=False
        )
        all_artworks.extend(artworks)
        
        # GAN generation
        n_gan = n_artworks - n_standard - n_vae
        print(f"\n3. Generating {n_gan} GAN artworks...")
        artworks = self.batch_generate(
            n_artworks=n_gan,
            seed_start=seed_start + n_standard + n_vae,
            use_vae=False,
            use_gan=True,
            quality_threshold=0.5
        )
        all_artworks.extend(artworks)
        
        self.generated_artworks = all_artworks
        
        # Create combined gallery
        print("\n4. Creating combined gallery...")
        self.create_gallery_from_batch(colormap='viridis', n_cols=5)
        
        print("\n" + "=" * 60)
        print(f"Diverse collection complete! Generated {len(all_artworks)} artworks.")
        print("=" * 60)
        
        return all_artworks


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Automated art generation')
    parser.add_argument('--n', type=int, default=10, help='Number of artworks to generate')
    parser.add_argument('--seed-start', type=int, default=None, help='Starting seed')
    parser.add_argument('--output-dir', type=str, default='output/automated', help='Output directory')
    parser.add_argument('--width', type=int, default=512, help='Image width')
    parser.add_argument('--height', type=int, default=512, help='Image height')
    parser.add_argument('--use-vae', action='store_true', help='Use VAE generation')
    parser.add_argument('--use-gan', action='store_true', help='Use GAN filtering')
    parser.add_argument('--diverse', action='store_true', help='Generate diverse collection')
    parser.add_argument('--quality-threshold', type=float, default=0.5, help='GAN quality threshold')
    
    args = parser.parse_args()
    
    # Initialize automation
    automation = ArtAutomation(
        output_dir=args.output_dir,
        width=args.width,
        height=args.height
    )
    
    if args.diverse:
        # Generate diverse collection
        automation.generate_diverse_collection(
            n_artworks=args.n,
            seed_start=args.seed_start
        )
    else:
        # Standard batch generation
        automation.batch_generate(
            n_artworks=args.n,
            seed_start=args.seed_start,
            use_vae=args.use_vae,
            use_gan=args.use_gan,
            quality_threshold=args.quality_threshold
        )
        
        # Create gallery
        automation.create_gallery_from_batch()


if __name__ == '__main__':
    main()

