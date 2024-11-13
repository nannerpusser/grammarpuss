import os, threading, re, sys
import tkinter as tk
from tkinter import ttk, WORD
import customtkinter as ctk
import pywinstyles
from anagrams import *


ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
DICTIONARY_FILENAME = os.path.join(ASSETS, "wordament_dictionary.txt")

def CenterWindowToDisplay(
    Screen: ctk.CTkToplevel, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 2)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"
def apply_theme_to_titlebar(window):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        pywinstyles.change_header_color(window, "#2b2b2b")
        pywinstyles.change_border_color(window, "#2b2b2b")
        window.wm_attributes("-alpha", "0.95")
        
    elif version.major == 10 and version.build < 22000:
        pywinstyles.apply_style(window, "dark")
        window.wm_attributes("-alpha", "0.9")
        window.wm_attributes("-alpha", "1.0")
        
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:         #mostly boilerplate Trie for iterative dfs
    def __contains__(self, word):
        return self.search(word)

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):

        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return False
            node = node.children[char]
        return True
    
class ToplevelWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        apply_theme_to_titlebar(self)
        self.title("Anagrams")
        self.geometry(CenterWindowToDisplay(self, 400, 500))
        self.label = ctk.CTkLabel(self, text="Scrabble Solver/Anagram Finder", font=(ctk.CTkFont(family="Segoe UI", size=16)))
        self.label.pack(padx=5, pady=10)

        self.entry = ctk.CTkEntry(self, width=300, height=30, font=(ctk.CTkFont(family="Segoe UI", size=14)), placeholder_text="min. 4 letters")
        self.entry.pack(padx=5, pady=10) if self.entry else 0

        self.go_button = ctk.CTkButton(self, width=100, height=30, text="Get Anagrams", fg_color="#33b40b", hover_color="#2a9b0a", command=self.get_anagrams, font=(ctk.CTkFont(family="Segoe UI", size=16)))
        self.go_button.pack(padx=5, pady=10, side="bottom")

        self.clear_button = ctk.CTkButton(self, width=100, height=30, text="Clear", command=self.clear, font=(ctk.CTkFont(family="Segoe UI", size=16)))
        self.clear_button.pack(padx=5, pady=10, side="bottom")

        self.close_button = ctk.CTkButton(self, width=100, height=30, text="Close", fg_color="#c8434e", hover_color="#b91a3d", command=self.withdraw_top, font=(ctk.CTkFont(family="Segoe UI", size=16)))
        self.close_button.pack(padx=5, pady=10, side="bottom") 
        
        self.list = ctk.CTkTextbox(self,font=(ctk.CTkFont(family="Segoe UI", size=16)), activate_scrollbars=True, wrap=WORD)
        self.list.pack(padx=5, pady=5, ipadx=5, ipady=5, fill="both", expand=True, side ="top")

    def get_anagrams(self):
        trie = AnagramSolver.make_trie(AnagramSolver.read_words(DICTIONARY_FILENAME))
        letters = self.entry.get().lower()
        words = [word for word in AnagramSolver.anagram(letters, trie)]
        words = sorted(words, key=lambda x: (len(x), x))
        words = [word for word in words if len(word) >= 4]

        for word in words:
            self.list.delete("1.0", tk.END)
            self.list.insert(tk.END, ', '.join(words))
    def clear(self):
        self.list.delete("1.0", tk.END)

    def withdraw_top(self):
        app.deiconify()
        self.destroy()


class WordamentGUI(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        apply_theme_to_titlebar(self)

        load_font = "Segoe UI"
        self.entry_font = (ctk.CTkFont(family=load_font, size=26))
        self.other_font = (ctk.CTkFont(family=load_font, size=16))
        self.resizable(False, False)
        self.width = int(self.winfo_screenwidth() * 0.5)
        self.height = int(self.winfo_screenheight() * 0.66)
        self.title("Wordup: Wordament Solver")
        self.geometry(CenterWindowToDisplay(self, self.width, self.height, 1.0))
        #self.minsize(self.width, self.height)
        #self.maxsize(self.width, self.height)


        self.entries = []

        self.solver = WordamentSolver()
        self.solver.load_dictionary(os.path.join(ASSETS, "wordament_dictionary.txt"))

        self.toplevel_window = None
    
    

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.focus_set()
            self.iconify() # hide the main window
        else:
            self.toplevel_window.focus() 
            self.iconify()  # if window exists focus it

    def quit(self):
        self.destroy()
        

    def clear_board(self):
        for row in self.entries:
            for entry in row:
                entry.delete(0, tk.END)
        self.entries[0][0].focus_set()
        for item in self.tree.get_children():
            self.tree.delete(item)

    def treeview_sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]

        if col == 'Word':
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)
        elif col in ['Length', 'Value']:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
            self.tree.item(k, tags=('oddrow' if index % 2 else 'evenrow',))

        # Reverse sort next time
        self.tree.heading(col, command=lambda: self.treeview_sort_column(col, not reverse))


    def run(self):
        self.create_widgets()
        self.clear_board()
        self.mainloop()

    def create_widgets(self):
        self.grid_columnconfigure((0, 1), weight=1, uniform="both")
        self.grid_rowconfigure((0, 1), weight=1, uniform="both")

        # frame (top left)
        board_frame = ctk.CTkFrame(self, bg_color="transparent", fg_color="#d1ba35")
        board_frame.grid(row=0, column=0)
        self.entry_vars = [[ctk.StringVar() for _ in range(4)] for _ in range(4)]

        for i in range(4):
            row = []
            for j in range(4):
                entry = ctk.CTkEntry(board_frame, width=80, height=78,  justify='center', font=self.entry_font, textvariable=self.entry_vars[i][j], corner_radius=4)
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.grid_rowconfigure((0, 1, 2, 3), weight=1)
                entry.grid_columnconfigure((0, 1, 2, 3), weight=1)
                #entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.validate_input(e, r, c))
                row.append(entry)
                self.entry_vars[i][j].trace_add('write', lambda *args, r=i, c=j: self.validate_input(r, c))
            self.entries.append(row)
        # frame (top right)
        button_frame = ctk.CTkFrame(self, bg_color="black", fg_color="transparent", border_width=0, corner_radius=2)
        button_frame.grid(row=0, column=1, padx=6, pady=6, ipadx=5, ipady=5, sticky="ew")
        button_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        pywinstyles.set_opacity(widget=button_frame, color="black", value=1.0)


        self.anagram_button = ctk.CTkButton(button_frame, text="Anagram Tool", command=self.open_toplevel, fg_color="#7cd0dd", hover_color="#66a4e2", text_color="#ffffff", border_width=1, corner_radius=3, font=(self.entry_font, 20, "bold"), width=130, height=20)
        self.anagram_button.grid(row=0, column=1, padx=5, pady=25, sticky="nsew")

        self.solve_button = ctk.CTkButton(button_frame, text="Solve", command=self.solve, fg_color="#33b40b", text_color="#ffffff", border_width=1, hover_color="#3ace0d", corner_radius=3, font=(self.entry_font, 20, "bold"), width=130, height=20)
        self.solve_button.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_board, fg_color="#8bc1c9", hover_color="#66a4e2", text_color="#ffffff", border_width=1, corner_radius=3, font=(self.entry_font, 20, "bold"), width=130, height=20)
        self.clear_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        self.quit_button = ctk.CTkButton(button_frame, text="Quit", command=self.quit, fg_color="#c8434e", hover_color="#b91a3d", corner_radius=3, text_color="#ffffff", border_width=1, font=(self.entry_font, 20, "bold"), width=130, height=20)
        self.quit_button.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

        # Treeview frame (bottom, spanning width)

        tree_frame = ctk.CTkFrame(self, bg_color="black", corner_radius=2, border_width=0)
        tree_frame.grid(row=4, column=0, columnspan=2, padx=5, pady=5, ipadx=2, ipady=2, sticky="nsew")
        tree_frame.grid_rowconfigure((0, 1), weight=1, uniform="both")
        tree_frame.grid_columnconfigure((0, 1), weight=1, uniform="both")
        self.background_color = "#4e4e4e"
        self.foreground_color = "#efefef"

        self.tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse", padding=(1, 1, 1, 1))
        pywinstyles.set_opacity(widget=tree_frame, color="black", value=1.0)      # Treeview
        
        style = ttk.Style()
        style.theme_use('alt')
                
        style.configure('Treeview',
            background=self.background_color,
            foreground=self.foreground_color,
            fieldbackground="#2b2b2b",
            borderwidth=0,
            font=self.other_font,
            )

        style.configure('Treeview.Heading',
            background=self.background_color,
            foreground=self.foreground_color,
            relief="flat",
            font=self.other_font,
            )
        
        style.map('Treeview', background=[('selected', self.background_color)])
        style.map('Treeview.Heading', foreground=[('active', self.foreground_color)])
        style.map('Treeview', foreground=[('selected', self.foreground_color)])
        style.map('Treeview.Heading', background=[('active', "#81a5cc")])

        tree_frame.grid(row=1, column=0, columnspan=2, padx=1, pady=1, ipadx=1, ipady=1, sticky="nsew")
        tree_frame.grid_rowconfigure((0, 1), weight=1, uniform="both")
        tree_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=('Word', 'Length', 'Value'), show='headings', selectmode="none", style="Treeview")
        self.tree.heading('Word', text='Word', command=lambda: self.treeview_sort_column('Word', True))
        self.tree.heading('Length', text='Length', command=lambda: self.treeview_sort_column('Length', False))
        self.tree.heading('Value', text='Value', command=lambda: self.treeview_sort_column('Value', False))
        self.tree.column('Word', width=160, anchor='w', stretch=True)
        self.tree.column('Length', width=110, anchor='e', stretch=False)
        self.tree.column('Value', width=110, anchor='e', stretch=False)
        self.tree.pack(side=tk.LEFT, expand=True, fill="both", padx=3, pady=3)

        # Scrollbar for Treeview, had trouble keeping it slim and padded on y axis
        self.scrollbar = ctk.CTkScrollbar(tree_frame, orientation="vertical", command=self.tree.yview, border_spacing=2, corner_radius=2)
        self.scrollbar.configure(bg_color="black")
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y", ipadx=1, pady=2, padx=1, ipady=2)
        pywinstyles.set_opacity(widget=self.scrollbar, color="black", value=.90)

        # Configure tag for alternating row colors
        self.tree.tag_configure('oddrow', background='#2c2f30', font=(self.other_font, 14))
        self.tree.tag_configure('evenrow', background='#212325', font=(self.other_font, 14))



    def validate_input(self, row, col):
        value = self.entry_vars[row][col].get().upper()

        valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ-/")
        filtered_value = "".join(char for char in value if char in valid_chars)[:4].upper() # jank, has to work

        # Ditto
        if len(filtered_value) > 1:
         # Allow up to 4 characters for dick tile
            if  len(filtered_value) > 3 and filtered_value.endswith('-'):
                filtered_value = filtered_value[:4]
            elif len(filtered_value) > 3 and filtered_value.startswith('-'):
                filtered_value = filtered_value[:3]
            elif len(filtered_value) > 2 and '-' in filtered_value[1:-1]:
                filtered_value = filtered_value.replace('-', '')
            elif len(filtered_value) > 2 and '/' in filtered_value[-1:]:
                filtered_value = filtered_value.replace('/', '')
            elif len(filtered_value) > 2 and '/' in filtered_value[:1]:
                filtered_value = filtered_value.replace('/', '')
            elif len(filtered_value) > 2 and '/' in filtered_value[-1:1]:
                filtered_value = filtered_value[:1]
            elif filtered_value == '//':
                filtered_value = ''
            elif filtered_value == '--':
                filtered_value = ''
            elif filtered_value == re.match('[A-Z]{2,3}', filtered_value) and filtered_value.endswith('/'):
                filtered_value = filtered_value[:-1]
        else:
            filtered_value = filtered_value[:1]
        # Update the entry
        self.entries[row][col].delete(0, tk.END)
        self.entries[row][col].insert(0, filtered_value)


    def solve(self):
        board = [[entry.get().upper() for entry in row] for row in self.entries]
        special_tiles = {}
        for i in range(4):
            for j in range(4):
                tile = board[i][j]
                if re.match(r'^[A-Z]{2,3}-$', tile) or \
                   re.match(r'^-[A-Z]{2,3}$', tile) or \
                   re.match(r'^[A-Z]{2,3}$', tile) or \
                   '/' in tile:
                    special_tiles[(i, j)] = tile
                elif len(tile) != 1:
                    tk.messagebox.showwarning(title="Invalid Input", message="Properly fill in tiles")
                    return
        self.solver.set_board(board, special_tiles)

        def solve_thread():
            self.words = self.solver.solve()
            self.after(0, self.display_results)

        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree.insert('', 'end', values=('Solving...', '', ''))
        threading.Thread(target=solve_thread, daemon=True).start() # totally uncessary threading operation

    def display_results(self):
    # Sort by length by default
        sorted_words = sorted(self.words, key=lambda x: (-x[1], x[0]))

        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, (word, length, value) in enumerate(sorted_words):
            tag = 'oddrow' if i % 2 else 'evenrow'
            self.tree.insert('', 'end', values=(word, length, value), tags=(tag,))

class WordamentSolver:
    def __init__(self):
        self.trie = Trie()
        self.board = []
        self.special_tiles = {}
        self.letter_values = {
            'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2, 'H': 4, 'I': 1,
            'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
            'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10
        }
# Problem here is tile value isn't a constant and there are various multipliers. The multipliers might be constants for word length, but conditionals apply in outlier circumstances
    def load_dictionary(self, file_path):
        with open(file_path, 'r') as f:
            for word in f:
                self.trie.insert(word.strip())


    def set_board(self, board, special_tiles):
        self.board = [[tile.upper() for tile in row] for row in board]
        for (i, j), tile in special_tiles.items():
            if '/' in tile:
                self.board[i][j] = tile.split('/')  # Store as a list of possible characters, fix for infinite recursion hangs
            else:
                self.board[i][j] = tile

    def calculate_word_value(self, word):
        return sum(self.letter_values.get(letter.upper(), 0) for letter in word)

    def solve(self):
        self.words = []
        self.visited = set()

        for i in range(4):
            for j in range(4):
                self.iterative_dfs(i, j, "", set())

        return sorted(list(set(self.words)), key=lambda x: (-len(x), x))

    def iterative_dfs(self, i, j, current_word, visited):
        stack = [(i, j, current_word, visited)]

        while stack:
            i, j, current_word, visited = stack.pop()

            if (i, j) in visited:
                continue

            visited = visited.copy()
            visited.add((i, j))

            tile = self.board[i][j]
            if isinstance(tile, list):  # Handle either/or tiles
                possible_chars = tile
            else:
                possible_chars = [tile]

            for char in possible_chars:
                new_word = current_word + char

                if new_word in self.trie:
                    if len(new_word) >= 3 and new_word in self.trie:
                        self.words.append((new_word, len(new_word), self.calculate_word_value(new_word)))

                if self.trie.starts_with(new_word):
                    for ni, nj in self.get_neighbors(i, j):
                        if (ni, nj) not in visited:
                            stack.append((ni, nj, new_word, visited))

    def get_neighbors(self, i, j):     # preventing infinite recursion errors
        neighbors = []
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= ni < 4 and 0 <= nj < 4 and (di != 0 or dj != 0):
                    neighbors.append((ni, nj))
        return neighbors



if __name__ == "__main__":
    app = WordamentGUI()
    app.run()
