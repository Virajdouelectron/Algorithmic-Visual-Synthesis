"""
Generative Model Logic - VAE and GAN Concepts
Implemented using NumPy and mathematical functions (no deep learning libraries).
"""

import numpy as np
from typing import Tuple, Dict, List, Optional
from generate_art_data import ArtDataGenerator


class PatternEncoder:
    """
    VAE Encoder Concept: Encodes mathematical pattern parameters into latent space.
    Treats pattern parameters as features and maps them to a latent representation.
    """
    
    def __init__(self, latent_dim: int = 16):
        """
        Initialize the encoder.
        
        Args:
            latent_dim: Dimension of the latent space
        """
        self.latent_dim = latent_dim
        # Learnable transformation matrices (simulated with random initialization)
        # In a real VAE, these would be learned, here we use fixed transformations
        np.random.seed(42)
        self.encoding_matrix = np.random.randn(10, latent_dim) * 0.1
        self.bias = np.random.randn(latent_dim) * 0.05
    
    def encode_parameters(self, params: Dict[str, float]) -> np.ndarray:
        """
        Encode pattern parameters into latent space.
        
        Args:
            params: Dictionary of pattern parameters (frequency, phase, turns, etc.)
        
        Returns:
            Latent vector representation
        """
        # Extract and normalize parameters
        feature_vector = np.array([
            params.get('frequency', 0.0),
            params.get('phase', 0.0),
            params.get('turns', 0.0),
            params.get('tightness', 0.0),
            params.get('freq1', 0.0),
            params.get('freq2', 0.0),
            params.get('center_x', 0.0),
            params.get('center_y', 0.0),
            params.get('octaves', 0.0),
            params.get('scale', 0.0)
        ])
        
        # Normalize features to [-1, 1] range
        feature_vector = np.tanh(feature_vector)
        
        # Project to latent space (simulated encoding)
        latent = np.dot(feature_vector, self.encoding_matrix) + self.bias
        
        # Apply non-linearity and normalize
        latent = np.tanh(latent)
        
        return latent
    
    def encode_pattern_type(self, pattern_type: str) -> np.ndarray:
        """
        Encode pattern type name into a numerical vector.
        
        Args:
            pattern_type: Name of the pattern (e.g., 'sine_wave', 'spiral')
        
        Returns:
            Encoded pattern type vector
        """
        pattern_types = {
            'sine_wave': 0,
            'cosine_wave': 1,
            'spiral': 2,
            'wave_interference': 3,
            'random_noise': 4,
            'perlin_noise': 5,
            'radial_gradient': 6
        }
        
        pattern_idx = pattern_types.get(pattern_type.split('_')[0], 0)
        # One-hot encoding
        encoded = np.zeros(7)
        encoded[pattern_idx] = 1.0
        
        return encoded


class PatternDecoder:
    """
    VAE Decoder Concept: Reconstructs patterns from latent space vectors.
    Maps latent vectors back to pattern parameters and generates visual patterns.
    """
    
    def __init__(self, latent_dim: int = 16):
        """
        Initialize the decoder.
        
        Args:
            latent_dim: Dimension of the latent space
        """
        self.latent_dim = latent_dim
        # Decoding transformation matrix
        np.random.seed(43)
        self.decoding_matrix = np.random.randn(latent_dim, 10) * 0.1
        self.decoding_bias = np.random.randn(10) * 0.05
    
    def decode_to_parameters(self, latent: np.ndarray) -> Dict[str, float]:
        """
        Decode latent vector back to pattern parameters.
        
        Args:
            latent: Latent space vector
        
        Returns:
            Dictionary of pattern parameters
        """
        # Project from latent space to parameter space
        params_vector = np.dot(latent, self.decoding_matrix) + self.decoding_bias
        params_vector = np.tanh(params_vector)
        
        # Map to reasonable parameter ranges
        params = {
            'frequency': params_vector[0] * 5 + 5,  # [0, 10]
            'phase': params_vector[1] * np.pi,  # [-pi, pi]
            'turns': params_vector[2] * 5 + 5,  # [0, 10]
            'tightness': params_vector[3] * 2 + 1,  # [-1, 3]
            'freq1': params_vector[4] * 4 + 4,  # [0, 8]
            'freq2': params_vector[5] * 4 + 6,  # [2, 10]
            'center_x': params_vector[6] * 0.5,  # [-0.5, 0.5]
            'center_y': params_vector[7] * 0.5,  # [-0.5, 0.5]
            'octaves': int(np.clip(params_vector[8] * 3 + 4, 3, 6)),
            'scale': params_vector[9] * 0.15 + 0.1  # [0.05, 0.25]
        }
        
        return params
    
    def decode_to_pattern(self, latent: np.ndarray, pattern_type: str, 
                         generator: ArtDataGenerator) -> np.ndarray:
        """
        Decode latent vector directly to a visual pattern.
        
        Args:
            latent: Latent space vector
            pattern_type: Type of pattern to generate
            generator: ArtDataGenerator instance
        
        Returns:
            2D array representing the pattern
        """
        params = self.decode_to_parameters(latent)
        
        # Generate pattern based on type
        if 'sine' in pattern_type.lower():
            return generator.sine_wave(
                frequency=params['frequency'],
                phase=params['phase']
            )
        elif 'cosine' in pattern_type.lower():
            return generator.cosine_wave(
                frequency=params['frequency'],
                phase=params['phase']
            )
        elif 'spiral' in pattern_type.lower():
            return generator.spiral(
                turns=params['turns'],
                tightness=params['tightness']
            )
        elif 'interference' in pattern_type.lower():
            return generator.wave_interference(
                freq1=params['freq1'],
                freq2=params['freq2']
            )
        elif 'perlin' in pattern_type.lower():
            return generator.perlin_like_noise(
                octaves=params['octaves'],
                scale=params['scale']
            )
        elif 'radial' in pattern_type.lower():
            return generator.radial_gradient(
                center_x=params['center_x'],
                center_y=params['center_y']
            )
        else:
            return generator.random_noise()


class VariationalAutoEncoder:
    """
    VAE Concept: Complete encoder-decoder system with latent space sampling.
    Implements the VAE idea using mathematical transformations.
    """
    
    def __init__(self, latent_dim: int = 16):
        """
        Initialize the VAE.
        
        Args:
            latent_dim: Dimension of the latent space
        """
        self.latent_dim = latent_dim
        self.encoder = PatternEncoder(latent_dim)
        self.decoder = PatternDecoder(latent_dim)
    
    def encode(self, params: Dict[str, float]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Encode parameters to latent space (mean and log-variance for VAE concept).
        
        Args:
            params: Pattern parameters
        
        Returns:
            Tuple of (mean, log_variance) in latent space
        """
        latent = self.encoder.encode_parameters(params)
        
        # Split into mean and log-variance (VAE concept)
        mean = latent[:self.latent_dim // 2]
        log_var = latent[self.latent_dim // 2:]
        
        # Ensure log_var is in reasonable range
        log_var = np.clip(log_var, -5, 5)
        
        return mean, log_var
    
    def sample_latent(self, mean: np.ndarray, log_var: np.ndarray, 
                     seed: Optional[int] = None) -> np.ndarray:
        """
        Sample from latent space using reparameterization trick concept.
        
        Args:
            mean: Mean vector
            log_var: Log variance vector
            seed: Random seed
        
        Returns:
            Sampled latent vector
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Reparameterization trick: z = mean + std * epsilon
        std = np.exp(0.5 * log_var)
        epsilon = np.random.randn(len(mean))
        z = mean + std * epsilon
        
        # Combine with remaining dimensions if needed
        if len(z) < self.latent_dim:
            remaining = np.random.randn(self.latent_dim - len(z)) * 0.1
            z = np.concatenate([z, remaining])
        
        return z
    
    def decode(self, latent: np.ndarray, pattern_type: str = 'sine_wave',
               generator: Optional[ArtDataGenerator] = None) -> np.ndarray:
        """
        Decode latent vector to pattern.
        
        Args:
            latent: Latent space vector
            pattern_type: Type of pattern to generate
            generator: ArtDataGenerator instance
        
        Returns:
            Generated pattern
        """
        if generator is None:
            generator = ArtDataGenerator()
        
        return self.decoder.decode_to_pattern(latent, pattern_type, generator)
    
    def generate(self, pattern_type: str = 'sine_wave', 
                generator: Optional[ArtDataGenerator] = None,
                seed: Optional[int] = None) -> np.ndarray:
        """
        Generate a new pattern by sampling from latent space.
        
        Args:
            pattern_type: Type of pattern to generate
            generator: ArtDataGenerator instance
            seed: Random seed
        
        Returns:
            Generated pattern
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Sample from prior distribution (standard normal)
        latent = np.random.randn(self.latent_dim) * 0.5
        latent = np.tanh(latent)  # Normalize to [-1, 1]
        
        return self.decode(latent, pattern_type, generator)
    
    def reconstruct(self, params: Dict[str, float], pattern_type: str = 'sine_wave',
                   generator: Optional[ArtDataGenerator] = None,
                   seed: Optional[int] = None) -> np.ndarray:
        """
        Encode and reconstruct a pattern (full VAE cycle).
        
        Args:
            params: Original pattern parameters
            pattern_type: Type of pattern
            generator: ArtDataGenerator instance
            seed: Random seed
        
        Returns:
            Reconstructed pattern
        """
        mean, log_var = self.encode(params)
        latent = self.sample_latent(mean, log_var, seed)
        return self.decode(latent, pattern_type, generator)


class ArtGenerator:
    """
    GAN Generator Concept: Creates random art patterns.
    Generates diverse visual patterns using randomized parameters.
    """
    
    def __init__(self, width: int = 512, height: int = 512):
        """
        Initialize the generator.
        
        Args:
            width: Image width
            height: Image height
        """
        self.width = width
        self.height = height
        self.art_generator = ArtDataGenerator(width, height)
        self.pattern_types = [
            'sine_wave', 'cosine_wave', 'spiral', 'wave_interference',
            'random_noise', 'perlin_noise', 'radial_gradient'
        ]
    
    def generate_random_pattern(self, seed: Optional[int] = None) -> Tuple[np.ndarray, str, Dict]:
        """
        Generate a random art pattern with random parameters.
        
        Args:
            seed: Random seed
        
        Returns:
            Tuple of (pattern, pattern_type, parameters)
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Randomly select pattern type
        pattern_type = np.random.choice(self.pattern_types)
        
        # Generate random parameters
        params = self._generate_random_params(pattern_type)
        
        # Generate pattern
        pattern = self._generate_from_params(pattern_type, params)
        
        return pattern, pattern_type, params
    
    def _generate_random_params(self, pattern_type: str) -> Dict:
        """Generate random parameters for a pattern type."""
        if 'sine' in pattern_type or 'cosine' in pattern_type:
            return {
                'frequency': np.random.uniform(2, 8),
                'phase': np.random.uniform(0, 2 * np.pi)
            }
        elif 'spiral' in pattern_type:
            return {
                'turns': np.random.uniform(3, 8),
                'tightness': np.random.uniform(0.5, 2.0)
            }
        elif 'interference' in pattern_type:
            return {
                'freq1': np.random.uniform(2, 6),
                'freq2': np.random.uniform(4, 8)
            }
        elif 'perlin' in pattern_type:
            return {
                'octaves': np.random.randint(3, 6),
                'scale': np.random.uniform(0.05, 0.2)
            }
        elif 'radial' in pattern_type:
            return {
                'center_x': np.random.uniform(-0.5, 0.5),
                'center_y': np.random.uniform(-0.5, 0.5)
            }
        else:
            return {'seed': np.random.randint(0, 10000)}
    
    def _generate_from_params(self, pattern_type: str, params: Dict) -> np.ndarray:
        """Generate pattern from parameters."""
        if 'sine' in pattern_type:
            return self.art_generator.sine_wave(**params)
        elif 'cosine' in pattern_type:
            return self.art_generator.cosine_wave(**params)
        elif 'spiral' in pattern_type:
            return self.art_generator.spiral(**params)
        elif 'interference' in pattern_type:
            return self.art_generator.wave_interference(**params)
        elif 'perlin' in pattern_type:
            return self.art_generator.perlin_like_noise(**params)
        elif 'radial' in pattern_type:
            return self.art_generator.radial_gradient(**params)
        else:
            return self.art_generator.random_noise(seed=params.get('seed'))
    
    def generate_batch(self, n: int, seed: Optional[int] = None) -> List[Tuple[np.ndarray, str, Dict]]:
        """
        Generate a batch of random patterns.
        
        Args:
            n: Number of patterns to generate
            seed: Random seed
        
        Returns:
            List of (pattern, pattern_type, parameters) tuples
        """
        if seed is not None:
            np.random.seed(seed)
        
        return [self.generate_random_pattern() for _ in range(n)]


class PatternDiscriminator:
    """
    GAN Discriminator Concept: Filters visually pleasing outputs.
    Evaluates patterns based on mathematical properties that indicate visual quality.
    """
    
    def __init__(self):
        """Initialize the discriminator."""
        # Quality thresholds (learned from experience, in real GAN these are learned)
        self.min_contrast = 0.1
        self.max_contrast = 0.9
        self.min_entropy = 2.0  # Minimum information content
        self.max_entropy = 7.0  # Maximum information content
    
    def evaluate(self, pattern: np.ndarray) -> Tuple[float, Dict]:
        """
        Evaluate a pattern and return a quality score.
        
        Args:
            pattern: 2D pattern array
        
        Returns:
            Tuple of (score [0-1], evaluation details)
        """
        # Calculate various quality metrics
        contrast = self._calculate_contrast(pattern)
        entropy = self._calculate_entropy(pattern)
        smoothness = self._calculate_smoothness(pattern)
        symmetry = self._calculate_symmetry(pattern)
        
        # Combine metrics into a score
        score = 0.0
        
        # Contrast score (prefer medium to high contrast)
        if self.min_contrast <= contrast <= self.max_contrast:
            score += 0.3
        elif contrast > 0.05:
            score += 0.15
        
        # Entropy score (prefer medium entropy - not too uniform, not too random)
        if self.min_entropy <= entropy <= self.max_entropy:
            score += 0.3
        elif entropy > 1.0:
            score += 0.15
        
        # Smoothness score (prefer some smoothness but not too much)
        if 0.3 <= smoothness <= 0.7:
            score += 0.2
        elif 0.1 <= smoothness <= 0.9:
            score += 0.1
        
        # Symmetry score (bonus for symmetry)
        if symmetry > 0.6:
            score += 0.2
        elif symmetry > 0.4:
            score += 0.1
        
        # Normalize score
        score = min(score, 1.0)
        
        details = {
            'contrast': contrast,
            'entropy': entropy,
            'smoothness': smoothness,
            'symmetry': symmetry,
            'score': score
        }
        
        return score, details
    
    def _calculate_contrast(self, pattern: np.ndarray) -> float:
        """Calculate contrast (standard deviation)."""
        return float(np.std(pattern))
    
    def _calculate_entropy(self, pattern: np.ndarray, bins: int = 256) -> float:
        """Calculate information entropy."""
        hist, _ = np.histogram(pattern.flatten(), bins=bins, range=(0, 1))
        hist = hist[hist > 0]  # Remove zeros
        prob = hist / hist.sum()
        entropy = -np.sum(prob * np.log2(prob))
        return float(entropy)
    
    def _calculate_smoothness(self, pattern: np.ndarray) -> float:
        """Calculate smoothness (inverse of gradient magnitude)."""
        grad_y, grad_x = np.gradient(pattern)
        gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        smoothness = 1.0 / (1.0 + np.mean(gradient_magnitude))
        return float(smoothness)
    
    def _calculate_symmetry(self, pattern: np.ndarray) -> float:
        """Calculate symmetry score (horizontal and vertical)."""
        h, w = pattern.shape
        
        # Horizontal symmetry
        top_half = pattern[:h//2, :]
        bottom_half = np.flipud(pattern[h//2:, :])
        h_symmetry = 1.0 - np.mean(np.abs(top_half - bottom_half[:top_half.shape[0], :]))
        
        # Vertical symmetry
        left_half = pattern[:, :w//2]
        right_half = np.fliplr(pattern[:, w//2:])
        v_symmetry = 1.0 - np.mean(np.abs(left_half - right_half[:, :left_half.shape[1]]))
        
        return float((h_symmetry + v_symmetry) / 2.0)
    
    def filter(self, patterns: List[np.ndarray], threshold: float = 0.5) -> List[Tuple[np.ndarray, float]]:
        """
        Filter patterns based on quality score.
        
        Args:
            patterns: List of patterns to filter
            threshold: Minimum score to keep
        
        Returns:
            List of (pattern, score) tuples that pass the threshold
        """
        filtered = []
        for pattern in patterns:
            score, _ = self.evaluate(pattern)
            if score >= threshold:
                filtered.append((pattern, score))
        return filtered
    
    def is_real(self, pattern: np.ndarray, threshold: float = 0.5) -> bool:
        """
        Determine if a pattern is "real" (visually pleasing) or "fake".
        
        Args:
            pattern: Pattern to evaluate
            threshold: Quality threshold
        
        Returns:
            True if pattern passes quality check
        """
        score, _ = self.evaluate(pattern)
        return score >= threshold


class GenerativeAdversarialNetwork:
    """
    GAN Concept: Complete generator-discriminator system.
    Generator creates patterns, discriminator filters them.
    """
    
    def __init__(self, width: int = 512, height: int = 512):
        """
        Initialize the GAN.
        
        Args:
            width: Image width
            height: Image height
        """
        self.generator = ArtGenerator(width, height)
        self.discriminator = PatternDiscriminator()
    
    def generate_art(self, n: int = 10, quality_threshold: float = 0.5,
                    seed: Optional[int] = None) -> List[Tuple[np.ndarray, str, Dict, float]]:
        """
        Generate art patterns and filter by quality.
        
        Args:
            n: Number of patterns to generate
            quality_threshold: Minimum quality score
            seed: Random seed
        
        Returns:
            List of (pattern, pattern_type, parameters, score) tuples
        """
        # Generate patterns
        patterns = self.generator.generate_batch(n, seed)
        
        # Filter by quality
        results = []
        for pattern, pattern_type, params in patterns:
            score, details = self.discriminator.evaluate(pattern)
            if score >= quality_threshold:
                results.append((pattern, pattern_type, params, score))
        
        # Sort by score (best first)
        results.sort(key=lambda x: x[3], reverse=True)
        
        return results
    
    def generate_best(self, n_candidates: int = 50, n_best: int = 10,
                     seed: Optional[int] = None) -> List[Tuple[np.ndarray, str, Dict, float]]:
        """
        Generate many candidates and return the best ones.
        
        Args:
            n_candidates: Number of candidates to generate
            n_best: Number of best patterns to return
            seed: Random seed
        
        Returns:
            List of best (pattern, pattern_type, parameters, score) tuples
        """
        all_results = self.generate_art(n_candidates, quality_threshold=0.0, seed=seed)
        return all_results[:n_best]

