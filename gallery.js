// Art Gallery JavaScript - Dynamic Art Generation

class ArtGenerator {
    constructor() {
        this.artworks = [];
        this.artworkId = 0;
        this.init();
    }

    init() {
        // Bind event listeners
        document.getElementById('generateBtn').addEventListener('click', () => this.generateArt());
        document.getElementById('generateBatchBtn').addEventListener('click', () => this.generateBatch(9));
        document.getElementById('clearBtn').addEventListener('click', () => this.clearGallery());
        
        // Load any saved artworks from localStorage
        this.loadFromStorage();
    }

    // Generate a single artwork
    generateArt() {
        const patternType = document.getElementById('patternSelect').value;
        const colormap = document.getElementById('colormapSelect').value;
        const size = parseInt(document.getElementById('sizeSelect').value);
        
        const canvas = document.createElement('canvas');
        canvas.width = size;
        canvas.height = size;
        const ctx = canvas.getContext('2d');
        
        // Generate pattern
        const pattern = this.generatePattern(patternType, size);
        
        // Apply colormap
        const imageData = this.applyColormap(pattern, colormap, size);
        ctx.putImageData(imageData, 0, 0);
        
        // Add to gallery
        this.addArtworkToGallery(canvas, patternType, colormap);
    }

    // Generate pattern based on type
    generatePattern(type, size) {
        const pattern = new Array(size * size);
        const center = size / 2;
        
        for (let y = 0; y < size; y++) {
            for (let x = 0; x < size; x++) {
                const idx = y * size + x;
                const nx = (x / size) * 2 - 1;
                const ny = (y / size) * 2 - 1;
                
                let value = 0;
                
                switch(type) {
                    case 'sine':
                        value = Math.sin((nx + ny) * Math.PI * 5) * 0.5 + 0.5;
                        break;
                    case 'cosine':
                        value = Math.cos((nx + ny) * Math.PI * 5) * 0.5 + 0.5;
                        break;
                    case 'spiral':
                        const angle = Math.atan2(ny, nx);
                        const dist = Math.sqrt(nx * nx + ny * ny);
                        value = Math.sin(angle * 5 + dist * 10) * 0.5 + 0.5;
                        break;
                    case 'interference':
                        const wave1 = Math.sin(nx * Math.PI * 4);
                        const wave2 = Math.sin(ny * Math.PI * 6);
                        value = (wave1 * wave2) * 0.5 + 0.5;
                        break;
                    case 'perlin':
                        value = this.perlinNoise(nx * 5, ny * 5);
                        break;
                    case 'radial':
                        const r = Math.sqrt(nx * nx + ny * ny);
                        value = Math.max(0, 1 - r);
                        break;
                    case 'random':
                    default:
                        value = Math.random();
                        break;
                }
                
                pattern[idx] = value;
            }
        }
        
        return pattern;
    }

    // Simple Perlin-like noise
    perlinNoise(x, y) {
        const p = [
            151, 160, 137, 91, 90, 15, 131, 13, 201, 95, 96, 53, 194, 233, 7, 225,
            140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148
        ];
        
        const fade = t => t * t * t * (t * (t * 6 - 15) + 10);
        const lerp = (a, b, t) => a + t * (b - a);
        
        const xi = Math.floor(x) & 255;
        const yi = Math.floor(y) & 255;
        const xf = x - Math.floor(x);
        const yf = y - Math.floor(y);
        
        const u = fade(xf);
        const v = fade(yf);
        
        const a = p[xi] + yi;
        const aa = p[a];
        const ab = p[a + 1];
        const b = p[xi + 1] + yi;
        const ba = p[b];
        const bb = p[b + 1];
        
        return lerp(
            lerp(aa, ba, u),
            lerp(ab, bb, u),
            v
        ) / 255;
    }

    // Apply colormap to pattern
    applyColormap(pattern, colormapName, size) {
        const imageData = new ImageData(size, size);
        const colormap = this.getColormap(colormapName);
        
        for (let i = 0; i < pattern.length; i++) {
            const value = Math.max(0, Math.min(1, pattern[i]));
            const color = colormap(value);
            
            const idx = i * 4;
            imageData.data[idx] = color.r;
            imageData.data[idx + 1] = color.g;
            imageData.data[idx + 2] = color.b;
            imageData.data[idx + 3] = 255;
        }
        
        return imageData;
    }

    // Get colormap function
    getColormap(name) {
        const colormaps = {
            viridis: (t) => {
                const r = Math.floor(68 + (228 - 68) * t);
                const g = Math.floor(1 + (109 - 1) * t);
                const b = Math.floor(84 + (176 - 84) * t);
                return { r, g, b };
            },
            plasma: (t) => {
                const r = Math.floor(13 + (240 - 13) * t);
                const g = Math.floor(8 + (249 - 8) * t);
                const b = Math.floor(135 + (33 - 135) * t);
                return { r, g, b };
            },
            inferno: (t) => {
                const r = Math.floor(0 + (252 - 0) * t);
                const g = Math.floor(0 + (141 - 0) * t);
                const b = Math.floor(4 + (10 - 4) * t);
                return { r, g, b };
            },
            magma: (t) => {
                const r = Math.floor(0 + (252 - 0) * t);
                const g = Math.floor(0 + (3 - 0) * t);
                const b = Math.floor(4 + (136 - 4) * t);
                return { r, g, b };
            },
            turbo: (t) => {
                const r = Math.floor(48 + (254 - 48) * t);
                const g = Math.floor(18 + (231 - 18) * t);
                const b = Math.floor(59 + (41 - 59) * t);
                return { r, g, b };
            },
            rainbow: (t) => {
                const hue = t * 360;
                return this.hsvToRgb(hue, 1, 1);
            },
            sunset: (t) => {
                if (t < 0.33) {
                    const r = Math.floor(26 + (229 - 26) * (t / 0.33));
                    const g = Math.floor(26 + (69 - 26) * (t / 0.33));
                    const b = Math.floor(46 + (105 - 46) * (t / 0.33));
                    return { r, g, b };
                } else if (t < 0.66) {
                    const r = Math.floor(229 + (255 - 229) * ((t - 0.33) / 0.33));
                    const g = Math.floor(69 + (107 - 69) * ((t - 0.33) / 0.33));
                    const b = Math.floor(105 + (5 - 105) * ((t - 0.33) / 0.33));
                    return { r, g, b };
                } else {
                    const r = Math.floor(255 + (255 - 255) * ((t - 0.66) / 0.34));
                    const g = Math.floor(107 + (165 - 107) * ((t - 0.66) / 0.34));
                    const b = Math.floor(5 + (0 - 5) * ((t - 0.66) / 0.34));
                    return { r, g, b };
                }
            },
            ocean: (t) => {
                const r = Math.floor(0 + (0 - 0) * t);
                const g = Math.floor(4 + (78 - 4) * t);
                const b = Math.floor(40 + (255 - 40) * t);
                return { r, g, b };
            },
            aurora: (t) => {
                if (t < 0.5) {
                    const r = Math.floor(0 + (0 - 0) * (t / 0.5));
                    const g = Math.floor(17 + (170 - 17) * (t / 0.5));
                    const b = Math.floor(34 + (255 - 34) * (t / 0.5));
                    return { r, g, b };
                } else {
                    const r = Math.floor(0 + (170 - 0) * ((t - 0.5) / 0.5));
                    const g = Math.floor(170 + (255 - 170) * ((t - 0.5) / 0.5));
                    const b = Math.floor(255 + (0 - 255) * ((t - 0.5) / 0.5));
                    return { r, g, b };
                }
            },
            cyberpunk: (t) => {
                if (t < 0.5) {
                    const r = Math.floor(0 + (0 - 0) * (t / 0.5));
                    const g = Math.floor(0 + (0 - 0) * (t / 0.5));
                    const b = Math.floor(51 + (255 - 51) * (t / 0.5));
                    return { r, g, b };
                } else {
                    const r = Math.floor(0 + (255 - 0) * ((t - 0.5) / 0.5));
                    const g = Math.floor(0 + (0 - 0) * ((t - 0.5) / 0.5));
                    const b = Math.floor(255 + (255 - 255) * ((t - 0.5) / 0.5));
                    return { r, g, b };
                }
            }
        };
        
        return colormaps[name] || colormaps.viridis;
    }

    // Convert HSV to RGB
    hsvToRgb(h, s, v) {
        const c = v * s;
        const x = c * (1 - Math.abs((h / 60) % 2 - 1));
        const m = v - c;
        
        let r, g, b;
        if (h < 60) { r = c; g = x; b = 0; }
        else if (h < 120) { r = x; g = c; b = 0; }
        else if (h < 180) { r = 0; g = c; b = x; }
        else if (h < 240) { r = 0; g = x; b = c; }
        else if (h < 300) { r = x; g = 0; b = c; }
        else { r = c; g = 0; b = x; }
        
        return {
            r: Math.floor((r + m) * 255),
            g: Math.floor((g + m) * 255),
            b: Math.floor((b + m) * 255)
        };
    }

    // Add artwork to gallery
    addArtworkToGallery(canvas, patternType, colormap) {
        const gallery = document.getElementById('gallery');
        
        // Remove empty state if present
        const emptyState = gallery.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
        }
        
        // Create artwork card
        const card = document.createElement('div');
        card.className = 'artwork-card new';
        this.artworkId++;
        
        const artworkId = `artwork-${this.artworkId}`;
        const timestamp = new Date().toLocaleString();
        
        card.innerHTML = `
            <div class="artwork-image-container">
                <img src="${canvas.toDataURL()}" alt="Generated Art" class="artwork-image" id="${artworkId}">
            </div>
            <div class="artwork-info">
                <div class="artwork-title">${this.formatPatternName(patternType)}</div>
                <div class="artwork-meta">
                    <span>${colormap}</span>
                    <span>${timestamp}</span>
                </div>
                <div class="artwork-actions">
                    <button class="btn-small btn-download" onclick="artGenerator.downloadArt('${artworkId}')">Download</button>
                    <button class="btn-small btn-delete" onclick="artGenerator.deleteArt(this)">Delete</button>
                </div>
            </div>
        `;
        
        gallery.insertBefore(card, gallery.firstChild);
        
        // Save to storage
        this.saveToStorage();
        
        // Remove animation class after animation completes
        setTimeout(() => {
            card.classList.remove('new');
        }, 500);
    }

    // Format pattern name
    formatPatternName(type) {
        const names = {
            'sine': 'Sine Wave',
            'cosine': 'Cosine Wave',
            'spiral': 'Spiral',
            'interference': 'Wave Interference',
            'perlin': 'Perlin Noise',
            'radial': 'Radial Gradient',
            'random': 'Random Pattern'
        };
        return names[type] || type;
    }

    // Generate batch of artworks
    generateBatch(count) {
        const button = document.getElementById('generateBatchBtn');
        const originalText = button.textContent;
        button.disabled = true;
        button.textContent = 'Generating...';
        
        let generated = 0;
        const generateNext = () => {
            if (generated < count) {
                // Randomize parameters for variety
                const patterns = ['sine', 'cosine', 'spiral', 'interference', 'perlin', 'radial', 'random'];
                const colormaps = ['viridis', 'plasma', 'inferno', 'magma', 'turbo', 'rainbow', 'sunset', 'ocean', 'aurora', 'cyberpunk'];
                
                document.getElementById('patternSelect').value = patterns[Math.floor(Math.random() * patterns.length)];
                document.getElementById('colormapSelect').value = colormaps[Math.floor(Math.random() * colormaps.length)];
                
                this.generateArt();
                generated++;
                
                // Small delay for visual effect
                setTimeout(generateNext, 100);
            } else {
                button.disabled = false;
                button.textContent = originalText;
            }
        };
        
        generateNext();
    }

    // Clear gallery
    clearGallery() {
        if (confirm('Are you sure you want to clear all artworks?')) {
            const gallery = document.getElementById('gallery');
            gallery.innerHTML = '<div class="empty-state"><p>🎨 Click "Generate New Art" to create your first artwork!</p></div>';
            this.artworks = [];
            this.artworkId = 0;
            localStorage.removeItem('artGallery');
        }
    }

    // Download artwork
    downloadArt(imageId) {
        const img = document.getElementById(imageId);
        const link = document.createElement('a');
        link.download = `artwork-${Date.now()}.png`;
        link.href = img.src;
        link.click();
    }

    // Delete artwork
    deleteArt(button) {
        const card = button.closest('.artwork-card');
        card.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            card.remove();
            
            // Show empty state if gallery is empty
            const gallery = document.getElementById('gallery');
            if (gallery.children.length === 0) {
                gallery.innerHTML = '<div class="empty-state"><p>🎨 Click "Generate New Art" to create your first artwork!</p></div>';
            }
            
            this.saveToStorage();
        }, 300);
    }

    // Save to localStorage
    saveToStorage() {
        const gallery = document.getElementById('gallery');
        const artworks = [];
        
        gallery.querySelectorAll('.artwork-card').forEach(card => {
            const img = card.querySelector('img');
            const title = card.querySelector('.artwork-title').textContent;
            const meta = card.querySelector('.artwork-meta').textContent;
            
            artworks.push({
                image: img.src,
                title: title,
                meta: meta
            });
        });
        
        localStorage.setItem('artGallery', JSON.stringify(artworks));
    }

    // Load from localStorage
    loadFromStorage() {
        const saved = localStorage.getItem('artGallery');
        if (saved) {
            const artworks = JSON.parse(saved);
            artworks.forEach(artwork => {
                const gallery = document.getElementById('gallery');
                const emptyState = gallery.querySelector('.empty-state');
                if (emptyState) {
                    emptyState.remove();
                }
                
                const card = document.createElement('div');
                card.className = 'artwork-card';
                this.artworkId++;
                
                const artworkId = `artwork-${this.artworkId}`;
                
                card.innerHTML = `
                    <div class="artwork-image-container">
                        <img src="${artwork.image}" alt="Generated Art" class="artwork-image" id="${artworkId}">
                    </div>
                    <div class="artwork-info">
                        <div class="artwork-title">${artwork.title}</div>
                        <div class="artwork-meta">${artwork.meta}</div>
                        <div class="artwork-actions">
                            <button class="btn-small btn-download" onclick="artGenerator.downloadArt('${artworkId}')">Download</button>
                            <button class="btn-small btn-delete" onclick="artGenerator.deleteArt(this)">Delete</button>
                        </div>
                    </div>
                `;
                
                gallery.appendChild(card);
            });
        }
    }
}

// Initialize gallery when page loads
let artGenerator;
document.addEventListener('DOMContentLoaded', () => {
    artGenerator = new ArtGenerator();
});

// Add fadeOut animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: scale(1);
        }
        to {
            opacity: 0;
            transform: scale(0.9);
        }
    }
`;
document.head.appendChild(style);

