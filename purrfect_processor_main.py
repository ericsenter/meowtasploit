#!/usr/bin/env python3

import os
import shutil
import datetime
import re
import json
import sys
import uuid # For generating insight_ids
from datetime import timezone # Specifically import timezone
import argparse # For importer arguments

# --- ANSI Color Codes ---
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

# --- ASCII Cat Art (Using (_^_) for legs for better compatibility) ---
cat_legs_ascii = "(_^_)" 

CAT_ART_WELCOME = f"""
{BLUE}
    /\_/\           -----------------------------------------
   ( o.o )          Welcome to PurrfectPurpleProcessor!
    > ^ <           Ready to pounce on some data!
   {cat_legs_ascii}          Type 'help' for commands.
                 -----------------------------------------
{ENDC}
"""

CAT_ART_GOODBYE = f"""
{BLUE}
    /\_/\           ------------------------------------
   ( -.- ) Zzz...    PurrfectPurpleProcessor signing off!
    > ^ <           Come back soon!
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_SUCCESS = f"""
{GREEN}
    /\_/\
   ( ^.^ )          Success! That was purrfect!
    > ^ <
   {cat_legs_ascii}
{ENDC}
"""

CAT_ART_ERROR = f"""
{RED}
    /\_/\
   ( >.< )          Oh no! A hiss-take occurred!
    > ^ <           Check the message above.
   {cat_legs_ascii}
{ENDC}
"""

CAT_ART_THINKING = f"""
{YELLOW}
    /\_/\
   ( ?.?)           Hmm... let me think about that...
    > ^ <
   {cat_legs_ascii}
{ENDC}
"""

CAT_ART_WORKING = f"""
{CYAN}
    /\_/\
   ( o_O )          Working on it! One moment, meow...
    > ^ <
   {cat_legs_ascii}
{ENDC}
"""

CAT_ART_INPUT = f"""
{MAGENTA}
    /\_/\
   ( ^_~ ) wink!    Waiting for your purr-ameters...
    > ^ <
   {cat_legs_ascii}
{ENDC}
"""

CAT_ART_PROJECT_NEW = f"""
{GREEN}
    /\_/\           ---------------------------------
   ( ^.^ )ニャー      New project cache established!
    > ^ <           Let the purr-oceedings begin!
   {cat_legs_ascii}          ---------------------------------
{ENDC}
"""

CAT_ART_PROJECT_LOAD = f"""
{BLUE}
    /\_/\           ---------------------------------
   ( o.o )          Project cache loaded!
    > ^ <           Ready for your commands.
   {cat_legs_ascii}          ---------------------------------
{ENDC}
"""

CAT_ART_PROJECT_FAIL = f"""
{YELLOW}
    /\_/\           ---------------------------------
   ( T_T )          Hmm, that project seems elusive...
    > ^ <           Could not create/load project.
   {cat_legs_ascii}          ---------------------------------
{ENDC}
"""

CAT_ART_LOG_ENTRY = f"""
{CYAN}
    /\_/\           ---------------------------------
   ( o.O ) zzZ       Noted! Adding to the cat-alogue...
    > ^ <           
   {cat_legs_ascii}          ---------------------------------
{ENDC}
"""

CAT_ART_TODO_ADD = f"""
{GREEN}
    /\_/\           ---------------------------------
   ( •̀ω•́ )✧       Task added to the Scratch List!
    > ^ <           Let's get it done!
   {cat_legs_ascii}          ---------------------------------
{ENDC}
"""

CAT_ART_TODO_LIST = f"""
{BLUE}
    /\_/\           ---------------------------------
   ( ◎ܫ◎)          Here's your Scratch List, boss!
    > ^ <           What's next on the agenda?
   {cat_legs_ascii}          ---------------------------------
{ENDC}
"""

CAT_ART_TODO_DONE = f"""
{MAGENTA}
    /\_/\           ---------------------------------
   ( ^０^ )        Another one bites the dust! Task done!
    > ^ <           Purr-fect progress!
   {cat_legs_ascii}          ---------------------------------
{ENDC}
"""

CAT_ART_PLUGIN_ADD = f"""
{GREEN}
    /\_/\           ------------------------------------
   (=◉ܫ◉=)         New component catalogued! Purr-ecise!
    > ^ <           Let's investigate this critter...
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_PLUGIN_LIST = f"""
{BLUE}
    /\_/\           ------------------------------------
   ( ♦_♦ )          Behold! The Catalog of Curious Components!
    > ^ <           Which plugin piques your interest?
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_PLUGIN_UPDATE = f"""
{CYAN}
    /\_/\           ------------------------------------
   ( ･ω･)ﾉ         Plugin details updated! Keeping tabs...
    > ^ <           
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""
CAT_ART_AJAX_ADD = f"""
{GREEN}
    /\_/\           ------------------------------------
   ( ¬‿¬ )          AJAX action sniffed out and noted! 
    > ω <           Let's see what it whispers...
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_AJAX_LIST = f"""
{BLUE}
    /\_/\           ------------------------------------
   ( dòдób )         The Whisker List of Web Hooks awaits!
    > ^ <           Which AJAX call shall we prod?
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_ASSET_ADD = f"""
{GREEN}
    /\_/\           ------------------------------------
   (=ච ω ච=)       New Meow-chine catalogued! Target acquired!
    > ^ <           Let's see what services it's purr-viding...
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_ASSET_LIST = f"""
{BLUE}
    /\_/\           ------------------------------------
   ( ▼д▼)          Behold! The Registry of Target Meow-chines!
    > ^ <           Which asset requires our fangs-on attention?
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_SERVICE_ADD = f"""
{CYAN}
    /\_/\           ------------------------------------
   ( o⚐ हान          Service paw-sitively identified and noted!
    > ^ <
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_FINDING_ADD = f"""
{GREEN}
    /\_/\           ------------------------------------
   ( detective )    A new clue for the collection! Purr-imary evidence!
    > . <           (Imagine a magnifying glass)
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_FINDING_LIST = f"""
{BLUE}
    /\_/\           ------------------------------------
   ( O_o )          Reviewing the Clue Collector Cache...
    > ? <           What secrets does it hold?
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

CAT_ART_IMPORTER = f"""
{MAGENTA}
    /\_/\           ------------------------------------
   ( >ω< )         Data Ingestion Purr-o-col Activated! 
    > ^ <           Feeding new insights to the cache...
   {cat_legs_ascii}          ------------------------------------
{ENDC}
"""

# --- Project Management Globals ---
BASE_PROJECTS_DIR = "PurrfectProjects"
CURRENT_PROJECT_NAME = None
CURRENT_PROJECT_PATH = None

FILE_SEPARATOR = "\n" + "="*35 + f" {CYAN}NEW FILE ENTRY{ENDC} " + "="*35 + "\n\n"
FLAT_FILE_SEPARATOR = "\n" + "="*30 + f" {MAGENTA}NEW SOURCE FLAT FILE BEGINS{ENDC} " + "="*30 + "\n\n"


# --- Helper Functions ---
def log_message(message, color=None, cat_art=None, no_cat_prefix=False):
    if cat_art: print(cat_art)
    prefix = "" if no_cat_prefix else f"{CYAN}[PurrBot]{ENDC} "
    print(f"{prefix}{color if color else ''}{message}{ENDC if color else ''}")

def get_paths_from_user(prompt_message, must_exist=True, allow_multiple=True, entity_type="path"):
    paths = []
    log_message(prompt_message, MAGENTA, no_cat_prefix=True)
    if allow_multiple: log_message("Enter paths separated by commas, or one path per line (empty line to finish).", YELLOW, no_cat_prefix=True)
    first_input = True
    while True:
        try:
            path_input = input(f"{BLUE}{'Path(s)' if first_input and allow_multiple else 'Path'}> {ENDC}").strip()
            if not path_input and not allow_multiple and not paths: 
                log_message("Input cannot be empty.", RED)
                continue
            if not path_input and (allow_multiple or paths): 
                break
            current_paths_raw = [p.strip() for p in path_input.split(',') if p.strip()] or ([path_input] if path_input else [])
            current_paths_expanded = [os.path.expanduser(p) for p in current_paths_raw]
            valid_line = True
            temp_line_paths = []
            for p_exp in current_paths_expanded:
                if must_exist and not os.path.exists(p_exp): 
                    log_message(f"Path '{p_exp}' not found.", RED)
                    valid_line=False; break
                if must_exist and entity_type=="dir" and not os.path.isdir(p_exp): 
                    log_message(f"'{p_exp}' not a directory.", RED)
                    valid_line=False; break
                if must_exist and entity_type=="file" and not os.path.isfile(p_exp): 
                    log_message(f"'{p_exp}' not a file.", RED)
                    valid_line=False; break
                temp_line_paths.append(p_exp)
            if valid_line: 
                paths.extend(temp_line_paths)
                first_input = False
            elif allow_multiple and ',' in path_input : 
                log_message("Re-enter line or one path per line.", YELLOW)
            if not allow_multiple and paths: 
                break
        except Exception as e: 
            log_message(f"Input error: {e}", RED, CAT_ART_ERROR)
            paths=[] 
    return paths

def get_output_filename_from_user(prompt_message, default_name):
    log_message(prompt_message, MAGENTA, no_cat_prefix=True)
    while True:
        filename = input(f"{BLUE}Output Filename (default: {default_name})> {ENDC}").strip() or default_name
        if not filename.strip(): 
            log_message("Filename empty.", RED)
            continue
        if any(c in filename for c in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']): 
            log_message("Invalid chars.", RED)
            continue
        return filename

def get_project_path(project_name=None):
    return os.path.join(BASE_PROJECTS_DIR, project_name) if project_name else CURRENT_PROJECT_PATH

def ensure_project_loaded(command_name="This command"):
    if not CURRENT_PROJECT_NAME: 
        log_message(f"{command_name} needs a project. Use 'load_project' or 'new_project'.", YELLOW, CAT_ART_THINKING)
        return False
    return True

def get_project_specific_path(sub_path, project_name_override=None):
    root = get_project_path(project_name_override) if project_name_override else CURRENT_PROJECT_PATH
    return os.path.join(root, sub_path) if root else None

def _get_enum_input(prompt_text, options, default_value, allow_empty_for_default=True):
    options_display = '/'.join(options)
    full_prompt = f"{BLUE}{prompt_text} ({options_display}, default: {default_value})> {ENDC}"
    user_input = input(full_prompt).strip()
    
    if not user_input and allow_empty_for_default:
        return default_value
    
    for opt in options: 
        if user_input.lower() == opt.lower():
            return opt 
    
    log_message(f"Invalid option. Using default '{default_value}'. Valid: {options_display}", YELLOW)
    return default_value

# --- Project Management Functions ---
# ... (All Project Management functions - Corrected and Verified) ...
def create_new_project():
    global CURRENT_PROJECT_NAME, CURRENT_PROJECT_PATH
    log_message("Create New Project", BOLD + MAGENTA, CAT_ART_INPUT)
    project_name_input = input(f"{BLUE}New project name> {ENDC}").strip()
    if not project_name_input:
        log_message("Project name cannot be empty.", RED)
        return
    if not re.match(r"^[a-zA-Z0-9_-]+$", project_name_input):
        log_message("Invalid project name (use alphanumeric, _, -).", RED)
        return
    project_path = get_project_path(project_name_input)
    if os.path.exists(project_path):
        log_message(f"Project '{project_name_input}' already exists.", YELLOW)
        load_confirmation = input(f"{BLUE}Load it? (y/N)> {ENDC}").lower()
        if load_confirmation == 'y': 
            load_project(project_name_input)
        return
    try:
        for sub in ["findings", "logs", "notes", "crawl_outputs"]: 
            os.makedirs(get_project_specific_path(sub, project_name_input), exist_ok=True)
        CURRENT_PROJECT_NAME = project_name_input
        CURRENT_PROJECT_PATH = os.path.abspath(project_path)
        log_message(f"Project '{CURRENT_PROJECT_NAME}' created and loaded.", GREEN, CAT_ART_PROJECT_NEW)
        log_action_automatic(f"Project '{CURRENT_PROJECT_NAME}' created.")
    except Exception as e: 
        log_message(f"Error creating project: {e}", RED, CAT_ART_PROJECT_FAIL)
        CURRENT_PROJECT_NAME = CURRENT_PROJECT_PATH = None

def load_project(project_name_to_load=None):
    global CURRENT_PROJECT_NAME, CURRENT_PROJECT_PATH
    p_name = project_name_to_load if project_name_to_load else input(f"{BLUE}Project name to load> {ENDC}").strip()
    if not p_name: 
        log_message("Project name empty.", RED)
        return
    project_path = get_project_path(p_name)
    if not os.path.isdir(project_path): 
        log_message(f"Project '{p_name}' not found.", RED, CAT_ART_PROJECT_FAIL)
        return
    CURRENT_PROJECT_NAME = p_name
    CURRENT_PROJECT_PATH = os.path.abspath(project_path)
    log_message(f"Project '{CURRENT_PROJECT_NAME}' loaded.", BLUE, CAT_ART_PROJECT_LOAD)
    try: 
        for sub in ["findings", "logs", "notes", "crawl_outputs"]: 
            os.makedirs(get_project_specific_path(sub), exist_ok=True)
    except Exception as e: 
        log_message(f"Warning: Could not verify subdirs for '{CURRENT_PROJECT_NAME}': {e}", YELLOW)

def display_current_project():
    if CURRENT_PROJECT_NAME: 
        log_message(f"Current project: {BOLD}{CURRENT_PROJECT_NAME}{ENDC} at {CURRENT_PROJECT_PATH}", CYAN)
    else: 
        log_message("No project loaded.", YELLOW, CAT_ART_THINKING)

def list_available_projects():
    log_message("Available Projects", BOLD + MAGENTA)
    if not os.path.isdir(BASE_PROJECTS_DIR) or not os.listdir(BASE_PROJECTS_DIR):
        log_message(f"No projects in '{BASE_PROJECTS_DIR}'. Use 'new_project'.", YELLOW)
        return
    projects = sorted([d for d in os.listdir(BASE_PROJECTS_DIR) if os.path.isdir(get_project_path(d))])
    if not projects: 
        log_message("No projects found.", YELLOW)
        return
    log_message("Your purr-ojects:", BLUE)
    for idx, p_name in enumerate(projects): 
        print(f"  {idx + 1}. {GREEN}{p_name}{ENDC}")
    if CURRENT_PROJECT_NAME and CURRENT_PROJECT_NAME in projects: 
        log_message(f"(Current: {BOLD}{CURRENT_PROJECT_NAME}{ENDC})", CYAN)


# --- Action Log Functions ---
# ... (As in previous script, with standardized UTC ISO timestamps) ...
def log_action_automatic(description):
    if not CURRENT_PROJECT_PATH: return
    log_file = get_project_specific_path("logs/action_log.txt")
    if not log_file: return
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'a', encoding='utf-8') as f: 
            f.write(f"[{datetime.datetime.now(timezone.utc).isoformat()}] [AUTO] - {description}\n")
    except Exception: pass

def log_action_manual():
    if not ensure_project_loaded("Logging action"): return
    log_message("Log Manual Action", BOLD + MAGENTA, CAT_ART_INPUT)
    desc = input(f"{BLUE}Describe action> {ENDC}").strip()
    if not desc: 
        log_message("Description empty.", RED)
        return
    log_file = get_project_specific_path("logs/action_log.txt")
    if not log_file: 
        log_message("Error: Log path.", RED)
        return
    try:
        with open(log_file, 'a', encoding='utf-8') as f: 
            f.write(f"[{datetime.datetime.now(timezone.utc).isoformat()}] [MANUAL] - {desc}\n")
        log_message("Action logged!", GREEN, CAT_ART_LOG_ENTRY)
    except Exception as e: 
        log_message(f"Error writing log: {e}", RED, CAT_ART_ERROR)

def view_action_log():
    if not ensure_project_loaded("Viewing log"): return
    log_message("Action Log", BOLD + MAGENTA)
    log_file = get_project_specific_path("logs/action_log.txt")
    if not log_file or not os.path.exists(log_file): 
        log_message("Log empty/not found.", YELLOW, CAT_ART_THINKING)
        return
    num_last = input(f"{BLUE}Entries to show (e.g. 10, 'all')> {ENDC}").strip().lower()
    grep_kw = input(f"{BLUE}Keyword filter (empty for none)> {ENDC}").strip().lower()
    try:
        with open(log_file, 'r', encoding='utf-8') as f: lines = f.readlines()
        if grep_kw: lines = [l for l in lines if grep_kw in l.lower()]
        if not lines: 
            log_message("No matching entries.", YELLOW)
            return
        to_show = len(lines) if num_last == 'all' else (int(num_last) if num_last.isdigit() and int(num_last)>0 else len(lines))
        log_message(f"--- Last {min(to_show, len(lines))} of {len(lines)} matching entries ---", CYAN)
        for line in lines[-to_show:]: 
            print(f"{GREEN}{line.strip()}{ENDC}")
        log_message("--- End of Log ---", CYAN)
    except ValueError: 
        log_message("Invalid number.", YELLOW)
        _display_lines_helper(lines, grep_kw) 
    except Exception as e: 
        log_message(f"Error reading log: {e}", RED, CAT_ART_ERROR)

def _display_lines_helper(lines_to_display, keyword=""): 
    log_message(f"--- Displaying all matching for '{keyword}' ---" if keyword else "--- Displaying all ---", CYAN)
    for line_item in lines_to_display: 
        print(f"{GREEN}{line_item.strip()}{ENDC}")
    log_message("--- End of Log ---", CYAN)

# --- To-Do List Functions ---
# ... (All To-Do functions, with syntax corrections and standardized UTC ISO timestamps)
def get_todos_filepath(): return get_project_specific_path("notes/todos.json")
def load_todos():
    fp = get_todos_filepath();
    if not fp or not os.path.exists(fp): return []
    try:
        with open(fp,'r',encoding='utf-8') as f: data = json.load(f)
        for task in data: 
            task.setdefault('severity', "None")
            task.setdefault('category', "General")
            task.setdefault('target', "N/A")
            task.setdefault('creation_date', datetime.datetime.now(timezone.utc).isoformat()) 
            task.setdefault('last_modified_date', task['creation_date'])
        return data
    except Exception as e: 
        log_message(f"Corrupted todos.json. Error: {e}. Starting with empty list.",YELLOW)
        return []
def save_todos(todos):
    fp = get_todos_filepath();
    if not fp: 
        log_message("No project for todos.",RED)
        return False
    try:
        os.makedirs(os.path.dirname(fp),exist_ok=True);
        with open(fp,'w',encoding='utf-8') as f: json.dump(todos,f,indent=4)
        return True
    except Exception as e: 
        log_message(f"Error saving todos: {e}",RED)
        return False
def get_next_todo_id(todos): return max([t.get("id",0) for t in todos]+[0])+1
def _update_task_modification_date(task): task["last_modified_date"]=datetime.datetime.now(timezone.utc).isoformat()

def add_todo_item():
    if not ensure_project_loaded("Adding todo"): return
    log_message("Add New To-Do",BOLD+MAGENTA,CAT_ART_TODO_ADD)
    desc=input(f"{BLUE}Desc> {ENDC}").strip()
    if not desc:
        log_message("Desc empty.",RED)
        return
    pri_opts=["High","Medium","Low","Triage"]; pri = _get_enum_input("Pri", pri_opts, "Triage")
    sev_opts=["Critical","High","Medium","Low","Informational","None"]; sev = _get_enum_input("Sev", sev_opts, "None")
    cat_in=input(f"{BLUE}Cat (opt, default: General)> {ENDC}").strip(); cat = cat_in if cat_in else "General"
    tgt_in=input(f"{BLUE}Tgt (opt, default: N/A)> {ENDC}").strip(); tgt = tgt_in if tgt_in else "N/A"
    todos=load_todos();now_utc_iso=datetime.datetime.now(timezone.utc).isoformat()
    new_t={"id":get_next_todo_id(todos),"description":desc,"priority":pri,"severity":sev,"status":"Pending","category":cat,"target":tgt,"creation_date":now_utc_iso,"last_modified_date":now_utc_iso,"completion_date":None}
    todos.append(new_t)
    if save_todos(todos):
        log_message(f"Task ID {new_t['id']} added.",GREEN,CAT_ART_SUCCESS)
        log_action_automatic(f"Added ToDo ID {new_t['id']}: '{desc}'")

def list_todo_items():
    if not ensure_project_loaded("Listing todos"): return
    log_message("To-Do List",BOLD+MAGENTA,CAT_ART_TODO_LIST);todos=load_todos()
    if not todos:
        log_message("List empty!",YELLOW)
        return
    status_options = ["Pending", "In Progress", "Done", "All"]
    f_st = _get_enum_input("Filter Status", status_options, "Pending")

    pri_opts_f=["High","Medium","Low","Triage","All"]; f_pri = _get_enum_input("Filter Pri", pri_opts_f, "All")
    sev_opts_f=["Critical","High","Medium","Low","Informational","None","All"]; f_sev = _get_enum_input("Filter Sev", sev_opts_f, "All")
    
    f_cat=input(f"{BLUE}Filter Cat (empty for all)> {ENDC}").strip()
    f_tgt=input(f"{BLUE}Filter Tgt (empty for all)> {ENDC}").strip()
    sort_new=input(f"{BLUE}Sort newest first? (y/N)> {ENDC}").lower()=='y'
    
    filtered=[t for t in todos if(f_st=="All"or t.get("status")==f_st)and(f_pri=="All"or t.get("priority")==f_pri)and(f_sev=="All"or t.get("severity","None")==f_sev)and(not f_cat or t.get("category","").lower()==f_cat.lower())and(not f_tgt or t.get("target","").lower()==f_tgt.lower())]
    if not filtered:
        log_message("No tasks match filters.",YELLOW)
        return
    if sort_new:filtered.sort(key=lambda x:x.get("creation_date","0"),reverse=True)
    else:pri_order={"High":0,"Medium":1,"Low":2,"Triage":3};filtered.sort(key=lambda x:(pri_order.get(x.get("priority","Triage"),3),x.get("id",0)))
    log_message(f"\n--- Filtered Tasks ({len(filtered)}) ---",CYAN)
    for t in filtered:
        s_c=GREEN if t.get("status")=="Done" else YELLOW if t.get("status")=="In Progress" else RED;pri_v=t.get("priority","Triage");pri_c=RED if pri_v=="High" else YELLOW if pri_v=="Medium" else BLUE if pri_v=="Low" else WHITE;sev_v=t.get("severity","None");sev_map={"Critical":BOLD+RED,"High":RED,"Medium":YELLOW,"Low":BLUE,"Informational":CYAN,"None":WHITE};sev_c=sev_map.get(sev_v,WHITE)
        print(f"  {BOLD}ID:{t.get('id')}{ENDC}|{s_c}Status:{t.get('status')}{ENDC}|{pri_c}Pri:{pri_v}{ENDC}|{sev_c}Sev:{sev_v}{ENDC}")
        print(f"    Task:{BLUE}{t.get('description')}{ENDC}\n    Cat:{CYAN}{t.get('category','N/A')}{ENDC}|Tgt:{CYAN}{t.get('target','N/A')}{ENDC}")
        cd_iso=t.get('creation_date','N/A'); md_iso=t.get('last_modified_date',cd_iso); age=""
        try:
            cr_dt = datetime.datetime.fromisoformat(cd_iso.replace("Z", "+00:00")) if isinstance(cd_iso, str) else None
            if cr_dt:
                if cr_dt.tzinfo is None: cr_dt = cr_dt.replace(tzinfo=timezone.utc) 
                d = datetime.datetime.now(timezone.utc) - cr_dt
                if d.days > 0: age=f" ({d.days}d ago)"
                elif d.seconds//3600 > 0: age=f" ({d.seconds//3600}h ago)"
                elif d.seconds//60 > 0: age=f" ({d.seconds//60}m ago)"
                else: age=" (Just now)"
        except Exception: pass 
        completion_date_str = f"|Completed:{t.get('completion_date')}" if t.get("status")=="Done"and t.get("completion_date") else ""
        print(f"    Created:{cd_iso}{age} | Modified:{md_iso} {completion_date_str}");print("    "+"-"*40)
    log_message("--- End of Scratch List ---",CYAN)


def _find_todo_by_id(id_str):
    if not id_str or not id_str.isdigit():
        log_message("Invalid ID.",RED)
        return None,None
    id_val=int(id_str)
    todos=load_todos()
    for t in todos:
        if t.get("id")==id_val:return t,todos
    log_message(f"Task ID {id_val} not found.",RED);return None,None

def mark_todo_done(id_val=None):
    if not ensure_project_loaded("Marking todo"):return
    id_s=id_val if id_val else input(f"{BLUE}ID to mark done> {ENDC}").strip()
    task,todos=_find_todo_by_id(id_s)
    if task:
        if task["status"]=="Done":
            log_message(f"Task {task['id']} already done.",YELLOW)
            return
        task["status"]="Done"
        task["completion_date"]=datetime.datetime.now(timezone.utc).isoformat() 
        _update_task_modification_date(task)
        if save_todos(todos):
            log_message(f"Task {task['id']} marked done!",GREEN,CAT_ART_TODO_DONE)
            log_action_automatic(f"Marked ToDo ID {task['id']} Done: '{task['description']}'")

def edit_todo_item(id_val=None):
    if not ensure_project_loaded("Editing todo"): return
    id_s = id_val if id_val else input(f"{BLUE}ID to edit> {ENDC}").strip()
    task, todos = _find_todo_by_id(id_s)
    if not task: return
    log_message(f"Editing Task ID: {task['id']}", BOLD + MAGENTA,CAT_ART_INPUT); original_task_copy = task.copy()

    new_desc = input(f"{BLUE}New Desc (curr:'{task.get('description', 'N/A')}')> {ENDC}").strip()
    if new_desc: task["description"] = new_desc
    
    pri_opts=["High","Medium","Low","Triage"]; current_pri = task.get('priority', 'Triage')
    new_pri_in = _get_enum_input("New Pri", pri_opts, current_pri, allow_empty_for_default=False)
    if new_pri_in : task["priority"]=new_pri_in
    elif input(f"{YELLOW}Keep current priority '{current_pri}'? (Y/n)> {ENDC}").lower() == 'n':
        task["priority"] = _get_enum_input("Re-enter Pri", pri_opts, "Triage")
        
    sev_opts=["Critical","High","Medium","Low","Informational","None"]; current_sev = task.get('severity','None')
    new_sev_in= _get_enum_input("New Sev", sev_opts, current_sev, allow_empty_for_default=False)
    if new_sev_in: task["severity"]=new_sev_in
    elif input(f"{YELLOW}Keep current severity '{current_sev}'? (Y/n)> {ENDC}").lower() == 'n':
        task["severity"] = _get_enum_input("Re-enter Sev", sev_opts, "None")

    current_cat = task.get('category','General')
    new_cat_val = input(f"{BLUE}New Cat (curr:'{current_cat}')> {ENDC}").strip()
    if new_cat_val: task["category"] = new_cat_val
    elif new_cat_val == "" and input(f"{YELLOW}Keep current category '{current_cat}' (set to General if clearing)? (Y/n)> {ENDC}").lower() == 'n': 
        task["category"] = input(f"{BLUE}Re-enter Cat (default: General)> {ENDC}").strip() or "General"
    elif new_cat_val == "" and current_cat != "General": # Explicitly clear to default
         if input(f"{YELLOW}Clear current category '{current_cat}' (set to General)? (y/N)> {ENDC}").lower() == 'y': task["category"]="General"

    current_tgt = task.get('target','N/A')
    new_tgt = input(f"{BLUE}New Tgt (curr:'{current_tgt}')> {ENDC}").strip()
    if new_tgt: task["target"] = new_tgt
    elif new_tgt == "" and current_tgt != "N/A":
        if input(f"{YELLOW}Clear current target '{current_tgt}' (set to N/A)? (y/N)> {ENDC}").lower() == 'y': task["target"]="N/A"

    stat_opts=["Pending","In Progress","Done"]; current_stat = task.get('status')
    new_stat_in= _get_enum_input("New Status", stat_opts, current_stat, allow_empty_for_default=False)
    if new_stat_in: task["status"]=new_stat_in
    elif input(f"{YELLOW}Keep current status '{current_stat}'? (Y/n)> {ENDC}").lower() == 'n':
        task["status"] = _get_enum_input("Re-enter Status", stat_opts, "Pending")

    if task["status"]=="Done" and not task.get("completion_date"): 
        task["completion_date"]=datetime.datetime.now(timezone.utc).isoformat()
    elif task["status"]!="Done": 
        task["completion_date"]=None
    
    _update_task_modification_date(task)
    if save_todos(todos):
        log_message(f"Task ID {task['id']} updated.",GREEN)
        chgs=[f"{k}:'{original_task_copy.get(k)}'->'{task.get(k)}'" for k in["description","priority","severity","category","target","status"]if original_task_copy.get(k)!=task.get(k)]
        log_action_automatic(f"Edited ToDo ID {task['id']}. Changes: {'; '.join(chgs)if chgs else'No textual change'}.")

def remove_todo_item(id_val=None):
    if not ensure_project_loaded("Removing todo"):return
    id_s=id_val if id_val else input(f"{BLUE}ID to remove> {ENDC}").strip()
    task,todos=_find_todo_by_id(id_s);
    if not task:return
    desc_log=task['description']
    todos = [t for t in todos if t.get("id") != task.get("id")] 
    if save_todos(todos):
        log_message(f"Task ID {task['id']} removed.",GREEN)
        log_action_automatic(f"Removed ToDo ID {task['id']}: '{desc_log}'")

# --- Plugin Tracker Functions ---
# ... (All Plugin Tracker functions - Corrected and Verified)
def get_plugins_filepath(): return get_project_specific_path("findings/plugins.json")
def load_plugins():
    fp=get_plugins_filepath();
    if not fp or not os.path.exists(fp):return[]
    try:
        with open(fp,'r',encoding='utf-8')as f: data = json.load(f)
        for p_entry in data:
            p_entry.setdefault('date_added', datetime.datetime.now(timezone.utc).isoformat())
            p_entry.setdefault('last_updated', p_entry['date_added'])
        return data
    except Exception as e:log_message(f"Corrupted plugins.json. Error: {e}",YELLOW);return[]
def save_plugins(plugins):
    fp=get_plugins_filepath();
    if not fp:log_message("No project for plugins.",RED);return False
    try:
        os.makedirs(os.path.dirname(fp),exist_ok=True);
        with open(fp,'w',encoding='utf-8')as f:json.dump(plugins,f,indent=4)
        return True
    except Exception as e:log_message(f"Error saving plugins:{e}",RED);return False
def get_next_plugin_id(plugins):return max([p.get("plugin_id",0)for p in plugins]+[0])+1
def _update_plugin_modification_date(p_entry):p_entry["last_updated"]=datetime.datetime.now(timezone.utc).isoformat()

def add_plugin_entry():
    if not ensure_project_loaded("Adding plugin"):return
    log_message("Add New Plugin",BOLD+MAGENTA,CAT_ART_PLUGIN_ADD)
    slug=input(f"{BLUE}Slug> {ENDC}").strip().lower()
    if not slug:
        log_message("Slug empty.",RED)
        return
    hosts_in=input(f"{BLUE}Target Host(s) (csv)> {ENDC}").strip()
    hosts_list=[h.strip()for h in hosts_in.split(',')if h.strip()]if hosts_in else["N/A"]
    ver_obs=input(f"{BLUE}Version Observed (for all hosts)> {ENDC}").strip()or"Unknown"
    old_ver=input(f"{BLUE}Oldest Version Known (opt, for all)> {ENDC}").strip()or ver_obs
    stat_opts=["To Investigate","Needs Version Check","Known Vulnerable","Testing PoC","Patched","Not Vulnerable","Informational","Monitor"]
    status = _get_enum_input("Status", stat_opts, "To Investigate")
    
    cves_in=input(f"{BLUE}CVEs (csv,for all)> {ENDC}").strip()
    cves=[c.strip().upper()for c in cves_in.split(',')if c.strip()]if cves_in else[]
    src_path=input(f"{BLUE}Source of Discovery (opt)> {ENDC}").strip()or"N/A"
    readme=input(f"{BLUE}Readme Snippet (opt,max 200)> {ENDC}").strip()[:200]or"N/A"
    notes=input(f"{BLUE}Notes (opt)> {ENDC}").strip()or"N/A"
    plugins=load_plugins();added_c=0;now_utc_iso=datetime.datetime.now(timezone.utc).isoformat()
    for host_entry in hosts_list:
        new_id=get_next_plugin_id(plugins)
        new_p={"plugin_id":new_id,"plugin_slug":slug,"target_host":host_entry,"version_observed":ver_obs,"oldest_version_known":old_ver,"status":status,"cve_ids":cves.copy(),"source_of_discovery_path":src_path,"readme_content_snippet":readme,"notes":notes,"date_added":now_utc_iso,"last_updated":now_utc_iso}
        plugins.append(new_p)
        log_message(f"Prep entry for '{slug}' on '{host_entry}' (ID:{new_id}).",CYAN,no_cat_prefix=True)
        added_c+=1
    if added_c>0 and save_plugins(plugins):
        log_message(f"Added {added_c} entries for '{slug}'.",GREEN,CAT_ART_SUCCESS)
        log_action_automatic(f"Added {added_c} entries for Plugin '{slug}' v{ver_obs}. Hosts:{', '.join(hosts_list)}")
    elif added_c==0:
        log_message(f"No valid hosts for '{slug}'.",YELLOW)

def _display_plugin_details(p):
    s_map={"To Investigate":YELLOW,"Needs Version Check":YELLOW,"Known Vulnerable":RED,"Testing PoC":MAGENTA,"Patched":GREEN,"Not Vulnerable":GREEN,"Informational":CYAN,"Monitor":BLUE};s_c=s_map.get(p.get('status',"N/A"),WHITE)
    print(f"  {BOLD}ID:{p.get('plugin_id')}{ENDC}|Slug:{BLUE}{p.get('plugin_slug')}{ENDC}|Tgt:{CYAN}{p.get('target_host')}{ENDC}\n    VerObs:{p.get('version_observed')}|Oldest:{p.get('oldest_version_known')}\n    Status:{s_c}{p.get('status')}{ENDC}\n    CVEs:{RED if p.get('cve_ids')else WHITE}{', '.join(p.get('cve_ids',[]))or'None'}{ENDC}\n    Src:{p.get('source_of_discovery_path')}|Readme:{p.get('readme_content_snippet')}\n    Notes:{p.get('notes')}\n    Added:{p.get('date_added')}|Updated:{p.get('last_updated')}\n    "+"-"*40)

def list_plugin_entries():
    if not ensure_project_loaded("Listing plugins"):return
    log_message("Plugin Catalog",BOLD+MAGENTA,CAT_ART_PLUGIN_LIST);plugins=load_plugins()
    if not plugins:log_message("Catalog empty.",YELLOW);return
    f_slug=input(f"{BLUE}Filter Slug (empty for all)> {ENDC}").strip().lower()
    f_tgt=input(f"{BLUE}Filter Target (empty for all)> {ENDC}").strip()
    stat_opts_f = ["To Investigate","Needs Version Check","Known Vulnerable","Testing PoC","Patched","Not Vulnerable","Informational","Monitor", "All"]
    f_stat = _get_enum_input("Filter Status", stat_opts_f, "All")
    
    f_cve=input(f"{BLUE}Filter Has CVEs? (y/n/a, def:a)> {ENDC}").strip().lower()
    filtered=[p for p in plugins if(not f_slug or p.get("plugin_slug","").lower()==f_slug)and(not f_tgt or p.get("target_host","").lower()==f_tgt.lower())and(f_stat=="All" or p.get("status","")==f_stat)and(f_cve=="a"or(f_cve=="y"and p.get("cve_ids"))or(f_cve=="n"and not p.get("cve_ids")))]
    if not filtered:log_message("No plugins match filters.",YELLOW);return
    filtered.sort(key=lambda x:(x.get("plugin_slug",""),x.get("version_observed","")))
    log_message(f"\n--- Filtered Plugins ({len(filtered)}) ---",CYAN)
    for p_entry in filtered: _display_plugin_details(p_entry)
    log_message("--- End of Catalog ---",CYAN)

def _find_plugin_by_id(id_str):
    if not id_str or not id_str.isdigit():
        log_message("Invalid ID.",RED)
        return None,None
    id_val=int(id_str);plugins=load_plugins()
    for p in plugins:
        if p.get("plugin_id")==id_val:return p,plugins
    log_message(f"Plugin ID {id_val} not found.",RED);return None,None

def view_plugin_details(id_val=None):
    if not ensure_project_loaded("Viewing plugin"):return
    id_s=id_val if id_val else input(f"{BLUE}Plugin ID to view> {ENDC}").strip()
    plugin,_=_find_plugin_by_id(id_s)
    if plugin:
        log_message(f"Details for Plugin ID:{plugin['plugin_id']}",BOLD+CYAN,no_cat_prefix=True)
        _display_plugin_details(plugin)

def update_plugin_entry(id_val=None): 
    if not ensure_project_loaded("Updating plugin"):return
    id_s=id_val if id_val else input(f"{BLUE}Plugin ID to update> {ENDC}").strip()
    plugin,plugins=_find_plugin_by_id(id_s);
    if not plugin:return
    log_message(f"Updating Plugin ID:{plugin['plugin_id']}",BOLD+MAGENTA,CAT_ART_INPUT);orig=plugin.copy()
    
    new_ver=input(f"{BLUE}New VerObs (curr:{plugin['version_observed']})> {ENDC}").strip()
    if new_ver:
        plugin['version_observed']=new_ver
    elif new_ver == "" and input(f"{YELLOW}Clear current version '{plugin['version_observed']}' (set to Unknown)? (y/N)> {ENDC}").lower() == 'y': 
        plugin['version_observed']="Unknown"

    stat_opts=["To Investigate","Needs Version Check","Known Vulnerable","Testing PoC","Patched","Not Vulnerable","Informational","Monitor"]
    current_status = plugin.get('status')
    new_stat = _get_enum_input("New Status", stat_opts, current_status, allow_empty_for_default=False)
    if new_stat: 
        plugin['status']=new_stat
    elif input(f"{YELLOW}Keep current status '{current_status}'? (Y/n)> {ENDC}").lower() == 'n':
         plugin['status'] = _get_enum_input("Re-enter Status", stat_opts, "To Investigate")
        
    new_cves=input(f"{BLUE}New CVEs (csv,curr:{','.join(plugin.get('cve_ids',[]))},'clear' to empty)> {ENDC}").strip()
    if new_cves.lower()=='clear':
        plugin['cve_ids']=[]
    elif new_cves:
        plugin['cve_ids']=[c.strip().upper()for c in new_cves.split(',')if c.strip()]
    
    current_notes = plugin.get('notes','N/A')
    new_notes=input(f"{BLUE}Update Notes (curr:'{current_notes}')> {ENDC}").strip()
    if new_notes:
        plugin['notes']=new_notes
    elif new_notes == "" and input(f"{YELLOW}Clear current notes '{current_notes}'? (y/N)> {ENDC}").lower() == 'y': 
        plugin['notes']="N/A"

    _update_plugin_modification_date(plugin)
    if save_plugins(plugins):
        log_message(f"Plugin ID {plugin['plugin_id']} updated.",GREEN,CAT_ART_PLUGIN_UPDATE)
        chgs=[f"{k}:'{orig.get(k)}'->'{plugin.get(k)}'"for k in["version_observed","status","cve_ids","notes"]if orig.get(k)!=plugin.get(k)]
        log_action_automatic(f"Updated Plugin ID {plugin['plugin_id']}({plugin['plugin_slug']}).Changes:{'; '.join(chgs)if chgs else'No change'}.")

def remove_plugin_entry(id_val=None):
    if not ensure_project_loaded("Removing plugin"):return
    id_s=id_val if id_val else input(f"{BLUE}Plugin ID to remove> {ENDC}").strip()
    plugin,plugins=_find_plugin_by_id(id_s);
    if not plugin:return
    slug_log=plugin['plugin_slug']
    plugins = [p for p in plugins if p.get("plugin_id") != plugin.get("plugin_id")] 
    if save_plugins(plugins):
        log_message(f"Plugin ID {plugin['plugin_id']} removed.",GREEN)
        log_action_automatic(f"Removed Plugin ID {plugin['plugin_id']}:'{slug_log}'")

# --- AJAX Action Tracker Functions ---
# ... (All AJAX Tracker functions - Corrected and Verified)
def get_ajax_actions_filepath(): return get_project_specific_path("findings/ajax_actions.json")
def load_ajax_actions():
    fp=get_ajax_actions_filepath();
    if not fp or not os.path.exists(fp):return[]
    try:
        with open(fp,'r',encoding='utf-8')as f: data = json.load(f)
        for item in data:
            item.setdefault('date_added', datetime.datetime.now(timezone.utc).isoformat())
            item.setdefault('last_updated', item['date_added'])
        return data
    except Exception as e:log_message(f"Corrupted ajax_actions.json. Error: {e}",YELLOW);return[]
def save_ajax_actions(actions):
    fp=get_ajax_actions_filepath();
    if not fp:log_message("No project for AJAX actions.",RED);return False
    try:
        os.makedirs(os.path.dirname(fp),exist_ok=True);
        with open(fp,'w',encoding='utf-8')as f:json.dump(actions,f,indent=4)
        return True
    except Exception as e:log_message(f"Error saving AJAX actions:{e}",RED);return False
def get_next_ajax_id(actions):return max([a.get("ajax_id",0)for a in actions]+[0])+1
def _update_ajax_action_modification_date(a_entry):a_entry["last_updated"]=datetime.datetime.now(timezone.utc).isoformat()

def add_ajax_action_entry():
    if not ensure_project_loaded("Adding AJAX action"):return
    log_message("Add New AJAX Action",BOLD+MAGENTA,CAT_ART_AJAX_ADD)
    name=input(f"{BLUE}AJAX Name> {ENDC}").strip()
    if not name:
        log_message("Name empty.",RED)
        return
    host=input(f"{BLUE}Target Host> {ENDC}").strip()or"N/A"
    p_src=input(f"{BLUE}Source Plugin (opt)> {ENDC}").strip()or"Unknown"
    priv_opts=["nopriv","auth","admin","specific_capability","Unknown"]
    priv = _get_enum_input("Privilege", priv_opts, "Unknown")
    
    stat_opts=["Pending Test","Tested - Benign","Tested - Interesting Output","Tested - Vulnerable","Needs Further Investigation","Monitor"]
    status = _get_enum_input("Test Status", stat_opts, "Pending Test")
    
    meth_in=input(f"{BLUE}HTTP Methods (csv,def:GET,POST)> {ENDC}").strip().upper()
    methods=[m.strip()for m in meth_in.split(',')if m.strip()]if meth_in else["GET","POST"]
    params_in=input(f"{BLUE}Interesting Params (csv,opt)> {ENDC}").strip()
    params=[p.strip()for p in params_in.split(',')if p.strip()]if params_in else[]
    cves_in=input(f"{BLUE}Related CVEs (csv,opt)> {ENDC}").strip()
    cves=[c.strip().upper()for c in cves_in.split(',')if c.strip()]if cves_in else[]
    src_disc=input(f"{BLUE}Source of Discovery (opt)> {ENDC}").strip()or"N/A"
    notes=input(f"{BLUE}Notes (opt)> {ENDC}").strip()or"N/A"
    actions=load_ajax_actions();now_utc_iso=datetime.datetime.now(timezone.utc).isoformat()
    new_a={"ajax_id":get_next_ajax_id(actions),"action_name":name,"target_host":host,"plugin_source_slug":p_src,"privilege_level":priv,"test_status":status,"http_methods_observed":methods,"interesting_parameters":params,"cve_ids_related":cves,"source_of_discovery":src_disc,"notes":notes,"date_added":now_utc_iso,"last_updated":now_utc_iso}
    actions.append(new_a)
    if save_ajax_actions(actions):
        log_message(f"AJAX '{name}'(ID:{new_a['ajax_id']})added.",GREEN,CAT_ART_SUCCESS)
        log_action_automatic(f"Added AJAX ID {new_a['ajax_id']}:'{name}'for {host}")

def _display_ajax_action_details(a):
    s_map={"Pending Test":YELLOW,"Tested - Benign":GREEN,"Tested - Interesting Output":CYAN,"Tested - Vulnerable":RED,"Needs Further Investigation":MAGENTA,"Monitor":BLUE};s_c=s_map.get(a.get('test_status',"N/A"),WHITE)
    p_map={"nopriv":RED,"auth":YELLOW,"admin":MAGENTA,"specific_capability":BLUE,"Unknown":WHITE};p_c=p_map.get(a.get('privilege_level',"N/A"),WHITE)
    print(f"  {BOLD}ID:{a.get('ajax_id')}{ENDC}|Name:{BLUE}{a.get('action_name')}{ENDC}|Tgt:{CYAN}{a.get('target_host')}{ENDC}\n    Plugin Src:{a.get('plugin_source_slug')}|Priv:{p_c}{a.get('privilege_level')}{ENDC}\n    Test Status:{s_c}{a.get('test_status')}{ENDC}\n    Methods:{', '.join(a.get('http_methods_observed',[]))or'None'}|Params:{', '.join(a.get('interesting_parameters',[]))or'None'}\n    CVEs:{RED if a.get('cve_ids_related')else WHITE}{', '.join(a.get('cve_ids_related',[]))or'None'}{ENDC}\n    Discovered Via:{a.get('source_of_discovery')}|Notes:{a.get('notes')}\n    Added:{a.get('date_added')}|Updated:{a.get('last_updated')}\n    "+"-"*40)

def list_ajax_action_entries():
    if not ensure_project_loaded("Listing AJAX"):return
    log_message("AJAX Whisker List",BOLD+MAGENTA,CAT_ART_AJAX_LIST);actions=load_ajax_actions()
    if not actions:log_message("List empty.",YELLOW);return
    f_name=input(f"{BLUE}Filter Name (contains,empty for all)> {ENDC}").strip().lower()
    f_tgt=input(f"{BLUE}Filter Target (empty for all)> {ENDC}").strip()
    stat_opts_f = ["Pending Test","Tested - Benign","Tested - Interesting Output","Tested - Vulnerable","Needs Further Investigation","Monitor","All"]
    f_stat = _get_enum_input("Filter Status", stat_opts_f, "All")
    priv_opts_f = ["nopriv","auth","admin","specific_capability","Unknown","All"]
    f_priv = _get_enum_input("Filter Privilege", priv_opts_f, "All")
    
    filtered=[a for a in actions if(not f_name or f_name in a.get("action_name","").lower())and(not f_tgt or a.get("target_host","").lower()==f_tgt.lower())and(f_stat=="All" or a.get("test_status","")==f_stat)and(f_priv=="All" or a.get("privilege_level","").lower()==f_priv)]
    if not filtered:log_message("No AJAX actions match.",YELLOW);return
    filtered.sort(key=lambda x:(x.get("action_name",""),x.get("target_host","")))
    log_message(f"\n--- Filtered AJAX Actions ({len(filtered)}) ---",CYAN)
    for ajax_entry in filtered: _display_ajax_action_details(ajax_entry)
    log_message("--- End of List ---",CYAN)

def _find_ajax_action_by_id(id_str):
    if not id_str or not id_str.isdigit():
        log_message("Invalid ID.",RED)
        return None,None
    id_val=int(id_str);actions=load_ajax_actions()
    for a in actions:
        if a.get("ajax_id")==id_val:return a,actions
    log_message(f"AJAX ID {id_val} not found.",RED);return None,None

def view_ajax_action_details(id_val=None):
    if not ensure_project_loaded("Viewing AJAX"):return
    id_s=id_val if id_val else input(f"{BLUE}AJAX ID to view> {ENDC}").strip()
    action,_=_find_ajax_action_by_id(id_s)
    if action:
        log_message(f"Details for AJAX ID:{action['ajax_id']}",BOLD+CYAN,no_cat_prefix=True)
        _display_ajax_action_details(action)

def update_ajax_action_entry(id_val=None):
    if not ensure_project_loaded("Updating AJAX"):return
    id_s=id_val if id_val else input(f"{BLUE}AJAX ID to update> {ENDC}").strip()
    action,actions=_find_ajax_action_by_id(id_s);
    if not action:return
    log_message(f"Updating AJAX ID:{action['ajax_id']}",BOLD+MAGENTA,CAT_ART_INPUT);orig=action.copy()
    
    priv_opts=["nopriv","auth","admin","specific_capability","Unknown"]
    current_priv = action.get('privilege_level')
    new_priv = _get_enum_input("New Priv", priv_opts, current_priv, allow_empty_for_default=False)
    if new_priv: action['privilege_level']=new_priv
    elif input(f"{YELLOW}Keep current privilege '{current_priv}'? (Y/n)> {ENDC}").lower() == 'n':
        action['privilege_level'] = _get_enum_input("Re-enter Priv", priv_opts, "Unknown")

    stat_opts=["Pending Test","Tested - Benign","Tested - Interesting Output","Tested - Vulnerable","Needs Further Investigation","Monitor"]
    current_stat = action.get('test_status')
    new_stat = _get_enum_input("New Test Status", stat_opts, current_stat, allow_empty_for_default=False)
    if new_stat: action['test_status']=new_stat
    elif input(f"{YELLOW}Keep current status '{current_stat}'? (Y/n)> {ENDC}").lower() == 'n':
        action['test_status'] = _get_enum_input("Re-enter Status", stat_opts, "Pending Test")
        
    new_cves=input(f"{BLUE}Update CVEs (csv,curr:{','.join(action.get('cve_ids_related',[]))},'clear' to empty)> {ENDC}").strip()
    if new_cves.lower()=='clear':action['cve_ids_related']=[]
    elif new_cves:action['cve_ids_related']=[c.strip().upper()for c in new_cves.split(',')if c.strip()]
    
    current_notes = action.get('notes','N/A')
    new_notes=input(f"{BLUE}Update Notes (curr:'{current_notes}')> {ENDC}").strip()
    if new_notes: action['notes']=new_notes
    elif new_notes == "" and input(f"{YELLOW}Clear current notes '{current_notes}'? (y/N)> {ENDC}").lower() == 'y': action['notes']="N/A"

    _update_ajax_action_modification_date(action)
    if save_ajax_actions(actions):
        log_message(f"AJAX ID {action['ajax_id']} updated.",GREEN,CAT_ART_PLUGIN_UPDATE)
        chgs=[f"{k}:'{orig.get(k)}'->'{action.get(k)}'"for k in["privilege_level","test_status","cve_ids_related","notes"]if orig.get(k)!=action.get(k)]
        log_action_automatic(f"Updated AJAX ID {action['ajax_id']}({action['action_name']}).Changes:{'; '.join(chgs)if chgs else'No change'}.")

def remove_ajax_action_entry(id_val=None):
    if not ensure_project_loaded("Removing AJAX"):return
    id_s=id_val if id_val else input(f"{BLUE}AJAX ID to remove> {ENDC}").strip()
    action,actions=_find_ajax_action_by_id(id_s);
    if not action:return
    name_log=action['action_name']
    actions = [act for act in actions if act.get("ajax_id") != action.get("ajax_id")] 
    if save_ajax_actions(actions):
        log_message(f"AJAX ID {action['ajax_id']} removed.",GREEN)
        log_action_automatic(f"Removed AJAX ID {action['ajax_id']}:'{name_log}'")

# --- Asset Tracker Functions ---
# ... (All Asset Tracker functions - Corrected and Verified with UTC ISO Timestamps)
def get_assets_filepath():
    return get_project_specific_path("findings/assets.json")

def load_assets():
    assets_filepath = get_assets_filepath()
    if not assets_filepath or not os.path.exists(assets_filepath): return []
    try:
        with open(assets_filepath, 'r', encoding='utf-8') as f: data = json.load(f)
        for asset in data: 
            asset.setdefault('services', [])
            for key in ["finding", "plugin_inventory", "ajax_inventory", "todo"]: asset.setdefault(f"linked_{key}_ids", [])
            asset.setdefault('date_added', datetime.datetime.now(timezone.utc).isoformat())
            asset.setdefault('last_updated', asset['date_added'])
            for service in asset.get('services', []):
                 service.setdefault('last_seen_timestamp', asset['last_updated'])
        return data
    except Exception as e: 
        log_message(f"Corrupted assets.json. Error: {e}. Starting fresh.", YELLOW)
        return []

def save_assets(assets):
    assets_filepath = get_assets_filepath()
    if not assets_filepath: 
        log_message("Error: No project path for assets.", RED, CAT_ART_PROJECT_FAIL)
        return False
    try:
        os.makedirs(os.path.dirname(assets_filepath), exist_ok=True)
        with open(assets_filepath, 'w', encoding='utf-8') as f: json.dump(assets, f, indent=4)
        return True
    except Exception as e: 
        log_message(f"Error saving assets: {e}", RED, CAT_ART_ERROR)
        return False

def get_next_asset_id(assets):
    return max([item.get("asset_id", 0) for item in assets] + [0]) + 1

def get_next_service_id_for_asset(asset_entry):
    return max([s.get("service_id", 0) for s in asset_entry.get("services", [])] + [0]) + 1

def _update_asset_modification_date(asset_entry):
    asset_entry["last_updated"] = datetime.datetime.now(timezone.utc).isoformat()

def _find_asset_by_id_or_identifier(identifier_or_id_in):
    assets = load_assets()
    identifier_or_id = str(identifier_or_id_in).strip() 
    if not identifier_or_id: return None, None
    if identifier_or_id.isdigit():
        target_id = int(identifier_or_id)
        for asset in assets:
            if asset.get("asset_id") == target_id: return asset, assets
    search_term = identifier_or_id.lower()
    for asset in assets: 
        if asset.get("primary_identifier", "").lower() == search_term: return asset, assets
    for asset in assets: 
        if search_term in [ip.lower() for ip in asset.get("ip_addresses", [])]: return asset, assets
        if search_term in [h.lower() for h in asset.get("hostnames", [])]: return asset, assets
    log_message(f"Asset '{identifier_or_id}' not found.", RED, CAT_ART_THINKING); return None, None

def add_asset_entry():
    if not ensure_project_loaded("Adding an asset"): return
    log_message("Add New Asset to Catalog of Meow-chines", BOLD + MAGENTA, CAT_ART_ASSET_ADD)
    primary_identifier = input(f"{BLUE}Primary Identifier (main IP or FQDN)> {ENDC}").strip()
    if not primary_identifier: 
        log_message("Primary identifier cannot be empty.", RED)
        return
    assets = load_assets()
    for asset_in_list in assets:
        if asset_in_list.get("primary_identifier","").lower() == primary_identifier.lower():
            log_message(f"Asset with primary ID '{primary_identifier}' already exists (ID: {asset_in_list.get('asset_id')}). Use 'update_asset'.", YELLOW)
            return
            
    asset_type_options = ["HostIP", "Hostname", "WebsiteURL", "NetworkService", "CloudResource", "Domain", "Unknown"]
    default_asset_type = "HostIP" if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", primary_identifier) else "Hostname"
    asset_type = _get_enum_input("Asset Type", asset_type_options, default_asset_type)
    
    ip_addresses_input = input(f"{BLUE}Additional IP Addresses (comma-separated, optional)> {ENDC}").strip()
    ip_addresses = [ip.strip() for ip in ip_addresses_input.split(',') if ip.strip()]
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", primary_identifier) and primary_identifier not in ip_addresses: 
        ip_addresses.insert(0, primary_identifier)
    ip_addresses = sorted(list(set(ip_addresses)))
    
    hostnames_input = input(f"{BLUE}Additional Hostnames/Domains (comma-separated, optional)> {ENDC}").strip()
    hostnames = [h.strip().lower() for h in hostnames_input.split(',') if h.strip()]
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", primary_identifier) and primary_identifier.lower() not in hostnames: 
        hostnames.insert(0, primary_identifier.lower())
    hostnames = sorted(list(set(hostnames)))
    
    os_details = input(f"{BLUE}OS Details (optional, default: Unknown)> {ENDC}").strip() or "Unknown"
    environment_tags_input = input(f"{BLUE}Environment Tags (comma-separated)> {ENDC}").strip()
    environment_tags = sorted(list(set([tag.strip().title() for tag in environment_tags_input.split(',') if tag.strip()])))
    
    description = input(f"{BLUE}Description (optional, default: N/A)> {ENDC}").strip() or "N/A"
    
    asset_status_options = ["Active_InScope", "Active_OutOfScope", "Monitored", "Investigating", "Decommissioned", "Unknown"]
    asset_status = _get_enum_input("Status", asset_status_options, "Investigating")
    
    notes_asset = input(f"{BLUE}General Notes for Asset (optional, default: N/A)> {ENDC}").strip() or "N/A"
    
    now_utc_iso = datetime.datetime.now(timezone.utc).isoformat()
    new_asset = {"asset_id": get_next_asset_id(assets), "project_id": CURRENT_PROJECT_NAME, "asset_type": asset_type, "primary_identifier": primary_identifier, "ip_addresses": ip_addresses, "hostnames": hostnames, "os_details": os_details, "environment_tags": environment_tags, "description": description, "status": asset_status, "services": [], "notes_asset": notes_asset, "date_added": now_utc_iso,"last_updated": now_utc_iso, "linked_finding_ids": [], "linked_plugin_inventory_ids": [], "linked_ajax_inventory_ids": [], "linked_todo_ids": []}
    assets.append(new_asset)
    if save_assets(assets): 
        log_message(f"Asset '{primary_identifier}' (ID: {new_asset['asset_id']}) added.", GREEN,CAT_ART_SUCCESS)
        log_action_automatic(f"Added Asset ID {new_asset['asset_id']}: '{primary_identifier}'")

def _display_asset_details(asset, with_services=True):
    status_colors = {"Active_InScope": GREEN, "Investigating": YELLOW, "Active_OutOfScope": BLUE, "Monitored": CYAN, "Decommissioned": RED, "Unknown": WHITE}
    status_color = status_colors.get(asset.get('status', 'Unknown'), WHITE)
    print(f"  {BOLD}Asset ID: {asset.get('asset_id')}{ENDC} | Primary ID: {BLUE}{asset.get('primary_identifier')}{ENDC}")
    print(f"    Type: {asset.get('asset_type', 'N/A')} | Status: {status_color}{asset.get('status', 'N/A').replace('_',' ')}{ENDC}")
    print(f"    IPs: {', '.join(asset.get('ip_addresses', [])) or 'N/A'}")
    print(f"    Hostnames: {', '.join(asset.get('hostnames', [])) or 'N/A'}")
    print(f"    OS: {asset.get('os_details', 'N/A')}")
    print(f"    Tags: {', '.join(asset.get('environment_tags', [])) or 'N/A'}")
    print(f"    Description: {asset.get('description', 'N/A')}")
    print(f"    Notes: {asset.get('notes_asset', 'N/A')}")
    print(f"    Added: {asset.get('date_added')} | Last Updated: {asset.get('last_updated')}")
    if with_services and asset.get("services"):
        print(f"    {MAGENTA}--- Services ({len(asset['services'])}) ---{ENDC}")
        for s in sorted(asset['services'], key=lambda x: (x.get('port',0), x.get('protocol',''))):
            s_id=s.get('service_id','N/A'); state_col=GREEN if s.get('state')=='open' else RED if s.get('state')=='closed' else YELLOW
            p_p_s=f"{s.get('port','?')}/{s.get('protocol','?')} ({state_col}{s.get('state','unk')}{ENDC})"
            s_name=s.get('service_name','N/A'); s_prod=s.get('service_product',''); s_ver=s.get('service_version','')
            ver_str=f"{s_prod} {s_ver}".strip() or "N/A"
            print(f"      {CYAN}SvcID: {s_id}{ENDC} | {p_p_s:<28} | Name: {s_name:<15} | Version: {ver_str}")
            if s.get('banner'): print(f"        Banner: {s.get('banner')[:100].replace(os.linesep, ' ')}...")
            if s.get('notes_service'): print(f"        Svc Notes: {s.get('notes_service')}")
            print(f"        Last Seen: {s.get('last_seen_timestamp', 'N/A')}")
    elif with_services: print(f"    {MAGENTA}--- Services (None Recorded) ---{ENDC}")
    links={k.replace("linked_","").replace("_ids","").title():len(v) for k,v in asset.items() if k.startswith("linked_") and v}
    if links: print(f"    Linked Items: {json.dumps(links)}")
    print("    " + "-" * 60)

def list_assets():
    if not ensure_project_loaded("Listing assets"): return
    log_message("Asset Catalog", BOLD + MAGENTA, CAT_ART_ASSET_LIST)
    assets = load_assets()
    if not assets: 
        log_message("Catalog empty.", YELLOW)
        return
    f_id = input(f"{BLUE}Filter Primary ID (contains, CI, empty for all)> {ENDC}").strip().lower()
    f_ip = input(f"{BLUE}Filter IP (contains, empty for all)> {ENDC}").strip()
    f_host = input(f"{BLUE}Filter Hostname (contains, CI, empty for all)> {ENDC}").strip().lower()
    f_tag = input(f"{BLUE}Filter Tag (exact, CI, empty for all)> {ENDC}").strip().lower()
    f_os = input(f"{BLUE}Filter OS (contains, CI, empty for all)> {ENDC}").strip().lower()
    f_svc_name = input(f"{BLUE}Filter Service Name (contains, CI, e.g. http, empty for all)> {ENDC}").strip().lower()
    f_port_proto = input(f"{BLUE}Filter Port/Proto (e.g. 80/tcp, 53, empty for all)> {ENDC}").strip().lower()
    filtered = [a for a in assets if (not f_id or f_id in a.get("primary_identifier","").lower()) and \
                                   (not f_ip or any(f_ip in ip_addr for ip_addr in a.get("ip_addresses",[]))) and \
                                   (not f_host or any(f_host in hn.lower() for hn in a.get("hostnames",[]))) and \
                                   (not f_tag or any(f_tag == tag.lower() for tag in a.get("environment_tags",[]))) and \
                                   (not f_os or f_os in a.get("os_details","").lower()) and \
                                   (not f_svc_name or any(f_svc_name in s.get("service_name","").lower() for s in a.get("services",[]))) and \
                                   (not f_port_proto or any(f_port_proto == f"{s.get('port','')}/{s.get('protocol','').lower()}" or \
                                                            (f_port_proto.isdigit() and s.get('port') == int(f_port_proto)) or \
                                                            (f_port_proto.startswith('/') and s.get('protocol','').lower() == f_port_proto[1:]) 
                                                            for s in a.get("services",[])))]
    if not filtered: 
        log_message("No assets match filters.", YELLOW)
        return
    filtered.sort(key=lambda x: x.get("primary_identifier","").lower())
    log_message(f"\n--- Filtered Assets ({len(filtered)}) ---", CYAN)
    for asset_entry in filtered: 
        _display_asset_details(asset_entry, with_services=False) 
    log_message("--- End of Asset Catalog Summary ---", CYAN)
    log_message("Use 'view_asset <id|ident>' for full details.", BLUE)

def view_asset_details_cmd(asset_identifier_val=None):
    if not ensure_project_loaded("Viewing asset"): return
    ident = asset_identifier_val if asset_identifier_val else input(f"{BLUE}Asset ID or Primary Identifier> {ENDC}").strip()
    if not ident: 
        log_message("Identifier empty.", RED)
        return
    asset, _ = _find_asset_by_id_or_identifier(ident)
    if asset: 
        log_message(f"Details for Asset: {asset['primary_identifier']}",BOLD+CYAN,no_cat_prefix=True)
        _display_asset_details(asset)

def update_asset_entry(asset_identifier_val=None):
    if not ensure_project_loaded("Updating asset"): return
    ident = asset_identifier_val if asset_identifier_val else input(f"{BLUE}Asset ID or Primary Identifier to update> {ENDC}").strip()
    if not ident: 
        log_message("Identifier empty.", RED)
        return
    asset, assets = _find_asset_by_id_or_identifier(ident)
    if not asset: return
    log_message(f"Updating Asset: {asset['primary_identifier']}",BOLD+MAGENTA,CAT_ART_INPUT); orig_copy={k:(v.copy() if isinstance(v,(list,dict)) else v) for k,v in asset.items()}
    
    new_pid=input(f"{BLUE}New Primary ID (curr: '{asset['primary_identifier']}')> {ENDC}").strip()
    if new_pid: 
        asset['primary_identifier']=new_pid
    
    asset_type_options = ["HostIP","Hostname","WebsiteURL","NetworkService","CloudResource","Domain","Unknown"]
    current_asset_type = asset.get('asset_type')
    new_asset_type_in = input(f"{BLUE}New Asset Type ({'/'.join(asset_type_options)}, curr:'{current_asset_type}')> {ENDC}").strip().title()
    if new_asset_type_in in asset_type_options: 
        asset['asset_type'] = new_asset_type_in
    elif new_asset_type_in == "" and input(f"{YELLOW}Keep current asset type '{current_asset_type}'? (Y/n)> {ENDC}").lower() == 'n':
        asset['asset_type'] = _get_enum_input("Re-enter Asset Type", asset_type_options, current_asset_type)

    current_os = asset.get('os_details')
    new_os = input(f"{BLUE}OS (curr:'{current_os}')> {ENDC}").strip()
    if new_os: 
        asset['os_details'] = new_os
    elif new_os == "" and input(f"{YELLOW}Clear current OS '{current_os}' (set to Unknown)? (y/N)> {ENDC}").lower() == 'y': 
        asset['os_details'] = "Unknown"

    current_tags_str = ','.join(asset.get('environment_tags',[]))
    new_tags_str = input(f"{BLUE}Tags (csv, curr:'{current_tags_str}', 'clear' to empty)> {ENDC}").strip()
    if new_tags_str.lower()=='clear': 
        asset['environment_tags'] = []
    elif new_tags_str: 
        asset['environment_tags'] = sorted(list(set([t.strip().title() for t in new_tags_str.split(',') if t.strip()])))
    
    current_desc = asset.get('description')
    new_desc = input(f"{BLUE}Desc (curr:'{current_desc}')> {ENDC}").strip()
    if new_desc: 
        asset['description'] = new_desc
    elif new_desc == "" and input(f"{YELLOW}Clear current description '{current_desc}' (set to N/A)? (y/N)> {ENDC}").lower() == 'y': 
        asset['description'] = "N/A"
        
    current_notes = asset.get('notes_asset')
    new_notes = input(f"{BLUE}Notes (curr:'{current_notes}')> {ENDC}").strip()
    if new_notes: 
        asset['notes_asset'] = new_notes
    elif new_notes == "" and input(f"{YELLOW}Clear current asset notes '{current_notes}' (set to N/A)? (y/N)> {ENDC}").lower() == 'y': 
        asset['notes_asset'] = "N/A"
        
    stat_opts=["Active_InScope","Active_OutOfScope","Monitored","Investigating","Decommissioned","Unknown"]
    current_stat_display = asset.get('status').replace('_',' ')
    new_stat_in=input(f"{BLUE}Status ({'/'.join(stat_opts)}, curr:'{current_stat_display}')> {ENDC}").strip().replace(" ","_").title() 
    if new_stat_in in stat_opts: 
        asset['status'] = new_stat_in
    
    _update_asset_modification_date(asset)
    if save_assets(assets):
        log_message(f"Asset ID {asset['asset_id']} updated.",GREEN,CAT_ART_PLUGIN_UPDATE)
        chgs=[f"{k}:'{orig_copy.get(k)}'->'{asset.get(k)}'" for k in ["primary_identifier","asset_type","os_details","environment_tags","description","notes_asset","status"] if orig_copy.get(k)!=asset.get(k)]
        log_action_automatic(f"Updated Asset ID {asset['asset_id']}. Changes: {'; '.join(chgs) if chgs else 'No textual change'}.")

def add_asset_service_cmd(asset_identifier_val=None):
    if not ensure_project_loaded("Adding asset service"): return
    ident = asset_identifier_val if asset_identifier_val else input(f"{BLUE}Asset ID or Primary Identifier> {ENDC}").strip()
    if not ident: 
        log_message("Identifier empty.", RED)
        return
    asset, assets = _find_asset_by_id_or_identifier(ident)
    if not asset: return
    log_message(f"Adding Service to Asset: {asset['primary_identifier']}",BOLD+MAGENTA,CAT_ART_SERVICE_ADD)
    
    port_str = input(f"{BLUE}Port number> {ENDC}").strip()
    if not port_str.isdigit() or not (0 <= int(port_str) <= 65535): 
        log_message("Invalid port (0-65535).", RED)
        return
    port = int(port_str)
    
    protocol = input(f"{BLUE}Protocol (tcp/udp, def: tcp)> {ENDC}").strip().lower() or "tcp"
    if protocol not in ["tcp", "udp"]: 
        log_message("Invalid protocol.", RED)
        return
        
    asset.setdefault("services", []) 
    for s in asset["services"]:
        if s.get("port")==port and s.get("protocol")==protocol:
            log_message(f"Service {port}/{protocol} already exists (SvcID: {s.get('service_id')}). Use 'update_svc'.",YELLOW)
            return
            
    state_opts=["open","closed","filtered","unknown"]
    state_in = input(f"{BLUE}State ({'/'.join(state_opts)}, def: open)> {ENDC}").strip().lower() 
    state = state_in if state_in in state_opts else "open"
        
    svc_name = input(f"{BLUE}Service Name (e.g. http, optional, default: Unknown)> {ENDC}").strip() or "Unknown"
    svc_prod = input(f"{BLUE}Service Product (opt)> {ENDC}").strip()
    svc_ver = input(f"{BLUE}Service Version (opt)> {ENDC}").strip()
    banner = input(f"{BLUE}Banner (opt)> {ENDC}").strip()
    notes_svc = input(f"{BLUE}Notes for service (opt)> {ENDC}").strip()
    
    new_svc_id = get_next_service_id_for_asset(asset)
    new_svc = {"service_id":new_svc_id, "port":port, "protocol":protocol, "state":state, "service_name":svc_name, "service_product":svc_prod or None, "service_version":svc_ver or None, "banner":banner or None, "notes_service":notes_svc or None, "last_seen_timestamp":datetime.datetime.now(timezone.utc).isoformat()}
    asset["services"].append(new_svc)
    _update_asset_modification_date(asset) 
    if save_assets(assets): 
        log_message(f"Service {port}/{protocol} (SvcID: {new_svc_id}) added to asset {asset['asset_id']}.",GREEN,CAT_ART_SUCCESS)
        log_action_automatic(f"Added service {port}/{protocol} ({svc_name}) to Asset ID {asset['asset_id']}")

def update_asset_service_cmd(asset_identifier_val=None):
    if not ensure_project_loaded("Updating asset service"): return
    ident = asset_identifier_val if asset_identifier_val else input(f"{BLUE}Asset ID or Primary Identifier> {ENDC}").strip()
    if not ident: 
        log_message("Identifier empty.", RED)
        return
    asset, assets = _find_asset_by_id_or_identifier(ident)
    if not asset or not asset.get("services"): 
        log_message(f"Asset '{ident}' has no services or not found.", YELLOW)
        return
        
    log_message(f"Services for Asset: {asset['primary_identifier']}", BOLD+CYAN)
    for s_idx, s_entry in enumerate(asset["services"]): 
        print(f"  [{s_idx}] SvcID: {s_entry['service_id']}, Port: {s_entry['port']}/{s_entry['protocol']}, Name: {s_entry['service_name']}")
    
    choice_str = input(f"{BLUE}Enter SvcID or list index [0-{len(asset['services'])-1}] of service to update> {ENDC}").strip()
    svc_to_update = None
    if choice_str.isdigit():
        choice_idx_or_id = int(choice_str)
        if 0 <= choice_idx_or_id < len(asset["services"]): 
            svc_to_update = asset["services"][choice_idx_or_id]
        else: 
            svc_to_update = next((s for s in asset["services"] if s.get("service_id") == choice_idx_or_id), None)
    
    if not svc_to_update: 
        log_message(f"Service choice '{choice_str}' not found on this asset.", RED)
        return

    log_message(f"Updating SvcID {svc_to_update['service_id']} ({svc_to_update['port']}/{svc_to_update['protocol']})",BOLD+MAGENTA,CAT_ART_INPUT); orig_svc_copy=svc_to_update.copy()
    
    state_opts=["open","closed","filtered","unknown"]
    current_state = svc_to_update.get('state')
    new_st = input(f"{BLUE}New State ({'/'.join(state_opts)}, curr:'{current_state}')> {ENDC}").strip().lower() 
    if new_st in state_opts: 
        svc_to_update['state']=new_st
    elif new_st == "" and input(f"{YELLOW}Keep current state '{current_state}'? (Y/n)> {ENDC}").lower() == 'n': 
        svc_to_update['state'] = _get_enum_input("Re-enter State", state_opts, "unknown")

    current_name = svc_to_update.get('service_name')
    new_nm = input(f"{BLUE}New Name (curr:'{current_name}')> {ENDC}").strip()
    if new_nm: 
        svc_to_update['service_name']=new_nm
    elif new_nm == "" and input(f"{YELLOW}Clear current name '{current_name}' (set to Unknown)? (y/N)> {ENDC}").lower() == 'y': 
        svc_to_update['service_name']="Unknown"

    current_prod = svc_to_update.get('service_product','None')
    new_prod = input(f"{BLUE}New Product (curr:'{current_prod}')> {ENDC}").strip()
    if new_prod: svc_to_update['service_product']=new_prod
    elif new_prod == "" and input(f"{YELLOW}Clear current product '{current_prod}'? (y/N)> {ENDC}").lower() == 'y': svc_to_update['service_product']=None
        
    current_ver = svc_to_update.get('service_version','None')
    new_ver = input(f"{BLUE}New Version (curr:'{current_ver}')> {ENDC}").strip()
    if new_ver: svc_to_update['service_version']=new_ver
    elif new_ver == "" and input(f"{YELLOW}Clear current version '{current_ver}'? (y/N)> {ENDC}").lower() == 'y': svc_to_update['service_version']=None

    current_banner = svc_to_update.get('banner','None')
    new_banner = input(f"{BLUE}New Banner (curr:'{current_banner}')> {ENDC}").strip()
    if new_banner: svc_to_update['banner']=new_banner
    elif new_banner == "" and input(f"{YELLOW}Clear current banner? (y/N)> {ENDC}").lower() == 'y': svc_to_update['banner']=None
        
    current_svc_notes = svc_to_update.get('notes_service','None')
    new_notes = input(f"{BLUE}New Svc Notes (curr:'{current_svc_notes}')> {ENDC}").strip()
    if new_notes: svc_to_update['notes_service']=new_notes
    elif new_notes == "" and input(f"{YELLOW}Clear current service notes? (y/N)> {ENDC}").lower() == 'y': svc_to_update['notes_service']=None
        
    svc_to_update['last_seen_timestamp'] = datetime.datetime.now(timezone.utc).isoformat()
    _update_asset_modification_date(asset)
    if save_assets(assets):
        log_message(f"Service SvcID {svc_to_update['service_id']} on Asset ID {asset['asset_id']} updated.", GREEN, CAT_ART_SUCCESS)
        chgs=[f"{k}:'{orig_svc_copy.get(k)}'->'{svc_to_update.get(k)}'" for k in ["state","service_name","service_product","service_version","banner","notes_service"] if orig_svc_copy.get(k)!=svc_to_update.get(k)]
        log_action_automatic(f"Updated Service SvcID {svc_to_update['service_id']} on Asset ID {asset['asset_id']}. Changes: {'; '.join(chgs) if chgs else 'No change'}.")

def remove_asset_service_cmd(asset_identifier_val=None): # Corrected
    if not ensure_project_loaded("Removing asset service"): return
    ident = asset_identifier_val if asset_identifier_val else input(f"{BLUE}Asset ID or Primary Identifier> {ENDC}").strip()
    if not ident: 
        log_message("Identifier empty.", RED)
        return
    asset, assets = _find_asset_by_id_or_identifier(ident)
    if not asset or not asset.get("services"): 
        log_message(f"Asset '{ident}' has no services to remove or not found.", YELLOW)
        return
        
    log_message(f"Services for Asset: {asset['primary_identifier']}", BOLD+CYAN)
    for s_idx, s_entry in enumerate(asset["services"]): 
        print(f"  [{s_idx}] SvcID: {s_entry['service_id']}, Port: {s_entry['port']}/{s_entry['protocol']}, Name: {s_entry['service_name']}")
    
    choice_str = input(f"{BLUE}Enter SvcID or list index [0-{len(asset['services'])-1}] of service to remove> {ENDC}").strip()
    service_to_remove = None
    service_index_to_remove = -1

    if choice_str.isdigit():
        choice_idx_or_id = int(choice_str)
        if 0 <= choice_idx_or_id < len(asset["services"]): 
            service_index_to_remove = choice_idx_or_id
            service_to_remove = asset["services"][service_index_to_remove]
        else: 
            for idx, s_item in enumerate(asset["services"]):
                if s_item.get("service_id") == choice_idx_or_id:
                    service_to_remove = s_item
                    service_index_to_remove = idx
                    break
    
    if not service_to_remove: 
        log_message(f"Service choice '{choice_str}' not found on this asset.", RED)
        return

    svc_desc_log = f"{service_to_remove['port']}/{service_to_remove['protocol']} ({service_to_remove['service_name']})"
    if input(f"{RED}{BOLD}Really remove Service SvcID {service_to_remove['service_id']} ({svc_desc_log}) from Asset ID {asset['asset_id']}? (yes/NO)> {ENDC}").lower()!='yes':
        log_message("Service removal cancelled.",YELLOW)
        return

    asset["services"].pop(service_index_to_remove)
    _update_asset_modification_date(asset)
    if save_assets(assets):
        log_message(f"Service SvcID {service_to_remove['service_id']} ({svc_desc_log}) removed from Asset ID {asset['asset_id']}.", GREEN, CAT_ART_SUCCESS)
        log_action_automatic(f"Removed Service SvcID {service_to_remove['service_id']} ({svc_desc_log}) from Asset ID {asset['asset_id']}")

def remove_asset_entry(asset_identifier_val=None):
    if not ensure_project_loaded("Removing asset"): return
    ident = asset_identifier_val if asset_identifier_val else input(f"{BLUE}Asset ID or Primary Identifier to remove> {ENDC}").strip()
    if not ident: 
        log_message("Identifier empty.", RED)
        return
    asset, assets = _find_asset_by_id_or_identifier(ident);
    if not asset: return
    primary_id_log=asset['primary_identifier']; asset_id_log=asset['asset_id']
    if input(f"{RED}{BOLD}Really remove Asset ID {asset_id_log} ('{primary_id_log}')? (yes/NO)> {ENDC}").lower()!='yes':
        log_message("Removal cancelled.",YELLOW)
        return
    assets = [a for a in assets if a.get("asset_id") != asset_id_log] 
    if save_assets(assets): 
        log_message(f"Asset ID {asset_id_log} removed.",GREEN, CAT_ART_SUCCESS)
        log_action_automatic(f"Removed Asset ID {asset_id_log}: '{primary_id_log}'")

# --- General Findings Tracker Functions ---
def get_general_findings_filepath():
    return get_project_specific_path("findings/general_findings.json")

def load_general_findings():
    fp = get_general_findings_filepath()
    if not fp or not os.path.exists(fp): return []
    try:
        with open(fp, 'r', encoding='utf-8') as f: data = json.load(f)
        for finding in data: 
            finding.setdefault('asset_ids', [])
            finding.setdefault('linked_plugin_ids', [])
            finding.setdefault('linked_ajax_ids', [])
            finding.setdefault('linked_todo_ids', [])
            finding.setdefault('key_data_points', {})
            finding.setdefault('tags', [])
            finding.setdefault('date_added_to_ppp', datetime.datetime.now(timezone.utc).isoformat()) 
            finding.setdefault('last_updated_in_ppp', finding['date_added_to_ppp'])
            finding.setdefault('timestamp_event_utc', finding['date_added_to_ppp']) # Sensible default for older data
            finding.setdefault('timestamp_generated_utc', finding['date_added_to_ppp'])
        return data
    except Exception as e: 
        log_message(f"Corrupted general_findings.json. Error: {e}. Starting fresh.", YELLOW)
        return []

def save_general_findings(findings):
    fp = get_general_findings_filepath()
    if not fp: 
        log_message("Error: No project path for general findings.", RED, CAT_ART_PROJECT_FAIL)
        return False
    try:
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, 'w', encoding='utf-8') as f: json.dump(findings, f, indent=4)
        return True
    except Exception as e: 
        log_message(f"Error saving general findings: {e}", RED, CAT_ART_ERROR)
        return False

def get_next_finding_id(findings):
    return max([item.get("finding_id", 0) for item in findings] + [0]) + 1

def _update_finding_modification_date(finding_entry):
    finding_entry["last_updated_in_ppp"] = datetime.datetime.now(timezone.utc).isoformat()

def add_finding_entry():
    if not ensure_project_loaded("Adding a finding"): return
    log_message("Add New Finding to Clue Collector Cache", BOLD + MAGENTA, CAT_ART_FINDING_ADD)
    
    findings = load_general_findings()
    now_utc_iso = datetime.datetime.now(timezone.utc).isoformat()

    new_finding = {
        "finding_id": get_next_finding_id(findings),
        "project_id": CURRENT_PROJECT_NAME,
        "insight_id": str(uuid.uuid4()), 
        "date_added_to_ppp": now_utc_iso,
        "last_updated_in_ppp": now_utc_iso,
        "asset_ids": [], "linked_plugin_ids": [], "linked_ajax_ids": [], "linked_todo_ids": []
    }

    target_context_in = input(f"{BLUE}Target Context (IP, FQDN, URL, component name, 'N/A' if general)> {ENDC}").strip()
    new_finding["target_context"] = target_context_in if target_context_in else "N/A"
    
    source_type_options = ["ToolOutput", "LLMAnalysis", "ManualEntry", "LLMSuggestion"]
    new_finding["source_type"] = _get_enum_input("Source Type", source_type_options, "ManualEntry")
    
    source_tool_default = "ManualObservation"
    if new_finding["source_type"] == "ToolOutput": source_tool_default = "UnknownTool"
    elif new_finding["source_type"] == "LLMAnalysis": source_tool_default = "Gemini:GeneralAnalysis" 
    elif new_finding["source_type"] == "LLMSuggestion": source_tool_default = "Gemini:Suggestion"   
    source_tool_name_in = input(f"{BLUE}Source Tool/Analyst Name (default: {source_tool_default})> {ENDC}").strip()
    new_finding["source_tool_name"] = source_tool_name_in if source_tool_name_in else source_tool_default
    
    source_reference_in = input(f"{BLUE}Source Reference (filename, doc title, URL, optional, default: N/A)> {ENDC}").strip()
    new_finding["source_reference"] = source_reference_in if source_reference_in else "N/A"
    
    timestamp_event_str = input(f"{BLUE}Timestamp of Event (YYYY-MM-DD HH:MM:SS, optional, Enter for now for current UTC)> {ENDC}").strip()
    if timestamp_event_str:
        try:
            dt_obj_naive = datetime.datetime.strptime(timestamp_event_str, "%Y-%m-%d %H:%M:%S")
            dt_obj_utc = dt_obj_naive.replace(tzinfo=timezone.utc) 
            new_finding["timestamp_event_utc"] = dt_obj_utc.isoformat()
        except ValueError:
            log_message("Invalid event timestamp format (YYYY-MM-DD HH:MM:SS). Storing as current UTC.", YELLOW)
            new_finding["timestamp_event_utc"] = now_utc_iso
    else:
        new_finding["timestamp_event_utc"] = now_utc_iso

    new_finding["timestamp_generated_utc"] = now_utc_iso

    cat_default = "General"
    if new_finding["source_tool_name"] and "nmap" in new_finding["source_tool_name"].lower(): cat_default = "NetworkScan"
    elif new_finding["source_tool_name"] and "wpscan" in new_finding["source_tool_name"].lower(): cat_default = "WebAppScan"
    category_in = input(f"{BLUE}Category (e.g., NetworkScan, WebAppFinding, OSINT, default: {cat_default})> {ENDC}").strip().title()
    new_finding["category"] = category_in if category_in else cat_default
    
    type_default = "Observation"
    if new_finding["category"] == "NetworkScan": type_default = "PortScanInfo"
    elif new_finding["category"] == "WebAppScan": type_default = "WebAppObservation"
    type_in = input(f"{BLUE}Specific Type (e.g., OpenPort, XSS, default: {type_default})> {ENDC}").strip().title()
    new_finding["type"] = type_in if type_in else type_default
    
    new_finding["title"] = input(f"{BLUE}Title (concise summary)> {ENDC}").strip()
    if not new_finding["title"]: 
        log_message("Title cannot be empty.", RED)
        return
    
    log_message("Enter Detailed Description (multi-line, 'ENDDESC' on new line to finish):", BLUE)
    description_lines = []
    while True:
        line = sys.stdin.readline().rstrip(os.linesep)
        if line.strip().upper() == 'ENDDESC': break
        description_lines.append(line)
    new_finding["description"] = "\n".join(description_lines)
    if not new_finding["description"]: new_finding["description"] = "N/A"

    severity_options = ["Critical", "High", "Medium", "Low", "Informational", "NotApplicable"]
    new_finding["severity_assessment"] = _get_enum_input("Severity Assessment", severity_options, "Informational")
    
    confidence_options = ["Certain", "High", "Medium", "Low", "Speculative"]
    new_finding["confidence"] = _get_enum_input("Confidence", confidence_options, "Medium")

    status_options = ["Open", "Investigating", "NeedsVerification", "Remediated", "FalsePositive", "Closed"]
    new_finding["status"] = _get_enum_input("Status", status_options, "Open")

    actionable_recommendation_in = input(f"{BLUE}Actionable Recommendation (optional, default: N/A)> {ENDC}").strip()
    new_finding["actionable_recommendation"] = actionable_recommendation_in if actionable_recommendation_in else "N/A"
    
    key_data_points_str = input(f"{BLUE}Key Data Points (JSON string, e.g., {{\"port\": 80}}, or empty)> {ENDC}").strip()
    if key_data_points_str:
        try: 
            loaded_kdp = json.loads(key_data_points_str)
            if isinstance(loaded_kdp, dict):
                new_finding["key_data_points"] = loaded_kdp
            else:
                log_message("Invalid JSON: Key Data Points must be a dictionary/object. Storing as empty.", YELLOW)
                new_finding["key_data_points"] = {}
        except json.JSONDecodeError: 
            log_message("Invalid JSON for Key Data Points. Storing as empty object.", YELLOW)
            new_finding["key_data_points"] = {}
    else: 
        new_finding["key_data_points"] = {}
        
    tags_input = input(f"{BLUE}Tags (comma-separated, optional)> {ENDC}").strip()
    new_finding["tags"] = sorted(list(set([tag.strip().lower() for tag in tags_input.split(',') if tag.strip()])))
    
    notes_in = input(f"{BLUE}Your Analyst Notes for this finding (optional, default: N/A)> {ENDC}").strip()
    new_finding["notes"] = notes_in if notes_in else "N/A"
    
    raw_log_snippet_in = input(f"{BLUE}Raw Log Snippet (optional, brief context)> {ENDC}").strip()
    new_finding["raw_input_snippet_if_applicable"] = raw_log_snippet_in if raw_log_snippet_in else None

    findings.append(new_finding)
    if save_general_findings(findings):
        log_message(f"Finding ID {new_finding['finding_id']} ('{new_finding['title']}') added.", GREEN, CAT_ART_FINDING_ADD)
        log_action_automatic(f"Added Finding ID {new_finding['finding_id']}: '{new_finding['title']}'")

def _display_finding_details_full(finding):
    # ... (As in previous full script)
    print(f"  {BOLD}Finding ID: {finding.get('finding_id')}{ENDC} | Insight ID (Source): {finding.get('insight_id')}")
    print(f"    Title: {BLUE}{finding.get('title')}{ENDC}")
    print(f"    Target Context: {CYAN}{finding.get('target_context')}{ENDC}")
    print(f"    Source: {finding.get('source_tool_name')} (Ref: {finding.get('source_reference')}, Type: {finding.get('source_type')})")
    sev_colors = {"Critical": BOLD+RED, "High": RED, "Medium": YELLOW, "Low": BLUE, "Informational": GREEN, "NotApplicable": WHITE}
    stat_colors = {"Open": RED, "Investigating": YELLOW, "NeedsVerification": MAGENTA, "Remediated": GREEN, "FalsePositive": BLUE, "Closed": WHITE }
    print(f"    Severity: {sev_colors.get(finding.get('severity_assessment'),WHITE)}{finding.get('severity_assessment')}{ENDC} | Confidence: {finding.get('confidence')}")
    print(f"    Status: {stat_colors.get(finding.get('status'),WHITE)}{finding.get('status')}{ENDC}")
    print(f"    Category: {finding.get('category')} | Type: {finding.get('type')}")
    print(f"    Event Time (UTC): {finding.get('timestamp_event_utc')} | Generated (UTC): {finding.get('timestamp_generated_utc')}")
    print(f"    Added to PPP: {finding.get('date_added_to_ppp')} | Last Updated in PPP: {finding.get('last_updated_in_ppp')}")
    print(f"    {MAGENTA}Description:{ENDC}\n      {finding.get('description','N/A').replace(os.linesep, os.linesep + '      ')}")
    if finding.get('key_data_points'):
        print(f"    {MAGENTA}Key Data Points:{ENDC}")
        try:
            print(f"      {json.dumps(finding.get('key_data_points',{}), indent=6).replace(os.linesep, os.linesep + '      ')}")
        except TypeError: 
            print(f"      {str(finding.get('key_data_points'))}")

    print(f"    Actionable Recommendation: {finding.get('actionable_recommendation','N/A')}")
    print(f"    Analyst Notes: {finding.get('notes','N/A')}")
    if finding.get('tags'): print(f"    Tags: {', '.join(finding.get('tags'))}")
    if finding.get('raw_input_snippet_if_applicable'): print(f"    Raw Snippet: {finding.get('raw_input_snippet_if_applicable')}")
    
    linked_summary = []
    if finding.get('asset_ids'): linked_summary.append(f"Assets: {', '.join(map(str,finding['asset_ids']))}")
    if finding.get('linked_plugin_ids'): linked_summary.append(f"Plugins: {', '.join(map(str,finding['linked_plugin_ids']))}")
    if finding.get('linked_ajax_ids'): linked_summary.append(f"AJAX Actions: {', '.join(map(str,finding['linked_ajax_ids']))}")
    if finding.get('linked_todo_ids'): linked_summary.append(f"ToDos: {', '.join(map(str,finding['linked_todo_ids']))}")
    if linked_summary: print(f"    Linked Items: {', '.join(linked_summary)}")
    print("    " + "-" * 60)


def list_general_findings():
    # ... (As in previous full script)
    if not ensure_project_loaded("Listing general findings"): return
    log_message("General Findings Cache", BOLD + MAGENTA, CAT_ART_FINDING_LIST)
    findings = load_general_findings()
    if not findings: log_message("No general findings in cache. Use 'add_finding'.", YELLOW); return

    f_target = input(f"{BLUE}Filter Target Context (contains, CI, empty for all)> {ENDC}").strip().lower()
    f_tool = input(f"{BLUE}Filter Source Tool (exact, CI, empty for all)> {ENDC}").strip().lower()
    f_cat = input(f"{BLUE}Filter Category (exact, CI, empty for all)> {ENDC}").strip().lower()
    f_type = input(f"{BLUE}Filter Type (exact, CI, empty for all)> {ENDC}").strip().lower()
    sev_opts_f = ["Critical", "High", "Medium", "Low", "Informational", "NotApplicable", "All"]
    f_sev = _get_enum_input("Filter Severity", sev_opts_f, "All")
    stat_opts_f = ["Open", "Investigating", "NeedsVerification", "Remediated", "FalsePositive", "Closed", "All"]
    f_stat = _get_enum_input("Filter Status", stat_opts_f, "All")
    
    f_tags_in = input(f"{BLUE}Filter Tags (csv, finding must have ALL, empty for all)> {ENDC}").strip().lower()
    f_tags = [t.strip() for t in f_tags_in.split(',') if t.strip()]
    
    sort_opts = {"d": "date", "s": "severity", "t": "title"}
    sort_choice = input(f"{BLUE}Sort by (d:date event, s:severity, t:title, default:date event newest first)> {ENDC}").strip().lower()
    sort_key = sort_opts.get(sort_choice, "date")
    sort_reverse = True if sort_key == "date" else False 

    filtered = [f for f in findings if \
                (not f_target or f_target in f.get("target_context","").lower()) and \
                (not f_tool or f.get("source_tool_name","").lower() == f_tool) and \
                (not f_cat or f.get("category","").lower() == f_cat.lower()) and \
                (not f_type or f.get("type","").lower() == f_type.lower()) and \
                (f_sev == "All" or f.get("severity_assessment","") == f_sev) and \
                (f_stat == "All" or f.get("status","") == f_stat) and \
                (not f_tags or all(tag_filter in f.get("tags",[]) for tag_filter in f_tags))
               ]
    if not filtered: log_message("No findings match your filter criteria.", YELLOW); return
    
    sev_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3, "Informational": 4, "NotApplicable": 5, "None": 6}
    if sort_key == "date": 
        filtered.sort(key=lambda x: (x.get("timestamp_event_utc") or x.get("date_added_to_ppp","0")), reverse=sort_reverse)
    elif sort_key == "severity": 
        filtered.sort(key=lambda x: (sev_order.get(x.get("severity_assessment","NotApplicable"), 5), x.get("title","").lower()))
    else: 
        filtered.sort(key=lambda x: x.get("title","").lower())

    log_message(f"\n--- Filtered Findings ({len(filtered)}) ---", CYAN)
    for finding_entry in filtered: _display_finding_details_full(finding_entry)
    log_message("--- End of Findings ---", CYAN)

def _find_finding_by_id(id_str): # Corrected
    if not id_str or not id_str.isdigit(): 
        log_message("Invalid Finding ID (must be a number).", RED)
        return None, None
    fid = int(id_str)
    findings = load_general_findings()
    for f_entry in findings:
        if f_entry.get("finding_id") == fid: 
            return f_entry, findings
    log_message(f"Finding ID {fid} not found.", RED)
    return None, None

def view_finding_details_cmd(finding_id_val=None): # Corrected
    if not ensure_project_loaded("Viewing finding"): return
    fid_str = finding_id_val if finding_id_val else input(f"{BLUE}Finding ID to view> {ENDC}").strip()
    if not fid_str: 
        log_message("Finding ID cannot be empty.", RED)
        return
    finding, _ = _find_finding_by_id(fid_str)
    if finding: 
        _display_finding_details_full(finding)

def update_finding_entry(finding_id_val=None): # Corrected
    if not ensure_project_loaded("Updating finding"): return
    fid_str = finding_id_val if finding_id_val else input(f"{BLUE}Finding ID to update> {ENDC}").strip()
    if not fid_str: 
        log_message("Finding ID cannot be empty.", RED)
        return
    finding, findings = _find_finding_by_id(fid_str)
    if not finding: return
    log_message(f"Updating Finding ID: {finding['finding_id']} - Title: '{finding['title']}'", BOLD + MAGENTA, CAT_ART_INPUT); orig_copy = finding.copy()

    new_title = input(f"{BLUE}New Title (curr: '{finding.get('title')}')> {ENDC}").strip() 
    if new_title: finding['title'] = new_title
    
    log_message(f"Current Description:\n{finding.get('description', 'N/A')}", CYAN)
    if input(f"{BLUE}Edit Description? (y/N)> {ENDC}").lower() == 'y':
        log_message("Enter New Detailed Description (multi-line, 'ENDDESC' on new line to finish):", BLUE)
        desc_lines = []; 
        while True: 
            line = sys.stdin.readline().rstrip(os.linesep)
            if line.strip().upper() == 'ENDDESC': break
            desc_lines.append(line)
        if desc_lines: 
            finding["description"] = "\n".join(desc_lines)
        elif input(f"{YELLOW}Clear current description? (y/N)> {ENDC}").lower() == 'y': 
            finding["description"] = "N/A"

    sev_opts = ["Critical", "High", "Medium", "Low", "Informational", "NotApplicable"]
    new_sev = _get_enum_input("New Severity Assessment", sev_opts, finding.get('severity_assessment'))
    if new_sev: finding['severity_assessment'] = new_sev
    
    stat_opts = ["Open", "Investigating", "NeedsVerification", "Remediated", "FalsePositive", "Closed"]
    new_stat = _get_enum_input("New Status", stat_opts, finding.get('status'))
    if new_stat: finding['status'] = new_stat

    new_reco = input(f"{BLUE}New Actionable Recommendation (curr: '{finding.get('actionable_recommendation', 'N/A')}')> {ENDC}").strip()
    if new_reco: 
        finding['actionable_recommendation'] = new_reco
    elif new_reco == "" and input(f"{YELLOW}Clear recommendation? (y/N)> {ENDC}").lower() == 'y': 
        finding['actionable_recommendation'] = "N/A"

    new_notes = input(f"{BLUE}Update Analyst Notes (curr: '{finding.get('notes', 'N/A')}')> {ENDC}").strip()
    if new_notes: 
        finding['notes'] = new_notes
    elif new_notes == "" and input(f"{YELLOW}Clear notes? (y/N)> {ENDC}").lower() == 'y': 
        finding['notes'] = "N/A"

    new_tags_in = input(f"{BLUE}New Tags (csv, curr: '{','.join(finding.get('tags',[]))}', 'clear' to empty)> {ENDC}").strip().lower()
    if new_tags_in.lower() == 'clear': 
        finding['tags'] = []
    elif new_tags_in: 
        finding['tags'] = sorted(list(set([t.strip() for t in new_tags_in.split(',') if t.strip()])))

    if input(f"{BLUE}Update Key Data Points? (y/N)> {ENDC}").lower() == 'y':
        log_message(f"Current Key Data Points: {json.dumps(finding.get('key_data_points',{}), indent=2)}", CYAN) 
        kdp_str = input(f"{BLUE}New Key Data Points (JSON string, or 'clear' to empty)> {ENDC}").strip()
        if kdp_str.lower() == 'clear': 
            finding['key_data_points'] = {}
        elif kdp_str:
            try: 
                loaded_kdp = json.loads(kdp_str)
                if isinstance(loaded_kdp, dict):
                    finding['key_data_points'] = loaded_kdp
                else:
                    log_message("Invalid JSON: Key Data Points must be a dictionary/object. Not changed.", YELLOW)
            except json.JSONDecodeError: 
                log_message("Invalid JSON for Key Data Points. Not changed.", YELLOW)
            
    _update_finding_modification_date(finding)
    if save_general_findings(findings):
        log_message(f"Finding ID {finding['finding_id']} updated.", GREEN, CAT_ART_SUCCESS)
        chgs = [f"{k}:'{orig_copy.get(k)}'->'{finding.get(k)}'" for k in finding if orig_copy.get(k) != finding.get(k) and k not in ['last_updated_in_ppp', 'date_added_to_ppp', 'project_id', 'finding_id', 'insight_id', 'asset_ids', 'linked_plugin_ids', 'linked_ajax_ids', 'linked_todo_ids']]
        log_action_automatic(f"Updated Finding ID {finding['finding_id']}. Changes: {'; '.join(chgs) if chgs else 'No textual change in key fields.'}")

def remove_finding_entry(finding_id_val=None):
    if not ensure_project_loaded("Removing finding"): return
    fid_str = finding_id_val if finding_id_val else input(f"{BLUE}Finding ID to remove> {ENDC}").strip()
    if not fid_str: 
        log_message("Finding ID cannot be empty.", RED)
        return
    finding, findings = _find_finding_by_id(fid_str)
    if not finding: return
    title_log = finding['title']; fid_log = finding['finding_id']
    if input(f"{RED}{BOLD}Really remove Finding ID {fid_log} ('{title_log}')? (yes/NO)> {ENDC}").lower()!='yes':
        log_message("Removal cancelled.", YELLOW)
        return
    findings = [f for f in findings if f.get("finding_id") != fid_log]
    if save_general_findings(findings):
        log_message(f"Finding ID {fid_log} removed.", GREEN, CAT_ART_SUCCESS)
        log_action_automatic(f"Removed Finding ID {fid_log}: '{title_log}'")

# --- Data Processing Functions ---
# ... (As in previous script)
def combine_folders_to_flat_file():
    if not ensure_project_loaded("Combining folders"): return
    log_message("Combine Folders to Flat File", BOLD + MAGENTA, CAT_ART_WORKING)
    source_dirs = get_paths_from_user("Enter source directory paths.",must_exist=True,allow_multiple=True,entity_type="dir")
    if not source_dirs: log_message("No source directories.", YELLOW); return
    user_output_filename_base = get_output_filename_from_user(f"Base name for combined file (in project '{CURRENT_PROJECT_NAME}/crawl_outputs/'):", "combined_folder_contents.txt")
    output_file_path = get_project_specific_path(os.path.join("crawl_outputs", user_output_filename_base))
    if not output_file_path: log_message("Error: Output path issue.", RED); return
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    files_processed, files_failed = 0, 0
    try:
        with open(output_file_path, 'w', encoding='utf-8', errors='ignore') as outfile:
            for src_dir in source_dirs:
                log_message(f"Processing source: {src_dir}", CYAN)
                src_basename = os.path.basename(os.path.normpath(src_dir))
                for root, _, files in os.walk(src_dir):
                    for filename in files:
                        f_path = os.path.join(root, filename); rel_path = os.path.relpath(f_path, src_dir)
                        try:
                            outfile.write(f"Source Root Directory: {src_basename} (Full: {src_dir})\nFile Path within Source: {rel_path}\nFull Disk Path: {f_path}\n{'-'*40}\n")
                            with open(f_path, 'r', encoding='utf-8', errors='ignore') as infile: outfile.write(infile.read())
                            outfile.write(FILE_SEPARATOR); files_processed += 1
                            log_message(f"    [+] Added: {rel_path} from {src_basename}", GREEN)
                        except Exception as e:
                            log_message(f"    [!] Error with {f_path}: {e}", RED)
                            outfile.write(f"Error processing file {f_path}: {e}\n{FILE_SEPARATOR}"); files_failed += 1
        log_message(f"Processed {files_processed} files. Failed: {files_failed}.", GREEN if files_failed==0 else YELLOW, CAT_ART_SUCCESS if files_failed == 0 else None)
        if files_failed > 0: log_message(f"Failed to process {files_failed} files.", RED, CAT_ART_ERROR if files_failed > 0 and files_processed == 0 else None)
        log_message(f"Combined into: {os.path.abspath(output_file_path)}", BLUE); log_action_automatic(f"Combined folders to '{user_output_filename_base}'. Processed: {files_processed}, Failed: {files_failed}.")
    except Exception as e: log_message(f"Critical error: {e}", RED, CAT_ART_ERROR)

def combine_multiple_flat_files_project_aware():
    if not ensure_project_loaded("Combining flat files"): return
    log_message("Combine Multiple Flat Files", BOLD + MAGENTA, CAT_ART_WORKING)
    input_files = get_paths_from_user("Paths of flat files to combine.", must_exist=True, allow_multiple=True, entity_type="file")
    if not input_files: log_message("No input files.", YELLOW); return
    user_output_filename_base = get_output_filename_from_user(f"Base name for new combined file (in project '{CURRENT_PROJECT_NAME}/crawl_outputs/'):", "super_combined_output.txt")
    output_file_path = get_project_specific_path(os.path.join("crawl_outputs", user_output_filename_base))
    if not output_file_path: log_message("Error: Output path issue.", RED); return
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    files_combined = 0
    try:
        with open(output_file_path, 'w', encoding='utf-8', errors='ignore') as outfile:
            for flat_file in input_files:
                try:
                    outfile.write(f"--- Content from: {os.path.basename(flat_file)} (Full: {flat_file}) ---{FLAT_FILE_SEPARATOR}")
                    with open(flat_file, 'r', encoding='utf-8', errors='ignore') as infile: shutil.copyfileobj(infile, outfile)
                    outfile.write("\n"); files_combined += 1; log_message(f"    [+] Combined: {flat_file}", GREEN)
                except Exception as e: log_message(f"    [!] Error with {flat_file}: {e}", RED); outfile.write(f"Error with {flat_file}: {e}{FLAT_FILE_SEPARATOR}")
        log_message(f"Combined {files_combined} files into {os.path.abspath(output_file_path)}.", GREEN, CAT_ART_SUCCESS); log_action_automatic(f"Combined flat files to '{user_output_filename_base}'. Sources: {len(input_files)}.")
    except Exception as e: log_message(f"Critical error: {e}", RED, CAT_ART_ERROR)

def query_strings_in_files_project_aware():
    if not ensure_project_loaded("Querying strings"): return
    log_message("Query Strings in Files", BOLD + MAGENTA, CAT_ART_THINKING)
    search_files = get_paths_from_user("Paths of flat files to search.",must_exist=True,allow_multiple=True,entity_type="file")
    if not search_files: log_message("No files to search.", YELLOW); return
    queries_in = input(f"{BLUE}Queries (comma-separated)> {ENDC}").strip();
    if not queries_in: log_message("No queries.", YELLOW); return
    queries = [q.strip() for q in queries_in.split(',') if q.strip()]
    case_sens = input(f"{BLUE}Case sensitive? (y/N)> {ENDC}").lower() == 'y'
    use_regex = input(f"{BLUE}Use regex? (y/N)> {ENDC}").lower() == 'y'
    save_res = input(f"{BLUE}Save results to file? (y/N)> {ENDC}").lower() == 'y'
    output_writer = None; results_filepath = None
    if save_res:
        res_dir_base = f"QueryPawsResults_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        res_dir_in_proj = get_project_specific_path(os.path.join("findings", res_dir_base))
        if not res_dir_in_proj: log_message("Error: Project path for results.", RED); save_res = False
        else:
            try:
                os.makedirs(res_dir_in_proj, exist_ok=True)
                res_fname_base = get_output_filename_from_user("Base filename for results:", f"query_matches_{datetime.datetime.now().strftime('%H%M%S')}.txt")
                results_filepath = os.path.join(res_dir_in_proj, res_fname_base)
                output_writer = open(results_filepath, 'w', encoding='utf-8'); log_message(f"Results will save to: {os.path.abspath(results_filepath)}", CYAN)
            except Exception as e: log_message(f"Error opening results file: {e}. Console only.", RED); output_writer=None; save_res=False
    log_message("Searching...", CYAN, CAT_ART_WORKING); total_matches = 0
    active_queries = list(queries) 
    for s_file in search_files:
        log_message(f"--- Searching in: {s_file} ---", BLUE)
        if output_writer: output_writer.write(f"--- Results from: {s_file} ---\nQueries:{', '.join(queries)} (Case:{case_sens},Regex:{use_regex})\n\n")
        try:
            with open(s_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line_content in enumerate(f, 1):
                    line_to_search = line_content if case_sens else line_content.lower()
                    temp_active_queries = list(active_queries) 
                    for query_idx, query in enumerate(temp_active_queries):
                        q_use = query if case_sens else query.lower(); match = False
                        try:
                            if use_regex and re.search(q_use, line_to_search): match = True
                            elif not use_regex and q_use in line_to_search: match = True
                        except re.error as re_err: 
                            log_message(f"Regex error for query '{query}': {re_err}. Skipping this query for this session.", RED)
                            if query in active_queries: active_queries.remove(query) 
                            continue
                        if match:
                            total_matches+=1; match_info=f"{GREEN}Match:{ENDC} File:{BOLD}{s_file}{ENDC},Line:{BOLD}{line_num}{ENDC}\nQuery:'{query}'\nContent:{line_content.strip()}"
                            print(match_info+"\n"+"-"*20)
                            if output_writer: output_writer.write(f"L{line_num}(Q:'{query}'):{line_content.strip()}\n\n"); break
        except Exception as e: log_message(f"Error reading {s_file}: {e}", RED)
        if output_writer: output_writer.write(f"Error reading {s_file}: {e}\n\n") 
    if output_writer: output_writer.close()
    if total_matches > 0:
        log_message(f"Found {total_matches} matches!", GREEN, CAT_ART_SUCCESS)
        if save_res and results_filepath: log_message(f"Results saved to: {os.path.abspath(results_filepath)}", BLUE); log_action_automatic(f"Query:'{queries_in}'. Files:{len(search_files)}. Found:{total_matches}. Saved:{os.path.abspath(results_filepath)}")
    else: log_message("No matches found.", YELLOW, CAT_ART_THINKING); log_action_automatic(f"Query:'{queries_in}'. Files:{len(search_files)}. No matches.")


# --- Main Application Loop and Help ---
def display_help():
    # ... (Help text as defined previously, now including General Findings commands and Importer)
    help_text = f"""
{BOLD + MAGENTA}PurrfectPurpleProcessor Help Menu:{ENDC}
{CAT_ART_INPUT}
{BOLD + BLUE}--- Project Management ---{ENDC}
  {GREEN}new_project{ENDC}           - Create project
  {GREEN}load_project [<name>]{ENDC} - Load project by name
  {GREEN}current_project{ENDC}       - Show current project
  {GREEN}list_projects{ENDC}         - List all projects

{BOLD + BLUE}--- Action Logging ---{ENDC}
  {GREEN}log_action{ENDC}            - Manually log action (Project loaded)
  {GREEN}view_log{ENDC}              - View action log (Project loaded)

{BOLD + BLUE}--- To-Do List (Project Loaded) ---{ENDC}
  {GREEN}add_todo{ENDC}              - Add task
  {GREEN}list_todos{ENDC}            - List tasks (filters: status, pri, sev, cat, tgt; sort by new)
  {GREEN}mark_done <id>{ENDC}        - Mark task ID as done
  {GREEN}edit_todo <id>{ENDC}        - Edit task ID
  {GREEN}remove_todo <id>{ENDC}      - Remove task ID

{BOLD + BLUE}--- Plugin Tracker (Project Loaded) ---{ENDC}
  {GREEN}add_plugin{ENDC}            - Add a new plugin entry.
  {GREEN}list_plugins{ENDC}          - List and filter plugin entries.
  {GREEN}view_plugin <id>{ENDC}      - View details of a specific plugin.
  {GREEN}update_plugin <id>{ENDC}    - Update an existing plugin entry.
  {GREEN}remove_plugin <id>{ENDC}    - Remove a plugin entry.

{BOLD + BLUE}--- AJAX Action Tracker (Project Loaded) ---{ENDC}
  {GREEN}add_ajax{ENDC}              - Add a new AJAX action entry.
  {GREEN}list_ajax{ENDC}             - List and filter AJAX action entries.
  {GREEN}view_ajax <id>{ENDC}        - View details of a specific AJAX action.
  {GREEN}update_ajax <id>{ENDC}      - Update an existing AJAX action entry.
  {GREEN}remove_ajax <id>{ENDC}      - Remove an AJAX action entry.

{BOLD + BLUE}--- Asset Tracker (Meow-chines - Project Loaded) ---{ENDC}
  {GREEN}add_asset{ENDC}             - Add a new asset (host, IP, website).
  {GREEN}list_assets{ENDC}           - List and filter assets.
  {GREEN}view_asset <id|ident>{ENDC} - View details of a specific asset.
  {GREEN}update_asset <id|ident>{ENDC}- Update an existing asset's general info.
  {GREEN}add_svc <id|ident>{ENDC}    - Add a network service (port/protocol) to an asset.
  {GREEN}update_svc <id|ident>{ENDC} - Update an existing service on an asset.
  {GREEN}remove_svc <id|ident>{ENDC} - Remove a service from an asset.
  {GREEN}remove_asset <id|ident>{ENDC}- Remove an asset.

{BOLD + BLUE}--- General Findings Tracker (Clue Collector - Project Loaded) ---{ENDC}
  {GREEN}add_finding{ENDC}           - Manually add a new finding.
  {GREEN}list_findings{ENDC}         - List and filter findings.
  {GREEN}view_finding <id>{ENDC}     - View details of a specific finding.
  {GREEN}update_finding <id>{ENDC}   - Update an existing finding.
  {GREEN}remove_finding <id>{ENDC}   - Remove a finding.
  {GREEN}import_findings <file.jsonl> [--tool <type>] [--project <name>]{ENDC} - Import findings from JSONL file.

{BOLD + BLUE}--- Data Processing (Project Loaded) ---{ENDC}
  {GREEN}1. combine_folders{ENDC}   - Combine folder contents to flat file (in project 'crawl_outputs/')
  {GREEN}2. combine_files{ENDC}     - Combine flat files (output to project 'crawl_outputs/')
  {GREEN}3. query{ENDC}             - Search strings in flat files (results to project 'findings/')
  
{BOLD + BLUE}--- General ---{ENDC}
  {CYAN}help{ENDC}, {CYAN}-h{ENDC}, {CYAN}--help{ENDC}   - Show this help
  {RED}exit{ENDC}                - Exit
"""
    print(help_text)

# --- Importer Function ---
def import_findings_cmd(args=None): # Modified to accept args for direct call
    if not ensure_project_loaded("Importing findings"): 
        if args and args.project_context: # Try to load project if specified in args
            load_project(args.project_context)
            if not ensure_project_loaded("Importing findings"): return
        else:
            return

    log_message("Data Ingestion Purr-o-col", BOLD + MAGENTA, CAT_ART_IMPORTER)

    filepath_to_import = None
    if args and args.filepath:
        filepath_to_import = args.filepath
    else:
        filepath_to_import_list = get_paths_from_user("Enter path to JSONL file to import:", must_exist=True, allow_multiple=False, entity_type="file")
        if not filepath_to_import_list:
            log_message("No file selected for import.", YELLOW)
            return
        filepath_to_import = filepath_to_import_list[0]

    if not os.path.exists(filepath_to_import):
        log_message(f"Error: File not found at '{filepath_to_import}'", RED)
        return

    all_findings_in_project = load_general_findings()
    imported_count = 0
    skipped_count = 0
    linked_to_assets_count = 0

    try:
        with open(filepath_to_import, 'r', encoding='utf-8') as f_in:
            for line_num, line in enumerate(f_in, 1):
                line_stripped = line.strip()
                if not line_stripped: continue # Skip empty lines

                try:
                    insight_data = json.loads(line_stripped)
                except json.JSONDecodeError as e:
                    log_message(f"Warning: Skipping line {line_num} due to JSON decode error: {e}", YELLOW)
                    skipped_count +=1
                    continue

                # Basic Schema Validation (presence of key fields)
                required_fields = ["insight_id", "target_context", "title", "source_tool_name", "category", "type", "timestamp_generated_utc", "timestamp_event_utc"]
                missing_fields = [field for field in required_fields if field not in insight_data]
                if missing_fields:
                    log_message(f"Warning: Skipping insight on line {line_num} due to missing fields: {', '.join(missing_fields)} (Original Insight ID: {insight_data.get('insight_id','N/A')})", YELLOW)
                    skipped_count +=1
                    continue
                
                # Create a new finding structure for PPP
                new_ppp_finding = {
                    "finding_id": get_next_finding_id(all_findings_in_project),
                    "project_id": CURRENT_PROJECT_NAME,
                    "insight_id": insight_data.get("insight_id"), # From source JSONL
                    "target_context": insight_data.get("target_context", "N/A"),
                    "source_type": insight_data.get("source_type", "ToolOutput"),
                    "source_tool_name": insight_data.get("source_tool_name", "UnknownTool"),
                    "source_reference": insight_data.get("source_reference", os.path.basename(filepath_to_import)),
                    "timestamp_generated_utc": insight_data.get("timestamp_generated_utc"),
                    "timestamp_event_utc": insight_data.get("timestamp_event_utc"),
                    "category": insight_data.get("category", "General"),
                    "type": insight_data.get("type", "Observation"),
                    "title": insight_data.get("title", "Imported Finding"),
                    "description": insight_data.get("description", "N/A"),
                    "severity_assessment": insight_data.get("severity_assessment", "Informational"),
                    "confidence": insight_data.get("confidence", "Medium"),
                    "status": insight_data.get("status", "Open"), # Default status for new imports
                    "actionable_recommendation": insight_data.get("actionable_recommendation", "N/A"),
                    "key_data_points": insight_data.get("key_data_points", {}),
                    "tags": sorted(list(set(insight_data.get("tags", [])))),
                    "notes": insight_data.get("notes", "N/A"), # Could be "Imported from file X"
                    "raw_input_snippet_if_applicable": insight_data.get("raw_input_snippet_if_applicable", None),
                    "date_added_to_ppp": datetime.datetime.now(timezone.utc).isoformat(),
                    "last_updated_in_ppp": datetime.datetime.now(timezone.utc).isoformat(),
                    "asset_ids": [], # Initialize; will attempt to populate
                    "linked_plugin_ids": [],
                    "linked_ajax_ids": [],
                    "linked_todo_ids": []
                }

                # Attempt to link to assets
                target_str = new_ppp_finding["target_context"]
                if target_str and target_str.lower() != "n/a":
                    # Use a simplified asset lookup for now, exact match on primary_identifier
                    # _find_asset_by_id_or_identifier can be adapted or a more specific lookup can be used
                    all_project_assets = load_assets() # Load fresh list for each finding for simplicity here
                    for asset in all_project_assets:
                        match_found = False
                        if target_str.lower() == asset.get("primary_identifier","").lower():
                            match_found = True
                        elif target_str.lower() in [ip.lower() for ip in asset.get("ip_addresses", [])]:
                            match_found = True
                        elif target_str.lower() in [h.lower() for h in asset.get("hostnames", [])]:
                             match_found = True
                        
                        if match_found:
                            if asset.get("asset_id") not in new_ppp_finding["asset_ids"]:
                                new_ppp_finding["asset_ids"].append(asset.get("asset_id"))
                                log_message(f"  Linked insight '{new_ppp_finding['title'][:30]}...' to asset ID {asset.get('asset_id')} ('{asset.get('primary_identifier')}')", GREEN)
                                if not linked_to_assets_count: # Count first link
                                     linked_to_assets_count +=1
                                elif new_ppp_finding["asset_ids"].count(asset.get("asset_id")) == 1 : # count additional links
                                     linked_to_assets_count +=1


                all_findings_in_project.append(new_ppp_finding)
                imported_count += 1
        
        if save_general_findings(all_findings_in_project):
            log_message(f"Successfully imported {imported_count} findings. Skipped: {skipped_count}.", GREEN, CAT_ART_SUCCESS)
            if linked_to_assets_count > 0:
                log_message(f"Attempted to link {linked_to_assets_count} findings to existing assets.", CYAN)
            log_action_automatic(f"Imported {imported_count} findings from '{os.path.basename(filepath_to_import)}'. Skipped: {skipped_count}. Linked: {linked_to_assets_count}")
        else:
            log_message(f"Imported {imported_count} findings, but failed to save to project file. Skipped: {skipped_count}.", RED)

    except FileNotFoundError:
        log_message(f"Error: Input file '{filepath_to_import}' not found during import operation.", RED, CAT_ART_ERROR)
    except Exception as e:
        log_message(f"An unexpected error occurred during import: {e}", RED, CAT_ART_ERROR)
        import traceback
        traceback.print_exc()

def main():
    global CURRENT_PROJECT_NAME, CURRENT_PROJECT_PATH, BASE_PROJECTS_DIR, timezone
    
    # Argument parser for invoking importer directly from command line
    cli_parser = argparse.ArgumentParser(description="PurrfectPurpleProcessor CLI", add_help=False) # add_help=False to allow custom help later
    cli_parser.add_argument('command', nargs='?', help="Command to execute (e.g., 'help', 'import_findings')")
    cli_parser.add_argument('filepath', nargs='?', help="Filepath for commands like 'import_findings'")
    cli_parser.add_argument('--tool_type_override', help="Override tool type for import_findings")
    cli_parser.add_argument('--project_context', help="Specify project context for import_findings if not loaded")
    # Add other top-level args if PPP evolves to support more direct CLI actions without interactive shell

    # Check if running with specific command for importer
    # This allows 'python purrfect_processor.py import_findings /path/to/file.jsonl --project_context MyProject'
    if len(sys.argv) > 1 and sys.argv[1] == 'import_findings':
        # Temporarily parse known args for importer, rest will be handled by interactive loop or ignored
        # This is a simple way to allow direct command invocation for the importer
        # For a more robust CLI argument system, a more sophisticated dispatcher would be needed.
        try:
            importer_args, _ = cli_parser.parse_known_args() # Parse known args, ignore others for now
            if importer_args.command == 'import_findings' and importer_args.filepath:
                if importer_args.project_context:
                    load_project(importer_args.project_context) # Attempt to load project
                import_findings_cmd(importer_args) # Pass parsed args
                return # Exit after direct command execution
            elif importer_args.command == 'import_findings' and not importer_args.filepath:
                log_message("Error: 'import_findings' command requires a filepath argument.", RED)
                return
        except SystemExit: # Argparse calls sys.exit on --help or error
            return # Allow argparse to handle its own exit
        except Exception as e: # Catch other parsing errors if any
            log_message(f"Error parsing direct command: {e}", RED)
            # Fall through to interactive shell
            pass


    if not os.path.isdir(BASE_PROJECTS_DIR):
        try: os.makedirs(BASE_PROJECTS_DIR, exist_ok=True)
        except Exception as e: 
            print(f"{RED}FATAL: Cannot create base dir '{BASE_PROJECTS_DIR}': {e}{ENDC}")
            return

    log_message("", None, CAT_ART_WELCOME, no_cat_prefix=True)
    if not CURRENT_PROJECT_NAME:
        log_message("No project loaded. Use 'new_project' or 'load_project'. Projects:", YELLOW, CAT_ART_THINKING)
        list_available_projects()
        print("-" * 30)
    display_help()

    while True:
        try:
            prompt_prefix = f"{BOLD}{CYAN}Purrfect"
            if CURRENT_PROJECT_NAME: 
                prompt_prefix += f"({BOLD}{GREEN}{CURRENT_PROJECT_NAME}{ENDC}{CYAN})"
            prompt_prefix += f">{ENDC} "
            
            cmd_full = input(f"\n{prompt_prefix}").strip()
            cmd_parts = cmd_full.split(); cmd = cmd_parts[0].lower() if cmd_parts else ""; args = cmd_parts[1:]

            if cmd == 'new_project': create_new_project()
            elif cmd == 'load_project': load_project(args[0] if args else None)
            elif cmd == 'current_project': display_current_project()
            elif cmd == 'list_projects': list_available_projects()
            elif cmd == 'log_action': log_action_manual()
            elif cmd == 'view_log': view_action_log()
            elif cmd == 'add_todo': add_todo_item()
            elif cmd == 'list_todos': list_todo_items()
            elif cmd == 'mark_done': mark_todo_done(args[0] if args else None)
            elif cmd == 'edit_todo': edit_todo_item(args[0] if args else None)
            elif cmd == 'remove_todo': remove_todo_item(args[0] if args else None)
            elif cmd == 'add_plugin': add_plugin_entry()
            elif cmd == 'list_plugins': list_plugin_entries()
            elif cmd == 'view_plugin': view_plugin_details(args[0] if args else None)
            elif cmd == 'update_plugin': update_plugin_entry(args[0] if args else None)
            elif cmd == 'remove_plugin': remove_plugin_entry(args[0] if args else None)
            elif cmd == 'add_ajax': add_ajax_action_entry()
            elif cmd == 'list_ajax': list_ajax_action_entries()
            elif cmd == 'view_ajax': view_ajax_action_details(args[0] if args else None)
            elif cmd == 'update_ajax': update_ajax_action_entry(args[0] if args else None)
            elif cmd == 'remove_ajax': remove_ajax_action_entry(args[0] if args else None)
            elif cmd == 'add_asset': add_asset_entry()
            elif cmd == 'list_assets': list_assets()
            elif cmd == 'view_asset': view_asset_details_cmd(args[0] if args else None)
            elif cmd == 'update_asset': update_asset_entry(args[0] if args else None)
            elif cmd == 'add_svc': add_asset_service_cmd(args[0] if args else None)
            elif cmd == 'update_svc': update_asset_service_cmd(args[0] if args else None)
            elif cmd == 'remove_svc': remove_asset_service_cmd(args[0] if args else None)
            elif cmd == 'remove_asset': remove_asset_entry(args[0] if args else None)
            elif cmd == 'add_finding': add_finding_entry()
            elif cmd == 'list_findings': list_general_findings()
            elif cmd == 'view_finding': view_finding_details_cmd(args[0] if args else None) 
            elif cmd == 'update_finding': update_finding_entry(args[0] if args else None)
            elif cmd == 'remove_finding': remove_finding_entry(args[0] if args else None)
            elif cmd == 'import_findings': # Interactive import
                # Construct a dummy args object for the function if called interactively
                # A more robust CLI would use sub-parsers in argparse.
                interactive_import_args = argparse.Namespace(
                    filepath=args[0] if args else None, 
                    tool_type_override=args[1] if len(args) > 1 else None, # Simplistic arg parsing
                    project_context=None # Not setting project_context here as it's from current loaded
                )
                if not interactive_import_args.filepath:
                    log_message("Usage: import_findings <filepath.jsonl> [--tool <tool_type>]", YELLOW)
                else:
                    import_findings_cmd(interactive_import_args)
            elif cmd == '1' or cmd == 'combine_folders': combine_folders_to_flat_file()
            elif cmd == '2' or cmd == 'combine_files': 
                if ensure_project_loaded("Combining flat files"): combine_multiple_flat_files_project_aware()
            elif cmd == '3' or cmd == 'query':
                if ensure_project_loaded("Querying strings"): query_strings_in_files_project_aware()
            elif cmd == 'help' or cmd == '-h' or cmd == '--help': display_help()
            elif cmd == 'exit': break
            elif not cmd: continue
            else: log_message(f"Meow? Unknown command: '{cmd}'. Type 'help'.", YELLOW, CAT_ART_THINKING)
        except KeyboardInterrupt: 
            log_message("\nCtrl+C. Exiting...", YELLOW)
            break
        except Exception as e:
            log_message(f"Unexpected hiss-ue: {e}", RED, CAT_ART_ERROR)
            import traceback
            traceback.print_exc()
    log_message("", None, CAT_ART_GOODBYE, no_cat_prefix=True)

if __name__ == "__main__":
    main()
