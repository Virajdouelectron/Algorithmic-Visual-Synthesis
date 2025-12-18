# Algorithmic Visual Synthesis - Generative Art System

A system that generates unique visual art by combining mathematical functions, randomness, and generative model concepts (VAE/GAN), displayed in a web-based gallery.

## Quick Start

### For Web Gallery (Netlify Deployment)

1. **Deploy to Netlify:**
   - Go to [netlify.com](https://netlify.com)
   - Drag and drop the project folder
   - Your gallery is live!

2. **Or test locally:**
   ```bash
   python -m http.server 8000
   # Open http://localhost:8000/gallery.html
   ```

### For Python Backend

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate art data:**
   ```bash
   python generate_art_data.py --samples 5 --width 256 --height 256
   ```

3. **Generate with automation:**
   ```bash
   python automate_generation.py --n 10 --seed-start 1000
   ```

## Project Structure

```
Algorithmic-Visual-Synthesis/
├── generate_art_data.py        # Data generation script (Step 1)
├── generative_models.py        # VAE/GAN concepts (Step 2)
├── art_visualization.py        # Art visualization system (Step 3)
├── automate_generation.py     # Automation system (Step 4)
├── gallery.html               # Web gallery page (Step 5)
├── gallery.css                 # Web gallery styling (Step 5)
├── gallery.js                  # Web gallery JavaScript (Step 5)
├── export_for_web.py          # Export script for web
├── netlify.toml                # Netlify configuration (Step 6)
├── config_automation.json      # Automation configuration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Step 1: Data Generation

### Overview

The data generation system creates pixel-level datasets using various mathematical functions:
- **Sine/Cosine Waves**: Periodic wave patterns
- **Spirals**: Rotational patterns with varying tightness
- **Wave Interference**: Interference patterns from multiple waves
- **Random Noise**: Pure random patterns
- **Perlin-like Noise**: Multi-octave noise for organic textures
- **Radial Gradients**: Circular gradient patterns

Each pattern can be combined with different color schemes:
- Grayscale
- Red, Green, Blue (single channel)
- Rainbow (hue-based)
- Warm (red/orange tones)
- Cool (blue/green tones)

### Installation

1. Install Python 3.8 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

Optional (for visualization):
```bash
pip install matplotlib
```

### Usage

#### Basic Usage

Generate a dataset with default settings (10 samples per pattern type, 512x512 images):

```bash
python generate_art_data.py
```

This will create:
- `data/art_dataset.csv` - Complete dataset with all patterns
- `data/art_dataset_sample.csv` - Sample pattern for quick inspection

#### Command-Line Options

```bash
python generate_art_data.py --samples 5 --width 256 --height 256 --output-dir data
```

Options:
- `--samples`: Number of samples per pattern type (default: 10)
- `--width`: Image width in pixels (default: 512)
- `--height`: Image height in pixels (default: 512)
- `--output-dir`: Output directory for CSV files (default: data)

**Note**: Larger images and more samples create larger CSV files. For initial testing, use:
```bash
python generate_art_data.py --samples 2 --width 256 --height 256
```

#### Custom Usage

You can modify the script to customize:
- Image dimensions (default: 512x512)
- Number of samples per pattern type
- Pattern parameters (frequencies, phases, etc.)
- Color schemes

Example in Python:

```python
from generate_art_data import ArtDataGenerator, generate_dataset

# Generate custom dataset
df = generate_dataset(output_dir='data', num_samples=20)

# Or create individual patterns
generator = ArtDataGenerator(width=256, height=256)
pattern = generator.sine_wave(frequency=5.0)
rgb = generator.generate_rgb_data(pattern, color_scheme='rainbow')
df = generator.to_dataframe(pattern, rgb, pattern_name='my_pattern')
```

### Dataset Format

The generated CSV file contains the following columns:

- `x`: X coordinate (0 to width-1)
- `y`: Y coordinate (0 to height-1)
- `intensity`: Normalized intensity value [0, 1]
- `r`: Red channel value [0, 1]
- `g`: Green channel value [0, 1]
- `b`: Blue channel value [0, 1]
- `pattern_type`: Unique identifier for each pattern

### Uploading to Kaggle

#### Prerequisites

1. Install Kaggle API:
```bash
pip install kaggle
```

2. Set up Kaggle credentials:
   - Go to https://www.kaggle.com/account
   - Scroll to "API" section
   - Click "Create New API Token"
   - Save `kaggle.json` to `~/.kaggle/` (Linux/Mac) or `C:\Users\<username>\.kaggle\` (Windows)

#### Upload Dataset

1. **Create a new dataset on Kaggle:**
   - Go to https://www.kaggle.com/datasets
   - Click "New Dataset"
   - Fill in dataset details

2. **Using Kaggle API (Recommended):**

```bash
# Install kaggle package if not already installed
pip install kaggle

# Create a dataset metadata file (dataset-metadata.json)
# Then upload:
kaggle datasets create -p data/ -r zip
```

3. **Manual Upload:**
   - Zip the CSV file(s)
   - Go to https://www.kaggle.com/datasets
   - Click "New Dataset"
   - Upload the zip file
   - Add description, tags, and license information

#### Dataset Metadata Template

Create `dataset-metadata.json`:

```json
{
  "title": "Algorithmic Visual Synthesis - Art Patterns",
  "id": "your-username/algorithmic-visual-synthesis",
  "licenses": [{"name": "CC0-1.0"}],
  "keywords": ["generative-art", "computer-vision", "mathematical-functions", "visual-synthesis"],
  "collaborators": []
}
```

### Dataset Statistics

After generation, the script displays:
- Total number of pixels
- Number of unique patterns
- File size
- Sample data preview

## Step 2: Generative Model Logic (VAE/GAN Concepts)

### Overview

The generative model system implements VAE and GAN concepts using NumPy and mathematical functions (no deep learning libraries required).

#### VAE Concept

- **Encoder**: Treats mathematical pattern parameters as features and maps them to a latent space representation
- **Latent Space**: Samples randomness from a learned latent distribution
- **Decoder**: Reconstructs patterns from latent vectors using mathematical transformations

#### GAN Concept (Lightweight)

- **Generator**: Creates random art patterns with diverse parameters
- **Discriminator**: Filters visually pleasing outputs based on quality metrics (contrast, entropy, smoothness, symmetry)

### Usage

#### VAE Example

```python
from generative_models import VariationalAutoEncoder
from generate_art_data import ArtDataGenerator

# Initialize VAE
vae = VariationalAutoEncoder(latent_dim=16)
generator = ArtDataGenerator(width=256, height=256)

# Encode pattern parameters
params = {'frequency': 5.0, 'phase': np.pi/4}
mean, log_var = vae.encode(params)

# Sample from latent space
latent = vae.sample_latent(mean, log_var, seed=42)

# Decode to pattern
pattern = vae.decode(latent, 'sine_wave', generator)

# Generate new pattern from random latent
new_pattern = vae.generate('spiral', generator, seed=123)
```

#### GAN Example

```python
from generative_models import GenerativeAdversarialNetwork

# Initialize GAN
gan = GenerativeAdversarialNetwork(width=256, height=256)

# Generate high-quality art
high_quality_patterns = gan.generate_art(
    n=20, 
    quality_threshold=0.5, 
    seed=42
)

# Generate best patterns from many candidates
best_patterns = gan.generate_best(
    n_candidates=50, 
    n_best=10, 
    seed=42
)
```

#### Example Usage

```python
# VAE encoding/decoding example
from generative_models import VariationalAutoEncoder
from generate_art_data import ArtDataGenerator
import numpy as np

vae = VariationalAutoEncoder(latent_dim=16)
generator = ArtDataGenerator(width=256, height=256)

# Encode and decode
params = {'frequency': 5.0, 'phase': np.pi/4}
mean, log_var = vae.encode(params)
latent = vae.sample_latent(mean, log_var, seed=42)
pattern = vae.decode(latent, 'sine_wave', generator)

# GAN generation example
from generative_models import GenerativeAdversarialNetwork

gan = GenerativeAdversarialNetwork(width=256, height=256)
best_patterns = gan.generate_best(n_candidates=50, n_best=10, seed=42)
```

### Model Components

#### VariationalAutoEncoder
- `encode(params)`: Encode parameters to latent space
- `sample_latent(mean, log_var)`: Sample from latent distribution
- `decode(latent, pattern_type)`: Decode latent to pattern
- `generate(pattern_type)`: Generate from random latent
- `reconstruct(params, pattern_type)`: Full encode-decode cycle

#### GenerativeAdversarialNetwork
- `generate_art(n, quality_threshold)`: Generate and filter patterns
- `generate_best(n_candidates, n_best)`: Generate many, return best

#### PatternDiscriminator
- `evaluate(pattern)`: Calculate quality score (0-1)
- `filter(patterns, threshold)`: Filter by quality
- `is_real(pattern, threshold)`: Binary quality check

Quality metrics:
- **Contrast**: Standard deviation (prefer medium-high)
- **Entropy**: Information content (prefer medium)
- **Smoothness**: Inverse gradient (prefer moderate)
- **Symmetry**: Horizontal/vertical symmetry (bonus)

## Step 3: Art Generation (Matplotlib)

### Overview

The visualization system converts numerical matrices into artistic images using Matplotlib colormaps. It provides:

- **Pattern Visualization**: Convert 2D arrays to images
- **Colormap Support**: 30+ built-in and 8 custom artistic colormaps
- **Gallery Creation**: Generate multi-image galleries
- **RGB Support**: Visualize full-color patterns
- **Batch Processing**: Convert CSV datasets to images

### Features

#### Colormaps

**Artistic Colormaps:**
- viridis, plasma, inferno, magma, turbo, rainbow, hsv, twilight

**Custom Artistic Colormaps:**
- sunset, ocean, forest, fire, aurora, neon, vintage, cyberpunk

**Diverging Colormaps:**
- RdBu, RdYlBu, Spectral, coolwarm, seismic, PiYG, PRGn, BrBG

**Sequential Colormaps:**
- Blues, Greens, Reds, Oranges, Purples, Greys, YlOrRd, YlGnBu, hot, cool

### Usage

#### Basic Visualization

```python
from art_visualization import ArtVisualizer
from generate_art_data import ArtDataGenerator

visualizer = ArtVisualizer()
generator = ArtDataGenerator(width=256, height=256)

# Generate and visualize
pattern = generator.sine_wave(frequency=5.0)
visualizer.visualize_pattern(
    pattern,
    colormap='plasma',
    title='Sine Wave Art',
    save_path='output/sine_wave.png'
)
```

#### Custom Colormaps

```python
# Use custom artistic colormaps
visualizer.visualize_pattern(
    pattern,
    colormap='aurora',  # or 'sunset', 'ocean', 'cyberpunk', etc.
    save_path='output/art.png'
)
```

#### Gallery Creation

```python
patterns = [pattern1, pattern2, pattern3, ...]
titles = ['Pattern 1', 'Pattern 2', 'Pattern 3', ...]

visualizer.create_gallery(
    patterns,
    titles=titles,
    colormap='viridis',
    n_cols=3,
    save_path='output/gallery.png'
)
```

#### Multi-Colormap Comparison

```python
# Show same pattern with different colormaps
visualizer.create_multi_colormap_gallery(
    pattern,
    colormaps=['viridis', 'plasma', 'inferno', 'aurora', 'cyberpunk'],
    save_path='output/comparison.png'
)
```

#### Load from CSV

```python
from art_visualization import load_pattern_from_csv

# Load pattern from Step 1 CSV
intensity, rgb = load_pattern_from_csv('data/art_dataset.csv', pattern_name='sine_wave_000')

# Visualize
visualizer.visualize_pattern(intensity, colormap='plasma', save_path='output/from_csv.png')
if rgb is not None:
    visualizer.visualize_rgb(rgb, save_path='output/from_csv_rgb.png')
```

#### Batch Processing

```python
from art_visualization import batch_visualize_from_csv

# Convert all patterns in CSV to images
batch_visualize_from_csv(
    'data/art_dataset.csv',
    output_dir='output/images',
    colormaps=['viridis', 'plasma', 'inferno'],
    pattern_limit=10  # Optional limit
)
```

#### Integration with VAE/GAN

```python
from generative_models import VariationalAutoEncoder, GenerativeAdversarialNetwork

# VAE visualization
vae = VariationalAutoEncoder()
pattern = vae.generate('spiral', generator, seed=42)
visualizer.visualize_pattern(pattern, colormap='plasma', save_path='output/vae_art.png')

# GAN visualization
gan = GenerativeAdversarialNetwork()
best_patterns = gan.generate_best(n_candidates=50, n_best=10)

for pattern, ptype, params, score in best_patterns:
    visualizer.visualize_pattern(
        pattern,
        colormap='viridis',
        title=f'{ptype} (Score: {score:.3f})',
        save_path=f'output/gan_{ptype}.png'
    )
```

### Example Usage

```python
from art_visualization import ArtVisualizer, batch_visualize_from_csv
from generate_art_data import ArtDataGenerator

# Generate and visualize
visualizer = ArtVisualizer()
generator = ArtDataGenerator(width=256, height=256)
pattern = generator.sine_wave(frequency=5.0)
visualizer.visualize_pattern(pattern, colormap='plasma', save_path='output/sine_wave.png')

# Batch process CSV
batch_visualize_from_csv('data/art_dataset.csv', output_dir='output/images')
```

### Output Structure

```
output/images/
├── basic_patterns/          # Individual pattern visualizations
├── vae/                    # VAE-generated art
├── gan/                    # GAN-generated art
├── batch/                  # Batch-processed CSV patterns
├── gallery_*.png          # Pattern galleries
└── multi_colormap_*.png   # Colormap comparisons
```

## Step 4: Automation

### Overview

The automation system runs the generator multiple times with different random seeds, producing unique artworks each time. It provides:

- **Batch Generation**: Generate multiple artworks automatically
- **Seed Management**: Control randomness with seed values
- **Multiple Methods**: Standard, VAE, and GAN generation
- **Progress Tracking**: Real-time progress and ETA
- **Metadata Tracking**: Complete metadata for each artwork
- **Gallery Creation**: Automatic gallery generation from batches

### Features

- **Sequential Seed Generation**: Each run uses a different seed for uniqueness
- **Multiple Generation Methods**: Standard, VAE, or GAN filtering
- **Customizable Parameters**: Pattern types, colormaps, quality thresholds
- **Diverse Collections**: Mix of standard, VAE, and GAN artworks
- **Automatic Organization**: Images, data, and metadata saved separately
- **Batch Summaries**: JSON summaries of each batch

### Usage

#### Basic Automation

```python
from automate_generation import ArtAutomation

automation = ArtAutomation(output_dir='output/automated')

# Generate 10 artworks with sequential seeds
artworks = automation.batch_generate(
    n_artworks=10,
    seed_start=1000
)
```

#### Command-Line Usage

```bash
# Generate 10 artworks
python automate_generation.py --n 10 --seed-start 1000

# Generate with VAE
python automate_generation.py --n 10 --use-vae

# Generate with GAN filtering
python automate_generation.py --n 10 --use-gan --quality-threshold 0.6

# Generate diverse collection (standard + VAE + GAN)
python automate_generation.py --n 30 --diverse

# Custom image size
python automate_generation.py --n 10 --width 256 --height 256
```

#### Advanced Usage

```python
# Generate with specific pattern types and colormaps
artworks = automation.batch_generate(
    n_artworks=20,
    seed_start=5000,
    pattern_types=['spiral', 'wave_interference'],
    colormaps=['plasma', 'inferno', 'aurora'],
    use_vae=False,
    use_gan=False
)

# Generate diverse collection
artworks = automation.generate_diverse_collection(
    n_artworks=30,
    seed_start=10000
)

# Create gallery from batch
automation.create_gallery_from_batch(colormap='viridis', n_cols=4)
```

#### Single Artwork Generation

```python
# Generate single artwork with specific seed
metadata = automation.generate_with_seed(
    seed=12345,
    pattern_type='spiral',
    colormap='plasma',
    use_vae=False,
    use_gan=False
)

print(f"Generated: {metadata['id']}")
print(f"Pattern: {metadata['pattern_type']}")
print(f"Image: {metadata['image_path']}")
```

### Output Structure

```
output/automated/
├── images/                    # Generated images
│   ├── art_1000_*.png        # Pattern images
│   └── art_1000_*_rgb.png    # RGB images
├── data/                      # CSV data files
│   └── art_1000_*.csv
├── metadata/                  # JSON metadata
│   └── art_1000_*.json
├── gallery_batch.png         # Batch gallery
└── batch_summary_*.json      # Batch summaries
```

### Metadata Format

Each artwork includes complete metadata:

```json
{
  "id": "art_1000_20251219_004329",
  "seed": 1000,
  "pattern_type": "wave_interference",
  "colormap": "plasma",
  "color_scheme": "rainbow",
  "generation_method": "standard",
  "width": 512,
  "height": 512,
  "timestamp": "20251219_004329",
  "image_path": "output/automated/images/art_1000_*.png",
  "data_path": "output/automated/data/art_1000_*.csv",
  "metadata_path": "output/automated/metadata/art_1000_*.json"
}
```

### Example Usage

```python
from automate_generation import ArtAutomation

# Basic automation
automation = ArtAutomation(output_dir='output/automated')
artworks = automation.batch_generate(n_artworks=10, seed_start=1000)

# Diverse collection (standard + VAE + GAN)
artworks = automation.generate_diverse_collection(n_artworks=30, seed_start=10000)
```

### Configuration

Edit `config_automation.json` to customize:
- Default settings
- Pattern types
- Colormaps
- Batch presets

### Best Practices

1. **Seed Management**: Use sequential seeds for reproducibility
2. **Batch Sizes**: Start with small batches (5-10) for testing
3. **Memory**: Close matplotlib figures between generations
4. **Organization**: Use separate output directories for different runs
5. **Quality**: Use GAN filtering for high-quality collections

## Step 5: Web Visualization (HTML + CSS + JavaScript)

### Overview

A modern, interactive web gallery for displaying and generating algorithmic art. Features:

- **Dynamic Art Generation**: Generate art directly in the browser using JavaScript
- **Interactive Gallery**: View, download, and manage generated artworks
- **Modern Design**: Beautiful, responsive UI with dark theme
- **Multiple Patterns**: 7 pattern types (sine, cosine, spiral, interference, perlin, radial, random)
- **10 Colormaps**: Including custom artistic colormaps (sunset, ocean, aurora, cyberpunk)
- **Batch Generation**: Generate multiple artworks at once
- **Local Storage**: Artworks persist in browser storage

### Features

- **Real-time Generation**: Generate art instantly in the browser
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Download Functionality**: Save artworks as PNG files
- **Gallery Management**: Add, view, and delete artworks
- **Customizable**: Choose pattern type, colormap, and size
- **No Backend Required**: Pure client-side JavaScript

### Usage

#### Opening the Gallery

1. **Simple Method**: Open `gallery.html` directly in a web browser
   ```bash
   # Double-click gallery.html or:
   start gallery.html  # Windows
   open gallery.html   # macOS
   xdg-open gallery.html  # Linux
   ```

2. **With Local Server** (Recommended):
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Then open: http://localhost:8000/gallery.html
   ```

#### Generating Art

1. **Single Artwork**: Click "Generate New Art" button
2. **Batch Generation**: Click "Generate Batch (9)" for multiple artworks
3. **Customize**: Select pattern type, colormap, and size from dropdowns
4. **Download**: Click "Download" on any artwork to save it
5. **Delete**: Click "Delete" to remove artworks from gallery

#### Exporting Python-Generated Art for Web

```bash
# Export 20 artworks for web gallery
python export_for_web.py --n 20 --seed-start 1000

# Images will be saved to web_gallery/images/
```

### File Structure

```
Algorithmic-Visual-Synthesis/
├── gallery.html          # Main gallery page
├── gallery.css           # Styling
├── gallery.js            # JavaScript for art generation
└── (images/ directory created when exporting)
    └── artwork_*.png
```

### Pattern Types

- **Sine Wave**: Periodic sine wave patterns
- **Cosine Wave**: Periodic cosine wave patterns
- **Spiral**: Rotational spiral patterns
- **Wave Interference**: Interference patterns from multiple waves
- **Perlin Noise**: Perlin noise for organic textures
- **Radial Gradient**: Circular gradient patterns
- **Random**: Random noise patterns

### Colormaps

**Standard:**
- Viridis, Plasma, Inferno, Magma, Turbo, Rainbow

**Custom Artistic:**
- Sunset, Ocean, Aurora, Cyberpunk

### Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Modern mobile browsers

### Customization

Edit `gallery.js` to:
- Add new pattern types
- Add new colormaps
- Modify generation parameters
- Change gallery layout

Edit `gallery.css` to:
- Change color scheme
- Modify layout
- Adjust card sizes
- Customize animations

### Integration with Python System

The web gallery can work standalone, but you can also:

1. **Export Python Artworks**: Use `export_for_web.py` to generate artworks with Python and export them
2. **Load Pre-generated Images**: Modify `gallery.js` to load images from `web_gallery/images/`
3. **Hybrid Approach**: Use Python for complex generation, JavaScript for quick previews

## Step 6: Deployment & Sharing

### Overview

Deploy your Algorithmic Visual Synthesis gallery to the web and share it with the world. Multiple deployment options are available, from free hosting to custom domains.

### Quick Deploy Options

#### Netlify (Recommended - Fast, Free, Easy)

**Steps:**
1. Go to [netlify.com](https://netlify.com)
2. Sign up/login (free account)
3. Click "Add new site" → "Import an existing project"
4. Drag and drop your project folder (or connect to Git)
5. Your site is live instantly!

**Or use CLI:**
```bash
npm install -g netlify-cli
netlify deploy --prod
```

**Configuration:**
- The `netlify.toml` file is already configured
- No build step needed (static site)
- Automatic HTTPS enabled
- Custom domain support

#### Other Options

**GitHub Pages:**
1. Create GitHub repository
2. Push your code
3. Enable GitHub Pages in repository settings
4. Your site is live at `https://yourusername.github.io/algorithmic-visual-synthesis/`

**Vercel:**
1. Go to [vercel.com](https://vercel.com)
2. Import your Git repository
3. Deploy automatically

**Local Testing:**
```bash
python -m http.server 8000
# Then visit: http://localhost:8000/gallery.html
```

### Pre-Deployment Checklist

- [ ] Test gallery locally
- [ ] Verify all files are present
- [ ] Test on multiple browsers
- [ ] Test on mobile devices
- [ ] Verify download functionality
- [ ] Check localStorage works
- [ ] Run `deploy.sh check` or `deploy.bat check`

### Custom Domain

All platforms support custom domains:
- **GitHub Pages**: Add `CNAME` file
- **Netlify**: Configure in dashboard
- **Vercel**: Add domain in project settings

### Sharing Your Gallery

Once deployed, share your gallery:
- Social media posts
- Embed in websites
- QR codes
- Direct links

### Deployment Tips

- **Netlify**: The `netlify.toml` file is pre-configured with redirects and security headers
- **Custom Domain**: Add your domain in Netlify dashboard → Site settings → Domain management
- **Performance**: All static files are automatically optimized and cached
- **HTTPS**: Automatically enabled on Netlify

### Next Steps

- Deploy your gallery
- Share with the world
- Collect feedback
- Iterate and improve

## License

This project is open source and available for experimentation and learning.

