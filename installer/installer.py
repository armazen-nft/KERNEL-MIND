#!/usr/bin/env python3
"""
KernelMind GUI Installer — Multi-language, AGPL-3.0 compliant.
Supports: English, Mandarin, Hindi, Spanish, French, Arabic, 
Bengali, Portuguese, Russian, German, Japanese, Indonesian.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import subprocess
import sys
import os
import json
import platform
from pathlib import Path
from translations import TRANSLATIONS, get_language_code, get_translation

class KernelMindInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("KernelMind Installer")
        self.root.geometry("900x720")
        self.root.resizable(True, True)
        
        # Store window state
        self.current_lang = "pt"
        self.accepted = False
        self.modifications_text = ""
        self.installation_thread = None
        
        # Configure style
        self.setup_style()
        self.create_widgets()
        
    def setup_style(self):
        """Configure ttk theme with professional colors."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        bg = "#F7F9FC"
        fg = "#1A2332"
        accent = "#00C49A"
        sky = "#3B82F6"
        
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TFrame', background=bg)
        style.configure('Header.TLabel', font=('Nunito', 16, 'bold'), foreground=fg)
        style.configure('Subtitle.TLabel', font=('Nunito', 10), foreground="#8099B0")
        style.configure('License.TLabel', font=('Courier', 9), foreground=fg)
        
    def create_widgets(self):
        """Build the entire UI."""
        # Main container with padding
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Language selector
        self.create_language_selector(main_frame)
        
        # License section
        self.create_license_section(main_frame)
        
        # Accept checkbox
        self.create_accept_section(main_frame)
        
        # Modifications section
        self.create_modifications_section(main_frame)
        
        # Buttons
        self.create_button_section(main_frame)
        
        # Status
        self.create_status_section(main_frame)
        
    def create_header(self, parent):
        """Create header with title and subtitle."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(
            header_frame, 
            text="KernelMind Installer",
            style='Header.TLabel'
        )
        title.pack(anchor=tk.W)
        
        subtitle = ttk.Label(
            header_frame,
            text="Lightweight ethical AI kernel manager — AGPL-3.0 + PoE Ethics",
            style='Subtitle.TLabel'
        )
        subtitle.pack(anchor=tk.W)
        
    def create_language_selector(self, parent):
        """Create language dropdown."""
        lang_frame = ttk.Frame(parent)
        lang_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(lang_frame, text="Language / Idioma / 语言:", font=('Nunito', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        languages = [
            ("English", "en"),
            ("Português", "pt"),
            ("中文 (Mandarin)", "zh"),
            ("हिन्दी (Hindi)", "hi"),
            ("Español", "es"),
            ("Français", "fr"),
            ("العربية (Arabic)", "ar"),
            ("বাংলা (Bengali)", "bn"),
            ("Русский", "ru"),
            ("Deutsch", "de"),
            ("日本語", "ja"),
            ("Bahasa Indonesia", "id"),
        ]
        
        self.lang_var = tk.StringVar(value="Português")
        lang_display = [lang[0] for lang in languages]
        
        combo = ttk.Combobox(
            lang_frame, 
            textvariable=self.lang_var, 
            values=lang_display, 
            state="readonly",
            width=30
        )
        combo.pack(anchor=tk.W, fill=tk.X)
        combo.bind("<<ComboboxSelected>>", lambda e: self.change_language())
        self.lang_combo = combo
        
    def create_license_section(self, parent):
        """Create scrollable license text area."""
        lic_frame = ttk.LabelFrame(parent, text="AGPL-3.0 License + PoE Ethical Clause", padding=10)
        lic_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create scrolled text widget
        self.license_text = scrolledtext.ScrolledText(
            lic_frame,
            height=12,
            width=80,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=('Courier', 8),
            bg="#FAFFFE",
            fg="#1A2332",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.license_text.pack(fill=tk.BOTH, expand=True)
        
        # Load initial license
        self.update_license_text()
        
    def create_accept_section(self, parent):
        """Create license acceptance checkbox."""
        accept_frame = ttk.Frame(parent)
        accept_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.accept_var = tk.BooleanVar(value=False)
        self.checkbox = ttk.Checkbutton(
            accept_frame,
            text="I accept the AGPL-3.0 license terms and commit to sharing modifications / "
                 "Aceito os termos da AGPL-3.0 e me comprometo a compartilhar modificações",
            variable=self.accept_var,
            command=self.update_button_state
        )
        self.checkbox.pack(anchor=tk.W, fill=tk.X)
        
    def create_modifications_section(self, parent):
        """Create modifications description area."""
        mod_frame = ttk.LabelFrame(
            parent,
            text="Describe modifications (if this is a fork) / Descreva modificações (se for um fork):",
            padding=10
        )
        mod_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 15))
        
        self.modifications = tk.Text(
            mod_frame,
            height=4,
            width=80,
            wrap=tk.WORD,
            font=('Nunito', 9),
            bg="#FAFFFE",
            fg="#1A2332",
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.modifications.pack(fill=tk.BOTH, expand=True)
        self.modifications.insert("1.0", "Optional: describe any changes you made...")
        
    def create_button_section(self, parent):
        """Create action buttons."""
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Download/Install button (initially disabled)
        self.download_btn = ttk.Button(
            btn_frame,
            text="Download from GitHub and Install",
            command=self.start_installation,
            state=tk.DISABLED
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Help button
        help_btn = ttk.Button(
            btn_frame,
            text="Help",
            command=self.show_help
        )
        help_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Cancel button
        cancel_btn = ttk.Button(
            btn_frame,
            text="Cancel",
            command=self.root.quit
        )
        cancel_btn.pack(side=tk.LEFT)
        
    def create_status_section(self, parent):
        """Create status display area."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X)
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready",
            foreground="#00C49A",
            font=('Nunito', 9)
        )
        self.status_label.pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.pack(fill=tk.X, pady=(5, 0))
        
    def change_language(self):
        """Handle language change."""
        display_name = self.lang_var.get()
        lang_map = {
            "English": "en",
            "Português": "pt",
            "中文 (Mandarin)": "zh",
            "हिन्दी (Hindi)": "hi",
            "Español": "es",
            "Français": "fr",
            "العربية (Arabic)": "ar",
            "বাংলা (Bengali)": "bn",
            "Русский": "ru",
            "Deutsch": "de",
            "日本語": "ja",
            "Bahasa Indonesia": "id",
        }
        self.current_lang = lang_map.get(display_name, "en")
        self.update_license_text()
        
    def update_license_text(self):
        """Update license text based on current language."""
        self.license_text.config(state=tk.NORMAL)
        self.license_text.delete("1.0", tk.END)
        
        license_text = get_translation(self.current_lang, "license_text")
        self.license_text.insert("1.0", license_text)
        self.license_text.config(state=tk.DISABLED)
        
    def update_button_state(self):
        """Enable download button only if license is accepted."""
        if self.accept_var.get():
            self.download_btn.config(state=tk.NORMAL)
        else:
            self.download_btn.config(state=tk.DISABLED)
            
    def start_installation(self):
        """Begin the installation process."""
        if not self.accept_var.get():
            messagebox.showerror("Error", "Please accept the license terms first.")
            return
        
        # Get modifications text
        self.modifications_text = self.modifications.get("1.0", tk.END).strip()
        if self.modifications_text == "Optional: describe any changes you made...":
            self.modifications_text = ""
        
        # Disable button and show progress
        self.download_btn.config(state=tk.DISABLED)
        self.progress.start()
        self.status_label.config(text="Downloading from GitHub...")
        self.root.update()
        
        try:
            # Clone repository
            self.status_label.config(text="Cloning repository...")
            repo_path = os.path.expanduser("~/kernelmind")
            
            if os.path.exists(repo_path):
                # Update existing
                subprocess.run(
                    ["git", "-C", repo_path, "pull"],
                    check=True,
                    capture_output=True
                )
            else:
                # Clone new
                subprocess.run(
                    [
                        "git", "clone",
                        "https://github.com/armazen-nft/KERNEL-MIND.git",
                        repo_path
                    ],
                    check=True,
                    capture_output=True
                )
            
            # Install package
            self.status_label.config(text="Installing dependencies...")
            self.root.update()
            
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-e", repo_path],
                check=True,
                capture_output=True
            )
            
            # Save installation metadata
            self.save_installation_metadata(repo_path)
            
            # Success
            self.progress.stop()
            self.status_label.config(
                text="✓ Installation complete! Run: km --help",
                foreground="#00C49A"
            )
            
            messagebox.showinfo(
                get_translation(self.current_lang, "success_title"),
                get_translation(self.current_lang, "success_message")
            )
            
            self.show_completion_screen()
            
        except subprocess.CalledProcessError as e:
            self.progress.stop()
            self.status_label.config(text="✗ Installation failed", foreground="#FF6B6B")
            self.download_btn.config(state=tk.NORMAL)
            messagebox.showerror(
                "Installation Error",
                f"Error during installation:\n{str(e)}\n\n"
                "Please check your internet connection and try again."
            )
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="✗ Installation failed", foreground="#FF6B6B")
            self.download_btn.config(state=tk.NORMAL)
            messagebox.showerror("Error", f"Unexpected error:\n{str(e)}")
    
    def save_installation_metadata(self, install_path):
        """Save metadata about this installation."""
        metadata = {
            "language": self.current_lang,
            "os": platform.system(),
            "python_version": sys.version,
            "modifications": self.modifications_text,
            "timestamp": __import__('datetime').datetime.now().isoformat(),
        }
        
        meta_file = Path(install_path) / ".kernelmind_installer_meta.json"
        try:
            with open(meta_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception:
            pass  # Non-critical failure
    
    def show_completion_screen(self):
        """Show completion message."""
        completion_msg = (
            "🎉 KernelMind installed successfully!\n\n"
            "Next steps:\n"
            "1. Run: km --help\n"
            "2. Try: km snapshot\n"
            "3. Start API: km-api\n"
            "4. View docs: https://github.com/armazen-nft/KERNEL-MIND\n\n"
            "Thank you for supporting ethical AI!"
        )
        messagebox.showinfo("Installation Complete", completion_msg)
    
    def show_help(self):
        """Show help dialog."""
        help_text = (
            "KernelMind Installer Help\n"
            "═══════════════════════════════════════\n\n"
            "1. Select your language from the dropdown\n"
            "2. Read and accept the AGPL-3.0 license\n"
            "3. Optionally describe any modifications (if forking)\n"
            "4. Click 'Download from GitHub and Install'\n"
            "5. The installer will:\n"
            "   • Clone the repository from GitHub\n"
            "   • Install dependencies via pip\n"
            "   • Register KernelMind in your system\n\n"
            "Requirements:\n"
            "• Python 3.10 or higher\n"
            "• Git installed and in PATH\n"
            "• Internet connection\n"
            "• ~200 MB free disk space\n\n"
            "For issues, visit:\n"
            "https://github.com/armazen-nft/KERNEL-MIND/issues"
        )
        messagebox.showinfo("Help", help_text)


def main():
    """Entry point."""
    root = tk.Tk()
    app = KernelMindInstaller(root)
    root.mainloop()


if __name__ == "__main__":
    main()
