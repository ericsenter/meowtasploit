#!/usr/bin/env python3
# ppp_cat_art_variants.py

"""
Provides a collection of theme-aware ASCII art variants for the
PurrfectPurpleProcessor (PPP) / Meow-tasploit application.
This module serves as a key content provider for ppp_catitude_engine.py.

All art pieces are defined as lambdas that, when called, use functions
from ppp_theme_manager.py to render themed strings.
"""

# --- Assumed Theme Manager Imports ---
# These functions are expected to be provided by ppp_theme_manager.py
# For standalone testing of this module, stubs would be needed if ppp_theme_manager is not available.
try:
    from ppp_theme_manager import get_theme_color, apply_theme_to_string, get_theme_icon
    # If ENDC, BOLD etc. are exposed and used directly by art, import them too.
    # from ppp_theme_manager import ENDC, BOLD
except ImportError:
    # Fallback stubs if ppp_theme_manager is not found (for isolated testing or dev)
    # In a real environment, these should not be used; the actual theme manager must be present.
    print("WARNING: ppp_cat_art_variants - ppp_theme_manager.py not found. Using basic stubs for theming.")
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
        _stub_colors = {
            "success": _FB_GREEN, "error": _FB_RED, "warning": _FB_YELLOW,
            "info": _FB_BLUE, "accent1": _FB_MAGENTA, "text_secondary": _FB_CYAN,
            "header": _FB_MAGENTA, "art_style.banner_primary_color_key": _FB_CYAN,
            "art_style.banner_accent_color_key": _FB_MAGENTA,
            "art_style.generic_art_primary_color_key": _FB_CYAN,
            "text_primary": _FB_WHITE, "prompt_main_text": _FB_CYAN, "critical": _FB_RED,
            "endc": _FB_ENDC # Added endc for _create_themed_art stub
        }
        if color_key == "art_style.banner_primary_color_key": return _stub_colors.get("art_style.banner_primary_color_key", default_fallback)
        if color_key == "art_style.banner_accent_color_key": return _stub_colors.get("art_style.banner_accent_color_key", default_fallback)
        if color_key == "art_style.generic_art_primary_color_key": return _stub_colors.get("art_style.generic_art_primary_color_key", default_fallback)
        return _stub_colors.get(color_key, default_fallback)

    def apply_theme_to_string(text, color_key, bold=False, underline=False, italic=False, dim=False, reverse=False):
        color = get_theme_color(color_key)
        s = f"{_FB_BOLD if bold else ''}{color}{text}{_FB_ENDC}"
        return s

    def get_theme_icon(icon_key, default_fallback="❖"):
        return default_fallback # Simple stub

# --- Common Art Elements ---
CAT_ART_LEGS_ORIGINAL = "( लेगा )"
CAT_ART_LEGS_SIMPLE = "(_^(_)^_)"
CAT_ART_LEGS_CURL = " ( भाई ) " # Another leg variant from original PPP source

# --- Helper for Creating Themed Art ---
def _create_themed_art(art_template: str, primary_color_key: str = "art_style.generic_art_primary_color_key", **kwargs) -> str:
    """
    Colors a simple ASCII art template with a primary theme color.
    The art_template can contain placeholders to be filled by kwargs.
    """
    # Ensure primary_color_key resolves correctly, including art_style indirections
    # The get_theme_color function from the theme manager should handle this.
    color = get_theme_color(primary_color_key)
    end_code = get_theme_color('endc', _FB_ENDC) # Fetch ENDC from theme if possible

    formatted_art = art_template
    if kwargs:
        try:
            formatted_art = art_template.format(**kwargs)
        except KeyError as e:
            # In a real app, this might log to the main app logger
            print(f"DEBUG: _create_themed_art - KeyError formatting art: {e}. Template: {art_template[:50]}...")
            pass # Return template with color but without placeholder filled

    return f"{color}{formatted_art}{end_code}"

# --- Startup Banner Integration ---
# Meticulously reviewed and integrated from ppp_banner_art.py
# Each banner is a lambda, uses get_theme_color/apply_theme_to_string,
# and the 'p' placeholders dictionary.

_banner_default_placeholders = { # Renamed to avoid conflict if imported elsewhere
    "version": "v0.0", "codename": "Unset", "module_count": 0,
    "asset_count": 0, "finding_count": 0, "pun": "Initializing...",
    "tool_name": "Meow-tasploit"
}

MEOWTASPLOIT_BANNERS_COLLECTION = [
    # Banner 1 (Original Welcome)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}    /\\_/\\  {apply_theme_to_string(f"Welcome to {(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')}!", 'header', bold=True)}
   ( o.o ) {apply_theme_to_string(f"Version: {(p or _banner_default_placeholders).get('version', 'N/A')} ({(p or _banner_default_placeholders).get('codename', 'N/A')})", 'info')}
    > ^ <  {apply_theme_to_string(f"\"{apply_theme_to_string((p or _banner_default_placeholders).get('pun', 'Purrfectly ready!'), 'prompt_main_text')}\"", 'prompt_main_text')}
   {CAT_ART_LEGS_ORIGINAL} {apply_theme_to_string(f"Modules: {(p or _banner_default_placeholders).get('module_count', 0)} | Assets: {(p or _banner_default_placeholders).get('asset_count', 0)} | Findings: {(p or _banner_default_placeholders).get('finding_count', 0)}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 2 (Digital Alleycat)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
{apply_theme_to_string('Digital Alleycat Mode', 'header', bold=True)}
      |\\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\\ (  `'-'
    '---''(_/--'  `-'\\_)   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
{apply_theme_to_string('Sniffing out vulnerabilities... one paw print at a time.', 'prompt_main_text')}
{apply_theme_to_string(f"Codename: {(p or _banner_default_placeholders).get('codename', 'N/A')} - {(p or _banner_default_placeholders).get('pun', 'Purrs Ahead!')}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 3 (NyanSec)
    lambda p=None: f"""
{apply_theme_to_string('NyanSec Operations Engaged!', 'header', bold=True)}
{get_theme_color('art_style.banner_accent_color_key')} _,.--.,_ _{get_theme_color('endc')}
{get_theme_color('art_style.banner_accent_color_key')}(" |    `";{get_theme_color('endc')}     {get_theme_color('art_style.banner_primary_color_key')}..----.._
{get_theme_color('art_style.banner_accent_color_key')} `-|    | ;{get_theme_color('endc')}   {get_theme_color('art_style.banner_primary_color_key')}_|       |\\_
{get_theme_color('art_style.banner_accent_color_key')}   |    |{get_theme_color('endc')} {get_theme_color('art_style.banner_primary_color_key')} ("\\  |      /") )
{get_theme_color('art_style.banner_accent_color_key')}   |    |{get_theme_color('endc')} {get_theme_color('art_style.banner_primary_color_key')}   `-|      |-'
{get_theme_color('art_style.banner_accent_color_key')}   ;----|{get_theme_color('endc')}     {get_theme_color('art_style.banner_primary_color_key')}  "-.  .--"
{get_theme_color('art_style.banner_accent_color_key')}   `----'{get_theme_color('endc')}       {get_theme_color('art_style.banner_primary_color_key')} `--"`
{apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')}: Riding the rainbow of data! {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
{apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Taste the data-bow!')} - Modules: {(p or _banner_default_placeholders).get('module_count', 0)}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 4 (Schrödinger)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
  ??????-------?????-------??????
  |  {apply_theme_to_string('Schrödinger\'s Packet', 'header', bold=True)}  |
  |       /\\_/\\             |
  |      ( ?.?) {apply_theme_to_string('Observing...', 'warning')}  |  {apply_theme_to_string("Is the vuln there or not?", 'prompt_main_text')}
  |       > ^ <             |
  ??????-------?????-------??????
{apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')} - {(p or _banner_default_placeholders).get('pun', 'Maybe...')}", 'info')}
{get_theme_color('endc')}""",
    # Banner 5 (Furrwall)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}  .--""--.__        {apply_theme_to_string('Furrwall Guardian Protocol', 'header', bold=True)}
 /          \\\\      {apply_theme_to_string(f"Version: {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
|  {get_theme_color('art_style.banner_accent_color_key')}  (^==^){get_theme_color('art_style.banner_primary_color_key')}  |      {apply_theme_to_string("Protecting the Meow-trix!", 'success')}
 \\\\  {get_theme_color('art_style.banner_accent_color_key')} O''O {get_theme_color('art_style.banner_primary_color_key')} /       {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'None shall pass!')}", 'prompt_main_text')}
  '.____.'         {apply_theme_to_string(f"Assets Secured: {(p or _banner_default_placeholders).get('asset_count', 0)}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 6 (Keyboard Cat Cavalry)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}   {apply_theme_to_string('Keyboard Cat Cavalry - Deploying the Kittens!', 'header', bold=True)}
  _________________      /\\_/\\
 ||               ||    ( >ω< )
 ||[][] Gateway [][]||     > ^ <
 ||_______________||    人____)し
 [ -= MEOW =- MEOW ]   (_(_(_)_(_(   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
{apply_theme_to_string(f"Orchestrating {(p or _banner_default_placeholders).get('module_count', 0)} tools for purr-fect pwnage! {(p or _banner_default_placeholders).get('pun', 'Charge!')}", 'prompt_main_text')}
{get_theme_color('endc')}""",
    # Banner 7 (Hacker Hoodie)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
      _.---.._             {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} - In the Shadows", 'header', bold=True)}
     .'        '.
    /   {apply_theme_to_string('O', 'text_primary')}      {apply_theme_to_string('O', 'text_primary')} \\\\          {apply_theme_to_string(f"Version {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
   |    {get_theme_color('art_style.banner_accent_color_key')}(----){get_theme_color('art_style.banner_primary_color_key')}   |        {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Incognito...')}", 'prompt_main_text')}
   \\\\   '.__.'   /
    '.______.'           {apply_theme_to_string(f"Findings to report: {(p or _banner_default_placeholders).get('finding_count', 0)}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 8 (Paw on Server)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
  +-----------------+    {apply_theme_to_string('Server Access Purr-otocol', 'header', bold=True)}
  |   {get_theme_color('art_style.banner_accent_color_key')}  /\\_/\\    {get_theme_color('art_style.banner_primary_color_key')}   |
  |  {get_theme_color('art_style.banner_accent_color_key')} ( o.x )   {get_theme_color('art_style.banner_primary_color_key')}   | {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
  |   > ^ <     {apply_theme_to_string('[OK]', 'success', bold=True)}{get_theme_color('art_style.banner_primary_color_key')}  | {apply_theme_to_string('Leaving our mark... and the loot.', 'prompt_main_text')}
  |  {apply_theme_to_string(CAT_ART_LEGS_SIMPLE, 'accent1')}   | {apply_theme_to_string(f"Discovered {(p or _banner_default_placeholders).get('asset_count', 0)} assets.", 'text_primary')}
  +-----------------+    {apply_theme_to_string(f"Pun: {(p or _banner_default_placeholders).get('pun', 'Gotcha!')}", 'info')}
{get_theme_color('endc')}""",
    # Banner 9 (Matrix Cats)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}0101{get_theme_color('art_style.banner_accent_color_key')}(^._.^)ﾉ{get_theme_color('art_style.banner_primary_color_key')}01010    {apply_theme_to_string('Entering the Meow-trix', 'header', bold=True)}
101{get_theme_color('art_style.banner_accent_color_key')}( >.< ){get_theme_color('art_style.banner_primary_color_key')}1010101   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
01010{get_theme_color('art_style.banner_accent_key')}(ᓚᘏᗢ){get_theme_color('art_style.banner_primary_color_key')}101001  {apply_theme_to_string('Follow the white rabbit... or the cat.', 'prompt_main_text')}
100{get_theme_color('art_style.banner_accent_color_key')}(=;ω;=){get_theme_color('art_style.banner_primary_color_key')}010110  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Neo-w?')} :: Modules: {(p or _banner_default_placeholders).get('module_count', 0)}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 10 (Lockpick Cat)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
      {get_theme_color('art_style.banner_accent_color_key')}  .--.
{get_theme_color('art_style.banner_accent_color_key')}     /.-. '----------.
{get_theme_color('art_style.banner_accent_color_key')}     \\\\'-' .--"--""-"`
{get_theme_color('art_style.banner_accent_color_key')}      '--'{get_theme_color('art_style.banner_primary_color_key')}  /\\_/\\   {apply_theme_to_string('The Purr-fessional Lockpicker', 'header', bold=True)}
             ( o.o )  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
              > ^ <   {apply_theme_to_string('No system is impurr-vious.', 'prompt_main_text')}
             {CAT_ART_LEGS_ORIGINAL} {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Click!')}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 11 (Cyber Cat Visor)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}   /\\_/\\
  {get_theme_color('art_style.banner_accent_color_key')}( {get_theme_color('art_style.banner_primary_color_key')}0{get_theme_color('art_style.banner_accent_color_key')}={get_theme_color('art_style.banner_primary_color_key')}.{get_theme_color('art_style.banner_accent_color_key')}={get_theme_color('art_style.banner_primary_color_key')}0 {get_theme_color('art_style.banner_accent_color_key')}){get_theme_color('art_style.banner_primary_color_key')}    {apply_theme_to_string('Cybernetic Feline Operations', 'header', bold=True)}
  {get_theme_color('art_style.banner_accent_color_key')} (        ) {get_theme_color('art_style.banner_primary_color_key')}   {apply_theme_to_string(f"Enhancing {(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
   {apply_theme_to_string(' > ^ <', 'accent1')}      {apply_theme_to_string('Scanning with purr-cision.', 'prompt_main_text')}
   {apply_theme_to_string(f'{CAT_ART_LEGS_ORIGINAL}', 'accent1')}     {apply_theme_to_string(f"Codename: {(p or _banner_default_placeholders).get('codename', 'RoboCat')}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 12 (Cat Coding)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
  > ( ( ({apply_theme_to_string('#!/bin/meow', 'warning', bold=True)}) ) ) <      {apply_theme_to_string('Script Kitty Evolution', 'header', bold=True)}
 / \\\\ `|||`                  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
(   )oO {apply_theme_to_string('// Purrgramming...', 'text_primary')}
 \\\\ / \\_/                 {apply_theme_to_string(f"Crafting {(p or _banner_default_placeholders).get('module_count', 0)} new exploits.", 'prompt_main_text')}
  `   ~                    {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Code meows!')}", 'success')}
{get_theme_color('endc')}""",
    # Banner 13 (Data Stream Cat)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')} ~ ~ ~ ~ ~ ~ {apply_theme_to_string('Data Stream Purr-ocessor', 'header', bold=True)} ~ ~ ~ ~ ~ ~
{get_theme_color('art_style.banner_accent_color_key')}      <`)))>< <`)))>< <`)))><{get_theme_color('art_style.banner_primary_color_key')}
         /\\_/\\                {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
        ( o.O ) {apply_theme_to_string('Riding the waves of information.', 'prompt_main_text')}
         > ~ <                  {apply_theme_to_string(f"Findings: {(p or _banner_default_placeholders).get('finding_count', 0)}. {(p or _banner_default_placeholders).get('pun', 'Surf`s up!')}", 'text_primary')}
{get_theme_color('art_style.banner_accent_color_key')}  <`)))>< <`)))>< <`)))><{get_theme_color('art_style.banner_primary_color_key')}
{get_theme_color('endc')}""",
    # Banner 14 (Cat Detective)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
      .--""--.
     /        \\\\_         {apply_theme_to_string('Meow-lock Holmes Investigates', 'header', bold=True)}
    |  {apply_theme_to_string('O    O', 'text_primary')}  {get_theme_color('art_style.banner_accent_color_key')}(_){get_theme_color('art_style.banner_primary_color_key')}    {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
    \\\\  .--.  /          {apply_theme_to_string('The game is a-paw!', 'prompt_main_text')}
     '.____.'            {apply_theme_to_string(f"Uncovering {(p or _banner_default_placeholders).get('finding_count', 0)} clues. {(p or _banner_default_placeholders).get('pun', 'Elementary!')}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 15 (Circuit Cat)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}.--.      .--.     {apply_theme_to_string('Circuit Board Cat-alyst', 'header', bold=True)}
|  | {get_theme_color('art_style.banner_accent_color_key')}(^._.^){get_theme_color('art_style.banner_primary_color_key')} |  |   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
'--'{get_theme_color('art_style.banner_accent_color_key')}|  |  |{get_theme_color('art_style.banner_primary_color_key')}'--'   {apply_theme_to_string('Connecting the data nodes.', 'prompt_main_text')}
   {get_theme_color('art_style.banner_accent_color_key')}'--''--'{get_theme_color('art_style.banner_primary_color_key')}      {apply_theme_to_string(f"Modules online: {(p or _banner_default_placeholders).get('module_count', 0)}. {(p or _banner_default_placeholders).get('pun', 'Wired in!')}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 16 (Stealthy Paw Prints)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
{apply_theme_to_string('Operation: Silent Paws', 'header', bold=True)}
  {apply_theme_to_string('🐾', 'accent1')}      {apply_theme_to_string('🐾', 'accent1')}         {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
      {apply_theme_to_string('🐾', 'accent1')}           {apply_theme_to_string('Leaving no trace, only results.', 'prompt_main_text')}
 {apply_theme_to_string('🐾', 'accent1')}         {apply_theme_to_string('🐾', 'accent1')}    {apply_theme_to_string(f"Assets targeted: {(p or _banner_default_placeholders).get('asset_count', 0)}. {(p or _banner_default_placeholders).get('pun', 'Shhh!')}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 17 (Cat Ghost)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
   .-""\"-.             {apply_theme_to_string('Phantom Prowler Protocol', 'header', bold=True)}
  /       \\\\
 |  {get_theme_color('art_style.banner_accent_color_key')}o   o{get_theme_color('art_style.banner_primary_color_key')}  |         {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')} - Codename: {(p or _banner_default_placeholders).get('codename', 'Spectre')}", 'info')}
 |   {get_theme_color('art_style.banner_accent_color_key')}\\\\   /{get_theme_color('art_style.banner_primary_color_key')}   |         {apply_theme_to_string('Evading detection, finding secrets.', 'prompt_main_text')}
  '. ___ .'            {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Boo!')}", 'text_primary')}
    `~~~`
{get_theme_color('endc')}""",
    # Banner 18 (Binary Code Cat Face)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}01{get_theme_color('art_style.banner_accent_color_key')}( ^ ){get_theme_color('art_style.banner_primary_color_key')}10{get_theme_color('art_style.banner_accent_color_key')}( ^ ){get_theme_color('art_style.banner_primary_color_key')}01   {apply_theme_to_string('Binary Purr-fection', 'header', bold=True)}
101{get_theme_color('art_style.banner_accent_color_key')}(  o  ){get_theme_color('art_style.banner_primary_color_key')}101   {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
0101{get_theme_color('art_style.banner_accent_color_key')}( --- ){get_theme_color('art_style.banner_primary_color_key')}010   {apply_theme_to_string('Speaking the language of machines.', 'prompt_main_text')}
10101{get_theme_color('art_style.banner_accent_color_key')}{{ {get_theme_color('art_style.banner_primary_color_key')}O{get_theme_color('art_style.banner_accent_color_key')}}}{get_theme_color('art_style.banner_primary_color_key')}101  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', '0ne or Zer0?')} / {(p or _banner_default_placeholders).get('module_count', 0)} modules", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 19 (Cat with Network Cable)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
  /\\_/\\  -----{get_theme_color('art_style.banner_accent_color_key')}(){get_theme_color('art_style.banner_accent_color_key')}(){get_theme_color('art_style.banner_accent_color_key')}({get_theme_color('art_style.banner_primary_color_key')}---    {apply_theme_to_string('Network Sniffer Active', 'header', bold=True)}
 ( o x o ) {apply_theme_to_string('~', 'accent1')}              {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} {(p or _banner_default_placeholders).get('version', 'N/A')}", 'info')}
  >  ^  <  {apply_theme_to_string('~', 'accent1')}              {apply_theme_to_string('Tangled in the web of data.', 'prompt_main_text')}
 {CAT_ART_LEGS_ORIGINAL} {apply_theme_to_string('~~~', 'accent1')}             {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('pun', 'Packet Inspector!')} | Assets: {(p or _banner_default_placeholders).get('asset_count', 0)}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 20 (Minimalist Cat Head / Command Prompt)
    lambda p=None: f"""
{get_theme_color('art_style.banner_primary_color_key')}
  {apply_theme_to_string('Meow>', 'prompt_main_text', bold=True)} {get_theme_color('art_style.banner_accent_color_key')} /\\_/\\ {get_theme_color('art_style.banner_primary_color_key')}
  {apply_theme_to_string('Meow>', 'prompt_main_text', bold=True)} {get_theme_color('art_style.banner_accent_color_key')}(=•.•=){get_theme_color('art_style.banner_primary_color_key')}  {apply_theme_to_string(f"{(p or _banner_default_placeholders).get('tool_name', 'Meow-tasploit')} Core {(p or _banner_default_placeholders).get('version', 'N/A')}", 'header')}
  {apply_theme_to_string('Meow>', 'prompt_main_text', bold=True)} {get_theme_color('art_style.banner_accent_color_key')}('')_(''){get_theme_color('art_style.banner_primary_color_key')} {apply_theme_to_string(f"Awaiting purr-mission... {(p or _banner_default_placeholders).get('pun', 'Ready!')}", 'info')}
                       {apply_theme_to_string(f"Type 'help' or 'meow_tips'. Modules: {(p or _banner_default_placeholders).get('module_count', 0)}", 'text_primary')}
{get_theme_color('endc')}""",
    # Banner 21 (Meowtasploit Text Logo)
    lambda p=None: f"""
{apply_theme_to_string(r'''
███╗   ███╗███████╗ ██╗    ██████╗ ███████╗██████╗  ██╗      ██████╗██╗ ██████╗
████╗ ████║██╔════╝ ██║   ██╔═████╗██╔════╝██╔══██╗ ██║     ██╔════╝██║██╔═══██╗
██╔████╔██║█████╗   ██║   ██║██╔██║█████╗  ██████╔╝ ██║     ██║     ██║██║   ██║
██║╚██╔╝██║██╔══╝   ██║   ████╔╝██║██╔══╝  ██╔══██╗ ██║     ██║     ██║██║   ██║
██║ ╚═╝ ██║███████╗ ███████╗╚████╔╝ ███████╗██║  ██║ ███████╗╚██████╗██║╚██████╔╝
╚═╝     ╚═╝╚══════╝ ╚══════╝ ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚══════╝ ╚═════╝╚═╝ ╚═════╝ ''', 'art_style.banner_primary_color_key')}
{apply_theme_to_string(f"Version: {(p or _banner_default_placeholders).get('version', 'N/A')} | Codename: {(p or _banner_default_placeholders).get('codename', 'N/A')} | {(p or _banner_default_placeholders).get('pun', 'Ready for action!')}", 'info', bold=True)}
{apply_theme_to_string(f"Modules: {(p or _banner_default_placeholders).get('module_count', 0)} | Type 'help' for commands.", 'text_secondary')}
{get_theme_color('endc')}"""
]


# --- Expansion of Contextual Art Variants ---

# SUCCESS Art
CAT_ART_SUCCESS_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\\n   ( ^.^ )    Purr-fect! Job's done!\n    > L < \n   {CAT_ART_LEGS_ORIGINAL}", "success"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (๑•̀ㅂ•́)و✧  Nailed it! High paw!\n    > ω < \n   {CAT_ART_LEGS_SIMPLE}", "success"),
    lambda: _create_themed_art(f"    /\\_/\\\n   ( ´▽｀)ノ   Mission Accomplished!\n    > U < \n   {CAT_ART_LEGS_CURL}", "success"),
    lambda: _create_themed_art(f"  ୧(﹒︠ᴗ﹒︡)୨   Victory meow! Success!\n   <ﾉㄎ  ﾉㄎ>\n    <ココ>", "success"), # Kaomoji style
    lambda: _create_themed_art(f"    (=\\^・ェ・^=)\n   System Override: SUCCESSFUL\n    \"Meow-velous work!\"", "success"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (◉‿◉)      Target neutralized! Well done!\n    > ∆ < \n   {CAT_ART_LEGS_SIMPLE}", "success"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (*≧▽≦)   That was the cat's meow!\n    > Y < \n   {CAT_ART_LEGS_CURL}", "success")
]

# ERROR Art
CAT_ART_ERROR_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\\n   ( >д< )    HISSS! An error!\n    > X < \n   {CAT_ART_LEGS_ORIGINAL}", "error"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (✖╭╮✖)    Cat-astrophe! Check logs!\n    > ~ < \n   {CAT_ART_LEGS_SIMPLE}", "error"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (ノಠ益ಠ)ノ  A fur-midable glitch!\n    > # < \n   {CAT_ART_LEGS_CURL}", "error"),
    lambda: _create_themed_art(f"  くコ:彡     Something's fishy... ERROR!\n   (ᗒᗣᗕ)՞ \n    くコ:彡", "error"), # Squid cat error
    lambda: _create_themed_art(f"    (=ｘェｘ=)\n   Me-OUCH! That didn't work.\n    Try again?", "error"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (ಥ﹏ಥ)      System hiccup! Error detected.\n    > ∆ < \n   {CAT_ART_LEGS_SIMPLE}", "error"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (ﾒ` ﾛ ´)   Hairball in the mainframe!\n    > Z < \n   {CAT_ART_LEGS_CURL}", "error")
]

# THINKING Art
CAT_ART_THINKING_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\\n   ( ?.?)      Purr-colating thoughts...\n    > - < \n   {CAT_ART_LEGS_ORIGINAL}", "warning"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (思考中...)   Let me consult the catnip...\n    > . < \n   {CAT_ART_LEGS_SIMPLE}", "warning"), # Japanese "thinking"
    lambda: _create_themed_art(f"    /\\_/\\\n   (媤_媤)      Hmm, that's a whisker-twitcher!\n    > Y < \n   {CAT_ART_LEGS_CURL}", "warning"),
    lambda: _create_themed_art(f"  (  ?.?)\n  /)  .(\\   Pondering the im-paw-ssible...\n (( O ))\n  \\\\=(=/", "warning"), # Different style
    lambda: _create_themed_art(f"    (=?ェ?=)\n   Engaging tactical nap... I mean, thinking!\n    One moment...", "warning"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (•ิ_•ิ)?    Accessing ancient cat wisdom...\n    > ~ < \n   {CAT_ART_LEGS_SIMPLE}", "warning"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (⊙_☉)      That's a curious case!\n    > ? < \n   {CAT_ART_LEGS_CURL}", "warning")
]

# INPUT Art
CAT_ART_INPUT_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\\n   ( ^_~ )    Awaiting your purr-fect input...\n    > : < \n   {CAT_ART_LEGS_ORIGINAL}", "info"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (=ච ω ච=)  Ready for your command, Meow-ster!\n    > . < \n   {CAT_ART_LEGS_SIMPLE}", "info"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (猫入力)     Feed me data!\n    > ^ < \n   {CAT_ART_LEGS_CURL}", "info"), # Japanese "cat input"
    lambda: _create_themed_art(f"  ᓚᘏᗢ\n  Input purr-ameters below:\n   -----", "info"),
    lambda: _create_themed_art(f"    (=^･ω･^=)ﾉ\n   Your wish is my command line...\n    What's next?", "info"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (✧ω✧)      Listening with all my whiskers!\n    > 口 < \n   {CAT_ART_LEGS_SIMPLE}", "info"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (^-^*)      Tell me your secrets...\n    > ... < \n   {CAT_ART_LEGS_CURL}", "info")
]

# WORKING Art (New category as per assignment hints)
CAT_ART_WORKING_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\\n   ( o_O )    Working on it! Purr-cessing...\n    > . < \n   {CAT_ART_LEGS_ORIGINAL}", "info"), # Using info color from existing PPP
    lambda: _create_themed_art(f"    /\\_/\\\n   (ง •̀_•́)ง   Engaging the cyber-claws!\n    > ~ < \n   {CAT_ART_LEGS_SIMPLE}", "info"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (｀・ω・´)   Meow-ticulously working...\n    > - < \n   {CAT_ART_LEGS_CURL}", "info"),
    lambda: _create_themed_art(f"  (ฅ)　(ฅ)\n  (合成中)   Compiling the catnip code...\n  ૮₍´｡• ᵕ •｡`₎ა", "info"), # Japanese "synthesizing"
    lambda: _create_themed_art(f"    (=｀ω´=)\n   Digital zoomies in progress!\n    Stand by...", "info"),
    lambda: _create_themed_art(f"    /\\_/\\\n   (＠_＠)@    Spinning the yarn... of data!\n    > WWW < \n   {CAT_ART_LEGS_SIMPLE}", "info"),
    lambda: _create_themed_art(f"    /\\_/\\\n   ( ^..^)ﾉ~  Conjuring results!\n    > * < \n   {CAT_ART_LEGS_CURL}", "info")
]

# Other existing art from original PPP file, converted to VARS structure
CAT_ART_PROJECT_NEW_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   ( ^.^ )ニャー      New project cache established!\n    > ^ <           Let the purr-oceedings begin!\n   {CAT_ART_LEGS_ORIGINAL}          ---------------------------------", "success"),
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   (๑✧∀✧๑)      Territory Claimed! New Project!\n    > v <           Time to mark our data!\n   {CAT_ART_LEGS_SIMPLE}          ---------------------------------", "success"),
]
CAT_ART_PROJECT_LOAD_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   ( o.o )          Project cache loaded!\n    > ^ <           Ready for your commands.\n   {CAT_ART_LEGS_ORIGINAL}          ---------------------------------", "info"),
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   (◉ω◉｀)          Resuming the hunt! Project loaded.\n    > . <           Let's get back to it!\n   {CAT_ART_LEGS_SIMPLE}          ---------------------------------", "info"),
]
CAT_ART_PROJECT_FAIL_VARS = [ # Was YELLOW (warning)
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   ( T_T )          Hmm, that project seems elusive...\n    > ^ <           Could not create/load project.\n   {CAT_ART_LEGS_ORIGINAL}          ---------------------------------", "warning"),
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   (u_uメ)         Project access denied! Grrr...\n    > X <           Check path or permissions.\n   {CAT_ART_LEGS_SIMPLE}          ---------------------------------", "error"), # Variant can be error
]
CAT_ART_LOG_ENTRY_VARS = [ # Was CYAN (info/debug)
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   ( o.O ) zzZ       Noted! Adding to the cat-alogue...\n    > ^ < \n   {CAT_ART_LEGS_ORIGINAL}          ---------------------------------", "debug"),
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   ( ^黒^ )          Entry logged in the great scroll!\n    > . <           The archives grow...\n   {CAT_ART_LEGS_SIMPLE}          ---------------------------------", "debug"), # Kuro (black) cat
]

# ... (Continue for all other CAT_ART_* from original PPP script, converting them to _VARS lists with 5-7 variants each)
# For brevity, I'll list the categories and provide one example for expansion, you would fill these out:

CAT_ART_TODO_ADD_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   ( •̀ω•́ )✧       Task added to the Scratch List!\n    > ^ <           Let's get it done!\n   {CAT_ART_LEGS_ORIGINAL}          ---------------------------------", "success"),
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   (ὥ.ὥ)           New mission on the board!\n    > + <           Task accepted!\n   {CAT_ART_LEGS_CURL}           ---------------------------------", "success"),
    # ... 3-5 more variants
]
CAT_ART_TODO_LIST_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   ( ◎ܫ◎)          Here's your Scratch List, boss!\n    > ^ <           What's next on the agenda?\n   {CAT_ART_LEGS_ORIGINAL}          ---------------------------------", "info"),
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   (^・ω・^§)ﾉ    The Royal Decree of Tasks!\n    > List <        Review your objectives.\n   {CAT_ART_LEGS_SIMPLE}          ---------------------------------", "info"),
    # ... 3-5 more variants
]
CAT_ART_TODO_DONE_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   ( ^０^ )        Another one bites the dust! Task done!\n    > ^ <           Purr-fect progress!\n   {CAT_ART_LEGS_ORIGINAL}          ---------------------------------", "accent1"), # was magenta
    lambda: _create_themed_art(f"    /\\_/\\           ---------------------------------\n   (V●ᴥ●V)        Task Conquered! *Flexes Paw*\n    > ✓ <           Onwards and upwards!\n   {CAT_ART_LEGS_CURL}           ---------------------------------", "accent1"),
    # ... 3-5 more variants
]
CAT_ART_PLUGIN_ADD_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   (=◉ܫ◉=)         New component catalogued! Purr-ecise!\n    > ^ <           Let's investigate this critter...\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "success"),
    # ... 5-6 more variants
]
CAT_ART_PLUGIN_LIST_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   ( ♦_♦ )          Behold! The Catalog of Curious Components!\n    > ^ <           Which plugin piques your interest?\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "info"),
    # ... 5-6 more variants
]
CAT_ART_PLUGIN_UPDATE_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   ( ･ω･)ﾉ         Plugin details updated! Keeping tabs...\n    > ^ < \n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "info"), # was cyan
    # ... 5-6 more variants
]
CAT_ART_AJAX_ADD_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   ( ¬‿¬ )          AJAX action sniffed out and noted! \n    > ω <           Let's see what it whispers...\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "success"),
    # ... 5-6 more variants
]
CAT_ART_AJAX_LIST_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   ( dòдób )         The Whisker List of Web Hooks awaits!\n    > ^ <           Which AJAX call shall we prod?\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "info"),
    # ... 5-6 more variants
]
CAT_ART_ASSET_ADD_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   (=ච ω ච=)       New Meow-chine catalogued! Target acquired!\n    > ^ <           Let's see what services it's purr-viding...\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "success"),
    # ... 5-6 more variants
]
CAT_ART_ASSET_LIST_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   ( ▼д▼)          Behold! The Registry of Target Meow-chines!\n    > ^ <           Which asset requires our fangs-on attention?\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "info"),
    # ... 5-6 more variants
]
CAT_ART_SERVICE_ADD_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   ( o⚐ हान          Service paw-sitively identified and noted!\n    > ^ <\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "info"), # was cyan
    # ... 5-6 more variants
]
CAT_ART_FINDING_ADD_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   ( detective )    A new clue for the collection! Purr-imary evidence!\n    > . <           (Imagine a magnifying glass)\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "success"),
    # ... 5-6 more variants
]
CAT_ART_FINDING_LIST_VARS = [
    lambda: _create_themed_art(f"    /\\_/\\           ------------------------------------\n   ( O_o )          Reviewing the Clue Collector Cache...\n    > ? <           What secrets does it hold?\n   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------", "info"),
    # ... 5-6 more variants
]

# Specific Art Lambdas (from conceptual code or new)
CAT_ART_TIP_CAT_DEF_LAMBDA = lambda: _create_themed_art(
    f"""
    /\\_/\\
   (o.-.o) {apply_theme_to_string("A whisker of wisdom from the Meow-Master:", 'info', bold=True)}
    > § <
   {CAT_ART_LEGS_ORIGINAL}""", "art_style.generic_art_primary_color_key") # Using generic key for body

CAT_ART_WELCOME_LAMBDA = lambda: _create_themed_art( # Default welcome art if banners fail
    f"""
    /\\_/\\           -----------------------------------------
   ( o.o )          Welcome to PurrfectPurpleProcessor!
    > ^ <           Type 'help' for commands.
   {CAT_ART_LEGS_ORIGINAL}          -----------------------------------------""", "art_style.banner_primary_color_key")

CAT_ART_GOODBYE_LAMBDA = lambda: _create_themed_art(
    f"""
    /\\_/\\           ------------------------------------
   ( -.- ) Zzz...    PurrfectPurpleProcessor signing off!
    > ^ <           Come back soon!
   {CAT_ART_LEGS_ORIGINAL}          ------------------------------------""", "art_style.banner_primary_color_key")


# --- Static Fallback Art Lambdas ---
# These point to the first variant in their respective VARS list, or a specific defined lambda.
CAT_ART_SUCCESS_STATIC_LAMBDA = CAT_ART_SUCCESS_VARS[0]
CAT_ART_ERROR_STATIC_LAMBDA = CAT_ART_ERROR_VARS[0]
CAT_ART_THINKING_STATIC_LAMBDA = CAT_ART_THINKING_VARS[0]
CAT_ART_INPUT_STATIC_LAMBDA = CAT_ART_INPUT_VARS[0]
CAT_ART_WORKING_STATIC_LAMBDA = CAT_ART_WORKING_VARS[0]
CAT_ART_PROJECT_NEW_STATIC_LAMBDA = CAT_ART_PROJECT_NEW_VARS[0] if CAT_ART_PROJECT_NEW_VARS else DEFAULT_ART_POSITIVE_LAMBDA
CAT_ART_PROJECT_LOAD_STATIC_LAMBDA = CAT_ART_PROJECT_LOAD_VARS[0] if CAT_ART_PROJECT_LOAD_VARS else DEFAULT_ART_NEUTRAL_LAMBDA
# ... and so on for all other categories from original PPP script

# --- Generic Default Art Lambdas ---
DEFAULT_ART_POSITIVE_LAMBDA = CAT_ART_SUCCESS_STATIC_LAMBDA
DEFAULT_ART_NEGATIVE_LAMBDA = CAT_ART_ERROR_STATIC_LAMBDA
DEFAULT_ART_NEUTRAL_LAMBDA = lambda: _create_themed_art(
    f"""
    /\\_/\\
   ( . . )          Just a moment, purr-lease...
    > - <
   {CAT_ART_LEGS_SIMPLE}""", "text_secondary") # Generic neutral uses text_secondary
DEFAULT_ART_QUESTION_LAMBDA = CAT_ART_THINKING_STATIC_LAMBDA


if __name__ == "__main__":
    # Basic test to print a few art pieces.
    # This requires the theme manager stubs above to be active if ppp_theme_manager is not available.
    print(apply_theme_to_string("--- PPP Cat Art Variants Test ---", "header", bold=True))

    print(apply_theme_to_string("\n--- Testing Startup Banners (first 3) ---", "subheader", bold=True))
    test_placeholders = {
        "version": "v0.X.test", "codename": "Artful Dodger", "module_count": 99,
        "asset_count": 15, "finding_count": 7, "pun": "Art for art's sake!",
        "tool_name": "Meow-Art-Test"
    }
    for i, banner_lambda in enumerate(MEOWTASPLOIT_BANNERS_COLLECTION[:3]):
        print(f"Banner {i+1}:")
        print(banner_lambda(test_placeholders)) # Call lambda with placeholders
        print("-" * 20)
    if len(MEOWTASPLOIT_BANNERS_COLLECTION) > 3:
        print(f"Last Banner (Index {len(MEOWTASPLOIT_BANNERS_COLLECTION)-1}):") # Test the text logo banner
        print(MEOWTASPLOIT_BANNERS_COLLECTION[-1](test_placeholders))


    print(apply_theme_to_string("\n--- Testing Contextual Art ---", "subheader", bold=True))
    print("Success (random from VARS):")
    if CAT_ART_SUCCESS_VARS: print(random.choice(CAT_ART_SUCCESS_VARS)())
    print("\nError (static lambda):")
    if callable(CAT_ART_ERROR_STATIC_LAMBDA): print(CAT_ART_ERROR_STATIC_LAMBDA())
    print("\nThinking (default art lambda):")
    if callable(DEFAULT_ART_QUESTION_LAMBDA): print(DEFAULT_ART_QUESTION_LAMBDA())
    print("\nWorking (random from VARS):")
    if CAT_ART_WORKING_VARS: print(random.choice(CAT_ART_WORKING_VARS)())
    print("\nInput (random from VARS):")
    if CAT_ART_INPUT_VARS: print(random.choice(CAT_ART_INPUT_VARS)())

    print(apply_theme_to_string("\n--- Testing Specific Art ---", "subheader", bold=True))
    print("Tip Cat Def:")
    if callable(CAT_ART_TIP_CAT_DEF_LAMBDA): print(CAT_ART_TIP_CAT_DEF_LAMBDA())

    print(apply_theme_to_string("\n--- Art Test Complete ---", "header", bold=True))
