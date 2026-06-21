#!/usr/bin/env python3
"""
Project SparseMind Automation & Deployment Script
------------------------------------------------
This Python script is designed to run in Kaggle Notebooks or Google Colab.
It does the following:
1. Securely fetches your GitHub Personal Access Token (PAT) from Kaggle Secrets.
2. Clones the 'Neurollm' repository.
3. Automatically writes the minimalist, theme-swapping Dashboard files (index.html, style.css, script.js).
4. Commits and pushes the new files back to GitHub.

Author: Phoenix Tech Dev Team
Model: Neurosparse v1
"""

import os
import shutil
import subprocess
import sys

# ==========================================
# 1. CONFIGURATION (Customize as needed)
# ==========================================
REPO_OWNER = "phoenixdevellopment75-web"
REPO_NAME = "Neurollm"
BRANCH = "main"

# Git Commit Author Information
GIT_USER_NAME = "SparseMind Autopilot"
GIT_USER_EMAIL = "autopilot@sparsemind.ai"

# ==========================================
# 2. RETRIEVE SECURE CREDENTIALS
# ==========================================
print("=== [1/5] AUTHENTICATING SECURE TOKENS ===")
github_token = None

# A. Try Kaggle Secrets (UserSecretsClient)
try:
    from kaggle_secrets import UserSecretsClient
    user_secrets = UserSecretsClient()
    github_token = user_secrets.get_secret("GITHUB_TOKEN")
    if github_token:
        print("✔ Successfully retrieved GITHUB_TOKEN from Kaggle Secrets!")
except Exception as e:
    print(f"ℹ Kaggle secrets client not available or GITHUB_TOKEN not configured ({e}).")

# B. Try Colab Userdata Fallback
if not github_token:
    try:
        from google.colab import userdata
        github_token = userdata.get("GITHUB_TOKEN")
        if github_token:
            print("✔ Successfully retrieved GITHUB_TOKEN from Google Colab Secrets!")
    except Exception as e:
        print(f"ℹ Google Colab secrets not available.")

# C. Try Local Environment Variable Fallback
if not github_token:
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        print("✔ Successfully retrieved GITHUB_TOKEN from environment variables.")

# Validation Check
if not github_token:
    print("\n❌ ERROR: GITHUB_TOKEN NOT FOUND!")
    print("---------------------------------------------------------------------------")
    print("If you are running in Kaggle:")
    print("  Go to: Add-ons -> Secrets -> Add a new secret with name 'GITHUB_TOKEN'")
    print("  Set the value to your GitHub Personal Access Token (PAT) with repo permissions.")
    print("  Make sure to toggle the 'Share with Notebook' option on.")
    print("---------------------------------------------------------------------------")
    print("If you are running in Google Colab:")
    print("  Click the Key Icon (Secrets) in the left sidebar, add 'GITHUB_TOKEN'")
    print("  Paste your token, and grant notebook access.")
    print("---------------------------------------------------------------------------")
    sys.exit(1)

# ==========================================
# 3. WEBSITE CODE STRINGS
# ==========================================

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project SparseMind | Neurosparse v1 Dashboard</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&display=swap" />
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="cursor-glow" id="cursorGlow"></div>

    <div class="mesh-bg">
        <div class="mesh-blob b1"></div>
        <div class="mesh-blob b2"></div>
        <div class="mesh-blob b3"></div>
    </div>

    <canvas id="particles"></canvas>

    <div class="loader" id="loader">
        <div class="loader-text">
            <span style="--i:0">S</span><span style="--i:1">p</span><span style="--i:2">a</span><span style="--i:3">r</span><span style="--i:4">s</span><span style="--i:5">e</span><span style="--i:6">M</span><span style="--i:7">i</span><span style="--i:8">n</span><span style="--i:9">d</span>
        </div>
        <div class="loader-sub">Neurosparse v1 Core Interface</div>
        <div class="loader-bar"></div>
    </div>

    <main class="dashboard-container">
        <header class="dashboard-header">
            <div class="header-title-container">
                <div class="logo-accent"></div>
                <h1 class="header-title">PROJECT SPARSEMIND</h1>
                <span class="model-tag">Neurosparse v1</span>
            </div>
            
            <div class="header-controls">
                <div class="status-indicator">
                    <span class="status-dot"></span>
                    <span class="status-text">Status: <span class="status-active">Active / Training</span></span>
                </div>
                
                <button id="themeToggleBtn" class="theme-toggle-btn" aria-label="Toggle light/dark theme">
                    <span class="material-symbols-rounded" id="themeIcon">dark_mode</span>
                </button>
            </div>
        </header>

        <div class="dashboard-content">
            <section class="main-panel">
                <div class="card mission-card">
                    <div class="card-header">
                        <span class="card-num">01 —</span>
                        <h2>Mission Objective</h2>
                    </div>
                    <p class="mission-text">
                        Building a high-efficiency sparse Large Language Model (1M-5M parameters) optimized for commodity hardware, specifically targetting T4 GPU acceleration via dynamic activation sparsity and weight pruning.
                    </p>
                    <div class="tech-specs">
                        <span class="spec-tag">Target: T4 GPU</span>
                        <span class="spec-tag">Params: 1M - 5M</span>
                        <span class="spec-tag">Arch: MoE-Sparse</span>
                    </div>
                </div>

                <div class="card monitor-card">
                    <div class="card-header">
                        <span class="card-num">02 —</span>
                        <h2>Live Checkpoint Monitoring</h2>
                        <span class="live-badge">Live Feed</span>
                    </div>
                    
                    <div class="metrics-grid">
                        <div class="metric-box">
                            <span class="metric-label">CURRENT EPOCH</span>
                            <div class="metric-value" id="val-epoch">0</div>
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill" id="bar-epoch" style="width: 0%"></div>
                            </div>
                            <span class="metric-subtext">Target: 100 Epochs</span>
                        </div>

                        <div class="metric-box">
                            <span class="metric-label">TRAINING LOSS</span>
                            <div class="metric-value highlight-gold" id="val-loss">0.0000</div>
                            <div class="sparkline-container">
                                <canvas id="loss-canvas" width="160" height="30"></canvas>
                            </div>
                            <span class="metric-subtext">Target: &lt; 0.0500</span>
                        </div>

                        <div class="metric-box">
                            <span class="metric-label">SPARSITY RATIO</span>
                            <div class="metric-value highlight-matcha" id="val-sparsity">0.0%</div>
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill green-fill" id="bar-sparsity" style="width: 0%"></div>
                            </div>
                            <span class="metric-subtext">Target: &gt; 75.0%</span>
                        </div>
                    </div>

                    <div class="simulator-controls">
                        <span class="control-description">Simulate model training loop locally:</span>
                        <div class="btn-group">
                            <button id="btn-toggle-sim" class="btn btn-fill">PAUSE SIMULATION</button>
                            <button id="btn-reset-sim" class="btn btn-outline">RESET</button>
                        </div>
                    </div>
                </div>

                <div class="card logs-card">
                    <div class="card-header">
                        <span class="card-num">03 —</span>
                        <h2>System logs</h2>
                    </div>
                    <div class="console-body" id="console-logs">
                        <div class="log-line system">[SYSTEM] Dashboard loaded successfully. Initializing Neurosparse v1...</div>
                        <div class="log-line system">[SYSTEM] Connecting to local training socket...</div>
                        <div class="log-line simulation">[SIM] Running in demo mode. Toggle above to control simulation.</div>
                    </div>
                </div>
            </section>

            <section class="side-panel">
                <div class="capsule-card">
                    <div class="horizontal-stripes">
                        <div class="stripe stripe-1"></div>
                        <div class="stripe stripe-2"></div>
                        <div class="stripe stripe-3"></div>
                    </div>
                    
                    <div class="capsule-inner">
                        <div class="capsule-content">
                            <h3>Hardware stats</h3>
                            
                            <div class="stat-group">
                                <div class="stat-row">
                                    <span class="stat-label">GPU TEMP</span>
                                    <span class="stat-val">68°C</span>
                                </div>
                                <div class="bar-micro"><div class="bar-micro-fill" style="width: 68%"></div></div>
                            </div>

                            <div class="stat-group">
                                <div class="stat-row">
                                    <span class="stat-label">VRAM UTIL</span>
                                    <span class="stat-val">11.2 GB / 16 GB</span>
                                </div>
                                <div class="bar-micro"><div class="bar-micro-fill" style="width: 70%"></div></div>
                            </div>

                            <div class="stat-group">
                                <div class="stat-row">
                                    <span class="stat-label">T4 CORE SPEED</span>
                                    <span class="stat-val">1590 MHz</span>
                                </div>
                                <div class="bar-micro"><div class="bar-micro-fill" style="width: 85%"></div></div>
                            </div>

                            <div class="divider-dashed"></div>

                            <h3>Cloud sync</h3>
                            <div class="db-status-container">
                                <div class="db-dot offline" id="db-indicator"></div>
                                <span class="db-text" id="db-status-text">Local Simulated Feed</span>
                            </div>
                            <p class="db-desc">
                                Connect your cloud database (Supabase/Firebase) using the configuration in <span class="code-highlight">script.js</span>.
                            </p>
                        </div>
                    </div>
                </div>
            </section>
        </div>

        <footer class="dashboard-footer">
            <span class="footer-left">PHOENIX TECH &copy; 2026</span>
            <span class="footer-right">
                <a href="https://github.com/phoenixdevellopment75-web/Neurollm" target="_blank" class="github-link">
                    <svg height="14" viewBox="0 0 16 16" width="14" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
                    github.com/phoenixdevellopment75-web/Neurollm
                </a>
            </span>
        </footer>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

STYLE_CSS = """:root {
    --bg: #090a0d;
    --bg-card: rgba(16, 18, 25, 0.8);
    --border: rgba(255, 255, 255, 0.06);
    --text-primary: #faf9f6;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
    --matcha: #6b9a5b;
    --ml: #8ebb7a;
    --highlight-matcha: #8ebb7a;
    --gold: #c49a2a;
    --gl: #d4af4e;
    --highlight-gold: #d4af4e;
    --cream: #f5e6c8;
    --pill-bg: rgba(107, 154, 91, 0.04);
    --serif: 'DM Serif Display', Georgia, serif;
    --sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --mono: 'Space Grotesk', monospace;
    --shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    --mesh-opacity: 0.12;
    --glow-opacity: 0.06;
}

body.light-theme {
    --bg: #faf9f6;
    --bg-card: #ffffff;
    --border: rgba(0, 0, 0, 0.06);
    --text-primary: #1a1a1a;
    --text-secondary: #555555;
    --text-muted: #999999;
    --matcha: #6b9a5b;
    --ml: #6b9a5b;
    --highlight-matcha: #6b9a5b;
    --gold: #c49a2a;
    --gl: #c49a2a;
    --highlight-gold: #c49a2a;
    --pill-bg: rgba(107, 154, 91, 0.03);
    --shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    --mesh-opacity: 0.08;
    --glow-opacity: 0.04;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    background-color: var(--bg);
    color: var(--text-primary);
    font-family: var(--sans);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow-x: hidden;
    position: relative;
    padding: 30px;
    transition: background-color 0.4s ease, color 0.4s ease;
    -webkit-font-smoothing: antialiased;
}

::-webkit-scrollbar {
    width: 4px;
}
::-webkit-scrollbar-track {
    background: var(--bg);
}
::-webkit-scrollbar-thumb {
    background: var(--matcha);
    border-radius: 4px;
}

.cursor-glow {
    position: fixed;
    width: 400px;
    height: 400px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
    background: radial-gradient(circle, rgba(107, 154, 91, var(--glow-opacity)) 0%, transparent 70%);
    transform: translate(-50%, -50%);
    transition: transform 0.1s ease-out;
    will-change: transform;
}

#particles {
    position: fixed;
    inset: 0;
    z-index: 1;
    pointer-events: none;
}

.mesh-bg {
    position: fixed;
    inset: 0;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}

.mesh-blob {
    position: absolute;
    border-radius: 50%;
    filter: blur(120px);
    opacity: var(--mesh-opacity);
    animation: meshFloat 16s ease-in-out infinite;
    transition: opacity 0.4s ease;
}

.mesh-blob.b1 {
    width: min(600px, 80vw);
    height: min(600px, 80vw);
    background: var(--matcha);
    top: -10%;
    right: -10%;
    animation-delay: 0s;
}

.mesh-blob.b2 {
    width: min(500px, 70vw);
    height: min(500px, 70vw);
    background: var(--cream);
    bottom: -10%;
    left: -5%;
    animation-delay: -4s;
}

.mesh-blob.b3 {
    width: min(400px, 60vw);
    height: min(400px, 60vw);
    background: var(--gold);
    top: 40%;
    left: 40%;
    animation-delay: -8s;
}

@keyframes meshFloat {
    0%, 100% { transform: translate(0, 0) scale(1); }
    25% { transform: translate(40px, -30px) scale(1.05); }
    50% { transform: translate(-20px, 40px) scale(0.97); }
    75% { transform: translate(30px, 20px) scale(1.03); }
}

.loader {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: var(--bg);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    transition: clip-path 1.2s cubic-bezier(.77, 0, .18, 1), background-color 0.4s;
    clip-path: inset(0 0 0 0);
}

.loader.done {
    clip-path: inset(0 0 100% 0);
}

.loader-text {
    font-family: var(--serif);
    font-size: clamp(2.8rem, 6vw, 5rem);
    color: var(--text-primary);
    overflow: hidden;
    display: flex;
    letter-spacing: -0.02em;
}

.loader-text span {
    display: inline-block;
    animation: ldIn 0.8s cubic-bezier(.77, 0, .18, 1) calc(var(--i) * 0.05s) both;
}

.loader-sub {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-top: 1rem;
    animation: ldIn 0.8s 0.7s both;
}

.loader-bar {
    width: 100px;
    height: 1.5px;
    background: var(--border);
    margin-top: 2rem;
    border-radius: 1px;
    overflow: hidden;
    position: relative;
}

.loader-bar::after {
    content: '';
    display: block;
    width: 100%;
    height: 100%;
    background: var(--matcha);
    animation: ldBar 1.2s 0.4s ease-in-out both;
}

@keyframes ldIn {
    from { transform: translateY(120%); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

@keyframes ldBar {
    from { transform: scaleX(0); transform-origin: left; }
    to { transform: scaleX(1); transform-origin: left; }
}

.dashboard-container {
    position: relative;
    width: 100%;
    max-width: 1200px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 35px;
    z-index: 10;
    box-shadow: var(--shadow);
    backdrop-filter: blur(16px);
    display: flex;
    flex-direction: column;
    gap: 30px;
    transition: background-color 0.4s, border-color 0.4s, box-shadow 0.4s;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding-bottom: 20px;
}

.header-title-container {
    display: flex;
    align-items: center;
    gap: 15px;
}

.logo-accent {
    width: 3px;
    height: 28px;
    background: var(--matcha);
    border-radius: 2px;
}

.header-title {
    font-family: var(--serif);
    font-size: 2rem;
    font-weight: 400;
    letter-spacing: -0.02em;
    color: var(--text-primary);
}

.model-tag {
    font-family: var(--mono);
    font-size: 0.7rem;
    background: var(--pill-bg);
    color: var(--ml);
    border: 1px solid var(--border);
    padding: 3px 8px;
    border-radius: 4px;
    letter-spacing: 0.5px;
}

.header-controls {
    display: flex;
    align-items: center;
    gap: 20px;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 10px;
    border: 1px solid var(--border);
    padding: 6px 14px;
    border-radius: 20px;
    background: var(--bg);
}

.status-dot {
    width: 6px;
    height: 6px;
    background-color: var(--matcha);
    border-radius: 50%;
}

.status-text {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 500;
    color: var(--text-secondary);
}

.status-active {
    color: var(--ml);
}

.theme-toggle-btn {
    background: var(--btn-bg);
    border: 1px solid var(--btn-border);
    color: var(--btn-text);
    width: 36px;
    height: 36px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s, border-color 0.2s, color 0.2s, transform 0.2s;
}

.theme-toggle-btn:hover {
    background: var(--border);
    transform: scale(1.05);
}

.theme-toggle-btn span {
    font-size: 1.15rem;
}

.dashboard-content {
    display: grid;
    grid-template-columns: 1fr 320px;
    gap: 30px;
}

.main-panel {
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.card {
    background: transparent;
    border: none;
    border-bottom: 1px solid var(--border);
    border-radius: 0;
    padding: 0;
    padding-bottom: 25px;
    position: relative;
    transition: border-color 0.3s;
}

.card:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 15px;
}

.card-num {
    font-family: var(--mono);
    font-size: 0.8rem;
    color: var(--text-muted);
}

.card-header h2 {
    font-family: var(--serif);
    font-size: 1.25rem;
    font-weight: 400;
    letter-spacing: -0.01em;
    color: var(--text-primary);
}

.mission-text {
    font-size: 0.95rem;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 15px;
}

.tech-specs {
    display: flex;
    gap: 10px;
}

.spec-tag {
    font-family: var(--mono);
    font-size: 0.7rem;
    border: 1px solid var(--border);
    color: var(--text-secondary);
    padding: 4px 10px;
    border-radius: 4px;
    background: var(--bg);
}

.live-badge {
    margin-left: auto;
    font-family: var(--mono);
    font-size: 0.6rem;
    font-weight: 500;
    color: var(--matcha);
    border: 1px solid var(--border);
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.5px;
    background: var(--pill-bg);
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 20px;
}

.metric-box {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: background-color 0.2s, border-color 0.2s;
}

.metric-label {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 500;
    color: var(--text-muted);
    letter-spacing: 0.5px;
}

.metric-value {
    font-family: var(--mono);
    font-size: 1.85rem;
    font-weight: 400;
    color: var(--text-primary);
}

.highlight-matcha {
    color: var(--highlight-matcha);
}

.highlight-gold {
    color: var(--highlight-gold);
}

.progress-bar-container {
    height: 3px;
    background: var(--border);
    border-radius: 2px;
    overflow: hidden;
    margin-top: 3px;
}

.progress-bar-fill {
    height: 100%;
    background: var(--text-primary);
    border-radius: 2px;
    transition: width 0.5s cubic-bezier(0.1, 0.8, 0.2, 1);
}

.progress-bar-fill.green-fill {
    background: var(--matcha);
}

.sparkline-container {
    height: 30px;
    display: flex;
    align-items: center;
    margin-top: 3px;
}

.metric-subtext {
    font-family: var(--mono);
    font-size: 0.65rem;
    color: var(--text-muted);
}

.simulator-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--bg);
    border: 1px solid var(--border);
    padding: 12px 18px;
    border-radius: 8px;
}

.control-description {
    font-size: 0.8rem;
    color: var(--text-secondary);
}

.btn-group {
    display: flex;
    gap: 8px;
}

.btn {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 500;
    padding: 6px 14px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s, border-color 0.2s, color 0.2s;
}

.btn-fill {
    background: var(--text-primary);
    color: var(--bg);
    border: 1px solid var(--text-primary);
}

.btn-fill:hover {
    background: var(--text-secondary);
    border-color: var(--text-secondary);
}

.btn-outline {
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border);
}

.btn-outline:hover {
    background: var(--border);
}

.console-body {
    background: var(--bg);
    border: 1px solid var(--border);
    font-family: var(--mono);
    font-size: 0.75rem;
    color: var(--text-secondary);
    height: 105px;
    overflow-y: auto;
    padding: 12px;
    border-radius: 8px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    scrollbar-width: thin;
    scrollbar-color: var(--border) transparent;
}

.log-line {
    line-height: 1.4;
}

.log-line.system {
    color: var(--text-muted);
}

.log-line.simulation {
    color: var(--gold);
}

.log-line.update {
    color: var(--matcha);
}

.side-panel {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.capsule-card {
    position: relative;
    width: 100%;
    border: 1px solid var(--border);
    border-radius: 160px;
    height: 480px;
    overflow: visible;
    background: var(--bg-card);
    box-shadow: var(--shadow);
    transition: background-color 0.4s, border-color 0.4s;
}

.capsule-inner {
    position: absolute;
    inset: 1px;
    border-radius: 159px;
    background: var(--bg-card);
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 30px;
    z-index: 3;
    transition: background-color 0.4s;
}

.capsule-content {
    position: relative;
    z-index: 5;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}

.capsule-content h3 {
    font-family: var(--serif);
    font-size: 1.1rem;
    font-weight: 400;
    color: var(--text-primary);
    margin-bottom: 20px;
}

.horizontal-stripes {
    position: absolute;
    left: -25px;
    top: 75px;
    width: calc(100% + 50px);
    display: flex;
    flex-direction: column;
    gap: 8px;
    pointer-events: none;
    z-index: 2;
}

.stripe {
    height: 1px;
    background: var(--border);
}

.stripe-1 { width: 100%; }
.stripe-2 { width: 95%; margin-left: 2.5%; }
.stripe-3 { width: 88%; margin-left: 6%; }

.stat-group {
    width: 100%;
    margin-bottom: 14px;
    text-align: left;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    margin-bottom: 5px;
    font-family: var(--mono);
}

.stat-label {
    color: var(--text-secondary);
}

.stat-val {
    color: var(--text-primary);
}

.bar-micro {
    height: 2px;
    background: var(--border);
    overflow: hidden;
}

.bar-micro-fill {
    height: 100%;
    background: var(--text-primary);
}

.divider-dashed {
    width: 50%;
    border-bottom: 1px dashed var(--border);
    margin: 20px 0;
}

.db-status-container {
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid var(--border);
    padding: 6px 12px;
    border-radius: 6px;
    margin-bottom: 8px;
    background: var(--bg);
}

.db-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
}

.db-dot.offline {
    background-color: var(--gold);
}

.db-dot.online {
    background-color: var(--matcha);
}

.db-text {
    font-size: 0.65rem;
    font-family: var(--mono);
    color: var(--text-secondary);
}

.db-desc {
    font-size: 0.65rem;
    color: var(--text-muted);
    line-height: 1.4;
    padding: 0 10px;
}

.code-highlight {
    font-family: monospace;
    color: var(--gold);
}

.dashboard-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid var(--border);
    padding-top: 15px;
    font-size: 0.7rem;
    color: var(--text-muted);
    font-family: var(--mono);
}

.github-link {
    display: flex;
    align-items: center;
    gap: 6px;
    color: var(--text-muted);
    text-decoration: none;
    transition: color 0.2s;
}

.github-link:hover {
    color: var(--text-secondary);
}

@media (max-width: 1024px) {
    .dashboard-content {
        grid-template-columns: 1fr;
    }
    
    .side-panel {
        align-items: center;
    }
    
    .capsule-card {
        height: auto;
        border-radius: 30px;
        max-width: 450px;
    }
    
    .capsule-inner {
        position: relative;
        border-radius: 29px;
        padding: 30px;
        top: 0; left: 0; right: 0; bottom: 0;
    }
    
    .horizontal-stripes {
        display: none;
    }
}

@media (max-width: 768px) {
    body {
        padding: 15px;
    }
    
    .dashboard-container {
        padding: 20px;
    }
    
    .dashboard-header {
        flex-direction: column;
        gap: 15px;
        align-items: flex-start;
    }
    
    .metrics-grid {
        grid-template-columns: 1fr;
    }
    
    .header-title {
        font-size: 1.6rem;
    }
}"""

SCRIPT_JS = """window.addEventListener('load', () => {
    setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.classList.add('done');
        }
    }, 1500);
});

const glow = document.getElementById('cursorGlow');
if (glow) {
    document.addEventListener('mousemove', e => {
        glow.style.transform = `translate(${e.clientX - 200}px, ${e.clientY - 200}px)`;
    });
}

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
        drawLossSparkline();
    });
}

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

const epochValEl = document.getElementById('val-epoch');
const lossValEl = document.getElementById('val-loss');
const sparsityValEl = document.getElementById('val-sparsity');

const epochBarEl = document.getElementById('bar-epoch');
const sparsityBarEl = document.getElementById('bar-sparsity');

const btnToggleSim = document.getElementById('btn-toggle-sim');
const btnResetSim = document.getElementById('btn-reset-sim');
const consoleLogsEl = document.getElementById('console-logs');

const lossCanvas = document.getElementById('loss-canvas');
const ctx = lossCanvas ? lossCanvas.getContext('2d') : null;

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

window.addEventListener('DOMContentLoaded', () => {
    initTheme();
    updateMetrics(0, 1.8540, 0.0);
    startSimulation();
});"""

# ==========================================
# 4. CLONE AND DEPLOY PIPELINE
# ==========================================
print("\n=== [2/5] CONFIGURING ENVIRONMENT ===")
try:
    print(f"Setting global git configuration to {GIT_USER_NAME}...")
    subprocess.run(["git", "config", "--global", "user.name", GIT_USER_NAME], check=True)
    subprocess.run(["git", "config", "--global", "user.email", GIT_USER_EMAIL], check=True)
    print("✔ Git user configured successfully.")
except Exception as e:
    print(f"⚠ Failed to set global git config ({e}). This may fail if git is not installed.")

if os.path.exists(REPO_NAME):
    print(f"Cleaning up existing local directory '{REPO_NAME}'...")
    shutil.rmtree(REPO_NAME)

print("\n=== [3/5] CLONING REPOSITORY ===")
clone_url = f"https://{github_token}@github.com/{REPO_OWNER}/{REPO_NAME}.git"
try:
    subprocess.run(["git", "clone", "--quiet", clone_url], check=True)
    print(f"✔ Successfully cloned {REPO_OWNER}/{REPO_NAME}!")
except Exception as e:
    print(f"❌ Failed to clone repository: {e}")
    sys.exit(1)

print("\n=== [4/5] WRITING WEBSITE FILES ===")
repo_path = os.path.join(os.getcwd(), REPO_NAME)

try:
    html_path = os.path.join(repo_path, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(INDEX_HTML)
    print("✔ Wrote 'index.html'")

    css_path = os.path.join(repo_path, "style.css")
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(STYLE_CSS)
    print("✔ Wrote 'style.css'")

    js_path = os.path.join(repo_path, "script.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(SCRIPT_JS)
    print("✔ Wrote 'script.js'")
except Exception as e:
    print(f"❌ Failed to write website files to the repository directory: {e}")
    sys.exit(1)

print("\n=== [5/5] COMMITTING AND PUSHING TO GITHUB ===")
try:
    print("Staging changes...")
    subprocess.run(["git", "add", "index.html", "style.css", "script.js"], cwd=repo_path, check=True)

    status_proc = subprocess.run(
        ["git", "status", "--porcelain"], 
        cwd=repo_path, 
        capture_output=True, 
        text=True, 
        check=True
    )
    
    if not status_proc.stdout.strip():
        print("✔ No changes detected! Website files already match repository version.")
        sys.exit(0)

    print("Committing changes...")
    commit_msg = "Deploy aesthetic theme-switching Project SparseMind dashboard"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_path, check=True)

    print(f"Pushing to remote repository on branch '{BRANCH}'...")
    subprocess.run(["git", "push", "origin", BRANCH], cwd=repo_path, check=True)
    
    print("\n🚀 SUCCESS! The dashboard is live on your repository!")
    print(f"Repository Link: https://github.com/{REPO_OWNER}/{REPO_NAME}")
except Exception as e:
    print(f"❌ Git pipeline execution failed: {e}")
    sys.exit(1)
