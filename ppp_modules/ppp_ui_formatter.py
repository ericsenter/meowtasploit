#!/usr/bin/env python3
# ppp_ui_formatters.py

import json

# Attempt to import from ppp_theme_manager, with stubs for standalone testing/development
try:
    from ppp_theme_manager import (
        get_theme_color, get_theme_icon, apply_theme_to_string,
        ENDC, BOLD, DIM, ITALIC, UNDERLINE # Assuming these are exported for direct use if needed
    )
except ImportError:
    print("DEVELOPMENT MODE: ppp_ui_formatters.py - ppp_theme_manager.py not found, using stubs.")
    # Minimal stubs to allow this module to be parsed and basic logic tested
    def get_theme_color(color_key, default_fallback=""): return "" # No actual color
    def get_theme_icon(icon_key, default_fallback=""): return default_fallback if default_fallback else "I:"
    def apply_theme_to_string(text, color_key, bold=False, underline=False, italic=False, dim=False, reverse=False):
        return text # No actual styling
    ENDC, BOLD, DIM, ITALIC, UNDERLINE = "", "", "", "", ""


def _ui_formatter_log(message, level="debug"):
    """
    Placeholder for logging within UI formatters.
    In a real application, this would integrate with the main logging system
    which would itself use the theme manager for styled log output.
    """
    timestamp = "YYYY-MM-DD HH:MM:SS" # Replace with actual timestamping if needed for standalone
    # Basic print, as this module shouldn't assume the main logger's full capabilities
    print(f"[{timestamp}][{level.upper()}/UIFormatter] {message}")


def _truncate_text(text: str, max_width: int, ellipsis: str = '…') -> str:
    """
    Truncates text to max_width if it's longer, adding an ellipsis.
    Ensures that the ellipsis itself doesn't cause the string to exceed max_width.
    """
    if not isinstance(text, str):
        text = str(text) # Ensure we are working with a string

    if max_width <= 0:
        return "" # Cannot display anything in zero or negative width

    if len(ellipsis) > max_width: # Edge case: ellipsis is too long for the allowed width
        return ellipsis[:max_width]

    if len(text) > max_width:
        return text[:max_width - len(ellipsis)] + ellipsis
    return text


def format_list_item_line(item_data: dict, column_configs: list, default_na_str: str = 'N/A') -> str:
    """
    Formats a single dictionary item for a table-like list view based on column configurations.

    Args:
        item_data (dict): The dictionary representing one row of data.
        column_configs (list): A list of dictionaries, where each dict configures a column.
            Example config per column:
            {
                "key": "data_key_in_item_data",
                "label": "Column Header Label", (used by generate_list_header)
                "width": 20, # characters
                "align": "left" | "right" | "center" (defaults to left, or right for numbers),
                "color_key": "theme_color_role_for_value", (optional, defaults to text_primary)
                "bold": False, (optional)
                "italic": False, (optional)
                "underline": False, (optional)
                "dim": False, (optional)
                "formatter_func": lambda value, theme_access: "Formatted " + str(value), (optional)
                "dynamic_color_key_map": {"value1": "color_key1", "value2": "color_key2", "default": "default_color_key"}, (optional)
                "dynamic_color_trigger_field": "field_in_item_data_for_dynamic_color" (optional, defaults to current column's key)
            }
        default_na_str (str): String to display for missing or None values if no formatter handles it.

    Returns:
        str: A fully formatted and themed string representing the list item line.
    """
    line_parts = [get_theme_icon('list_item_bullet', default_fallback="• ")] # Start with a bullet
    theme_access = {
        "get_color": get_theme_color,
        "get_icon": get_theme_icon,
        "apply_style": apply_theme_to_string
    }
    na_themed = apply_theme_to_string(default_na_str, "text_secondary", dim=True)

    for config in column_configs:
        col_key = config.get("key")
        if not col_key:
            _ui_formatter_log(f"Column config missing 'key': {config}", level="warning")
            # Add a placeholder for the missing column to maintain layout
            width = config.get("width", 10)
            line_parts.append(" " * width) # Add empty space
            continue

        width = config.get("width", 20)
        raw_value = item_data.get(col_key)
        value_str = na_themed # Default if value is None or formatter fails and returns None

        if raw_value is not None:
            if config.get("formatter_func"):
                try:
                    formatted_val = config["formatter_func"](raw_value, theme_access=theme_access)
                    value_str = str(formatted_val) if formatted_val is not None else na_themed
                except Exception as e:
                    _ui_formatter_log(f"Error in custom list formatter for key '{col_key}': {e}", level="error")
                    value_str = apply_theme_to_string("FmtErr!", "error", bold=True)
            else:
                value_str = str(raw_value) # Ensure string conversion for various data types
        elif config.get("formatter_func"): # Allow formatter to handle None if it wants to
             try:
                formatted_val = config["formatter_func"](None, theme_access=theme_access)
                value_str = str(formatted_val) if formatted_val is not None else na_themed
             except Exception as e:
                _ui_formatter_log(f"Error in custom list formatter (for None value) for key '{col_key}': {e}", level="error")
                value_str = apply_theme_to_string("FmtErr!", "error", bold=True)


        # Alignment
        align = config.get("align")
        if align is None: # Default alignment based on (raw) type if not specified
            if isinstance(raw_value, (int, float)):
                align = "right"
            else:
                align = "left"

        truncated_value = _truncate_text(value_str if ENDC in value_str else value_str.strip(), width, ellipsis='…') # Strip non-styled for length calc

        # If value_str was already themed by formatter_func, we need to be careful with rjust/ljust/center
        # A simple approach: if it's themed, just truncate and left-align for now, or expect formatter to handle width.
        # For this implementation, we assume formatter_func returns a string that can be further processed.
        # If formatter_func returns a themed string, ANSI codes will mess up .ljust etc.
        # Solution: apply theming *after* alignment and truncation.
        
        # Re-evaluate value_str for alignment (use unstyled for length calculation)
        plain_value_for_align_calc = ""
        if raw_value is not None:
            if config.get("formatter_func"):
                # To get plain value for length, we'd ideally call formatter then strip ANSI
                # This is complex. Simpler: assume formatter output is for display, and we truncate it.
                # For now, we use the already potentially themed value_str for truncation.
                # A better way: formatter returns (plain_text, already_themed_flag)
                # Or, formatter should not apply colors if table needs to.
                # Let's assume formatter returns plain text for now for alignment logic.
                try:
                    # Re-call formatter if needed, or store its plain output if possible
                    # This is a simplification:
                    if config.get("formatter_func"):
                        plain_value_for_align_calc = str(config["formatter_func"](raw_value, theme_access=None)) # Pass None theme_access to get raw
                    else:
                        plain_value_for_align_calc = str(raw_value)
                except:
                    plain_value_for_align_calc = str(raw_value) if raw_value is not None else default_na_str

            else:
                plain_value_for_align_calc = str(raw_value) if raw_value is not None else default_na_str
        else:
            plain_value_for_align_calc = default_na_str


        truncated_plain_value = _truncate_text(plain_value_for_align_calc, width, ellipsis='…')


        if align == "right":
            aligned_value_text = truncated_plain_value.rjust(width)
        elif align == "center":
            aligned_value_text = truncated_plain_value.center(width)
        else: # Default to left
            aligned_value_text = truncated_plain_value.ljust(width)

        # Determine color for the aligned text
        color_key = config.get("color_key", "text_primary")
        if config.get("dynamic_color_key_map"):
            dynamic_field_key = config.get("dynamic_color_trigger_field", col_key)
            dynamic_field_value = str(item_data.get(dynamic_field_key, "Unknown")) # Ensure string for map lookup
            color_key = config["dynamic_color_key_map"].get(
                dynamic_field_value,
                config["dynamic_color_key_map"].get("default", color_key)
            )

        # Apply styling
        styled_cell = apply_theme_to_string(
            aligned_value_text,
            color_key,
            bold=config.get("bold", False),
            italic=config.get("italic", False),
            underline=config.get("underline", False),
            dim=config.get("dim", False)
        )
        line_parts.append(styled_cell)

    return "  ".join(line_parts) # Use a couple of spaces as a column separator


def generate_list_header(column_configs: list, header_title: str = None) -> str:
    """
    Generates a themed header string for list displays based on column_configs.
    """
    header_lines = []
    if header_title:
        title_icon = get_theme_icon('view_title_icon', default_fallback=" L ")
        header_lines.append(apply_theme_to_string(f"{title_icon}{header_title}", 'header', bold=True))

    labels_line_parts = [get_theme_icon('list_item_bullet', default_fallback="  ")] # Align with item bullet
    separator_line_parts = ["  "] # Align with item bullet

    for config in column_configs:
        col_key = config.get("key")
        if not col_key: # Skip misconfigured columns
             width = config.get("width", 10)
             labels_line_parts.append(" " * width)
             separator_line_parts.append(" " * width)
             continue

        width = config.get("width", 20)
        label_text = config.get("label", col_key.replace("_", " ").title())

        # Header alignment: uses "align_header" if present, falls back to "align", then "center"
        align = config.get("align_header", config.get("align", "center"))
        truncated_label = _truncate_text(label_text, width, ellipsis='…')

        if align == "right":
            aligned_label_text = truncated_label.rjust(width)
        elif align == "left":
            aligned_label_text = truncated_label.ljust(width)
        else: # Default header align to center
            aligned_label_text = truncated_label.center(width)

        labels_line_parts.append(apply_theme_to_string(aligned_label_text, 'subheader', bold=True))

        sep_char = get_theme_icon('table_header_separator_char', default_fallback="─")
        # Ensure separator char is not empty
        sep_char_to_use = sep_char if sep_char and sep_char.strip() else "─"
        
        # Color the separator line itself using subheader color but dimmed
        separator_segment = apply_theme_to_string(sep_char_to_use * width, 'subheader', dim=True)
        separator_line_parts.append(separator_segment)

    header_lines.append("  ".join(labels_line_parts))
    header_lines.append("  ".join(separator_line_parts))
    return "\n".join(header_lines)


def format_detailed_view(data_dict: dict, field_configs: list, entry_title: str = None, max_label_width_override: int = None) -> str:
    """
    Formats a single dictionary for a multi-line detailed view.

    Args:
        data_dict (dict): The data to display.
        field_configs (list): List of dicts, each configuring a field. Example:
            {
                "key": "data_key",
                "label": "Display Label", (defaults to key.title())
                "label_color_key": "theme_color_for_label", (optional)
                "value_color_key": "theme_color_for_value", (optional)
                "label_bold": True, (optional)
                "value_dim": False, (optional)
                "multiline": False, (if True, value newlines are preserved and indented)
                "formatter_func": lambda value, theme_access: "Formatted: " + str(value), (optional)
                "dynamic_color_key_map": {"val1":"color1", "default":"color_default"}, (optional, for value color)
                "dynamic_color_trigger_field": "field_for_dynamic_color_value" (optional, defaults to current key)
                "max_value_width": 80 (optional, for truncating simple string values on a single line)
            }
        entry_title (str): Optional title for the view.
        max_label_width_override (int): Optional override for label column width.

    Returns:
        str: A fully formatted and themed string for detailed display.
    """
    output_lines = []
    theme_access = {
        "get_color": get_theme_color,
        "get_icon": get_theme_icon,
        "apply_style": apply_theme_to_string
    }
    default_na_styled = theme_access["apply_style"]("N/A", "text_secondary", dim=True)

    if entry_title:
        title_icon = get_theme_icon('view_title_icon', default_fallback="❖ ")
        output_lines.append(apply_theme_to_string(f"{title_icon}{entry_title}", 'header', bold=True))
        major_separator = get_theme_icon('separator_major')
        if major_separator: # Only add if separator is not empty
             output_lines.append(major_separator)


    if not field_configs:
        _ui_formatter_log("format_detailed_view called with no field_configs.", level="warning")
        return "\n".join(output_lines)

    # Determine max label width for alignment
    if max_label_width_override is not None:
        label_width = max_label_width_override
    else:
        try:
            label_width = max(len(str(config.get("label", config.get("key", "")).replace("_", " "))) for config in field_configs if config.get("key")) + 1 # +1 for colon
        except ValueError: # Handles empty field_configs or configs without labels/keys
            label_width = 20 # Default
    label_width = max(10, label_width) # Ensure a minimum label width

    for config in field_configs:
        key = config.get("key")
        if not key:
            _ui_formatter_log(f"Field config missing 'key': {config}", level="warning")
            continue

        label_text = str(config.get("label", key.replace("_", " ").title()))
        raw_value = data_dict.get(key)

        # Label Styling
        label_color_key = config.get("label_color_key", "accent2")
        is_label_bold = config.get("label_bold", True) # Labels often bold by default
        themed_label = apply_theme_to_string(f"{label_text}:".ljust(label_width), label_color_key, bold=is_label_bold)

        # Value Styling & Formatting
        value_color_key_base = config.get("value_color_key", "text_primary")
        is_value_dim = config.get("value_dim", False)
        is_value_italic = config.get("value_italic", False) # Added
        is_value_bold = config.get("value_bold", False) # Added

        # Determine dynamic color for the value if configured
        final_value_color_key = value_color_key_base
        if config.get("dynamic_color_key_map"):
            dynamic_trigger_key = config.get("dynamic_color_trigger_field", key)
            dynamic_trigger_value = str(data_dict.get(dynamic_trigger_key, "Unknown"))
            final_value_color_key = config["dynamic_color_key_map"].get(
                dynamic_trigger_value,
                config["dynamic_color_key_map"].get("default", value_color_key_base)
            )
        
        formatted_value_str = ""
        # Handle None or empty values, but allow formatter_func to override this
        if raw_value is None or \
           (isinstance(raw_value, (str, list, dict)) and not raw_value and not config.get("formatter_func")):
            formatted_value_str = default_na_styled
        elif config.get("formatter_func"):
            try:
                # Pass raw value and theme_access dictionary
                temp_val = config["formatter_func"](raw_value, theme_access=theme_access)
                formatted_value_str = str(temp_val) if temp_val is not None else default_na_styled
                # If formatter didn't theme it, apply default value styling
                if ENDC not in formatted_value_str: # Basic check if already styled
                     formatted_value_str = apply_theme_to_string(formatted_value_str, final_value_color_key, dim=is_value_dim, italic=is_value_italic, bold=is_value_bold)
            except Exception as e:
                _ui_formatter_log(f"Error in custom detail formatter for key '{key}': {e}", level="error")
                formatted_value_str = apply_theme_to_string("FormatErr!", "error", bold=True)
        elif isinstance(raw_value, list):
            if not raw_value: formatted_value_str = default_na_styled
            else: formatted_value_str = apply_theme_to_string(", ".join(map(str, raw_value)), final_value_color_key, dim=is_value_dim, italic=is_value_italic, bold=is_value_bold)
        elif isinstance(raw_value, dict) and config.get("multiline"): # Nicer dict formatting for multiline
            if not raw_value: formatted_value_str = default_na_styled
            else:
                try:
                    json_str = json.dumps(raw_value, indent=2)
                    lines = json_str.splitlines()
                    styled_lines = [apply_theme_to_string(lines[0], final_value_color_key, dim=is_value_dim, italic=is_value_italic, bold=is_value_bold)]
                    for line in lines[1:]:
                        styled_lines.append(f"{' ' * (label_width + 1)}{apply_theme_to_string(line, final_value_color_key, dim=is_value_dim, italic=is_value_italic, bold=is_value_bold)}")
                    formatted_value_str = "\n".join(styled_lines)
                except TypeError: # Handle non-serializable dicts gracefully for display
                    formatted_value_str = apply_theme_to_string(str(raw_value), final_value_color_key, dim=is_value_dim, italic=is_value_italic, bold=is_value_bold)

        elif config.get("multiline") and isinstance(raw_value, str):
            lines = raw_value.splitlines()
            if not lines: formatted_value_str = default_na_styled
            else:
                styled_lines = [apply_theme_to_string(lines[0], final_value_color_key, dim=is_value_dim, italic=is_value_italic, bold=is_value_bold)]
                for line in lines[1:]:
                    styled_lines.append(f"{' ' * (label_width + 1)}{apply_theme_to_string(line, final_value_color_key, dim=is_value_dim, italic=is_value_italic, bold=is_value_bold)}")
                formatted_value_str = "\n".join(styled_lines)
        else: # Simple string or other primitive, apply truncation
            max_val_width = config.get("max_value_width", 80) # Default width for single line values
            display_value = _truncate_text(str(raw_value), max_val_width, ellipsis='…')
            formatted_value_str = apply_theme_to_string(display_value, final_value_color_key, dim=is_value_dim, italic=is_value_italic, bold=is_value_bold)

        output_lines.append(f"  {themed_label} {formatted_value_str}")

    minor_separator = get_theme_icon('separator_minor')
    if minor_separator: # Only add if separator is not empty
        output_lines.append(f"  {minor_separator}")
    return "\n".join(output_lines)
