#!/usr/bin/env python3
# ppp_catitude_engine.py

"""
Manages and delivers dynamic thematic content such as puns, tips,
and ASCII art (including startup banners) for PurrfectPurpleProcessor (PPP).
This module enhances the application's user experience and personality.
"""

import os
import json
import random

# --- Assumed Theme Manager Imports ---
# These functions are expected to be provided by ppp_theme_manager.py
# For standalone testing of this module, stubs would be needed if ppp_theme_manager is not available.
try:
    from ppp_theme_manager import get_theme_color, apply_theme_to_string, get_theme_icon
except ImportError:
    # Fallback stubs if ppp_theme_manager is not found (for isolated testing)
    # In a real environment, these should not be used.
    print("WARNING: ppp_catitude_engine - ppp_theme_manager.py not found. Using basic stubs for theming.")
    _FB_WHITE = '\033[97m'
    _FB_GREEN = '\033[92m'
    _FB_RED = '\033[91m'
    _FB_YELLOW = '\033[93m'
    _FB_BLUE = '\033[94m'
    _FB_MAGENTA = '\033[95m'
    _FB_CYAN = '\033[96m'
    _FB_ENDC = '\033[0m'
    _FB_BOLD = '\033[1m'

    def get_theme_color(color_key, default_fallback=_FB_WHITE):
        # Simplified stub
        _stub_colors = {
            "success": _FB_GREEN, "error": _FB_RED, "warning": _FB_YELLOW,
            "info": _FB_BLUE, "accent1": _FB_MAGENTA, "text_secondary": _FB_CYAN,
            "header": _FB_MAGENTA, "art_style.banner_primary_color_key": _FB_CYAN,
            "art_style.banner_accent_color_key": _FB_MAGENTA,
            "art_style.generic_art_primary_color_key": _FB_CYAN,
             "text_primary": _FB_WHITE, "prompt_main_text": _FB_CYAN
        }
        # Simplified resolution for art_style keys
        if color_key == "art_style.banner_primary_color_key": return _stub_colors.get("art_style.banner_primary_color_key", default_fallback)
        if color_key == "art_style.banner_accent_color_key": return _stub_colors.get("art_style.banner_accent_color_key", default_fallback)
        if color_key == "art_style.generic_art_primary_color_key": return _stub_colors.get("art_style.generic_art_primary_color_key", default_fallback)
        return _stub_colors.get(color_key, default_fallback)

    def apply_theme_to_string(text, color_key, bold=False, underline=False, italic=False, dim=False, reverse=False):
        color = get_theme_color(color_key)
        s = f"{_FB_BOLD if bold else ''}{color}{text}{_FB_ENDC}"
        return s

    def get_theme_icon(icon_key, default_fallback="❖"):
        # Simplified stub
        _stub_icons = {
            "TIP_CAT_DEF_ICON_PLACEHOLDER": "💡", # Placeholder if TIP_CAT_DEF art has an icon part
            "view_title_icon": "🔎 "
        }
        return _stub_icons.get(icon_key, default_fallback)

# --- Global Variables for Content ---
PUNS_DATA = {"general": ["Meow! Default Pun."]}
TIPS_DATA = [{"id": "tip_default", "category": "general", "text": "Stay curious, like a cat!"}]
APP_BASE_PATH_STORED = "." # Stores the application base path

# --- Internal Logging ---
_app_logger_catitude = None

def register_catitude_logger(logger_func):
    global _app_logger_catitude
    _app_logger_catitude = logger_func

def _catitude_log(message, level="info"):
    if _app_logger_catitude:
        _app_logger_catitude(f"[CatitudeEngine] {message}", level=level, no_cat_prefix=True)
    else:
        print(f"[{level.upper()}/CatitudeEngine] {message}")

# --- Content Management & Loading ---
def load_cat_attitude_content(app_base_path: str):
    """
    Loads puns and tips from JSON files located in 'app_base_path/data/'.
    Handles file errors gracefully.
    """
    global PUNS_DATA, TIPS_DATA, APP_BASE_PATH_STORED
    APP_BASE_PATH_STORED = app_base_path
    data_dir_path = os.path.join(app_base_path, "data")
    content_loaded_successfully = True

    # Load Puns
    puns_file_path = os.path.join(data_dir_path, "puns.json")
    try:
        with open(puns_file_path, 'r', encoding='utf-8') as f_puns:
            PUNS_DATA = json.load(f_puns)
        _catitude_log(f"Puns purr-fectly loaded from {puns_file_path}", level="debug")
    except FileNotFoundError:
        _catitude_log(f"Purr-don me, couldn't find 'puns.json' at {puns_file_path}. Using fallback meows.", level="warning")
        PUNS_DATA = {"general": ["Default: Puns file not found!"], "error": ["Error: Pun file missing."]}
        content_loaded_successfully = False
    except json.JSONDecodeError:
        _catitude_log(f"Oh dear, 'puns.json' seems to have a knot in it (JSON error). Using fallback.", level="error")
        PUNS_DATA = {"general": ["Default: Puns JSON error!"], "error": ["Error: Pun file corrupted."]}
        content_loaded_successfully = False

    # Load Tips
    tips_file_path = os.path.join(data_dir_path, "tips.json")
    try:
        with open(tips_file_path, 'r', encoding='utf-8') as f_tips:
            TIPS_DATA = json.load(f_tips)
        _catitude_log(f"Meow-Master's tips loaded from {tips_file_path}", level="debug")
    except FileNotFoundError:
        _catitude_log(f"Purr-don me, couldn't find 'tips.json' at {tips_file_path}. Using fallback wisdom.", level="warning")
        TIPS_DATA = [{"id": "tip_default_fnf", "category": "general", "text": "Default: Tip file not found!"}]
        content_loaded_successfully = False
    except json.JSONDecodeError:
        _catitude_log(f"Oh dear, 'tips.json' has a tangle (JSON error). Using fallback.", level="error")
        TIPS_DATA = [{"id": "tip_default_json", "category": "general", "text": "Default: Tip JSON error!"}]
        content_loaded_successfully = False

    if content_loaded_successfully:
        _catitude_log("Cat-itude Engine content successfully initialized!", level="info")
    else:
        _catitude_log("Cat-itude Engine initialized with some default content due to loading issues.", level="warning")

# --- ASCII Art Variants Definition & Management ---
# Each lambda, when called, returns a string of the ASCII art,
# dynamically themed by calling get_theme_color().

# Helper to simplify themed art creation within lambdas
def _create_themed_art(art_template: str, primary_color_key: str = "art_style.generic_art_primary_color_key", **kwargs) -> str:
    """Colors a simple ASCII art template with a primary theme color."""
    color = get_theme_color(primary_color_key)
    # Basic placeholder replacement, assumes art_template might have placeholders like {text}
    # More complex art might need dedicated placeholder logic.
    formatted_art = art_template
    if kwargs:
        try:
            formatted_art = art_template.format(**kwargs)
        except KeyError:
            _catitude_log(f"KeyError formatting art with {kwargs}. Template: {art_template[:50]}...", "debug")

    return f"{color}{formatted_art}{get_theme_color('endc', '')}" # Ensure ENDC is fetched if available

CAT_ART_LEGS_ORIGINAL = "( लेगा )" # As per user request for testing

CAT_ART_SUCCESS_VARS = [
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( ^.^ )          Success! That was purrfect!
    > ^ <
   {CAT_ART_LEGS_ORIGINAL}""", "success"),
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   (๑˃̵ᴗ˂̵)و         Pawsome! Task complete!
    > ω <
   {CAT_ART_LEGS_ORIGINAL}""", "success"),
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( ´ ∀ ` )         Purr-ecisely what we wanted!
    > ν <
   {CAT_ART_LEGS_ORIGINAL}""", "success")
]

CAT_ART_ERROR_VARS = [
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( >.< )          Oh no! A hiss-take occurred!
    > ^ <           Check the message above.
   {CAT_ART_LEGS_ORIGINAL}""", "error"),
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( T ^ T )         Claws out! Something's wrong!
    > X <
   {CAT_ART_LEGS_ORIGINAL}""", "error"),
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( ; ω ; )         A fur-midable error appeared!
    > ~ <
   {CAT_ART_LEGS_ORIGINAL}""", "error")
]

CAT_ART_THINKING_VARS = [
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( ?.?)           Hmm... let me think about that...
    > ^ <
   {CAT_ART_LEGS_ORIGINAL}""", "warning"),
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( ._. )           Purr-colating thoughts...
    > - <
   {CAT_ART_LEGS_ORIGINAL}""", "warning"),
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( ¬‿¬ )           Plotting my next pounce...
    > ω <
   {CAT_ART_LEGS_ORIGINAL}""", "warning")
]

CAT_ART_INPUT_VARS = [
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   ( ^_~ ) wink!    Waiting for your purr-ameters...
    > ^ <
   {CAT_ART_LEGS_ORIGINAL}""", "info"),
    lambda: _create_themed_art(
        f"""
    /\\_/\\
   (=ච ω ච=)       Ready for your command, Meow-ster!
    > . <
   {CAT_ART_LEGS_ORIGINAL}""", "info")
]

# Specific Art Lambdas
CAT_ART_TIP_CAT_DEF_LAMBDA = lambda: _create_themed_art(
    f"""
    /\\_/\\
   (o.-.o)          A whisker of wisdom from the Meow-Master:
    > § <
   {CAT_ART_LEGS_ORIGINAL}""", "info") # § could be themed icon if needed

# Static Fallback Art Lambdas (pointing to the first variant or a specific design)
CAT_ART_SUCCESS_STATIC_LAMBDA = CAT_ART_SUCCESS_VARS[0]
CAT_ART_ERROR_STATIC_LAMBDA = CAT_ART_ERROR_VARS[0]
CAT_ART_THINKING_STATIC_LAMBDA = CAT_ART_THINKING_VARS[0]
CAT_ART_INPUT_STATIC_LAMBDA = CAT_ART_INPUT_VARS[0]

# Generic Fallbacks Lambdas
DEFAULT_ART_POSITIVE_LAMBDA = CAT_ART_SUCCESS_STATIC_LAMBDA
DEFAULT_ART_NEGATIVE_LAMBDA = CAT_ART_ERROR_STATIC_LAMBDA
DEFAULT_ART_NEUTRAL_LAMBDA = lambda: _create_themed_art(
    f"""
    /\\_/\\
   ( . . )          Just a moment, purr-lease...
    > - <
   {CAT_ART_LEGS_ORIGINAL}""", "text_secondary")
DEFAULT_ART_QUESTION_LAMBDA = CAT_ART_THINKING_STATIC_LAMBDA

# --- Startup Banners Integration ---
# Adapted from user-provided 'ppp_banner_art.py'
# These lambdas expect a 'placeholders' dictionary.
# Fallback values from 'ppp_banner_art.py' are illustrative; real values should come from the app.
_banner_default_placeholders = {
    "version": "v0.1-alpha", "codename": "Calico Catalyst", "module_count": 0,
    "asset_count": 0, "finding_count": 0, "pun": "Ready to pounce!",
    "tool_name": "Meow-tasploit"
}

MEOWTASPLOIT_BANNER_LAMBDAS = [
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}    /\\_/\\  {apply_theme_to_string(f"Welcome to {(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')}!", 'header', bold=True)}
   ( o.o ) {apply_theme_to_string(f"Version: {(p or _banner_default_placeholders).get('version', 'N/A')} ({(p or _banner_default_placeholders).get('codename', 'N/A')})", 'info')}
    > ^ <  {apply_theme_to_string(f"\"{(p or _banner_default_placeholders).get('pun', 'Purrfectly ready!')}\"", 'prompt_main_text')}
   {CAT_ART_LEGS_ORIGINAL} {apply_theme_to_string(f"Modules: {(p or _banner_default_placeholders).get('module_count', 0)} | Assets: {(p or _banner_default_placeholders).get('asset_count', 0)} | Findings: {(p or _banner_default_placeholders).get('finding_count', 0)}", 'text_primary')}
{get_theme_color('endc', '')}""",
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}
{apply_theme_to_string('Digital Alleycat Mode', 'header', bold=True)}
      |\\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\\ (  `'-'
    '---''(_/--'  `-'\\_)   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
{apply_theme_to_string('Sniffing out vulnerabilities... one paw print at a time.', 'prompt_main_text')}
{apply_theme_to_string(f"Codename: {(p or _banner_default_placeholders).get('codename', 'N/A')} - {(p or _banner_default_placeholders).get('pun', 'Purrs Ahead!')}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # ... (Integrate all 20 banners here, ensuring they call get_theme_color/apply_theme_to_string
    # and use the 'p' placeholder dictionary correctly. For brevity, only showing the first two.)
    # Banner 3 (NyanSec)
    lambda p=None: f"""
{apply_theme_to_string('NyanSec Operations Engaged!', 'header', bold=True)}
{get_theme_color('art_style.banner_accent_color_key', '#PINK#')} _,.--.,_ _{get_theme_color('endc', '')}
{get_theme_color('art_style.banner_accent_color_key', '#PINK#')}(" |    `";{get_theme_color('endc', '')}     {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}..----.._
{get_theme_color('art_style.banner_accent_color_key', '#PINK#')} `-|    | ;{get_theme_color('endc', '')}   {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}_|       |\\_
{get_theme_color('art_style.banner_accent_color_key', '#PINK#')}   |    |{get_theme_color('endc', '')} {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')} ("\\  |      /") )
{get_theme_color('art_style.banner_accent_color_key', '#PINK#')}   |    |{get_theme_color('endc', '')} {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}   `-|      |-'
{get_theme_color('art_style.banner_accent_color_key', '#PINK#')}   ;----|{get_theme_color('endc', '')}     {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}  "-.  .--"
{get_theme_color('art_style.banner_accent_color_key', '#PINK#')}   `----'{get_theme_color('endc', '')}       {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')} `--"`
{apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')}: Riding the rainbow of data! {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
{apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Taste the data-bow!')} - Modules: {(p or _banner_default_placeholders).get('module_count', 0)}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 4 (Schrödinger)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#YELLOW#')}
  ??????-------?????-------??????
  |  {apply_theme_to_string('Schrödinger\'s Packet', 'header', bold=True)}  |
  |       /\\_/\\             |
  |      ( ?.?) {apply_theme_to_string('Observing...', 'warning')}  |  {apply_theme_to_string("Is the vuln there or not?", 'prompt_main_text')}
  |       > ^ <             |
  ??????-------?????-------??????
{apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')} - {(p or _banner_default_placeholders).get('pun', 'Maybe...')}", 'info')}
{get_theme_color('endc', '')}""",
    # Banner 5 (Furrwall)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}  .--""--.__        {apply_theme_to_string('Furrwall Guardian Protocol', 'header', bold=True)}
 /          \\\\      {apply_theme_to_string(f"Version: {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
|  {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}  (^==^){get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}  |      {apply_theme_to_string("Protecting the Meow-trix!", 'success')}
 \\\\  {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')} O''O {get_theme_color('art_style.banner_primary_color_key', '#GREEN#')} /       {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'None shall pass!')}", 'prompt_main_text')}
  '.____.'         {apply_theme_to_string(f"Assets Secured: {(p or _banner_default_placeholders).get('asset_count', 0)}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 6 (Keyboard Cat Cavalry)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#MAGENTA#')}   {apply_theme_to_string('Keyboard Cat Cavalry - Deploying the Kittens!', 'header', bold=True)}
  _________________      /\\_/\\
 ||               ||    ( >ω< )
 ||[][] Gateway [][]||     > ^ <
 ||_______________||    人____)し
 [ -= MEOW =- MEOW ]   (_(_(_)_(_(   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
{apply_theme_to_string(f"Orchestrating {(p or _banner_default_placeholders).get('module_count', 0)} tools for purr-fect pwnage! {(p or _banner_default_placeholders).get('pun', 'Charge!')}", 'prompt_main_text')}
{get_theme_color('endc', '')}""",
    # Banner 7 (Hacker Hoodie)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}
      _.---.._             {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} - In the Shadows", 'header', bold=True)}
     .'        '.
    /   O      O \\\\          {apply_theme_to_string(f"Version {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
   |    {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}(----){get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}   |        {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Incognito...')}", 'prompt_main_text')}
   \\\\   '.__.'   /
    '.______.'           {apply_theme_to_string(f"Findings to report: {(p or _banner_default_placeholders).get('finding_count', 0)}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 8 (Paw on Server)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}
  +-----------------+    {apply_theme_to_string('Server Access Purr-otocol', 'header', bold=True)}
  |   {get_theme_color('art_style.banner_accent_color_key', '#YELLOW#')}  /\\_/\\    {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}   |
  |  {get_theme_color('art_style.banner_accent_color_key', '#YELLOW#')} ( o.x )   {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}   | {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
  |   > ^ <     {get_theme_color('art_style.banner_accent_color_key', '#GREEN#')}[OK]{get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}  | {apply_theme_to_string('Leaving our mark... and the loot.', 'prompt_main_text')}
  |  {apply_theme_to_string(' (_(_(_)_)', 'accent1')}   | {apply_theme_to_string(f"Discovered {(p or _banner_default_placeholders).get('asset_count', 0)} assets.", 'text_primary')}
  +-----------------+    {apply_theme_to_string(f"Pun: {(p or _banner_default_placeholders).get('pun', 'Gotcha!')}", 'info')}
{get_theme_color('endc', '')}""",
    # Banner 9 (Matrix Cats)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}0101{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}(^._.^)ﾉ{get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}01010    {apply_theme_to_string('Entering the Meow-trix', 'header', bold=True)}
101{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}( >.< ){get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}1010101   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
01010{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}(ᓚᘏᗢ){get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}101001  {apply_theme_to_string('Follow the white rabbit... or the cat.', 'prompt_main_text')}
100{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}(=;ω;=){get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}010110  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Neo-w?')} :: Modules: {(p or _banner_default_placeholders).get('module_count', 0)}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 10 (Lockpick Cat)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}
      {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}  .--.
{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}     /.-. '----------.
{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}     \\\\'-' .--"--""-"`
{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}      '--'{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}  /\\_/\\   {apply_theme_to_string('The Purr-fessional Lockpicker', 'header', bold=True)}
             ( o.o )  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
              > ^ <   {apply_theme_to_string('No system is impurr-vious.', 'prompt_main_text')}
             {CAT_ART_LEGS_ORIGINAL} {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Click!')}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 11 (Cyber Cat Visor)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}   /\\_/\\
  {get_theme_color('art_style.banner_accent_color_key', '#RED#')}( {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}0{get_theme_color('art_style.banner_accent_color_key', '#RED#')}={get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}.{get_theme_color('art_style.banner_accent_color_key', '#RED#')}={get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}0 {get_theme_color('art_style.banner_accent_color_key', '#RED#')}){get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}    {apply_theme_to_string('Cybernetic Feline Operations', 'header', bold=True)}
  {get_theme_color('art_style.banner_accent_color_key', '#RED#')} (        ) {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}   {apply_theme_to_string(f"Enhancing {(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
   {apply_theme_to_string(' > ^ <', 'accent1')}      {apply_theme_to_string('Scanning with purr-cision.', 'prompt_main_text')}
   {apply_theme_to_string(f'{CAT_ART_LEGS_ORIGINAL}', 'accent1')}     {apply_theme_to_string(f"Codename: {(p or _banner_default_placeholders).get('codename', 'RoboCat')}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 12 (Cat Coding)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}
  > ( ( ({apply_theme_to_string('#!/bin/meow', 'warning')}) ) ) <      {apply_theme_to_string('Script Kitty Evolution', 'header', bold=True)}
 / \\\\ `|||`                  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
(   )oO {apply_theme_to_string('// Purrgramming...', 'text_primary')}
 \\\\ / \\_/                 {apply_theme_to_string(f"Crafting {(p or _banner_default_placeholders).get('module_count', 0)} new exploits.", 'prompt_main_text')}
  `   ~                    {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Code meows!')}", 'success')}
{get_theme_color('endc', '')}""",
    # Banner 13 (Data Stream Cat)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')} ~ ~ ~ ~ ~ ~ {apply_theme_to_string('Data Stream Purr-ocessor', 'header', bold=True)} ~ ~ ~ ~ ~ ~
{get_theme_color('art_style.banner_accent_color_key', '#CYAN#')}      <`)))>< <`)))>< <`)))><{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}
         /\\_/\\                {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
        ( o.O ) {apply_theme_to_string('Riding the waves of information.', 'prompt_main_text')}
         > ~ <                  {apply_theme_to_string(f"Findings: {(p or _banner_default_placeholders).get('finding_count', 0)}. {(p or _banner_default_placeholders).get('pun', 'Surf`s up!')}", 'text_primary')}
{get_theme_color('art_style.banner_accent_color_key', '#CYAN#')}  <`)))>< <`)))>< <`)))><{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}
{get_theme_color('endc', '')}""",
    # Banner 14 (Cat Detective)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#YELLOW#')}
      .--""--.
     /        \\\\_         {apply_theme_to_string('Meow-lock Holmes Investigates', 'header', bold=True)}
    |  O    O  {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}(_){get_theme_color('art_style.banner_primary_color_key', '#YELLOW#')}    {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
    \\\\  .--.  /          {apply_theme_to_string('The game is a-paw!', 'prompt_main_text')}
     '.____.'            {apply_theme_to_string(f"Uncovering {(p or _banner_default_placeholders).get('finding_count', 0)} clues. {(p or _banner_default_placeholders).get('pun', 'Elementary!')}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 15 (Circuit Cat)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}.--.      .--.     {apply_theme_to_string('Circuit Board Cat-alyst', 'header', bold=True)}
|  | {get_theme_color('art_style.banner_accent_color_key', '#GREEN#')}(^._.^){get_theme_color('art_style.banner_primary_color_key', '#CYAN#')} |  |   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
'--'{get_theme_color('art_style.banner_accent_color_key', '#YELLOW#')}|  |  |{get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}'--'   {apply_theme_to_string('Connecting the data nodes.', 'prompt_main_text')}
   {get_theme_color('art_style.banner_accent_color_key', '#YELLOW#')}'--''--'{get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}      {apply_theme_to_string(f"Modules online: {(p or _banner_default_placeholders).get('module_count', 0)}. {(p or _banner_default_placeholders).get('pun', 'Wired in!')}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 16 (Stealthy Paw Prints)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}
{apply_theme_to_string('Operation: Silent Paws', 'header', bold=True)}
  {apply_theme_to_string('🐾', 'accent1')}      {apply_theme_to_string('🐾', 'accent1')}         {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
      {apply_theme_to_string('🐾', 'accent1')}           {apply_theme_to_string('Leaving no trace, only results.', 'prompt_main_text')}
 {apply_theme_to_string('🐾', 'accent1')}         {apply_theme_to_string('🐾', 'accent1')}    {apply_theme_to_string(f"Assets targeted: {(p or _banner_default_placeholders).get('asset_count', 0)}. {(p or _banner_default_placeholders).get('pun', 'Shhh!')}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 17 (Cat Ghost)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#MAGENTA#')}
   .-""\"-.             {apply_theme_to_string('Phantom Prowler Protocol', 'header', bold=True)}
  /       \\\\
 |  {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}o   o{get_theme_color('art_style.banner_primary_color_key', '#MAGENTA#')}  |         {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')} - Codename: {(p or _banner_default_placeholders).get('codename', 'Spectre')}", 'info')}
 |   {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}\\\\   /{get_theme_color('art_style.banner_primary_color_key', '#MAGENTA#')}   |         {apply_theme_to_string('Evading detection, finding secrets.', 'prompt_main_text')}
  '. ___ .'            {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Boo!')}", 'text_primary')}
    `~~~`
{get_theme_color('endc', '')}""",
    # Banner 18 (Binary Code Cat Face)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}01{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}( ^ ){get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}10{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}( ^ ){get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}01   {apply_theme_to_string('Binary Purr-fection', 'header', bold=True)}
101{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}(  o  ){get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}101   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
0101{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}( --- ){get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}010   {apply_theme_to_string('Speaking the language of machines.', 'prompt_main_text')}
10101{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}{{ {get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}O{get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}}}{get_theme_color('art_style.banner_primary_color_key', '#GREEN#')}101  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', '0ne or Zer0?')} / {(p or _banner_default_placeholders).get('module_count', 0)} modules", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 19 (Cat with Network Cable)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}
  /\\_/\\  -----{get_theme_color('art_style.banner_accent_color_key', '#YELLOW#')}(){get_theme_color('art_style.banner_accent_color_key', '#YELLOW#')}(){get_theme_color('art_style.banner_accent_color_key', '#YELLOW#')}({get_theme_color('art_style.banner_primary_color_key', '#BLUE#')}---    {apply_theme_to_string('Network Sniffer Active', 'header', bold=True)}
 ( o x o ) {apply_theme_to_string('~', 'accent1')}              {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
  >  ^  <  {apply_theme_to_string('~', 'accent1')}              {apply_theme_to_string('Tangled in the web of data.', 'prompt_main_text')}
 {CAT_ART_LEGS_ORIGINAL} {apply_theme_to_string('~~~', 'accent1')}             {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Packet Inspector!')} | Assets: {(p or _banner_default_placeholders).get('asset_count', 0)}", 'text_primary')}
{get_theme_color('endc', '')}""",
    # Banner 20 (Minimalist Cat Head / Command Prompt)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}
  {apply_theme_to_string('Meow>', 'prompt_main_text', bold=True)} {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')} /\\_/\\ {get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}
  {apply_theme_to_string('Meow>', 'prompt_main_text', bold=True)} {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}(=•.•=){get_theme_color('art_style.banner_primary_color_key', '#CYAN#')}  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} Core {(p or _banner_default_placeholders).get('version', 'N/A')}", 'header')}
  {apply_theme_to_string('Meow>', 'prompt_main_text', bold=True)} {get_theme_color('art_style.banner_accent_color_key', '#WHITE#')}('')_(''){get_theme_color('art_style.banner_primary_color_key', '#CYAN#')} {apply_theme_to_string(f"Awaiting purr-mission... {(p or _banner_default_placeholders).get('pun', 'Ready!')}", 'info')}
                       {apply_theme_to_string(f"Type 'help' or 'meow_tips'. Modules: {(p or _banner_default_placeholders).get('module_count', 0)}", 'text_primary')}
{get_theme_color('endc', '')}"""
]


# --- Core Engine Logic Implementation ---
def get_random_pun(category: str = "general", **kwargs_for_pun_format) -> str:
    """Retrieves a random pun from the specified category, with optional formatting."""
    if not PUNS_DATA:
        _catitude_log("Puns data not loaded.", "warning")
        return "Meow? (Puns not loaded)"

    category_puns = PUNS_DATA.get(category)
    if not category_puns:  # Fallback to 'general' if category not found or empty
        _catitude_log(f"Pun category '{category}' not found, using 'general'.", "debug")
        category_puns = PUNS_DATA.get("general", ["No puns for this cat-egory!"])
    if not category_puns:  # Ultimate fallback
        return "Purr... (silence)"

    pun_template = random.choice(category_puns)
    try:
        return pun_template.format(**kwargs_for_pun_format) if kwargs_for_pun_format else pun_template
    except KeyError as e:
        _catitude_log(f"Pun formatting error: Missing key {e} for pun '{pun_template}'. Kwargs: {kwargs_for_pun_format}", "debug")
        return pun_template # Return raw pun

def get_random_tip(category_filter: str = None) -> dict:
    """Retrieves a random tip object, optionally filtered by category."""
    if not TIPS_DATA:
        _catitude_log("Tips data not loaded.", "warning")
        return {"id": "tip_fallback_empty", "category": "general", "text": "Stay paws-itive! (Tips not loaded)"}

    eligible_tips = TIPS_DATA
    if category_filter:
        normalized_filter = category_filter.lower()
        filtered = [tip for tip in TIPS_DATA if tip.get("category", "").lower() == normalized_filter]
        if filtered:
            eligible_tips = filtered
        else:
            _catitude_log(f"No tips found for category '{category_filter}', picking from all.", "debug")

    if not eligible_tips:
        return {"id": "tip_fallback_no_eligible", "category": "general", "text": "The Meow-Master is napping... no tips available!"}

    return random.choice(eligible_tips)

def get_random_art(art_key: str, **kwargs_for_art_format) -> str:
    """
    Retrieves a random themed ASCII art string.
    Selects from variant lists or falls back to static/generic art lambdas,
    then calls the lambda to get the themed string.
    kwargs_for_art_format can be used if the art lambda itself needs placeholder replacement.
    """
    art_key_upper = art_key.upper()
    # Try to find a list of variants first (e.g., CAT_ART_SUCCESS_VARS)
    variants_list_name = f"CAT_ART_{art_key_upper}_VARS"
    variants_list_lambdas = globals().get(variants_list_name)

    art_lambda_to_call = None

    if variants_list_lambdas and isinstance(variants_list_lambdas, list) and variants_list_lambdas:
        art_lambda_to_call = random.choice(variants_list_lambdas)
    else: # Fallback to a specific static lambda if variants list is not found/empty
        static_art_name = f"CAT_ART_{art_key_upper}_STATIC_LAMBDA"
        art_lambda_to_call = globals().get(static_art_name)

    # If still no specific art, use generic contextual fallbacks
    if not art_lambda_to_call:
        if "SUCCESS" in art_key_upper or "POSITIVE" in art_key_upper or "PROJECT_NEW" in art_key_upper or "TODO_ADD" in art_key_upper:
            art_lambda_to_call = DEFAULT_ART_POSITIVE_LAMBDA
        elif "ERROR" in art_key_upper or "NEGATIVE" in art_key_upper or "PROJECT_FAIL" in art_key_upper:
            art_lambda_to_call = DEFAULT_ART_NEGATIVE_LAMBDA
        elif "THINKING" in art_key_upper or "QUESTION" in art_key_upper:
            art_lambda_to_call = DEFAULT_ART_QUESTION_LAMBDA
        elif "INPUT" in art_key_upper:
            art_lambda_to_call = CAT_ART_INPUT_STATIC_LAMBDA # More specific than generic neutral
        elif "TIP_CAT_DEF" in art_key_upper : # Specific key from assignment
             art_lambda_to_call = CAT_ART_TIP_CAT_DEF_LAMBDA
        else: # Ultimate generic neutral
            art_lambda_to_call = DEFAULT_ART_NEUTRAL_LAMBDA

    if callable(art_lambda_to_call):
        try:
            art_string = art_lambda_to_call() # Call the lambda to get the base themed art
            if kwargs_for_art_format: # If additional formatting is needed for placeholders within the art
                return art_string.format(**kwargs_for_art_format)
            return art_string
        except Exception as e:
            _catitude_log(f"Error rendering art lambda for key '{art_key}': {e}", "error")
            # Provide a themed error message using apply_theme_to_string
            return apply_theme_to_string(f"[Art Error: {art_key}]", "error")
    else:
        _catitude_log(f"Art lambda for key '{art_key}' is not callable or not found.", "error")
        return apply_theme_to_string(f"[Art Not Found: {art_key}]", "error")


def get_random_startup_banner(placeholders: dict) -> str:
    """
    Selects a random startup banner from MEOWTASPLOIT_BANNER_LAMBDAS
    and populates it with the provided placeholders.
    """
    if not MEOWTASPLOIT_BANNER_LAMBDAS:
        _catitude_log("No startup banners available.", "warning")
        return apply_theme_to_string("Welcome to Meow-tasploit!", "header") # Basic fallback

    selected_banner_lambda = random.choice(MEOWTASPLOIT_BANNER_LAMBDAS)

    # Ensure placeholders are a dict; merge with defaults if necessary
    final_placeholders = _banner_default_placeholders.copy()
    if isinstance(placeholders, dict):
        final_placeholders.update(placeholders)

    try:
        return selected_banner_lambda(final_placeholders)
    except Exception as e:
        _catitude_log(f"Error rendering startup banner: {e}", "error")
        # Fallback to a very simple banner if complex one fails
        return apply_theme_to_string(
            f"Welcome to {final_placeholders.get('tool_name', 'Meow-tasploit')}! (Banner Error)",
            "header"
        )

# --- CLI Command Implementation ---
def meow_tips_command_handler(args=None):
    """
    Handles the 'meow_tips' command to display a random tip.
    Uses get_random_tip() and get_random_art('TIP_CAT_DEF').
    (This function will be called by the main application's command dispatcher)
    """
    category_request = None
    if args and isinstance(args, list) and len(args) > 0:
        category_request = args[0].lower()
    elif args and isinstance(args, str): # If a single string argument is passed
        category_request = args.lower()


    # Display the tip cat art
    print(get_random_art("TIP_CAT_DEF")) # Art key matches reference

    tip_data = get_random_tip(category_filter=category_request)

    tip_text_themed = apply_theme_to_string(tip_data.get('text', 'Always land on your feet!'), 'accent1')
    print(f"  {tip_text_themed}")

    if tip_data.get('category'):
        category_themed = apply_theme_to_string(f"(Category: {tip_data.get('category')})", 'text_secondary', dim=True)
        print(f"  {category_themed}")

    _catitude_log(f"Tip displayed (ID: {tip_data.get('id', 'N/A')})", level="debug")


# --- Main Guard for Standalone Testing ---
if __name__ == "__main__":
    # This block allows for basic testing of the Catitude Engine.
    # It requires stubs for ppp_theme_manager if not available.

    print(apply_theme_to_string("--- Catitude Engine Test ---", "header", bold=True))

    # Simulate registering a simple logger for testing _catitude_log
    def test_catitude_logger(message, level="info", no_cat_prefix=False):
        prefix = "" if no_cat_prefix else "[AppSim] "
        print(apply_theme_to_string(f"{prefix}{level.upper()}: {message}", "info"))
    register_catitude_logger(test_catitude_logger)

    # Test content loading (assuming 'data' subdir exists in the same dir as this script for test)
    # Create dummy data files for testing if they don't exist.
    test_data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(test_data_dir):
        os.makedirs(test_data_dir, exist_ok=True)
    
    # Create dummy puns.json for testing
    dummy_puns_path = os.path.join(test_data_dir, "puns.json")
    if not os.path.exists(dummy_puns_path):
        with open(dummy_puns_path, "w") as f:
            json.dump({
                "general": ["Test pun 1!", "Test pun 2 with {placeholder}!"],
                "success": ["Successful test pun!"]
            }, f)

    # Create dummy tips.json for testing
    dummy_tips_path = os.path.join(test_data_dir, "tips.json")
    if not os.path.exists(dummy_tips_path):
        with open(dummy_tips_path, "w") as f:
            json.dump([
                {"id": "test_tip_1", "category": "general", "text": "This is a general test tip."},
                {"id": "test_tip_2", "category": "ppp_usage", "text": "Use test commands for testing."}
            ], f)

    load_cat_attitude_content(os.path.dirname(__file__)) # Load from script's dir for test

    print(apply_theme_to_string("\n--- Testing Puns ---", "subheader", bold=True))
    print(f"General Pun: {get_random_pun()}")
    print(f"Success Pun: {get_random_pun('success')}")
    print(f"Formatted Pun: {get_random_pun('general', placeholder='MEOW!')}")
    print(f"Unknown Category Pun: {get_random_pun('unknown_cat')}")

    print(apply_theme_to_string("\n--- Testing Tips ---", "subheader", bold=True))
    print(f"Random Tip (any): {get_random_tip()}")
    print(f"Random Tip (ppp_usage): {get_random_tip('ppp_usage')}")
    print(f"Random Tip (unknown_cat): {get_random_tip('unknown_cat')}")

    print(apply_theme_to_string("\n--- Testing ASCII Art ---", "subheader", bold=True))
    print("Success Art:")
    print(get_random_art("SUCCESS"))
    print("Error Art:")
    print(get_random_art("ERROR"))
    print("Thinking Art:")
    print(get_random_art("THINKING"))
    print("Input Art:")
    print(get_random_art("INPUT"))
    print("Tip Cat Art:")
    print(get_random_art("TIP_CAT_DEF"))
    print("Unknown Art Key:")
    print(get_random_art("TOTALLY_MADE_UP_KEY"))


    print(apply_theme_to_string("\n--- Testing Startup Banners ---", "subheader", bold=True))
    test_banner_placeholders = {
        "version": "vTEST",
        "codename": "Test Kitty",
        "module_count": 7,
        "asset_count": 3,
        "finding_count": 1,
        "pun": get_random_pun("startup"),
        "tool_name": "Meow-tasploit Tester"
    }
    for i in range(3): # Show 3 random banners
        print(f"Banner {i+1}:")
        print(get_random_startup_banner(test_banner_placeholders))
        print("-" * 20)

    print(apply_theme_to_string("\n--- Testing 'meow_tips' Command ---", "subheader", bold=True))
    print("Tip with no category filter:")
    meow_tips_command_handler()
    print("\nTip with 'ppp_usage' filter:")
    meow_tips_command_handler(["ppp_usage"]) # Pass args as a list

    print(apply_theme_to_string("\n--- Catitude Engine Test Complete ---", "header", bold=True))