# Read Hydra script
with open('c:/Users/cuban/HydraToTD/html/hydra-synth.js', 'r', encoding='utf-8') as f:
    hydra_script = f.read()

# Read template
with open('c:/Users/cuban/HydraToTD/html/hydra_final.html', 'r', encoding='utf-8') as f:
    template = f.read()

# Insert Hydra script
html = template.replace('HYDRA_SCRIPT_PLACEHOLDER', hydra_script)

# Write final version
with open('c:/Users/cuban/HydraToTD/html/hydra_clean.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Created clean HTML: {len(html)} bytes")
print("No test patterns - ready for CodeManager control")
