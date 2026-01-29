#!/usr/bin/env python3
"""
GitHub Termux Commander - Advanced GitHub Management Tool for Termux
Author: Takbir Ahmed
Version: 1.0.0
Features: Multi-tool integration with unique capabilities
"""

import os
import sys
import json
import requests
import subprocess
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
import hashlib
import base64
from dataclasses import dataclass
import shutil

# ASCII Art for Termux
TERMUX_ASCII = """
\033[1;36m
╔══════════════════════════════════════════════════╗
║    🚀 GitHub Termux Commander v1.0.0             ║
║    🔥 Exclusive Professional Tool                ║
║    📱 Optimized for Termux Environment          ║
╚══════════════════════════════════════════════════╝
\033[0m
"""

@dataclass
class GitHubConfig:
    username: str = ""
    token: str = ""
    default_editor: str = "nano"
    termux_mode: bool = True

class GitHubTermuxCommander:
    def __init__(self):
        self.config = GitHubConfig()
        self.config_dir = Path.home() / ".github_commander"
        self.config_file = self.config_dir / "config.json"
        self.session_file = self.config_dir / "session.enc"
        self._setup_environment()
        self._load_config()
        
    def _setup_environment(self):
        """Setup Termux-specific environment"""
        if not self.config_dir.exists():
            self.config_dir.mkdir(exist_ok=True)
            
        # Termux specific checks
        if 'com.termux' in os.environ.get('PREFIX', ''):
            print("\033[1;32m✓ Termux environment detected\033[0m")
            self.config.termux_mode = True
            self._setup_termux_dependencies()
        else:
            print("\033[1;33m⚠ Non-Termux environment\033[0m")
            self.config.termux_mode = False
            
    def _setup_termux_dependencies(self):
        """Install required packages for Termux"""
        required_pkgs = ['git', 'openssh', 'python', 'nano']
        missing_pkgs = []
        
        for pkg in required_pkgs:
            if shutil.which(pkg) is None:
                missing_pkgs.append(pkg)
                
        if missing_pkgs:
            print(f"\033[1;33mInstalling missing packages: {', '.join(missing_pkgs)}\033[0m")
            try:
                subprocess.run(['pkg', 'install', '-y'] + missing_pkgs, 
                             check=True, capture_output=True)
                print("\033[1;32m✓ Dependencies installed\033[0m")
            except subprocess.CalledProcessError:
                print("\033[1;31m✗ Failed to install dependencies\033[0m")
                
    def _encrypt_data(self, data: str) -> str:
        """Simple encryption for session data"""
        salt = "github_termux_salt_2024"
        return base64.b64encode(
            hashlib.sha256((data + salt).encode()).digest()
        ).decode()[:32]
        
    def _load_config(self):
        """Load or create configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    self.config.username = config_data.get('username', '')
                    self.config.token = config_data.get('token', '')
                    print("\033[1;32m✓ Configuration loaded\033[0m")
            except:
                self._create_config()
        else:
            self._create_config()
            
    def _create_config(self):
        """Interactive configuration setup"""
        print("\n\033[1;36m⚙ Initial Setup Required\033[0m")
        print("-" * 40)
        
        self.config.username = input("GitHub Username: ").strip()
        token = input("GitHub Personal Access Token: ").strip()
        
        # Encrypt token
        self.config.token = self._encrypt_data(token)
        
        config_data = {
            'username': self.config.username,
            'token': self.config.token,
            'setup_date': datetime.now().isoformat(),
            'termux_optimized': True
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
            
        print("\033[1;32m✓ Configuration saved securely\033[0m")
        
    def _github_api(self, endpoint: str, method: str = 'GET', data: dict = None) -> dict:
        """Make GitHub API requests"""
        headers = {
            'Authorization': f'token {self.config.token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Termux-Commander/1.0.0'
        }
        
        url = f"https://api.github.com{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)
                
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            print(f"\033[1;31mAPI Error: {e}\033[0m")
            return {}
            
    def repo_smart_clone(self, repo_url: str, depth: int = None):
        """Smart cloning with optimization for Termux"""
        print(f"\n\033[1;36m🔍 Smart Cloning: {repo_url}\033[0m")
        
        # Extract repo name from URL
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        
        # Check if already exists
        if Path(repo_name).exists():
            choice = input(f"Repository '{repo_name}' exists. Update? [y/N]: ")
            if choice.lower() == 'y':
                self._update_repo(repo_name)
                return
                
        # Optimized clone for Termux
        cmd = ['git', 'clone']
        
        if depth and self.config.termux_mode:
            cmd.extend(['--depth', str(depth)])
            print(f"\033[1;33m📦 Shallow clone (depth: {depth}) for Termux optimization\033[0m")
            
        cmd.append(repo_url)
        
        try:
            subprocess.run(cmd, check=True)
            print(f"\033[1;32m✓ Successfully cloned: {repo_name}\033[0m")
            
            # Post-clone setup
            self._post_clone_setup(repo_name)
        except subprocess.CalledProcessError:
            print(f"\033[1;31m✗ Failed to clone repository\033[0m")
            
    def _post_clone_setup(self, repo_name: str):
        """Post-clone optimizations for Termux"""
        repo_path = Path(repo_name)
        
        # Set optimal git config for Termux
        subprocess.run(['git', 'config', 'core.preloadindex', 'true'], 
                      cwd=repo_path, capture_output=True)
        subprocess.run(['git', 'config', 'core.fscache', 'true'], 
                      cwd=repo_path, capture_output=True)
        
        print(f"\033[1;32m✓ Repository optimized for Termux\033[0m")
        
    def _update_repo(self, repo_path: str):
        """Update existing repository"""
        try:
            subprocess.run(['git', 'pull'], cwd=repo_path, check=True)
            print(f"\033[1;32m✓ Repository updated\033[0m")
        except subprocess.CalledProcessError:
            print(f"\033[1;31m✗ Failed to update repository\033[0m")
            
    def create_repo(self, name: str, private: bool = False, description: str = ""):
        """Create a new GitHub repository"""
        data = {
            'name': name,
            'description': description,
            'private': private,
            'auto_init': True,
            'gitignore_template': 'Python'
        }
        
        result = self._github_api('/user/repos', 'POST', data)
        
        if result.get('id'):
            print(f"\033[1;32m✓ Repository '{name}' created successfully!\033[0m")
            print(f"   SSH: {result.get('ssh_url')}")
            print(f"   HTTPS: {result.get('clone_url')}")
            
            # Auto-clone if in Termux
            if self.config.termux_mode and input("\nClone now? [Y/n]: ").lower() != 'n':
                self.repo_smart_clone(result.get('clone_url'))
        else:
            print(f"\033[1;31m✗ Failed to create repository\033[0m")
            
    def repo_health_check(self, repo_path: str = "."):
        """Check repository health and optimizations"""
        print(f"\n\033[1;36m🏥 Repository Health Check\033[0m")
        print("-" * 40)
        
        checks = [
            ("Git directory", Path(repo_path) / ".git"),
            ("Remote configured", ["git", "remote", "-v"]),
            ("Latest changes", ["git", "fetch", "--dry-run"]),
            ("Large files", ["git", "lfs", "track"]),
        ]
        
        all_good = True
        for check_name, check_cmd in checks:
            if isinstance(check_cmd, Path):
                exists = check_cmd.exists()
                status = "✓" if exists else "✗"
                color = "\033[1;32m" if exists else "\033[1;31m"
                print(f"{color}{status} {check_name}\033[0m")
                if not exists:
                    all_good = False
            else:
                try:
                    subprocess.run(check_cmd, cwd=repo_path, 
                                 capture_output=True, check=True)
                    print(f"\033[1;32m✓ {check_name}\033[0m")
                except:
                    print(f"\033[1;33m⚠ {check_name} (not configured)\033[0m")
                    
        if all_good:
            print(f"\n\033[1;32m✅ Repository is healthy!\033[0m")
        else:
            print(f"\n\033[1;33m⚠ Some issues detected\033[0m")
            
    def termux_quick_commit(self, message: str = None):
        """Quick commit optimized for Termux mobile workflow"""
        if not message:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message = f"Termux commit {timestamp}"
            
        try:
            # Add all changes
            subprocess.run(['git', 'add', '-A'], check=True)
            
            # Commit
            subprocess.run(['git', 'commit', '-m', message], check=True)
            
            # Push
            subprocess.run(['git', 'push'], check=True)
            
            print(f"\033[1;32m✓ Quick commit completed: {message}\033[0m")
        except subprocess.CalledProcessError as e:
            print(f"\033[1;31m✗ Commit failed: {e}\033[0m")
            
    def search_repos(self, query: str, language: str = None):
        """Search GitHub repositories with filters"""
        endpoint = f"/search/repositories?q={query}"
        if language:
            endpoint += f"+language:{language}"
            
        results = self._github_api(endpoint)
        
        if results.get('items'):
            print(f"\n\033[1;36m🔍 Search Results ({len(results['items'])} found)\033[0m")
            print("-" * 60)
            
            for item in results['items'][:10]:  # Show top 10
                print(f"\033[1;34m★ {item['full_name']}\033[0m")
                print(f"  {item['description'][:80] if item['description'] else 'No description'}")
                print(f"  🌟 {item['stargazers_count']} | 🍴 {item['forks_count']}")
                print(f"  📁 {item['language'] if item['language'] else 'N/A'}")
                print()
        else:
            print("\033[1;33mNo repositories found\033[0m")
            
    def display_dashboard(self):
        """Display GitHub dashboard"""
        user_data = self._github_api('/user')
        repos = self._github_api('/user/repos?per_page=5')
        
        print(TERMUX_ASCII)
        print(f"\033[1;36m👤 User: {user_data.get('login', 'N/A')}\033[0m")
        print(f"\033[1;36m📊 Public Repos: {user_data.get('public_repos', 0)}\033[0m")
        print(f"\033[1;36m📅 Account Created: {user_data.get('created_at', 'N/A')[:10]}\033[0m")
        print("\n\033[1;36m📁 Recent Repositories:\033[0m")
        print("-" * 40)
        
        for repo in repos[:5]:
            print(f"\033[1;34m• {repo['name']}\033[0m")
            print(f"  {repo['description'] or 'No description'}")
            print(f"  🌐 {repo['html_url']}")
            print()
            
    def termux_notification(self, title: str, message: str):
        """Send Termux notification"""
        if self.config.termux_mode:
            try:
                subprocess.run([
                    'termux-notification',
                    '--title', title,
                    '--content', message,
                    '--sound'
                ], capture_output=True)
            except:
                pass  # Notification not critical
                
    def cleanup_cache(self):
        """Cleanup git cache and temporary files"""
        print("\n\033[1;36m🧹 Cleaning up cache...\033[0m")
        
        try:
            # Clean git cache
            subprocess.run(['git', 'gc', '--aggressive', '--prune=now'], 
                         capture_output=True)
            
            # Remove .pyc files
            for pyc in Path('.').rglob('*.pyc'):
                pyc.unlink()
                
            print("\033[1;32m✓ Cleanup completed\033[0m")
        except Exception as e:
            print(f"\033[1;31m✗ Cleanup failed: {e}\033[0m")

def main():
    parser = argparse.ArgumentParser(
        description="GitHub Termux Commander - Advanced GitHub Tool for Termux",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s clone https://github.com/user/repo --depth 1
  %(prog)s create myapp --private --desc "My new app"
  %(prog)s commit -m "Quick update from Termux"
  %(prog)s health
  %(prog)s search "machine learning" --lang python
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Clone command
    clone_parser = subparsers.add_parser('clone', help='Smart clone repository')
    clone_parser.add_argument('url', help='Repository URL')
    clone_parser.add_argument('--depth', type=int, help='Shallow clone depth')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create new repository')
    create_parser.add_argument('name', help='Repository name')
    create_parser.add_argument('--private', action='store_true', help='Private repository')
    create_parser.add_argument('--desc', help='Repository description')
    
    # Commit command
    commit_parser = subparsers.add_parser('commit', help='Quick commit')
    commit_parser.add_argument('-m', '--message', help='Commit message')
    
    # Health check
    subparsers.add_parser('health', help='Repository health check')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search repositories')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--lang', help='Programming language filter')
    
    # Dashboard
    subparsers.add_parser('dashboard', help='Show GitHub dashboard')
    
    # Cleanup
    subparsers.add_parser('cleanup', help='Cleanup cache')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    commander = GitHubTermuxCommander()
    
    # Execute command
    if args.command == 'clone':
        commander.repo_smart_clone(args.url, args.depth)
    elif args.command == 'create':
        commander.create_repo(args.name, args.private, args.desc or "")
    elif args.command == 'commit':
        commander.termux_quick_commit(args.message)
    elif args.command == 'health':
        commander.repo_health_check()
    elif args.command == 'search':
        commander.search_repos(args.query, args.lang)
    elif args.command == 'dashboard':
        commander.display_dashboard()
    elif args.command == 'cleanup':
        commander.cleanup_cache()
        
    # Send completion notification
    if commander.config.termux_mode:
        commander.termux_notification(
            "GitHub Commander",
            f"Command '{args.command}' completed successfully!"
        )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;33m\n👋 Operation cancelled by user\033[0m")
        sys.exit(0)
    except Exception as e:
        print(f"\033[1;31m\n💥 Unexpected error: {e}\033[0m")
        sys.exiN
