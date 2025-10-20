# Download Hydra Locally

If CDN access is blocked or unreliable, download Hydra to use locally.

## Method 1: Direct Download

1. Go to: https://cdn.jsdelivr.net/npm/hydra-synth@1.3.20/dist/hydra-synth.js
2. Save the file to: `C:\Users\cuban\HydraToTD\html\hydra-synth.js`
3. Update your HTML to use local file:

```html
<script src="file:///C:/Users/cuban/HydraToTD/html/hydra-synth.js"></script>
```

## Method 2: Using curl/wget

In a terminal:

```bash
cd C:\Users\cuban\HydraToTD\html
curl -o hydra-synth.js https://cdn.jsdelivr.net/npm/hydra-synth@1.3.20/dist/hydra-synth.js
```

## Update HTML Template

Change the script tag in your HTML from:
```html
<script src="https://cdn.jsdelivr.net/npm/hydra-synth@1.3.20/dist/hydra-synth.js"></script>
```

To:
```html
<script src="file:///C:/Users/cuban/HydraToTD/html/hydra-synth.js"></script>
```

Or use relative path if Web Render TOP supports it:
```html
<script src="./hydra-synth.js"></script>
```
