#!/usr/bin/env python3
"""
Simple GitHub Commander for Termux - Lightweight Version
"""

import os
import sys
import subprocess
from pathlib import Path

def termux_check():
    """Check if running in Termux"""
    return 'com.termux' in os.environ.get('PREFIX', '')

def setup_termux():
    """Setup Termux environment"""
    if not termux_check():
        print("⚠ This tool is optimized for Termux")
        return
    
    print("🔧 Setting up Termux environment...")
    
    # Check and install git
    if not shutil.which('git'):
        print("📦 Installing git...")
        subprocess.run(['pkg', 'install', 'git', '-y'], 
                      capture_output=True)
    
    print("✅ Termux setup complete")

def quick_clone():
    """Quick repository cloning"""
    url = input("📌 GitHub repository URL: ").strip()
    if not url.startswith('http'):
        url = 'https://github.com/' + url
    
    repo_name = url.split('/')[-1].replace('.git', '')
    
    print(f"📥 Cloning {repo_name}...")
    result = subprocess.run(['git', 'clone', url], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Successfully cloned: {repo_name}")
        
        # Navigate to directory
        os.chdir(repo_name)
        print(f"📁 Switched to: {os.getcwd()}")
    else:
        print(f"❌ Error: {result.stderr}")

def git_status():
    """Check git status"""
    result = subprocess.run(['git', 'status'], 
                          capture_output=True, text=True)
    print(result.stdout if result.stdout else result.stderr)

def quick_commit():
    """Quick commit all changes"""
    message = input("💭 Commit message (default: Update): ").strip()
    if not message:
        message = "Update from Termux"
    
    # Add all changes
    subprocess.run(['git', 'add', '.'], capture_output=True)
    
    # Commit
    result = subprocess.run(['git', 'commit', '-m', message], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Committed: {message}")
        
        # Push if remote exists
        push = input("🚀 Push to GitHub? (y/N): ").strip().lower()
        if push == 'y':
            subprocess.run(['git', 'push'], capture_output=True)
            print("✅ Pushed to GitHub")
    else:
        print(f"❌ Commit failed: {result.stderr}")

def search_repo():
    """Search for GitHub repos using gh command or curl"""
    query = input("🔍 Search query: ").strip()
    
    if shutil.which('gh'):
        # Use GitHub CLI if available
        subprocess.run(['gh', 'repo', 'search', query])
    else:
        print(f"ℹ️ Search on GitHub: https://github.com/search?q={query}")
        print("Install GitHub CLI: pkg install gh")

def show_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("🚀 GITHUB TERMUX COMMANDER")
    print("="*50)
    print("[1] 📥 Clone Repository")
    print("[2] 📊 Check Git Status")
    print("[3] 💾 Quick Commit & Push")
    print("[4] 🔍 Search Repositories")
    print("[5] ⚙️ Setup Termux")
    print("[6] 📁 List Files")
    print("[7] 🚪 Exit")
    print("="*50)
    
    try:
        choice = input("👉 Select option (1-7): ").strip()
        return choice
    except KeyboardInterrupt:
        return '7'

def main():
    # Check for git
    import shutil
    if not shutil.which('git'):
        print("⚠ Git not found. Installing...")
        setup_termux()
    
    print("✅ GitHub Commander Ready!")
    print(f"📁 Current directory: {os.getcwd()}")
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            quick_clone()
        elif choice == '2':
            git_status()
        elif choice == '3':
            quick_commit()
        elif choice == '4':
            search_repo()
        elif choice == '5':
            setup_termux()
        elif choice == '6':
            subprocess.run(['ls', '-la'])
        elif choice == '7':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled")
    except Exception as e:
        print(f"💥 Error: {e}")
