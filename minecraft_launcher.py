#!/usr/bin/env python3
"""
⛏️ MINECRAFT LAUNCHER PRO - GAMER EDITION
Optimized UI/UX with modern sidebar navigation, neon accents, and custom geometry.
"""

import customtkinter as ctk
import os
import json
import shutil
import subprocess
import threading
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

# Core Launcher Imports
from minecraft_launcher_lib.command import get_minecraft_command
from minecraft_launcher_lib.install import install_minecraft_version
import minecraft_launcher_lib

# Set modern dark gaming palette
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # Base fallback

# Custom Theme Hex Codes for that Cyberpunk/Gaming Look
CLR_BG_DARK = "#12131a"       # Deep background
CLR_PANEL = "#1a1c24"         # Card/Sidebar panels
CLR_ACCENT = "#00adb5"        # Neon Cyan accent
CLR_LAUNCH = "#00b159"        # Emerald Play button
CLR_LAUNCH_HOVER = "#008f47"  # Darker emerald

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Launcher Authentication")
        self.geometry("460x420")
        self.resizable(False, False)
        self.configure(fg_color=CLR_BG_DARK)
        
        self.accounts_file = Path("launcher_accounts.json")
        self.load_accounts()
        
        self.protocol("WM_DELETE_WINDOW", self.on_force_exit)
        self.setup_ui()
        
        # Linux Crostini repaint / focus optimization stability layers
        self.update()
        self.transient(parent)
        self.grab_set()
        
    def load_accounts(self):
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r') as f:
                    self.accounts = json.load(f)
            except Exception:
                self.accounts = {}
        else:
            self.accounts = {}
            
    def save_accounts(self):
        with open(self.accounts_file, 'w') as f:
            json.dump(self.accounts, f, indent=4)
            
    def setup_ui(self):
        # Styled Tabview wrapper
        self.tabview = ctk.CTkTabview(self, width=430, height=380, segmented_button_fg_color=CLR_PANEL, segmented_button_selected_color=CLR_ACCENT)
        self.tabview.pack(padx=15, pady=15, fill="both", expand=True)
        
        self.login_tab = self.tabview.add("🔑 Login")
        self.register_tab = self.tabview.add("➕ Create Account")
        
        # ---- LOGIN TAB LAYOUT ----
        ctk.CTkLabel(self.login_tab, text="SIGN IN TO PROFILE", font=("Segoe UI", 16, "bold"), text_color=CLR_ACCENT).pack(pady=(15, 15))
        
        ctk.CTkLabel(self.login_tab, text="Username:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30)
        self.login_user = ctk.CTkEntry(self.login_tab, width=320, height=35, fg_color=CLR_BG_DARK, border_color=CLR_PANEL, placeholder_text="Username")
        self.login_user.pack(pady=(0, 15))
        
        ctk.CTkLabel(self.login_tab, text="Password:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30)
        self.login_pass = ctk.CTkEntry(self.login_tab, width=320, height=35, fg_color=CLR_BG_DARK, border_color=CLR_PANEL, show="*", placeholder_text="Password")
        self.login_pass.pack(pady=(0, 25))
        
        ctk.CTkButton(self.login_tab, text="LOG IN", height=40, font=("Segoe UI", 13, "bold"), fg_color=CLR_LAUNCH, hover_color=CLR_LAUNCH_HOVER, command=self.handle_login).pack(pady=5, fill="x", padx=30)
        
        # If an account already exists, auto-fill the username field to save time
        if self.accounts:
            last_user = list(self.accounts.keys())[-1]
            self.login_user.insert(0, last_user)
        
        # ---- REGISTER TAB LAYOUT ----
        ctk.CTkLabel(self.register_tab, text="CREATE NEW PROFILE", font=("Segoe UI", 16, "bold"), text_color=CLR_ACCENT).pack(pady=(15, 15))
        
        ctk.CTkLabel(self.register_tab, text="Choose Username:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30)
        self.reg_user = ctk.CTkEntry(self.register_tab, width=320, height=35, fg_color=CLR_BG_DARK, border_color=CLR_PANEL, placeholder_text="Unique Username")
        self.reg_user.pack(pady=(0, 15))
        
        ctk.CTkLabel(self.reg_user, text="Set Password:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=30)
        self.reg_pass = ctk.CTkEntry(self.register_tab, width=320, height=35, fg_color=CLR_BG_DARK, border_color=CLR_PANEL, show="*", placeholder_text="Secure Password")
        self.reg_pass.pack(pady=(0, 25))
        
        ctk.CTkButton(self.register_tab, text="REGISTER DISK PROFILE", height=40, font=("Segoe UI", 13, "bold"), fg_color=CLR_ACCENT, hover_color="#00828a", command=self.handle_registration).pack(pady=5, fill="x", padx=30)

    def handle_login(self):
        username = self.login_user.get().strip()
        password = self.login_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Incomplete Fields", "Please populate both fields.", parent=self)
            return
        if username in self.accounts and self.accounts[username] == password:
            self.parent.active_session_user = username
            self.parent.username_display_label.configure(text=f"👤 {username}")
            self.grab_release()
            self.destroy()
        else:
            messagebox.showerror("Auth Error", "Invalid Username or Password configuration.", parent=self)

    def handle_registration(self):
        username = self.reg_user.get().strip()
        password = self.reg_pass.get().strip()
        if not username or not password:
            messagebox.showwarning("Incomplete Fields", "Please fill inside both allocations.", parent=self)
            return
        if username in self.accounts:
            messagebox.showwarning("Profile Conflict", "Username already exists.", parent=self)
            return
        self.accounts[username] = password
        self.save_accounts()
        messagebox.showinfo("Success", "Profile safely generated! Switch tabs to login.", parent=self)
        self.reg_user.delete(0, tk.END)
        self.reg_pass.delete(0, tk.END)
        self.tabview.set("🔑 Login")
        self.login_user.delete(0, tk.END)
        self.login_user.insert(0, username)

    def on_force_exit(self):
        self.parent.destroy()
        os._exit(0)


class MinecraftLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Minecraft Launcher Pro (Gamer Edition)")
        self.geometry("1100x720")
        self.minimum_size = (950, 620)
        self.resizable(True, True)
        self.configure(fg_color=CLR_BG_DARK)
        
        self.active_session_user = "Player"
        self.game_process = None
        
        # Paths Setup
        self.minecraft_dir = Path.home() / ".minecraft"
        self.minecraft_dir.mkdir(exist_ok=True)
        self.versions_dir = self.minecraft_dir / "versions"
        self.mods_dir = self.minecraft_dir / "mods"
        self.resourcepacks_dir = self.minecraft_dir / "resourcepacks"
        self.config_file = Path("launcher_config.json")
        self.accounts_file = Path("launcher_accounts.json")
        
        for p in [self.versions_dir, self.mods_dir, self.resourcepacks_dir]: p.mkdir(exist_ok=True)
        
        self.load_config()
        self.setup_ui()
        
        self.protocol("WM_DELETE_WINDOW", self.force_close_launcher)
        
        # Check if an existing profile is saved to skip the login prompt step
        has_session = self.attempt_auto_session_login()
        if not has_session:
            self.after(100, self.trigger_login_sequence)
        
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f: self.config = json.load(f)
            except Exception: self.set_default_config()
        else:
            self.set_default_config()

    def set_default_config(self):
        self.config = {
            "account_type": "offline", "version": "latest-release", "ram": 3,
            "java_path": "java", "program_arguments": "", "mods_enabled": True,
            "resource_packs_enabled": True, "server_ip": "", "server_port": 25565
        }
        self.save_config()
    
    def save_config(self):
        with open(self.config_file, 'w') as f: json.dump(self.config, f, indent=4)
            
    def attempt_auto_session_login(self):
        """Checks if a local user account profile file exists and bypasses the splash screen."""
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r') as f:
                    accounts = json.load(f)
                if accounts:
                    # Automatically choose the last active registered username path profile
                    saved_user = list(accounts.keys())[-1]
                    self.active_session_user = saved_user
                    self.username_display_label.configure(text=f"👤 {saved_user}")
                    self.update_status(f"✓ Restored user session profile: {saved_user}")
                    return True
            except Exception:
                pass
        return False

    def trigger_login_sequence(self):
        LoginWindow(self)
    
    def setup_ui(self):
        # ----------------------------------------------------
        # SIDEBAR PANEL (Dashboard Layout)
        # ----------------------------------------------------
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=CLR_PANEL, border_color="#222530", border_width=1)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Brand Header inside sidebar
        brand_label = ctk.CTkLabel(self.sidebar, text="⛏️ CLIENT PRO", font=("Segoe UI", 20, "bold"), text_color=CLR_ACCENT)
        brand_label.pack(pady=(30, 40), padx=20, anchor="w")
        
        # Custom Sidebar Navigation Buttons
        self.btn_nav_dash = self.create_nav_btn("🎮  Dashboard", lambda: self.switch_view("dash"))
        self.btn_nav_mods = self.create_nav_btn("📦  Mod Manager", lambda: self.switch_view("mods"))
        self.btn_nav_packs = self.create_nav_btn("🎨  Resource Packs", lambda: self.switch_view("packs"))
        self.btn_nav_settings = self.create_nav_btn("⚙️  Engine Settings", lambda: self.switch_view("settings"))
        
        # User Badge inside Bottom Sidebar
        user_panel = ctk.CTkFrame(self.sidebar, fg_color=CLR_BG_DARK, height=60, corner_radius=8)
        user_panel.pack(side="bottom", fill="x", padx=15, pady=25)
        
        self.username_display_label = ctk.CTkLabel(user_panel, text="Authenticating...", font=("Segoe UI", 12, "bold"))
        self.username_display_label.pack(side="left", padx=15, pady=10)
        
        logout_btn = ctk.CTkButton(user_panel, text="🔄", width=30, height=30, fg_color="transparent", hover_color="#2c2f3b", font=("Segoe UI", 14), command=self.trigger_login_sequence)
        logout_btn.pack(side="right", padx=10)

        # ----------------------------------------------------
        # DISPLAY DECK WRAPPER
        # ----------------------------------------------------
        self.deck_container = ctk.CTkFrame(self, fg_color="transparent")
        self.deck_container.pack(side="right", fill="both", expand=True, padx=25, pady=25)
        
        # Initialize View Frames
        self.view_dash = ctk.CTkFrame(self.deck_container, fg_color="transparent")
        self.view_mods = ctk.CTkFrame(self.deck_container, fg_color="transparent")
        self.view_packs = ctk.CTkFrame(self.deck_container, fg_color="transparent")
        self.view_settings = ctk.CTkScrollableFrame(self.deck_container, fg_color="transparent")
        
        # Render layouts into views
        self.render_dashboard_view()
        self.render_mods_view()
        self.render_resourcepacks_view()
        self.render_settings_view()
        
        # Default view launch
        self.switch_view("dash")

    def create_nav_btn(self, label, cmd):
        btn = ctk.CTkButton(self.sidebar, text=label, font=("Segoe UI", 13, "bold"), height=45, fg_color="transparent", hover_color="#222530", anchor="w", corner_radius=6, command=cmd)
        btn.pack(fill="x", padx=12, pady=4)
        return btn

    def switch_view(self, target):
        # Reset button styling highlights
        for b in [self.btn_nav_dash, self.btn_nav_mods, self.btn_nav_packs, self.btn_nav_settings]:
            b.configure(fg_color="transparent", text_color="white")
            
        # Hide all structures
        for f in [self.view_dash, self.view_mods, self.view_packs, self.view_settings]: f.pack_forget()
        
        # Show chosen deck structure & update navigation indicators
        if target == "dash":
            self.view_dash.pack(fill="both", expand=True)
            self.btn_nav_dash.configure(fg_color="#1e293b", text_color=CLR_ACCENT)
        elif target == "mods":
            self.view_mods.pack(fill="both", expand=True)
            self.btn_nav_mods.configure(fg_color="#1e293b", text_color=CLR_ACCENT)
        elif target == "packs":
            self.view_packs.pack(fill="both", expand=True)
            self.btn_nav_packs.configure(fg_color="#1e293b", text_color=CLR_ACCENT)
        elif target == "settings":
            self.view_settings.pack(fill="both", expand=True)
            self.btn_nav_settings.configure(fg_color="#1e293b", text_color=CLR_ACCENT)

    # ----------------------------------------------------
    # RENDER VIEWS
    # ----------------------------------------------------
    def render_dashboard_view(self):
        # Header Banner Card
        banner = ctk.CTkFrame(self.view_dash, fg_color=CLR_PANEL, height=130, corner_radius=12, border_color="#222530", border_width=1)
        banner.pack(fill="x", pady=(0, 20))
        banner.pack_propagate(False)
        
        ctk.CTkLabel(banner, text="Ready for the Game?", font=("Segoe UI", 24, "bold"), text_color="white").pack(anchor="w", padx=25, pady=(35, 2))
        ctk.CTkLabel(banner, text="Configure your profile targets or drop into your active networks below.", font=("Segoe UI", 12), text_color="gray").pack(anchor="w", padx=25)
        
        # Quick Configuration Section Matrix (Center Grid Layout Frame)
        grid_frame = ctk.CTkFrame(self.view_dash, fg_color="transparent")
        grid_frame.pack(fill="x", pady=5)
        
        # Left Options Card Box
        cfg_box = ctk.CTkFrame(grid_frame, fg_color=CLR_PANEL, corner_radius=12, border_color="#222530", border_width=1)
        cfg_box.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)
        
        ctk.CTkLabel(cfg_box, text="Deployment Config", font=("Segoe UI", 14, "bold"), text_color=CLR_ACCENT).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Combo Row 1: Target Engine Profile Mapping
        r1 = ctk.CTkFrame(cfg_box, fg_color="transparent")
        r1.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(r1, text="Play Version:", font=("Segoe UI", 12, "bold")).pack(side="left")
        self.version_var = ctk.StringVar(value=self.config.get("version", "latest-release"))
        self.version_menu = ctk.CTkOptionMenu(r1, values=self.get_available_versions(), variable=self.version_var, fg_color=CLR_BG_DARK, button_color=CLR_BG_DARK, dropdown_fg_color=CLR_PANEL)
        self.version_menu.pack(side="right", fill="x", expand=True, padx=(15, 0))
        
        # Combo Row 2: Memory Optimization Allocation Settings
        r2 = ctk.CTkFrame(cfg_box, fg_color="transparent")
        r2.pack(fill="x", padx=20, pady=6)
        ctk.CTkLabel(r2, text="RAM Allocation:", font=("Segoe UI", 12, "bold")).pack(side="left")
        self.ram_var = ctk.StringVar(value=str(self.config.get("ram", 3)))
        ram_menu = ctk.CTkOptionMenu(r2, values=["1", "2", "3", "4", "6", "8", "12", "16"], variable=self.ram_var, width=100, fg_color=CLR_BG_DARK, button_color=CLR_BG_DARK, dropdown_fg_color=CLR_PANEL)
        ram_menu.pack(side="right")
        
        # Right Options Card Box (Direct Connect Server targets)
        srv_box = ctk.CTkFrame(grid_frame, fg_color=CLR_PANEL, corner_radius=12, border_color="#222530", border_width=1)
        srv_box.pack(side="right", fill="both", expand=True, padx=(10, 0), pady=5)
        
        ctk.CTkLabel(srv_box, text="Multiplayer Pass", font=("Segoe UI", 14, "bold"), text_color=CLR_ACCENT).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Server IP Row Layout Box Entry
        ctk.CTkLabel(srv_box, text="Direct Connection IP (Optional):", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20)
        self.server_entry = ctk.CTkEntry(srv_box, placeholder_text="e.g., play.hypixel.net", fg_color=CLR_BG_DARK, border_color="#2c2f3b")
        self.server_entry.insert(0, self.config.get("server_ip", ""))
        self.server_entry.pack(fill="x", padx=20, pady=(5, 15))
        
        # System Console Output Log Monitor Deck
        console_frame = ctk.CTkFrame(self.view_dash, fg_color=CLR_PANEL, corner_radius=12, border_color="#222530", border_width=1)
        console_frame.pack(fill="both", expand=True, pady=(15, 20))
        
        ctk.CTkLabel(console_frame, text="ACTIVITY LOG SYSTEM", font=("Segoe UI", 11, "bold"), text_color="gray").pack(anchor="w", padx=20, pady=(10, 2))
        self.status_text = ctk.CTkTextbox(console_frame, fg_color=CLR_BG_DARK, border_width=0, font=("Courier", 11))
        self.status_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.status_text.configure(state="disabled")
        self.update_status("Core Engine ready. Design overhaul layers loaded successfully.")
        
        # Massive Floating Bottom Core Control Platform
        actions_bar = ctk.CTkFrame(self.view_dash, fg_color="transparent")
        actions_bar.pack(fill="x", side="bottom")
        
        self.launch_btn = ctk.CTkButton(actions_bar, text="🚀  LAUNCH GAME", font=("Segoe UI", 16, "bold"), height=55, fg_color=CLR_LAUNCH, hover_color=CLR_LAUNCH_HOVER, corner_radius=10, command=self.launch_game)
        self.launch_btn.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.stop_btn = ctk.CTkButton(actions_bar, text="⏹️", font=("Segoe UI", 16), width=55, height=55, fg_color="#A32A2A", hover_color="#7A1F1F", corner_radius=10, command=self.stop_game)
        self.stop_btn.pack(side="right")

    def render_mods_view(self):
        ctk.CTkLabel(self.view_mods, text="LOCAL MOD ENGINE STORAGE", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 5))
        
        tgl_fr = ctk.CTkFrame(self.view_mods, fg_color=CLR_PANEL, height=50, corner_radius=8)
        tgl_fr.pack(fill="x", pady=5)
        tgl_fr.pack_propagate(False)
        self.mods_enabled_var = ctk.BooleanVar(value=self.config.get("mods_enabled", True))
        ctk.CTkSwitch(tgl_fr, text="Enable Local Mods Subdirectory Core Mounting Engine", variable=self.mods_enabled_var, command=self.save_config, progress_color=CLR_ACCENT).pack(side="left", padx=15, pady=10)
        
        wrapper = ctk.CTkFrame(self.view_mods, fg_color=CLR_PANEL, corner_radius=10)
        wrapper.pack(fill="both", expand=True, pady=10)
        
        self.mods_listbox = tk.Listbox(wrapper, bg=CLR_BG_DARK, fg="white", bd=0, highlightthickness=0, font=("Segoe UI", 11), selectbackground="#1e293b", selectforeground=CLR_ACCENT)
        self.mods_listbox.pack(fill="both", expand=True, padx=15, pady=15)
        
        btns = ctk.CTkFrame(self.view_mods, fg_color="transparent")
        btns.pack(fill="x")
        ctk.CTkButton(btns, text="➕ Import Mod (.jar)", fg_color="#1e293b", hover_color="#2c3e50", command=self.add_mod).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btns, text="❌ Purge Selection", fg_color="#3a1e1e", hover_color="#542b2b", text_color="#ff6b6b", command=self.remove_mod).pack(side="left")
        self.refresh_mods_list()

    def render_resourcepacks_view(self):
        ctk.CTkLabel(self.view_packs, text="RESOURCE PACK INTERFACE STORAGE", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 5))
        
        tgl_fr = ctk.CTkFrame(self.view_packs, fg_color=CLR_PANEL, height=50, corner_radius=8)
        tgl_fr.pack(fill="x", pady=5)
        tgl_fr.pack_propagate(False)
        self.resourcepacks_enabled_var = ctk.BooleanVar(value=self.config.get("resource_packs_enabled", True))
        ctk.CTkSwitch(tgl_fr, text="Enable Pack Directory Overlays Paths Engine System", variable=self.resourcepacks_enabled_var, command=self.save_config, progress_color=CLR_ACCENT).pack(side="left", padx=15, pady=10)
        
        wrapper = ctk.CTkFrame(self.view_packs, fg_color=CLR_PANEL, corner_radius=10)
        wrapper.pack(fill="both", expand=True, pady=10)
        
        self.resourcepacks_listbox = tk.Listbox(wrapper, bg=CLR_BG_DARK, fg="white", bd=0, highlightthickness=0, font=("Segoe UI", 11), selectbackground="#1e293b", selectforeground=CLR_ACCENT)
        self.resourcepacks_listbox.pack(fill="both", expand=True, padx=15, pady=15)
        
        btns = ctk.CTkFrame(self.view_packs, fg_color="transparent")
        btns.pack(fill="x")
        ctk.CTkButton(btns, text="➕ Import Pack (.zip)", fg_color="#1e293b", hover_color="#2c3e50", command=self.add_resourcepack).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btns, text="❌ Purge Selection", fg_color="#3a1e1e", hover_color="#542b2b", text_color="#ff6b6b", command=self.remove_resourcepack).pack(side="left")
        self.refresh_resourcepacks_list()

    def render_settings_view(self):
        # SECTION 1: DOWNLOAD ENGINE SYSTEM MANAGER
        ctk.CTkLabel(self.view_settings, text="📥 CORE CLIENT AUTOMATION ENGINE", font=("Segoe UI", 14, "bold"), text_color=CLR_ACCENT).pack(anchor="w", pady=(10, 5))
        f1 = ctk.CTkFrame(self.view_settings, fg_color=CLR_PANEL, corner_radius=10)
        f1.pack(fill="x", pady=5, padx=2)
        
        ctk.CTkLabel(f1, text="Platform Engine Framework Target Type:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(15, 2))
        self.loader_type_var = ctk.StringVar(value="Fabric")
        ctk.CTkOptionMenu(f1, values=["Fabric", "Forge", "Vanilla Core"], variable=self.loader_type_var, fg_color=CLR_BG_DARK, button_color=CLR_BG_DARK).pack(fill="x", padx=20, pady=5)
        
        ctk.CTkLabel(f1, text="Specific Platform Version Tag Profile:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(5, 2))
        self.loader_version_entry = ctk.CTkEntry(f1, placeholder_text="e.g., 1.20.1", fg_color=CLR_BG_DARK, border_color="#222530")
        self.loader_version_entry.insert(0, "1.20.1")
        self.loader_version_entry.pack(fill="x", padx=20, pady=5)
        
        self.install_loader_btn = ctk.CTkButton(f1, text="⚡ INITIALIZE ASSETS ACQUISITION SEQUENCE", font=("Segoe UI", 12, "bold"), fg_color=CLR_ACCENT, hover_color="#00828a", command=self.start_loader_installation)
        self.install_loader_btn.pack(fill="x", padx=20, pady=(15, 20))
        
        # SECTION 2: PATH ENVIRONMENT MAPPING
        ctk.CTkLabel(self.view_settings, text="📁 ADVANCED PATH DIRECTORY EXECUTION SETTINGS", font=("Segoe UI", 14, "bold"), text_color=CLR_ACCENT).pack(anchor="w", pady=(20, 5))
        f2 = ctk.CTkFrame(self.view_settings, fg_color=CLR_PANEL, corner_radius=10)
        f2.pack(fill="x", pady=5, padx=2)
        
        ctk.CTkLabel(f2, text="Java Runtime Binary Executable Path Redirect Target:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(15, 2))
        r_java = ctk.CTkFrame(f2, fg_color="transparent")
        r_java.pack(fill="x", padx=20, pady=(0, 10))
        self.java_path_entry = ctk.CTkEntry(r_java, fg_color=CLR_BG_DARK, border_color="#222530")
        self.java_path_entry.insert(0, self.config.get("java_path", "java"))
        self.java_path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(r_java, text="🔍 Auto Scan Engine Environments", fg_color="#1e293b", command=self.open_java_selector_window).pack(side="right")
        
        ctk.CTkLabel(f2, text="Custom Command Line JVM Arguments Data Token Block Strings:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(5, 2))
        self.args_entry = ctk.CTkEntry(f2, placeholder_text="Arguments string...", fg_color=CLR_BG_DARK, border_color="#222530")
        self.args_entry.insert(0, self.config.get("program_arguments", ""))
        self.args_entry.pack(fill="x", padx=20, pady=(0, 20))
        
        # UTILITIES FOOTER HUB PANEL
        f3 = ctk.CTkFrame(self.view_settings, fg_color=CLR_PANEL, corner_radius=10)
        f3.pack(fill="x", pady=15, padx=2)
        ctk.CTkButton(f3, text="📂 Open Operating Directory Target Base", fg_color="#1e293b", command=lambda: self.open_folder(self.minecraft_dir)).pack(side="left", padx=15, pady=15)
        ctk.CTkButton(f3, text="🔄 Factory Clear Config Master Storage", fg_color="#A32A2A", hover_color="#7A1F1F", command=self.reset_config).pack(side="right", padx=15, pady=15)

    # ----------------------------------------------------
    # CORE ENGINE UTILITIES & POPUPS
    # ----------------------------------------------------
    def open_java_selector_window(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Select Java Environment Engine")
        popup.geometry("650x450")
        popup.resizable(False, False)
        popup.configure(fg_color=CLR_BG_DARK)
        
        ctk.CTkLabel(popup, text="Detected Local Java Runtimes", font=("Segoe UI", 14, "bold"), text_color=CLR_ACCENT).pack(pady=15)
        list_frame = ctk.CTkFrame(popup, fg_color=CLR_PANEL, corner_radius=10)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        java_listbox = tk.Listbox(list_frame, bg=CLR_BG_DARK, fg="white", bd=0, highlightthickness=0, font=("Courier", 10), selectbackground="#1e293b", selectforeground=CLR_ACCENT)
        scrollbar = ctk.CTkScrollbar(list_frame, command=java_listbox.yview)
        java_listbox.config(yscrollcommand=scrollbar.set)
        java_listbox.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        detected_paths = [("System Default Global Alias (java)", "java")]
        search_dirs = ["/usr/lib/jvm", "/usr/java"]
        for s in search_dirs:
            p_obj = Path(s)
            if p_obj.exists():
                for item in p_obj.rglob("bin/java"):
                    if item.is_file() and os.access(item, os.X_OK):
                        display_name = str(item).replace("/bin/java", "").split("/")[-1]
                        detected_paths.append((f"{display_name} ({item.name})", str(item)))
        
        for idx, (name, path) in enumerate(detected_paths):
            java_listbox.insert(tk.END, f"[{idx + 1}] {name} -> Path: {path}")
            
        def confirm_selection():
            selection = java_listbox.curselection()
            if selection:
                chosen_idx = selection[0]
                _, selected_path = detected_paths[chosen_idx]
                self.java_path_entry.delete(0, tk.END)
                self.java_path_entry.insert(0, selected_path)
                self.update_status(f"✓ Java target path redirected: {selected_path}")
                popup.destroy()

        java_listbox.bind("<Double-Button-1>", lambda event: confirm_selection())
        
        act = ctk.CTkFrame(popup, fg_color="transparent")
        act.pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(act, text="✅ Link Chosen Runtime Environment", fg_color=CLR_LAUNCH, hover_color=CLR_LAUNCH_HOVER, command=confirm_selection).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(act, text="❌ Abort Context Selection", fg_color="#1e293b", command=popup.destroy).pack(side="right")

        # Repaint / stability configuration mechanics for Linux desktop ecosystems
        popup.update()
        popup.transient(self)
        popup.grab_set()

    def start_loader_installation(self):
        target_mc_version = self.loader_version_entry.get().strip()
        engine_choice = self.loader_type_var.get()
        if not target_mc_version: return
        self.install_loader_btn.configure(state="disabled", text="📥 SYNCHRONIZING ENGINE DEPENDENCIES...")
        installer_thread = threading.Thread(target=self._install_loader_worker, args=(engine_choice, target_mc_version))
        installer_thread.daemon = True
        installer_thread.start()

    def _install_loader_worker(self, engine, mc_version):
        try:
            self.update_status(f"📦 Downloading official Minecraft base assets for version {mc_version}...")
            install_minecraft_version(mc_version, str(self.minecraft_dir))
            if engine == "Fabric":
                self.update_status("⚡ Injecting Fabric Loader abstraction layer assets...")
                minecraft_launcher_lib.fabric.install_fabric(mc_version, str(self.minecraft_dir))
            elif engine == "Forge":
                self.update_status("⚡ Resolving Forge core asset mapping profiles...")
                forge_ver = minecraft_launcher_lib.forge.find_forge_version(mc_version)
                minecraft_launcher_lib.forge.install_forge_version(forge_ver, str(self.minecraft_dir))
            self.refresh_versions()
            messagebox.showinfo("Success", f"Framework deployment completed for {engine} {mc_version}!")
        except Exception as e:
            self.update_status(f"❌ Automation Failure Exception: {str(e)}")
        finally:
            self.install_loader_btn.configure(state="normal", text="⚡ INITIALIZE ASSETS ACQUISITION SEQUENCE")

    def get_available_versions(self):
        versions = []
        if self.versions_dir.exists():
            for d in self.versions_dir.iterdir():
                if d.is_dir(): versions.append(d.name)
        versions.extend(["latest-release", "latest-snapshot"])
        return sorted(list(set(versions)), reverse=True)
    
    def refresh_versions(self): self.version_menu.configure(values=self.get_available_versions())
    def refresh_mods_list(self):
        self.mods_listbox.delete(0, tk.END)
        for m in sorted(self.mods_dir.glob("*.jar")): self.mods_listbox.insert(tk.END, m.name)
    def refresh_resourcepacks_list(self):
        self.resourcepacks_listbox.delete(0, tk.END)
        for r in sorted(self.resourcepacks_dir.glob("*.zip")): self.resourcepacks_listbox.insert(tk.END, r.name)
    def add_mod(self):
        f = filedialog.askopenfilename(filetypes=[("JAR files", "*.jar")])
        if f: shutil.copy2(f, self.mods_dir / Path(f).name); self.refresh_mods_list()
    def remove_mod(self):
        s = self.mods_listbox.curselection()
        if s: (self.mods_dir / self.mods_listbox.get(s[0])).unlink(); self.refresh_mods_list()
    def add_resourcepack(self):
        f = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
        if f: shutil.copy2(f, self.resourcepacks_dir / Path(f).name); self.refresh_resourcepacks_list()
    def remove_resourcepack(self):
        s = self.resourcepacks_listbox.curselection()
        if s: (self.resourcepacks_dir / self.resourcepacks_listbox.get(s[0])).unlink(); self.refresh_resourcepacks_list()
    def open_folder(self, path):
        Path(path).mkdir(parents=True, exist_ok=True)
        subprocess.Popen(['xdg-open' if os.name == 'posix' else 'open', str(path)])
    def on_account_type_change(self, value): self.config["account_type"] = value; self.save_config()
    
    def update_status(self, message):
        self.status_text.configure(state="normal")
        self.status_text.insert("end", f"\n{message}")
        self.status_text.see("end")
        self.status_text.configure(state="disabled")
    
    def launch_game(self):
        self.config["version"] = self.version_var.get()
        self.config["ram"] = int(self.ram_var.get())
        self.config["java_path"] = self.java_path_entry.get().strip() or "java"
        self.config["program_arguments"] = self.args_entry.get().strip()
        self.config["mods_enabled"] = self.mods_enabled_var.get()
        self.config["resource_packs_enabled"] = self.resourcepacks_enabled_var.get()
        s_input = self.server_entry.get().strip()
        self.config["server_ip"] = s_input
        self.save_config()
        
        self.launch_btn.configure(state="disabled", text="🚀 GAME PIPELINE RUNNING IN BACKGROUND...")
        t = threading.Thread(target=self._launch_game_thread)
        t.daemon = True
        t.start()
    
    def _launch_game_thread(self):
        try:
            username = self.active_session_user
            version = self.config["version"]
            ram_gb = self.config["ram"]
            java_path = self.config["java_path"]
            args_input = self.config["program_arguments"]
            
            self.update_status(f"🔄 Spawning execution threads as local user: {username}")
            
            options = {"username": username, "uuid": "", "token": "0", "executablePath": java_path}
            if int(ram_gb) == 1: options["jvmArguments"] = ["-Xmx1G"]
            else: options["jvmArguments"] = [f"-Xmx{ram_gb}G", f"-Xms{ram_gb}G"]
                
            options["custom_args"] = ["--gameDir", str(self.minecraft_dir)]
            if args_input: options["custom_args"].extend(args_input.split())
            
            srv_args = []
            if self.config.get("server_ip"):
                parts = self.config["server_ip"].split(":")
                srv_args = ["--server", parts[0]]
                if len(parts) > 1: srv_args.extend(["--port", parts[1]])
            
            command = get_minecraft_command(version, str(self.minecraft_dir), options)
            if srv_args: command.extend(srv_args)
            
            self.after(0, self.withdraw)
            self.game_process = subprocess.Popen(command)
            self.game_process.wait()
            self.game_process = None
            self.after(0, self.deiconify)
        except Exception as e:
            self.after(0, self.deiconify)
            messagebox.showerror("Execution Framework Failure", str(e))
        finally:
            self.launch_btn.configure(state="normal", text="🚀  LAUNCH GAME")
    
    def stop_game(self):
        if self.game_process and self.game_process.poll() is None:
            self.game_process.terminate()
            self.deiconify()
            
    def force_close_launcher(self):
        if self.game_process and self.game_process.poll() is None: self.game_process.terminate()
        self.destroy()
        os._exit(0)
    
    def reset_config(self):
        if messagebox.askyesno("Confirm Master Reset", "Wipe all launcher dashboard configuration logs?"):
            self.set_default_config()
            self.ram_var.set("3")
            self.java_path_entry.delete(0, tk.END); self.java_path_entry.insert(0, "java")
            self.args_entry.delete(0, tk.END)

def main():
    app = MinecraftLauncher()
    app.mainloop()

if __name__ == "__main__":
    main()