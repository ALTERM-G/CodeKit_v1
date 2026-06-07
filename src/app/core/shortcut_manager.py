from PyQt6.QtWidgets import QApplication, QTextEdit
from PyQt6.QtGui import QKeySequence, QShortcut
from functools import partial

class ShortcutManager:
    def __init__(self, window):
        self.window = window
        """Initializes the ShortcutManager with a reference to the main window."""
        self.shortcuts = []

    def get_shortcut_action_keys(self):
        """Returns a list of all possible untranslated shortcut action keys."""
        actions = ["None", "Copy Current Output", "Go to Next Tab", "Go to Previous Tab"]
        actions.extend(["Go to: Python REPL", "Go to: ASCII Text Art", "Go to: Regex Tester"])
        for menu_name in self.window.menu_definitions:
            actions.append(f"Go to: {menu_name}")
        return actions

    def update_shortcut_key(self, index, key_sequence):
        """Updates a shortcut key in the settings."""
        self.window.settings["shortcuts"][index]["key"] = key_sequence.toString()
        self.window.save_settings()
        self.setup_shortcuts()

    def update_shortcut_action(self, index, combo):
        """Updates a shortcut action in the settings, using the untranslated key."""
        if not combo: return

        current_combo_index = combo.currentIndex()
        if 0 <= current_combo_index < len(combo.original_items):
            action_key = combo.original_items[current_combo_index]
            self.window.settings["shortcuts"][index]["action"] = action_key
            self.window.save_settings()
            self.setup_shortcuts()

    def update_shortcut_action_translations(self):
        """Re-populates the action combo boxes with translated strings."""
        for combo in self.window.shortcut_action_combos:
            self.window._translate_combobox_items(combo)

    def setup_shortcuts(self):
        """Create QShortcut objects based on current settings."""
        for shortcut in self.shortcuts:
            shortcut.setParent(None)
            shortcut.deleteLater()
        
        self.shortcuts.clear()
        for config in self.window.settings.get("shortcuts", []):
            if config["key"] and config["action"] != "None":
                shortcut = QShortcut(QKeySequence(config["key"]), self.window)
                shortcut.activated.connect(partial(self.execute_shortcut_action, config["action"]))
                self.shortcuts.append(shortcut)

    def execute_shortcut_action(self, action):
        """Executes the action associated with a triggered shortcut."""
        if action == "Copy Current Output":
            current_widget = self.window.stacked_widget.currentWidget()
            output_widget = current_widget.findChild(QTextEdit)
            if output_widget and output_widget.isReadOnly():
                QApplication.clipboard().setText(output_widget.toPlainText())
                self.window.play_sound("click")
        elif action in ["Go to Next Tab", "Go to Previous Tab"]:
            if hasattr(self.window, 'tab') and self.window.tab and self.window.tab.isVisible():
                count = self.window.tab.count()
                if count > 1:
                    current_index = self.window.tab.currentIndex()
                    if action == "Go to Next Tab":
                        new_index = (current_index + 1) % count
                    else: 
                        new_index = (current_index - 1 + count) % count
                    
                    self.window.tab.setCurrentIndex(new_index)
                    self.window.play_sound("tab")

        elif action.startswith("Go to: "):
            destination_key = action.replace("Go to: ", "")
            for key, translations in self.window.translations.items():
                for eng_text, trans_text in translations.items():
                    if trans_text == destination_key:
                        destination_key = eng_text
                        break
                if destination_key != action.replace("Go to: ", ""):
                    break

            self.window.show_welcome_screen()
            if destination_key in self.window.menu_definitions:
                self.window.show_submenu(destination_key)
            elif destination_key == "Python REPL": self.window.show_repl_ui()
            elif destination_key == "ASCII Text Art": self.window._show_ascii_text_art_ui()
            elif destination_key == "Regex Tester": self.window._show_regex_visualizer_ui()