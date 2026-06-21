/**
 * Project SparseMind - Dashboard Logic (Neurosparse v1)
 * Clean, minimal theme-switching, local metrics simulator, 
 * and database integration placeholders.
 */

// --- 1. Loader, Cursor Glow & Particles Setup ---

// Cinematic Loader Transition
window.addEventListener('load', () => {
    setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.classList.add('done');
        }
    }, 1500);
});

// Subtle Cursor Glow Tracking
const glow = document.getElementById('cursorGlow');
if (glow) {
    document.addEventListener('mousemove', e => {
        glow.style.transform = `translate(${e.clientX - 200}px, ${e.clientY - 200}px)`;
    });
}

// Minimal Floating Particles
(function() {
    const canvas = document.getElementById('particles');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let w, h;
    let pts = [];

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Faint, slow particles to prevent visual clutter
    for (let i = 0; i < 40; i++) {
        pts.push({
            x: Math.random() * w,
            y: Math.random() * h,
            r: Math.random() * 1.5 + 0.3,
            dx: (Math.random() - 0.5) * 0.15,
            dy: (Math.random() - 0.5) * 0.15,
            o: Math.random() * 0.2 + 0.05
        });
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);
        pts.forEach(p => {
            p.x += p.dx;
            p.y += p.dy;
            
            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            if (p.y < 0) p.y = h;
            if (p.y > h) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            // Draw using theme-adaptive color property or fallback matcha green
            const matchaColor = getComputedStyle(document.body).getPropertyValue('--matcha').trim() || '#6b9a5b';
            ctx.fillStyle = matchaColor;
            ctx.globalAlpha = p.o;
            ctx.fill();
            ctx.globalAlpha = 1.0;
        });
        requestAnimationFrame(draw);
    }
    draw();
})();


// --- 2. Theme Switching Logic ---
const themeToggleBtn = document.getElementById('themeToggleBtn');
const themeIcon = document.getElementById('themeIcon');

function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
        if (themeIcon) themeIcon.textContent = 'light_mode';
    } else {
        document.body.classList.remove('light-theme');
        if (themeIcon) themeIcon.textContent = 'dark_mode';
    }
}

if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-theme');
        const isLight = document.body.classList.contains('light-theme');
        
        if (themeIcon) {
            themeIcon.textContent = isLight ? 'light_mode' : 'dark_mode';
        }
        localStorage.setItem('theme', isLight ? 'light' : 'dark');
        
        // Redraw canvas with the correct theme color
        drawLossSparkline();
    });
}


// --- 3. Dynamic Training Metric Variables ---
let currentEpoch = 0;
let currentLoss = 1.8540;
let currentSparsity = 0.0;

const targetEpochs = 100;
const targetLoss = 0.0450;
const targetSparsity = 82.5;

let isSimulating = true;
let simIntervalId = null;
const lossHistory = [];
const maxLossHistoryPoints = 15;

// DOM Elements
const epochValEl = document.getElementById('val-epoch');
const lossValEl = document.getElementById('val-loss');
const sparsityValEl = document.getElementById('val-sparsity');

const epochBarEl = document.getElementById('bar-epoch');
const sparsityBarEl = document.getElementById('bar-sparsity');

const btnToggleSim = document.getElementById('btn-toggle-sim');
const btnResetSim = document.getElementById('btn-reset-sim');
const consoleLogsEl = document.getElementById('console-logs');

// Canvas for Loss Sparkline
const lossCanvas = document.getElementById('loss-canvas');
const ctx = lossCanvas ? lossCanvas.getContext('2d') : null;


// --- 4. Live Cloud Sync Template (Firebase / Supabase) ---
/**
 * TO INTEGRATE A CLOUD DATABASE (E.G., SUPABASE OR FIREBASE):
 * 
 * 1. Include the SDK inside index.html (or install via npm):
 *    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
 * 
 * 2. Set up the client and subscribe to real-time changes:
 * 
 *    const supabaseUrl = 'YOUR_SUPABASE_PROJECT_URL';
 *    const supabaseKey = 'YOUR_SUPABASE_ANON_KEY';
 *    const supabase = window.supabase.createClient(supabaseUrl, supabaseKey);
 * 
 * 3. Subscribe to your training logs table:
 * 
 *    function connectCloudDatabase() {
 *        logToConsole("[SYSTEM] Subscribing to Supabase Realtime channel...");
 *        
 *        // Disable local simulation since we are using cloud data
 *        stopSimulation();
 *        btnToggleSim.disabled = true;
 *        btnToggleSim.textContent = "CLOUD FEED ACTIVE";
 *        
 *        const dbIndicator = document.getElementById('db-indicator');
 *        const dbStatusText = document.getElementById('db-status-text');
 *        
 *        dbIndicator.classList.remove('offline');
 *        dbIndicator.classList.add('online');
 *        dbStatusText.textContent = "Supabase Realtime Synced";
 * 
 *        supabase
 *          .channel('training-stats')
 *          .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'metrics' }, payload => {
 *              const data = payload.new;
 *              
 *              // Update local values with real data from db
 *              updateMetrics(data.epoch, data.loss, data.sparsity);
 *              logToConsole(`[CLOUD] Received step: Epoch ${data.epoch} | Loss: ${data.loss.toFixed(4)}`);
 *          })
 *          .subscribe();
 *    }
 * 
 * 4. Simply call connectCloudDatabase() on window load if you want cloud updates to take over.
 */


// --- 5. DOM Update Functions ---
function updateMetrics(epoch, loss, sparsity) {
    currentEpoch = epoch;
    currentLoss = loss;
    currentSparsity = sparsity;

    if (epochValEl) epochValEl.textContent = currentEpoch;
    if (lossValEl) lossValEl.textContent = currentLoss.toFixed(4);
    if (sparsityValEl) sparsityValEl.textContent = currentSparsity.toFixed(1) + '%';

    const epochPercent = Math.min((currentEpoch / targetEpochs) * 100, 100);
    if (epochBarEl) epochBarEl.style.width = `${epochPercent}%`;

    const sparsityPercent = Math.min((currentSparsity / targetSparsity) * 100, 100);
    if (sparsityBarEl) sparsityBarEl.style.width = `${sparsityPercent}%`;

    lossHistory.push(currentLoss);
    if (lossHistory.length > maxLossHistoryPoints) {
        lossHistory.shift();
    }
    drawLossSparkline();
}

function logToConsole(message) {
    if (!consoleLogsEl) return;
    const logLine = document.createElement('div');
    logLine.classList.add('log-line');
    
    if (message.includes('[SYSTEM]')) {
        logLine.classList.add('system');
    } else if (message.includes('[SIM]')) {
        logLine.classList.add('simulation');
    } else {
        logLine.classList.add('update');
    }
    
    const now = new Date();
    const timeStr = now.toTimeString().split(' ')[0] + '.' + String(now.getMilliseconds()).padStart(3, '0');
    logLine.textContent = `[${timeStr}] ${message}`;
    
    consoleLogsEl.appendChild(logLine);
    consoleLogsEl.scrollTop = consoleLogsEl.scrollHeight;
}

function drawLossSparkline() {
    if (!ctx || !lossCanvas) return;
    ctx.clearRect(0, 0, lossCanvas.width, lossCanvas.height);
    if (lossHistory.length < 2) return;

    ctx.beginPath();
    
    // Resolve the active theme-specific highlight gold color
    const goldColor = getComputedStyle(document.body).getPropertyValue('--highlight-gold').trim() || '#dfb13c';
    ctx.strokeStyle = goldColor;
    ctx.lineWidth = 1.5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    const padding = 2;
    const chartWidth = lossCanvas.width - (padding * 2);
    const chartHeight = lossCanvas.height - (padding * 2);

    const minLoss = 0.0;
    const maxLoss = Math.max(2.0, ...lossHistory);

    for (let i = 0; i < lossHistory.length; i++) {
        const x = padding + (i / (lossHistory.length - 1)) * chartWidth;
        const y = padding + chartHeight - ((lossHistory[i] - minLoss) / (maxLoss - minLoss)) * chartHeight;
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.stroke();
}


// --- 6. Simulation Engine Loop ---
function runSimulationStep() {
    if (currentEpoch >= targetEpochs) {
        logToConsole('[SIM] Training cycle complete! Model converged.');
        stopSimulation();
        return;
    }

    const nextEpoch = currentEpoch + 1;
    const lossDecrease = (currentLoss - targetLoss) * (0.05 + Math.random() * 0.05);
    const nextLoss = Math.max(targetLoss, currentLoss - lossDecrease + (Math.random() - 0.5) * 0.01);
    const sparsityStep = (targetSparsity / targetEpochs) * (0.8 + Math.random() * 0.4);
    const nextSparsity = Math.min(targetSparsity, currentSparsity + sparsityStep);

    updateMetrics(nextEpoch, nextLoss, nextSparsity);
    
    if (nextEpoch % 5 === 0 || nextEpoch === 1) {
        logToConsole(`[SIM] Checkpoint saved. Epoch: ${nextEpoch} | Loss: ${nextLoss.toFixed(4)} | Sparsity: ${nextSparsity.toFixed(1)}%`);
    }
}

function startSimulation() {
    isSimulating = true;
    if (btnToggleSim) {
        btnToggleSim.textContent = "PAUSE SIMULATION";
        btnToggleSim.classList.remove('btn-outline');
        btnToggleSim.classList.add('btn-fill');
    }
    logToConsole('[SIM] Simulation training loop started.');
    simIntervalId = setInterval(runSimulationStep, 1500);
}

function stopSimulation() {
    isSimulating = false;
    if (btnToggleSim) {
        btnToggleSim.textContent = "RESUME SIMULATION";
        btnToggleSim.classList.remove('btn-fill');
        btnToggleSim.classList.add('btn-outline');
    }
    logToConsole('[SIM] Simulation paused.');
    if (simIntervalId) {
        clearInterval(simIntervalId);
    }
}

function resetSimulation() {
    stopSimulation();
    lossHistory.length = 0;
    updateMetrics(0, 1.8540, 0.0);
    logToConsole('[SYSTEM] Metric simulation reset.');
    startSimulation();
}


// --- 7. Event Listeners ---
if (btnToggleSim) {
    btnToggleSim.addEventListener('click', () => {
        if (isSimulating) {
            stopSimulation();
        } else {
            startSimulation();
        }
    });
}

if (btnResetSim) {
    btnResetSim.addEventListener('click', () => {
        resetSimulation();
    });
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    updateMetrics(0, 1.8540, 0.0);
    startSimulation();
});
