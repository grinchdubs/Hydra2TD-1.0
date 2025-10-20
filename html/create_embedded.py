import base64

# Read the Hydra script
with open('c:/Users/cuban/HydraToTD/html/hydra-synth.js', 'rb') as f:
    hydra_content = f.read()

# Read the template
template = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Hydra in TouchDesigner (Embedded)</title>
    <style>
        body { margin: 0; padding: 0; background: black; overflow: hidden; }
        canvas { display: block; width: 100vw !important; height: 100vh !important; }
        #debug { position: absolute; top: 10px; left: 10px; color: lime; font-family: monospace; 
                 font-size: 12px; background: rgba(0,0,0,0.8); padding: 10px; z-index: 1000; }
    </style>
</head>
<body>
    <div id="debug">Loading Hydra (embedded)...</div>
    <script>HYDRA_CODE_HERE</script>
    <script>
        console.log("Hydra embedded script started");
        
        function log(msg) {
            console.log(msg);
            const debug = document.getElementById('debug');
            if (debug) debug.innerHTML += '<br>' + msg;
        }

        setTimeout(function() {
            try {
                log("Checking Hydra...");
                if (typeof Hydra === 'undefined') {
                    log("ERROR: Hydra not defined!");
                } else {
                    log("✓ Hydra loaded (embedded)!");
                    
                    const hydra = new Hydra({ detectAudio: false, makeGlobal: true });
                    log("✓ Hydra initialized!");
                    
                    window.tdData = { chops: {}, timestamp: Date.now(), updateCount: 0 };
                    window.tdPerformance = { fps: 60, frameTime: 0, lastUpdate: Date.now(), chopUpdateRate: 0 };
                    
                    let frameCount = 0, lastTime = Date.now(), lastChopUpdate = Date.now();
                    
                    function updatePerformance() {
                        frameCount++;
                        const now = Date.now(), elapsed = now - lastTime;
                        if (elapsed >= 1000) {
                            window.tdPerformance.fps = (frameCount / elapsed) * 1000;
                            window.tdPerformance.frameTime = elapsed / frameCount;
                            frameCount = 0; lastTime = now;
                        }
                        requestAnimationFrame(updatePerformance);
                    }
                    updatePerformance();
                    
                    window.updateFromTD = function(jsonData) {
                        try {
                            const data = JSON.parse(jsonData);
                            window.tdData.chops = data;
                            window.tdData.timestamp = Date.now();
                            window.tdData.updateCount++;
                            const now = Date.now(), chopElapsed = now - lastChopUpdate;
                            if (chopElapsed > 0) window.tdPerformance.chopUpdateRate = 1000 / chopElapsed;
                            lastChopUpdate = now;
                        } catch(e) { console.error('Parse error:', e); }
                    };
                    
                    window.chop = function(name, index) {
                        return function() {
                            return (window.tdData.chops[name] && window.tdData.chops[name][index] !== undefined) 
                                ? window.tdData.chops[name][index] : 0;
                        };
                    };
                    
                    window.lfo = function(index) { return chop('lfo' + index, 0); };
                    window.midi = function(cc) { return chop('midi', cc); };
                    window.audioFFT = function(index) { return chop('audio_spectrum', index); };
                    
                    window.runHydraCode = function(code) {
                        try { eval(code); log("Code executed"); } 
                        catch(e) { console.error('Hydra error:', e); log("ERROR: " + e.message); }
                    };
                    
                    window.setOutput = function(index) {
                        try { render(eval('o' + index)); } 
                        catch(e) { console.error('Output error:', e); }
                    };
                    
                    window.getPerformance = function() { return JSON.stringify(window.tdPerformance); };
                    
                    window.registerVideoStream = function(url) {
                        try { s0.initStream(url); log('Video stream: ' + url); } 
                        catch(e) { console.error('Stream error:', e); }
                    };
                    
                    window.initWebcam = function() {
                        try { s0.initCam(); log('Webcam initialized'); } 
                        catch(e) { console.error('Webcam error:', e); }
                    };
                    
                    window.clearAll = function() {
                        solid(0).out(o0); solid(0).out(o1); solid(0).out(o2); solid(0).out(o3);
                    };
                    
                    log("✓ Helper functions created");
                    log("Running test: RED then oscillator...");
                    
                    solid(1, 0, 0).out();
                    setTimeout(() => { osc(10, 0.1, 1.4).out(); log("✓ READY!"); }, 1000);
                    setTimeout(() => { const d = document.getElementById('debug'); if(d) d.style.display = 'none'; }, 5000);
                }
            } catch(error) {
                log("FATAL: " + error.message);
                console.error("Fatal error:", error);
            }
        }, 100);
    </script>
</body>
</html>'''

# Replace placeholder with actual Hydra code
html = template.replace('HYDRA_CODE_HERE', hydra_content.decode('utf-8'))

# Write output
with open('c:/Users/cuban/HydraToTD/html/hydra_embedded.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Created embedded HTML file: {len(html)} bytes")
