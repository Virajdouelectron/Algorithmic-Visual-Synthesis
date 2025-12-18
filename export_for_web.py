"""
Export generated artworks for web gallery.
Converts Python-generated images to web-optimized format.
"""

import os
import json
import shutil
from pathlib import Path
from automate_generation import ArtAutomation


def export_for_web(n_artworks: int = 20, 
                   output_dir: str = 'web_gallery/images',
                   seed_start: int = None):
    """
    Generate artworks and export them for web gallery.
    
    Args:
        n_artworks: Number of artworks to generate
        output_dir: Output directory for web images
        seed_start: Starting seed
    """
    print("Exporting artworks for web gallery...")
    print("=" * 60)
    
    # Generate artworks
    automation = ArtAutomation(
        output_dir='output/web_export',
        width=512,
        height=512
    )
    
    artworks = automation.batch_generate(
        n_artworks=n_artworks,
        seed_start=seed_start,
        use_vae=False,
        use_gan=False
    )
    
    # Create web directory
    web_dir = Path(output_dir)
    web_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy images to web directory
    print(f"\nCopying images to {output_dir}...")
    image_list = []
    
    for i, artwork in enumerate(artworks):
        src_image = artwork['image_path']
        dst_image = web_dir / f"artwork_{i+1:03d}.png"
        
        shutil.copy2(src_image, dst_image)
        image_list.append({
            'id': f'artwork_{i+1:03d}',
            'filename': dst_image.name,
            'pattern_type': artwork['pattern_type'],
            'colormap': artwork['colormap'],
            'seed': artwork['seed']
        })
        
        print(f"  Copied: {dst_image.name}")
    
    # Save image list as JSON
    image_list_path = web_dir.parent / 'artworks.json'
    with open(image_list_path, 'w') as f:
        json.dump(image_list, f, indent=2)
    
    print(f"\nExported {len(artworks)} artworks to {output_dir}")
    print(f"Image list saved to: {image_list_path}")
    print("\nTo use in web gallery:")
    print(f"1. Place images in: {output_dir}")
    print("2. Open gallery.html in a web browser")
    print("3. Or use a local web server: python -m http.server 8000")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Export artworks for web gallery')
    parser.add_argument('--n', type=int, default=20, help='Number of artworks')
    parser.add_argument('--seed-start', type=int, default=None, help='Starting seed')
    parser.add_argument('--output-dir', type=str, default='web_gallery/images', help='Output directory')
    
    args = parser.parse_args()
    
    export_for_web(
        n_artworks=args.n,
        output_dir=args.output_dir,
        seed_start=args.seed_start
    )

