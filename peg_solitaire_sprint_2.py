import tkinter as tk
from tkinter import ttk


# ===================== GAME LOGIC =====================

class PegSolitaire:
    def __init__(self, size=7, board_type="cross"):
        self.size = size
        self.board_type = board_type
        self.board = []
        self.initialize_board()

    def initialize_board(self):
        self.board = [[1 for _ in range(self.size)] for _ in range(self.size)]

        mid = self.size // 2
        self.board[mid][mid] = 0

        if self.board_type == "cross":
            remove = self.size // 3
            for r in range(self.size):
                for c in range(self.size):
                    if (r < remove or r >= self.size - remove) and \
                       (c < remove or c >= self.size - remove):
                        self.board[r][c] = None

    def is_valid_move(self, r1, c1, r2, c2):
        if not (0 <= r2 < self.size and 0 <= c2 < self.size):
            return False

        if self.board[r1][c1] != 1 or self.board[r2][c2] != 0:
            return False

        dr = r2 - r1
        dc = c2 - c1

        if not (
            (abs(dr) == 2 and dc == 0) or
            (abs(dc) == 2 and dr == 0) or
            (abs(dr) == 2 and abs(dc) == 2)
        ):
            return False

        mid_r = r1 + dr // 2
        mid_c = c1 + dc // 2

        if self.board[mid_r][mid_c] != 1:
            return False

        return True

    def make_move(self, r1, c1, r2, c2):
        dr = r2 - r1
        dc = c2 - c1

        mid_r = r1 + dr // 2
        mid_c = c1 + dc // 2

        self.board[r1][c1] = 0
        self.board[mid_r][mid_c] = 0
        self.board[r2][c2] = 1

    def has_valid_moves(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 1:
                    for dr in [-2, 0, 2]:
                        for dc in [-2, 0, 2]:
                            if dr == 0 and dc == 0:
                                continue
                            if self.is_valid_move(r, c, r + dr, c + dc):
                                return True
        return False

    def count_pegs(self):
        return sum(row.count(1) for row in self.board if row)


# ===================== GUI =====================

class PegSolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")

        self.selected = None

        self.size_var = tk.IntVar(value=7)
        self.type_var = tk.StringVar(value="cross")

        # Controls
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Board Size:").pack(side=tk.LEFT)
        ttk.Combobox(
            control_frame,
            textvariable=self.size_var,
            values=[5, 7, 9],
            width=5,
            state="readonly"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Board Type:").pack(side=tk.LEFT)
        ttk.Combobox(
            control_frame,
            textvariable=self.type_var,
            values=["cross", "full"],
            width=8,
            state="readonly"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="New Game",
                   command=self.new_game).pack(side=tk.LEFT, padx=10)

        # Status
        self.status_label = tk.Label(root, text="")
        self.status_label.pack(pady=5)

        # Board
        self.board_frame = tk.Frame(root)
        self.board_frame.pack()

        self.new_game()

    def new_game(self):
        self.game = PegSolitaire(
            size=self.size_var.get(),
            board_type=self.type_var.get()
        )
        self.selected = None
        self.update_status("New Game Started")
        self.draw_board()

    def update_status(self, msg=""):
        text = f"Pegs Remaining: {self.game.count_pegs()}"
        if msg:
            text += f" | {msg}"
        self.status_label.config(text=text)

    def draw_board(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        for r in range(self.game.size):
            for c in range(self.game.size):
                cell = self.game.board[r][c]

                if cell is None:
                    tk.Label(self.board_frame, width=4, height=2).grid(row=r, column=c)
                else:
                    color = "blue" if cell == 1 else "white"

                    if self.selected == (r, c):
                        color = "red"

                    btn = tk.Button(
                        self.board_frame,
                        bg=color,
                        width=4,
                        height=2,
                        command=lambda r=r, c=c: self.cell_clicked(r, c)
                    )
                    btn.grid(row=r, column=c)

    def cell_clicked(self, r, c):
        if self.selected is None:
            if self.game.board[r][c] == 1:
                self.selected = (r, c)
                self.update_status("Peg selected")
                self.draw_board()
            return

        r1, c1 = self.selected

        # Deselect same peg
        if (r, c) == self.selected:
            self.selected = None
            self.update_status("Selection cleared")
            self.draw_board()
            return

        # Switch selection
        if self.game.board[r][c] == 1:
            self.selected = (r, c)
            self.update_status("Peg selected")
            self.draw_board()
            return

        # Attempt move
        if self.game.board[r][c] == 0:
            if self.game.is_valid_move(r1, c1, r, c):
                self.game.make_move(r1, c1, r, c)
                self.selected = None

                if self.game.count_pegs() == 1:
                    self.update_status("You Win!")
                elif not self.game.has_valid_moves():
                    self.update_status("No More Moves!")
                else:
                    self.update_status("Move completed")
            else:
                self.update_status("Invalid move")

            self.draw_board()


# ===================== RUN =====================

if __name__ == "__main__":
    root = tk.Tk()
    app = PegSolitaireGUI(root)
    root.mainloop()