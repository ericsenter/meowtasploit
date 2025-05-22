#!/usr/bin/env python3
# ppp_theme_manager.py

"""
Manages themes for PurrfectPurpleProcessor (PPP), providing functions
to load, apply, and switch between different color and icon schemes.
This module is intended to be integrated with the main PPP application.
"""

import os
import json
import sys # For sys.platform and potentially sys.stdout.write for background colors

# --- ANSI Color Codes (Essential Base Definitions) ---
# These are the primary, raw ANSI codes.
# Themes will map logical roles to these or more specific 256-color/RGB codes.
BLACK = '\033[30m'
RED = '\033[31m' # Often used for errors
BRIGHT_RED = '\033[91m' # More intense red
GREEN = '\033[32m' # Often used for success
BRIGHT_GREEN = '\033[92m'
YELLOW = '\033[33m' # Often used for warnings
BRIGHT_YELLOW = '\033[93m'
BLUE = '\033[34m' # Often used for info
BRIGHT_BLUE = '\033[94m'
MAGENTA = '\033[35m'
BRIGHT_MAGENTA = '\033[95m'
CYAN = '\033[36m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[37m' # Standard white
BRIGHT_WHITE = '\033[97m' # Brighter white

# Special 256-color examples (use if terminal supports)
ORANGE_256 = '\033[38;5;208m'
PURPLE_256 = '\033[38;5;141m'
PINK_256 = '\033[38;5;213m'
DARK_GREY_BG_256 = '\033[48;5;235m' # Background
LIGHT_GREY_FG_256 = '\033[38;5;250m' # Foreground

# Formatting
ENDC = '\033[0m'      # Resets all attributes
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
ITALIC = '\033[3m'    # Not universally supported but good to have
DIM = '\033[2m'       # Fainter text
REVERSE = '\033[7m'   # Swaps foreground and background

# --- Default Fallback Values ---
DEFAULT_COLOR_FALLBACK = WHITE # Fallback if a color_key is missing in a theme
DEFAULT_ICON_FALLBACK = "❖"   # Generic fallback icon
DEFAULT_PROJECT_PREFS_FILENAME = "ppp_prefs.json" # Name of the preferences file

# --- User Configuration Directory ---
def get_user_config_dir():
    """Gets the user-specific config directory for the application."""
    app_name = "purrfect_processor" # Or your specific app name like "meowtasploit"
    if sys.platform == "win32":
        return os.path.join(os.environ.get("APPDATA", ""), app_name)
    elif sys.platform == "darwin": # macOS
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", app_name)
    else: # Linux and other XDG-compliant systems
        xdg_config_home = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config"))
        return os.path.join(xdg_config_home, app_name)

DEFAULT_PROJECT_PREFS_PATH = os.path.join(get_user_config_dir(), DEFAULT_PROJECT_PREFS_FILENAME)

# --- OFFICIAL THEME KEYS DOCUMENTATION ---
# (Derived from conceptual code and existing PPP script needs)
#
# **Color Keys (for `colors` dictionary in themes):**
#   - "background": (str) ANSI code for full terminal background (use "terminal_default" for none).
#   - "text_primary": (str) Default text color.
#   - "text_secondary": (str) Secondary text color, for less emphasis.
#   - "prompt_main_text": (str) Color for the main part of the prompt (e.g., "Purrfect").
#   - "prompt_project_text": (str) Color for the project name in the prompt.
#   - "prompt_symbol": (str) Color for the prompt symbol (e.g., ">").
#   - "header": (str) Color for major section headers (e.g., help menu title).
#   - "subheader": (str) Color for subsection headers or column titles (e.g., in 'list_todos').
#   - "success": (str) Color for success messages (e.g., GREEN in current PPP).
#   - "error": (str) Color for error messages (e.g., RED in current PPP).
#   - "warning": (str) Color for warning messages (e.g., YELLOW in current PPP).
#   - "info": (str) Color for informational messages (e.g., BLUE or CYAN in current PPP).
#   - "debug": (str) Color for debug messages.
#   - "accent1": (str) Primary accent color (e.g., for IDs, important highlights like Magenta in current PPP).
#   - "accent2": (str) Secondary accent color (e.g., for labels, secondary highlights like Blue in current PPP).
#   - "critical": (str) Color for critical alerts/messages (often bold + a bright error color).
#
# **Icon Keys (for `icons` dictionary in themes):**
#   - "list_item_bullet": (str) Bullet point for list items.
#   - "status_pending": (str) Icon for "Pending" status.
#   - "status_done": (str) Icon for "Done" status.
#   - "status_error": (str) Icon for "Error/Failed" status.
#   - "status_inprogress": (str) Icon for "In Progress" status.
#   - "log_auto": (str) Prefix for automated log entries.
#   - "log_manual": (str) Prefix for manual log entries.
#   - "separator_major": (str) String for major visual separation.
#   - "separator_minor": (str) String for minor visual separation.
#   - "table_header_separator_char": (str) Character used to draw lines under table headers.
#   - "view_title_icon": (str) Icon used before detailed view titles.
#   - "help_intro_cat_icon": (str) Icon for the help menu intro (e.g., where CAT_ART_INPUT is used now).
#   - "prompt_critical_indicator": (str) Icon for critical state in prompt.
#   - "prompt_success_indicator": (str) Icon for success state in prompt.
#   - "prompt_default_indicator": (str) Default icon/symbol for the prompt (e.g., ">").
#   - "query_match_indicator": (str) Icon for a query match in search results.
#
# **Art Style Keys (for `art_style` dictionary in themes):**
#   - "banner_primary_color_key": (str) Theme color_key to use as primary for main banners.
#   - "banner_accent_color_key": (str) Theme color_key for accents in main banners.
#   - "generic_art_primary_color_key": (str) Default primary color for other ASCII art (e.g., success, error cats).
# --- END OFFICIAL THEME KEYS ---

# --- Theme Definitions ---
DEFAULT_THEME = {
    "name": "Purrfect Default",
    "description": "The classic PurrfectPurpleProcessor experience. Meow!",
    "colors": {
        "background": "terminal_default", # Special value, means don't change terminal background
        "text_primary": WHITE,
        "text_secondary": CYAN,
        "prompt_main_text": BOLD + CYAN,
        "prompt_project_text": BOLD + GREEN,
        "prompt_symbol": BOLD + CYAN, # For the ">" in prompt
        "header": BOLD + MAGENTA,    # For main titles like "PurrfectPurpleProcessor Help Menu:"
        "subheader": BOLD + BLUE,    # For sub-sections like "--- Project Management ---"
        "success": BRIGHT_GREEN,
        "error": BRIGHT_RED,
        "warning": BRIGHT_YELLOW,
        "info": BRIGHT_BLUE,
        "debug": DIM + MAGENTA,
        "accent1": BRIGHT_MAGENTA,   # For highlighting important things like IDs or user input prompts
        "accent2": BRIGHT_BLUE,      # For less important labels or secondary info
        "critical": BOLD + BRIGHT_RED,
    },
    "icons": {
        "list_item_bullet": f"{BRIGHT_CYAN}喵>{ENDC} ", # Cat paw or similar
        "status_pending": f"{BRIGHT_YELLOW}⏳{ENDC}",
        "status_done": f"{BRIGHT_GREEN}✔{ENDC}",
        "status_error": f"{BRIGHT_RED}✘{ENDC}",
        "status_inprogress": f"{BRIGHT_BLUE}⚙{ENDC}",
        "log_auto": f"{BLUE}[A]{ENDC}",
        "log_manual": f"{MAGENTA}[M]{ENDC}",
        "separator_major": f"{CYAN}{BOLD}---ฅ^•ﻌ•^ฅ---{ENDC}",
        "separator_minor": f"{BLUE}┈━┈━┈━┈━┈━┈{ENDC}",
        "table_header_separator_char": "─",
        "view_title_icon": f"{MAGENTA}🔎 {ENDC}",
        "help_intro_cat_icon": f"{BLUE}📖 {ENDC}", # Could also be a cat art key
        "prompt_critical_indicator": f"{BRIGHT_RED}⚡{ENDC}",
        "prompt_success_indicator": f"{BRIGHT_GREEN}🐾{ENDC}",
        "prompt_default_indicator": f"{CYAN}>{ENDC}",
        "query_match_indicator": f"{BRIGHT_YELLOW}🎯{ENDC}",
    },
    "art_style": {
        "banner_primary_color_key": "info", # Logical key from "colors" above
        "banner_accent_color_key": "accent1",
        "generic_art_primary_color_key": "text_secondary" # For general cat arts
    }
}

NIGHT_PROWLER_THEME = {
    "name": "Night Prowler",
    "description": "Stealthy and focused, for the nocturnal analyst.",
    "colors": {
        "background": "terminal_default",
        "text_primary": LIGHT_GREY_FG_256,
        "text_secondary": "\033[38;5;60m", # Darker Muted Blue/Grey
        "prompt_main_text": BOLD + "\033[38;5;75m",  # Muted Cyan
        "prompt_project_text": BOLD + "\033[38;5;105m", # Muted Purple
        "prompt_symbol": BOLD + "\033[38;5;75m",
        "header": BOLD + "\033[38;5;135m", # Muted Purple/Magenta
        "subheader": BOLD + "\033[38;5;67m", # Muted Dark Blue
        "success": "\033[38;5;71m",  # Muted Green
        "error": "\033[38;5;161m",    # Muted Red/Pink
        "warning": "\033[38;5;221m",  # Muted Yellow
        "info": "\033[38;5;75m",     # Muted Cyan (same as prompt_main)
        "debug": DIM + "\033[38;5;177m",   # Muted Magenta
        "accent1": "\033[38;5;111m",   # Brighter Muted Purple / Indigo
        "accent2": "\033[38;5;68m",    # Muted Darker Blue
        "critical": BOLD + "\033[38;5;203m", # Brighter Pink/Red
    },
    "icons": {
        "list_item_bullet": f"\033[38;5;39m潛行>{ENDC} ",
        "status_pending": f"\033[38;5;117m⏱{ENDC}",
        "status_done": f"\033[38;5;71m🎯{ENDC}",
        "status_error": f"\033[38;5;161m❗{ENDC}",
        "status_inprogress": f"\033[38;5;75m🛠{ENDC}",
        "log_auto": f"\033[38;5;75m[A]{ENDC}",
        "log_manual": f"\033[38;5;135m[M]{ENDC}",
        "separator_major": f"\033[38;5;60m{BOLD}---<<☾⋆>>---{ENDC}",
        "separator_minor": f"\033[38;5;67m·······{ENDC}",
        "table_header_separator_char": "·",
        "view_title_icon": f"\033[38;5;111m🌙 {ENDC}",
        "help_intro_cat_icon": f"\033[38;5;75m🦉 {ENDC}",
        "prompt_critical_indicator": f"\033[38;5;161m🔥{ENDC}",
        "prompt_success_indicator": f"\033[38;5;71m✨{ENDC}",
        "prompt_default_indicator": f"\033[38;5;75m❯{ENDC}",
        "query_match_indicator": f"\033[38;5;221m💡{ENDC}",
    },
    "art_style": {
        "banner_primary_color_key": "info",
        "banner_accent_color_key": "accent1",
        "generic_art_primary_color_key": "text_secondary"
    }
}

NYANSEC_THEME = {
    "name": "NyanSec Operations",
    "description": "Ride the rainbow of data! Pew pew pew!",
    "colors": {
        "background": "terminal_default",
        "text_primary": BRIGHT_WHITE,
        "text_secondary": PURPLE_256,
        "prompt_main_text": BOLD + PINK_256,
        "prompt_project_text": BOLD + BRIGHT_CYAN,
        "prompt_symbol": BOLD + BRIGHT_YELLOW,
        "header": BOLD + "\033[38;5;200m",   # Bright Pink/Fuchsia
        "subheader": BOLD + ORANGE_256,
        "success": BRIGHT_GREEN,
        "error": BRIGHT_RED,
        "warning": BRIGHT_YELLOW,
        "info": BRIGHT_BLUE,
        "debug": DIM + PURPLE_256,
        "accent1": PINK_256,
        "accent2": ORANGE_256,
        "critical": BOLD + BRIGHT_RED,
    },
    "icons": {
        "list_item_bullet": f"{PINK_256}★彡{ENDC} ",
        "status_pending": f"{BRIGHT_YELLOW}✨{ENDC}",
        "status_done": f"{BRIGHT_GREEN}🌈{ENDC}",
        "status_error": f"{BRIGHT_RED}💥{ENDC}",
        "status_inprogress": f"{BRIGHT_BLUE}🚀{ENDC}",
        "log_auto": f"{BRIGHT_BLUE}[N]{ENDC}",
        "log_manual": f"{PINK_256}[Y]{ENDC}",
        "separator_major": f"{BOLD}{ORANGE_256}-={BRIGHT_BLUE}≡{BRIGHT_YELLOW}★{BRIGHT_GREEN} {PINK_256}N{PURPLE_256}Y{BRIGHT_RED}A{ORANGE_256}N{BRIGHT_YELLOW} ★{BRIGHT_BLUE}≡{ORANGE_256}=-{ENDC}",
        "separator_minor": f"{BRIGHT_YELLOW}₊˚⊹♡⊹˚₊{ENDC}",
        "table_header_separator_char": "⋆",
        "view_title_icon": f"{PINK_256}🌠 {ENDC}",
        "help_intro_cat_icon": f"{BRIGHT_YELLOW}🌟 {ENDC}",
        "prompt_critical_indicator": f"{BRIGHT_RED}🚨{ENDC}",
        "prompt_success_indicator": f"{BRIGHT_GREEN}💖{ENDC}",
        "prompt_default_indicator": f"{BRIGHT_YELLOW}»{ENDC}",
        "query_match_indicator": f"{PINK_256}🎯{ENDC}",
    },
    "art_style": {
        "banner_primary_color_key": "accent1",
        "banner_accent_color_key": "info",
        "generic_art_primary_color_key": "text_secondary"
    }
}

AVAILABLE_THEMES = {
    "default": DEFAULT_THEME,
    "night_prowler": NIGHT_PROWLER_THEME,
    "nyansec": NYANSEC_THEME,
    # Add more themes here as they are created
}

CURRENT_THEME_SETTINGS = AVAILABLE_THEMES["default"].copy() # Default on load

# --- Internal Logging ---
# This should eventually call the main application's logging function.
_app_logger = None

def register_app_logger(logger_func):
    """Allows the main application to register its themed logger."""
    global _app_logger
    _app_logger = logger_func

def _log_theme_message(message, level="info"):
    """
    Internal themed logging for the theme manager itself.
    Uses the registered application logger if available, otherwise prints directly.
    Levels for app_logger could be: 'info', 'success', 'warning', 'error', 'debug'.
    """
    if _app_logger:
        # Assuming the app_logger can handle levels and map them to its own themed output.
        # The app_logger itself would use get_theme_color for its output.
        _app_logger(f"[ThemeManager] {message}", level=level, no_cat_prefix=True) # Example signature
    else:
        # Basic fallback if no app_logger is registered (e.g., during early init or standalone testing)
        log_colors = {
            "info": BLUE, "success": GREEN, "warning": YELLOW, "error": RED, "debug": MAGENTA
        }
        color = log_colors.get(level, WHITE)
        print(f"{color}[ThemeManager] {message}{ENDC}")


# --- Core Theme Functions ---
def initialize_themes(prefs_path: str = DEFAULT_PROJECT_PREFS_PATH):
    """
    Initializes themes at startup:
    1. Ensures the configuration directory exists.
    2. Loads user's theme preference from ppp_prefs.json if available.
    3. Falls back to the default theme if no preference is found or if loading fails.
    """
    global CURRENT_THEME_SETTINGS
    preferred_theme_name = "default" # Default to "default"

    try:
        config_dir = os.path.dirname(prefs_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
            _log_theme_message(f"Created preferences directory: {config_dir}", level='debug')

        if os.path.exists(prefs_path):
            with open(prefs_path, "r", encoding='utf-8') as f:
                prefs = json.load(f)
                preferred_theme_name = prefs.get("chosen_theme", "default")
            _log_theme_message(f"Loaded theme preference: '{preferred_theme_name}' from {prefs_path}", level='debug')
        else:
            _log_theme_message(f"Preferences file not found at {prefs_path}. Using default theme and creating file.", level='info')
            # Save the default theme choice to create the file
            load_theme_settings("default", prefs_path, is_initialization=True, save_preference=True)
            return # load_theme_settings already set CURRENT_THEME_SETTINGS

    except json.JSONDecodeError:
        _log_theme_message(f"Error decoding theme preferences from {prefs_path}. Using default.", level='warning')
        preferred_theme_name = "default" # Fallback
    except Exception as e:
        _log_theme_message(f"Could not load/create theme preferences at {prefs_path}: {e}. Using default.", level='warning')
        preferred_theme_name = "default" # Fallback

    # Load the determined theme (this also saves it if save_preference is True in load_theme_settings)
    load_theme_settings(preferred_theme_name, prefs_path, is_initialization=True, save_preference=False)


def load_theme_settings(theme_name: str = "default", prefs_path: str = DEFAULT_PROJECT_PREFS_PATH,
                        is_initialization: bool = False, save_preference: bool = True):
    """
    Loads the specified theme into CURRENT_THEME_SETTINGS.
    Optionally persists the choice to the preferences file.
    """
    global CURRENT_THEME_SETTINGS
    theme_name_lower = theme_name.lower()
    theme_to_load = AVAILABLE_THEMES.get(theme_name_lower)

    if theme_to_load:
        CURRENT_THEME_SETTINGS = theme_to_load.copy() # Use a copy to prevent accidental modification of originals
        if not is_initialization:
            _log_theme_message(f"Theme '{CURRENT_THEME_SETTINGS['name']}' loaded purr-fectly!", level='success')

        if save_preference:
            try:
                # Ensure directory exists (should be handled by initialize_themes, but good for direct calls)
                os.makedirs(os.path.dirname(prefs_path), exist_ok=True)
                with open(prefs_path, "w", encoding='utf-8') as f:
                    json.dump({"chosen_theme": theme_name_lower}, f, indent=2)
                if not is_initialization:
                    _log_theme_message(f"Theme preference '{theme_name_lower}' saved to {prefs_path}", level='debug')
            except Exception as e:
                if not is_initialization:
                    _log_theme_message(f"Could not save theme preference to {prefs_path}: {e}", level='warning')
    else:
        _log_theme_message(f"Theme '{theme_name}' not found. Using current theme: '{CURRENT_THEME_SETTINGS['name']}'.", level='warning')


def get_theme_color(color_key: str, default_fallback: str = None) -> str:
    """
    Gets a color ANSI string from the current theme's 'colors' dictionary.
    If a color_key refers to an 'art_style' key (e.g., "art_style.banner_primary_color_key"),
    it resolves it to the actual color key defined in art_style, then fetches that color.
    """
    if default_fallback is None:
        default_fallback = DEFAULT_COLOR_FALLBACK

    colors_dict = CURRENT_THEME_SETTINGS.get("colors", {})
    art_style_dict = CURRENT_THEME_SETTINGS.get("art_style", {})

    # Check if the key is an art_style indirection
    if color_key.startswith("art_style."):
        art_style_specific_key = color_key.split("art_style.")[1]
        # Get the actual color key (e.g., "info") from the art_style dictionary
        actual_color_key = art_style_dict.get(art_style_specific_key)
        if actual_color_key:
            return colors_dict.get(actual_color_key, default_fallback)
        else:
            # Fallback if the art_style key itself is not found
            return default_fallback
    else:
        return colors_dict.get(color_key, default_fallback)


def get_theme_icon(icon_key: str, default_fallback: str = None) -> str:
    """Gets an icon string from the current theme's 'icons' dictionary."""
    if default_fallback is None:
        default_fallback = DEFAULT_ICON_FALLBACK
    return CURRENT_THEME_SETTINGS.get("icons", {}).get(icon_key, default_fallback)


def apply_theme_to_string(text: str, color_key: str,
                          bold: bool = False, underline: bool = False,
                          italic: bool = False, dim: bool = False, reverse: bool = False) -> str:
    """
    Applies theme color and standard ANSI styles (bold, underline, etc.) to a string.
    Uses get_theme_color to resolve the color_key.
    """
    color_ansi = get_theme_color(color_key) # This will handle art_style indirection as well

    style_prefix = ""
    if bold: style_prefix += BOLD
    if underline: style_prefix += UNDERLINE
    if italic: style_prefix += ITALIC
    if dim: style_prefix += DIM
    if reverse: style_prefix += REVERSE

    # Avoid unnecessary wrapping if no specific style/color is applied beyond default text
    # This check might be too simplistic if default_fallback is changed or if color_ansi itself is just ""
    if not style_prefix and (color_ansi == DEFAULT_COLOR_FALLBACK or color_ansi == get_theme_color("text_primary")):
        # If only applying default text_primary with no styles, check if it's just WHITE or empty
        if color_ansi == WHITE or not color_ansi: # Basic check
             # Consider if we should always wrap with ENDC if any color is applied.
             # For now, if it's default color and no styles, return raw text.
             # This behavior might need refinement based on how text_primary is defined in themes.
             pass # Let it fall through to wrap with ENDC for consistency

    return f"{style_prefix}{color_ansi}{text}{ENDC}"


# --- CLI Command Handler Stubs ---
# These are intended to be called by the main application's command dispatcher.

def set_theme_command_handler(args):
    """Handles the 'set_theme <theme_name>' command."""
    if not args:
        # Use apply_theme_to_string for themed output even in handlers
        print(apply_theme_to_string("Usage: set_theme <theme_name>", 'warning', bold=True))
        list_themes_command_handler() # Call without args
        return

    theme_name_to_set = args[0]
    if theme_name_to_set.lower() in AVAILABLE_THEMES:
        load_theme_settings(theme_name_to_set) # This will also save the preference by default
        # Confirmation message will use the NEWLY set theme
        print(apply_theme_to_string(f"Fur-style changed to: {CURRENT_THEME_SETTINGS['name']}", 'success', bold=True))
    else:
        print(apply_theme_to_string(f"Theme '{theme_name_to_set}' is not a recognized fur-style.", 'error', bold=True))
        list_themes_command_handler()


def list_themes_command_handler(args=None): # args=None for consistent signature if called directly
    """Handles the 'list_themes' command."""
    print(apply_theme_to_string("Available Fur-styles (Themes):", 'header', bold=True))
    for name_key, theme_data in AVAILABLE_THEMES.items():
        description = theme_data.get('description', 'No purr-ticulars.')
        # Check against the name_key used in AVAILABLE_THEMES for active marker
        active_marker = get_theme_icon("prompt_success_indicator", "*") if CURRENT_THEME_SETTINGS['name'] == theme_data['name'] else " "

        themed_name = apply_theme_to_string(theme_data['name'], 'accent1', bold=True)
        themed_key = apply_theme_to_string(f"({name_key})", 'text_secondary', dim=True)
        themed_description = apply_theme_to_string(description, 'text_secondary')
        print(f"  {active_marker} {themed_name} {themed_key}: {themed_description}")


def current_theme_command_handler(args=None):
    """Handles the 'current_theme' command."""
    print(apply_theme_to_string(f"Current Fur-style: {CURRENT_THEME_SETTINGS['name']}", 'info', bold=True))
    print(apply_theme_to_string(f"  Description: {CURRENT_THEME_SETTINGS['description']}", 'text_secondary'))
    # For debugging, one might want to print the actual color map:
    # print(apply_theme_to_string("  Colors:", 'subheader'))
    # for k, v_ansi in CURRENT_THEME_SETTINGS.get('colors', {}).items():
    #     print(f"    {k}: {v_ansi}{k}_example{ENDC}")


if __name__ == "__main__":
    # Basic test sequence
    print(f"{BOLD}--- Theme Manager Test ---{ENDC}")

    # Simulate registering the main app's logger
    def test_app_logger(message, level="info", no_cat_prefix=False):
        # This test logger will use the theme manager's functions to style itself
        # In a real app, the main logger is already themed.
        prefix = "" if no_cat_prefix else "[AppSim] "
        color_map = {
            "info": "info", "success": "success", "warning": "warning",
            "error": "error", "debug": "debug"
        }
        log_color_key = color_map.get(level, "text_primary")
        print(apply_theme_to_string(f"{prefix}{message}", log_color_key))

    register_app_logger(test_app_logger)
    _log_theme_message("Test logger registered.", level="debug")

    initialize_themes() # Load default or saved theme

    print(f"\n{BOLD}Current Theme on Init:{ENDC}")
    current_theme_command_handler()

    print(f"\n{BOLD}Available Themes:{ENDC}")
    list_themes_command_handler()

    print(f"\n{BOLD}Testing apply_theme_to_string:{ENDC}")
    print(f"Default text: This is default text.")
    print(apply_theme_to_string("This is primary text.", "text_primary"))
    print(apply_theme_to_string("This is secondary text.", "text_secondary"))
    print(apply_theme_to_string("This is a success message!", "success", bold=True))
    print(apply_theme_to_string("This is an error message!", "error", bold=True))
    print(apply_theme_to_string("This is a warning message!", "warning"))
    print(apply_theme_to_string("This is an info message.", "info"))
    print(apply_theme_to_string("Accent1 text.", "accent1", bold=True, underline=True))
    print(apply_theme_to_string(f"Icon test: {get_theme_icon('list_item_bullet')}List item", "text_primary"))

    print(f"\n{BOLD}Testing Banner Color Keys (indirect resolution):{ENDC}")
    print(apply_theme_to_string("Banner Primary Color Test", "art_style.banner_primary_color_key"))
    print(apply_theme_to_string("Banner Accent Color Test", "art_style.banner_accent_color_key", bold=True))

    # Simulate setting a theme
    print(f"\n{BOLD}Attempting to set theme to 'night_prowler':{ENDC}")
    set_theme_command_handler(["night_prowler"]) # Pass args as a list

    print(f"\n{BOLD}Current Theme after 'night_prowler':{ENDC}")
    current_theme_command_handler()
    print(apply_theme_to_string("Night Prowler Success Test!", "success", bold=True))
    print(apply_theme_to_string("Night Prowler Error Test!", "error", bold=True))
    print(apply_theme_to_string("Banner Primary Color (Night Prowler)", "art_style.banner_primary_color_key"))


    print(f"\n{BOLD}Attempting to set theme to 'nyansec':{ENDC}")
    set_theme_command_handler(["nyansec"])

    print(f"\n{BOLD}Current Theme after 'nyansec':{ENDC}")
    current_theme_command_handler()
    print(apply_theme_to_string("NyanSec Success Test!", "success", bold=True))
    print(apply_theme_to_string("NyanSec Error Test!", "error", bold=True))
    print(apply_theme_to_string("NyanSec Header Test", "header", bold=True))
    print(apply_theme_to_string(f"{get_theme_icon('list_item_bullet')} NyanSec List Item", "text_primary"))
    print(apply_theme_to_string("Banner Primary Color (NyanSec)", "art_style.banner_primary_color_key"))


    print(f"\n{BOLD}Attempting to set theme to 'default':{ENDC}")
    set_theme_command_handler(["default"])
    print(f"\n{BOLD}Final theme check (Default):{ENDC}")
    current_theme_command_handler()

    print(f"\n{BOLD}--- Theme Manager Test Complete ---{ENDC}")
