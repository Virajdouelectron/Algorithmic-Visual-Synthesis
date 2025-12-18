# Step 6: Deployment & Sharing

## Overview

This guide covers multiple deployment options for the Algorithmic Visual Synthesis web gallery. Choose the method that best fits your needs.

## Quick Deploy Options

### 1. GitHub Pages (Free, Easy)

**Best for**: Open source projects, free hosting

#### Steps:

1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/algorithmic-visual-synthesis.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` / `root`
   - Click Save

3. **Your site will be live at:**
   ```
   https://yourusername.github.io/algorithmic-visual-synthesis/
   ```

#### GitHub Pages Configuration

Create `.nojekyll` file in root (if needed):
```bash
echo "" > .nojekyll
```

### 2. Netlify (Free, Easy, CDN)

**Best for**: Fast deployment, automatic HTTPS, custom domains

#### Steps:

1. **Install Netlify CLI** (optional):
   ```bash
   npm install -g netlify-cli
   ```

2. **Deploy via Netlify Dashboard**:
   - Go to [netlify.com](https://netlify.com)
   - Sign up/login
   - Click "Add new site" → "Import an existing project"
   - Connect to GitHub (or drag & drop folder)
   - Build command: (leave empty)
   - Publish directory: `/` (root)
   - Click "Deploy site"

3. **Deploy via CLI**:
   ```bash
   netlify deploy --prod
   ```

4. **Your site will be live at:**
   ```
   https://your-site-name.netlify.app
   ```

#### Netlify Configuration

The `netlify.toml` file is already created (see below).

### 3. Vercel (Free, Fast, Great DX)

**Best for**: Modern web apps, excellent developer experience

#### Steps:

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Or use Vercel Dashboard**:
   - Go to [vercel.com](https://vercel.com)
   - Sign up/login
   - Click "Add New Project"
   - Import from GitHub
   - Deploy

4. **Your site will be live at:**
   ```
   https://your-project.vercel.app
   ```

#### Vercel Configuration

The `vercel.json` file is already created (see below).

### 4. Surge.sh (Free, Simple)

**Best for**: Quick static site deployment

#### Steps:

1. **Install Surge**:
   ```bash
   npm install -g surge
   ```

2. **Deploy**:
   ```bash
   surge
   # Follow prompts to create account and deploy
   ```

3. **Your site will be live at:**
   ```
   https://your-site-name.surge.sh
   ```

### 5. Local Server (Development/Testing)

**For testing before deployment:**

```bash
# Python 3
python -m http.server 8000

# Node.js (if installed)
npx serve

# PHP (if installed)
php -S localhost:8000
```

Then visit: `http://localhost:8000/gallery.html`

## File Structure for Deployment

```
algorithmic-visual-synthesis/
├── gallery.html          # Main gallery page
├── gallery.css           # Styles
├── gallery.js            # JavaScript
├── README.md             # Documentation
├── .nojekyll            # GitHub Pages (if needed)
├── netlify.toml          # Netlify config
├── vercel.json           # Vercel config
└── CNAME                 # Custom domain (optional)
```

## Custom Domain Setup

### GitHub Pages

1. Add `CNAME` file with your domain:
   ```
   yourdomain.com
   ```

2. Configure DNS:
   - Add CNAME record: `yourdomain.com` → `yourusername.github.io`

### Netlify

1. Go to Site settings → Domain management
2. Add custom domain
3. Follow DNS configuration instructions

### Vercel

1. Go to Project settings → Domains
2. Add your domain
3. Configure DNS as instructed

## Deployment Checklist

- [ ] Test gallery locally
- [ ] Verify all files are included
- [ ] Check browser compatibility
- [ ] Test on mobile devices
- [ ] Verify HTTPS is enabled
- [ ] Test download functionality
- [ ] Check localStorage works
- [ ] Verify all patterns generate correctly
- [ ] Test all colormaps
- [ ] Check responsive design

## Continuous Deployment

### GitHub Pages (Automatic)

- Push to `main` branch → Auto-deploys
- No configuration needed

### Netlify (Automatic)

- Push to connected Git repo → Auto-deploys
- Configure in Netlify dashboard

### Vercel (Automatic)

- Push to connected Git repo → Auto-deploys
- Configure in Vercel dashboard

## Sharing Your Gallery

### Social Media

Share your deployed gallery URL:
```
🎨 Check out my Algorithmic Visual Synthesis Gallery!
[Your URL]
```

### Embed in Website

```html
<iframe 
  src="https://your-gallery-url.com/gallery.html" 
  width="100%" 
  height="800px" 
  frameborder="0">
</iframe>
```

### QR Code

Generate QR code for your gallery URL to share easily.

## Performance Optimization

### Before Deployment

1. **Minify CSS/JS** (optional):
   ```bash
   # Using online tools or build tools
   # Minify gallery.css and gallery.js
   ```

2. **Optimize Images** (if using exported images):
   - Compress PNG files
   - Use WebP format if possible

3. **Enable Compression**:
   - Most hosting platforms enable gzip automatically
   - Check in hosting settings

## Troubleshooting

### Gallery Not Loading

- Check browser console for errors
- Verify all files are uploaded
- Check file paths are correct
- Ensure HTTPS is enabled

### CORS Issues

- Most static hosts handle CORS automatically
- If issues occur, check hosting platform settings

### localStorage Not Working

- Ensure site is served over HTTP/HTTPS (not file://)
- Check browser allows localStorage
- Clear browser cache

## Security Considerations

- ✅ Static site (no server-side code)
- ✅ No sensitive data stored
- ✅ Client-side only generation
- ✅ HTTPS recommended (auto-enabled on most platforms)

## Analytics (Optional)

### Google Analytics

Add to `gallery.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Plausible Analytics

Add to `gallery.html` before `</head>`:

```html
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

## Support

For issues or questions:
- Check hosting platform documentation
- Review browser console for errors
- Test in different browsers
- Verify all files are present

## Next Steps

After deployment:
1. Share your gallery URL
2. Collect feedback
3. Iterate and improve
4. Add new features
5. Expand pattern library

