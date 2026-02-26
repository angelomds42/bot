from telegram import InlineKeyboardButton
from typing import Dict, List

HELP_MODULES: Dict[str, str] = {}


def register_module_help(module_name: str, help_key: str):
    HELP_MODULES[module_name] = help_key


def get_help_keyboard(
    back_callback: str = "start_main",
) -> List[List[InlineKeyboardButton]]:
    """Generates a keyboard with all registered modules in rows of 2."""
    buttons = [
        InlineKeyboardButton(name, callback_data=f"help_mod_{name}")
        for name in sorted(HELP_MODULES.keys())
    ]
    keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    keyboard.append([InlineKeyboardButton("« Back", callback_data=back_callback)])
    return keyboard


def get_module_help(module_name: str):
    return HELP_MODULES.get(module_name)
