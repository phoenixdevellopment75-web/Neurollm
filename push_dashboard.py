#!/usr/bin/env python3
"""
Project SparseMind Automation & Deployment Script
------------------------------------------------
This Python script is designed to run in Kaggle Notebooks or Google Colab.
It does the following:
1. Securely fetches your GitHub Personal Access Token (PAT) from Kaggle Secrets.
2. Clones the 'Neurollm' repository.
3. Automatically writes the minimalist, theme-swapping, static Dashboard files (index.html, style.css, script.js).
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
    <title>Project SparseMind | Neurosparse v1</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,0,0&display=swap" />
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="top-bar">
        <button id="themeToggleBtn" class="theme-toggle-btn" aria-label="Toggle light/dark theme">
            <span class="material-symbols-rounded" id="themeIcon">dark_mode</span>
        </button>
    </div>

    <div class="loader" id="loader">
        <div class="loader-text">
            <span style="--i:0">S</span><span style="--i:1">p</span><span style="--i:2">a</span><span style="--i:3">r</span><span style="--i:4">s</span><span style="--i:5">e</span><span style="--i:6">M</span><span style="--i:7">i</span><span style="--i:8">n</span><span style="--i:9">d</span>
        </div>
        <div class="loader-sub">Neurosparse v1 Core Interface</div>
        <div class="loader-bar"></div>
    </div>

    <main class="content-container">
        <header class="project-header">
            <span class="step-badge">STEP 1</span>
            <h1 class="project-title">Project SparseMind</h1>
            <p class="project-subtitle">Model: Neurosparse v1</p>
        </header>

        <div class="divider"></div>

        <section class="section">
            <h2 class="section-title">Objective</h2>
            <p class="goal-text">
                Building a high-efficiency sparse Large Language Model (1M-5M parameters) optimized for commodity hardware, specifically targetting T4 GPU acceleration via dynamic activation sparsity and weight pruning.
            </p>
        </section>

        <section class="section">
            <h2 class="section-title">Current Progress</h2>
            
            <div class="metrics-stack">
                <div class="metric-row">
                    <span class="metric-label">Current Checkpoint</span>
                    <span class="metric-value">1</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Training Loss</span>
                    <span class="metric-value">0.0000</span>
                </div>
                <div class="metric-row">
                    <span class="metric-label">Sparsity Ratio</span>
                    <span class="metric-value">0.0%</span>
                </div>
            </div>
        </section>

        <footer class="project-footer">
            <span class="footer-team">PHOENIX TECH</span>
            <a href="https://github.com/phoenixdevellopment75-web/Neurollm" target="_blank" class="github-link">
                <svg height="14" viewBox="0 0 16 16" width="14" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>
                github/Neurollm
            </a>
        </footer>
    </main>
    <script src="script.js"></script>
</body>
</html>"""

STYLE_CSS = """/* Minimalist & Clean Typography System for Project SparseMind */
:root {
    --bg: #0d0e12;
    --border: rgba(255, 255, 255, 0.08);
    --text-primary: #faf9f6;
    --text-secondary: #a0aec0;
    --text-muted: #4a5568;
    --matcha: #8ebb7a;
    --gold: #d4af4e;
    --serif: 'DM Serif Display', Georgia, serif;
    --sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --mono: 'Space Grotesk', monospace;
    --btn-bg: rgba(255, 255, 255, 0.03);
    --btn-border: rgba(255, 255, 255, 0.1);
}

body.light-theme {
    --bg: #faf9f6;
    --border: rgba(0, 0, 0, 0.08);
    --text-primary: #1a1a1a;
    --text-secondary: #4a5568;
    --text-muted: #a0aec0;
    --matcha: #6b9a5b;
    --gold: #c49a2a;
    --btn-bg: rgba(0, 0, 0, 0.02);
    --btn-border: rgba(0, 0, 0, 0.08);
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
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
    transition: background-color 0.4s ease, color 0.4s ease;
    -webkit-font-smoothing: antialiased;
}

.top-bar {
    position: absolute;
    top: 30px;
    right: 30px;
    z-index: 100;
}

.theme-toggle-btn {
    background: var(--btn-bg);
    border: 1px solid var(--btn-border);
    color: var(--text-primary);
    width: 40px;
    height: 40px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s, border-color 0.2s, transform 0.2s;
}

.theme-toggle-btn:hover {
    background: var(--border);
    transform: scale(1.05);
}

.theme-toggle-btn span {
    font-size: 1.2rem;
}

.content-container {
    width: 100%;
    max-width: 600px;
    display: flex;
    flex-direction: column;
    gap: 30px;
}

.project-header {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
}

.step-badge {
    font-family: var(--mono);
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 2px;
    color: var(--matcha);
    border: 1px solid var(--border);
    padding: 4px 10px;
    border-radius: 4px;
    background: var(--btn-bg);
}

.project-title {
    font-family: var(--serif);
    font-size: 2.8rem;
    font-weight: 400;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.project-subtitle {
    font-family: var(--mono);
    font-size: 0.8rem;
    letter-spacing: 1px;
    color: var(--text-secondary);
    text-transform: uppercase;
}

.divider {
    height: 1px;
    background-color: var(--border);
    width: 100%;
}

.section {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.section-title {
    font-family: var(--mono);
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
}

.goal-text {
    font-size: 1rem;
    line-height: 1.6;
    color: var(--text-secondary);
    font-weight: 400;
}

.metrics-stack {
    display: flex;
    flex-direction: column;
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
}

.metric-row:last-child {
    border-bottom: none;
}

.metric-label {
    font-family: var(--sans);
    font-size: 0.85rem;
    color: var(--text-secondary);
}

.metric-value {
    font-family: var(--mono);
    font-size: 1.1rem;
    font-weight: 500;
    color: var(--text-primary);
}

.project-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 1px;
}

.footer-team {
    font-weight: 500;
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

@media (max-width: 640px) {
    body {
        padding: 80px 24px 40px 24px;
    }
    .project-title {
        font-size: 2.2rem;
    }
}"""

SCRIPT_JS = """const themeToggleBtn = document.getElementById('themeToggleBtn');
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
    });
}

window.addEventListener('DOMContentLoaded', () => {
    initTheme();
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
    commit_msg = "Deploy clean minimalist typography Project SparseMind dashboard"
    subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_path, check=True)

    print(f"Pushing to remote repository on branch '{BRANCH}'...")
    subprocess.run(["git", "push", "origin", BRANCH], cwd=repo_path, check=True)
    
    print("\n🚀 SUCCESS! The dashboard is live on your repository!")
    print(f"Repository Link: https://github.com/{REPO_OWNER}/{REPO_NAME}")
except Exception as e:
    print(f"❌ Git pipeline execution failed: {e}")
    sys.exit(1)
