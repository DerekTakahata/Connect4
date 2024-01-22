import random
from tkinter import *
from tkinter import messagebox

class Connect4:
    def __init__(self, width, height):
        ''' Create a new Connect4 board with the given size '''
        
        self.width = width
        self.height = height
        self.board = []
        
        # Note: We take row 0 to be the top of the board
        for row in range(self.height):
            boardRow = []
            for col in range(self.width):
                boardRow += [' ']
            self.board += [boardRow]
        
    def __str__(self):
        ''' Returns a representation of the current state of the board'''

        # set up the board itself
        s = ''   # the string to return
        for row in range( self.height ):
            s += '|'   # add the separator character
            for col in range( self.width ):
                s += self.board[row][col] + '|'
            s += '\n'

        # add the column labels under the columns
        s += '--'*self.width + '-\n'
        for col in range(self.width):
            s += ' ' + str(col % 10)
        s += '\n'
        return s
    
    def is_legal_move(self, col):
        ''' Checks if valid column number and column has space '''
        # Check col exists, assumes user input is 0-6 and not 1-7 // CAN CHANGE BOUNDS LATER IF NECESSARY
        if (col < 0 or col > self.width -1):
            return False
        
        # Check if there is room (top spot of column is not filled)
        if (self.board[0][col] == ' '):
            return True
        return False

    def add_move(self, col, player):
        ''' Places 'player' chip in 'col' and returns True
            return False if move not legal 
            
            EDITED FOR GUI: return row, col tuple of where chip was placed'''
        # Check if move is legal
        if (not self.is_legal_move(col)):
            return
        
        # Initialize variables for while loop
        taken = True
        # Because this iterates from the bottom up, count starts at max valid index
        # and counts down
        count = self.height -1  
        
        # While previous spot taken, check if current is empty. If empty, place 'player' 
        # character there and change taken to false. Otherwise move up a spot
        # // kinda weird naming convention but I couldn't think of anything better
        while taken:
            if (self.board[count][col] == ' '):
                self.board[count][col] = player
                taken = False
                return (col, count)
            count -= 1

    def del_move(self, col):
        ''' Removes the top token in specified column. 
            If column is empty or nonexistent, do nothing. VOID METHOD'''
        
        # if col is invalid, pass
        if (col < 0 or col > self.width -1):
            pass

        # If bottom slot is empty, pass (because nothing above it has anything either)
        # must be done after checking col or else possible outOfBounds error
        if (self.board[self.height -1][col] == ' '):
            pass
        
        # Initilize varibles for while loop
        count = 0
        empty = True

        # Move down column, if not empty, remove
        while empty:
            if (self.board[count][col] != ' '):
                self.board[count][col] = ' '
                empty = False
            count += 1

    def clear(self):
        ''' clear the game board '''

        # Iterate thru 2D list, force everything to whitespace
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = ' '

    def is_full(self):
        ''' Return True if all spaces in the board are occupied, else return False '''

        # Check if first elem of board (top row) is empty, if any spots open: not full
        for elem in self.board[0]:
            if (elem == ' '):
                return False
        return True

    def is_win_for(self, player):
        ''' Return True if the designated player has won, otherwise False '''

        # check for horizontal wins
        for row in range(self.height):
            for col in range(self.width - 3):
                if self.board[row][col] == player and \
                   self.board[row][col+1] == player and \
                   self.board[row][col+2] == player and \
                   self.board[row][col+3] == player:
                    return True
        
        # Check for vertical win 
        for col in range(self.width):
            for row in range(self.height-3):
                if (self.board[row][col] == player and \
                    self.board[row+1][col] == player and \
                    self.board[row+2][col] == player and \
                    self.board[row+3][col] == player):
                    return True
                
        # Check for diagonals (from top left)
        for row in range(self.height -3):
            for col in range(self.width -3):
                if (self.board[row][col] == player and \
                    self.board[row+1][col+1] == player and \
                    self.board[row+2][col+2] == player and \
                    self.board[row+3][col+3] == player):
                    return True


        # Check for diagonals (from top right)
        for row in range(self.height -3):
            for col in range(self.width -1, 2, -1):
                if (self.board[row][col] == player and \
                    self.board[row+1][col-1] == player and \
                    self.board[row+2][col-2] == player and \
                    self.board[row+3][col-3] == player):
                    return True
                
        
        return False
            
    def host_game(self):
        ''' plays a game of connect four by asking for player moves, 
            checking for wins, etc '''
        
        # start with fresh board
        self.clear()

        # Reset/initialize variables for game
        p1 = 'X'
        p2 = 'O'
        counter = 0

        # Nice intro, pick character
        # Commenting out custom letters for new because it's useless
        '''
        print("Welcome to connect4! To begin, enter a character to use on the board")
        print("For default characters, enter \'skip\'")
        
        # Input p1 char
        p1 = input("Player 1: ")

        # If skip, set default char vals and skip picking process
        if (p1.lower() == 'skip'):
            p1 = 'X'
            p2 = 'O'
        else:

            # Take precautions for trying weird char selection (over 1 char or whitespace)
            while (len(p1) != 1 or p1== ' '):
                print("Invalid. Please enter a single visible character")
                p1 = input("Player 1: ")

            # Take precautions for trying weird char selection (over 1 char, whitespace, or same as p1)
            p2 = input("Player 2: ")
            while (len(p2) != 1 or p2 == p1 or p2 == ' '):
                print("Invalid. Please enter a single visible character different than Player 1")
                p2 = input("Player 2: ")

        print()
        '''
        print('BEGIN!')

        # Main runner
        live = True
        while live:
            
            # Before every turn, put who's who for less confusion
            print()
            print('Player 1: ', p1)
            print('Player 2: ', p2)

            # Player 1 turn
            if (counter % 2 == 0):
                # Print board and whos turn to players
                print("Turn: Player 1")
                print()
                print(self)

                # ask player what column to drop, if invalid, asks again, then drops chip
                while (counter % 2 == 0):
                    drop_col = int(input("Enter drop column: "))
                    if (self.is_legal_move(drop_col)):
                        self.add_move(drop_col, p1)
                        counter += 1
                    else: 
                        print("Invalid drop column, please enter valid number")
                        continue
            else:
                # Player 2 turn, print board and whos turn to players
                print("Turn: Player 2")
                print()
                print(self)

                # ask player what column to drop, if invalid, asks again, then drops chip
                while (counter % 2 == 1):
                    drop_col = int(input("Enter drop column: "))
                    if (self.is_legal_move(drop_col)):
                        self.add_move(drop_col, p2)
                        counter += 1
                    else: 
                        print("Invalid drop column, please enter valid number")
                        continue

            # Check win conditions, if any are met, print final board and winner, end loop, and break
            if(self.is_win_for(p1)):
                print(self)
                print("GAME OVER")
                print("Player 1 wins!")
                live = False
                break

            if (self.is_win_for(p2)):
                print(self)
                print("GAME OVER")
                print("Player 2 wins!")
                live = False
                break

            if (self.is_full()):
                print(self)
                print("GAME OVER")
                print("Draw! The board is full!")
                live = False
                break

    def play_game_with(self, ai):
        ''' Plays game against ai (minimal features because IDK if they'll be necessary in the final, I can add more later if it matters)'''
        print("you are X, the AI is O")
        live = True
        print(self)
        # Main loop
        while live:
            # Wrong input col protection (only necessary for human, ai checks in move calc)
            p1_move = True

            # Player move
            while p1_move:
                print("Your turn!")
                drop_col = int(input("Input drop column: "))
                if self.is_legal_move(drop_col):
                    self.add_move(drop_col, 'X')
                    p1_move = False
                else:
                    print("invalid move, try again")
                    continue
            print(self)

            # Check for win
            if self.is_win_for('X') or self.is_full():
                live = False
                break

            # AI turn
            print("AI turn!")
            ai_move = ai.next_move(self) 
            self.add_move(ai_move, 'O')
            print(self)
            #print("AI moved at col " + ai_move)

            # Check for win
            if self.is_win_for('O') or self.is_full():
                live = False
                break
        
        print("-------Game Over-------")
        print()
        print(self)
    

class Player:
    def __init__(self, player, tiebreaker, ply):
        ''' Initializes AI player, giving it look ahead depth of ply and 
        tiebreaker solution for picking equivilant spots'''
        self.player = player
        self.tiebreaker = tiebreaker
        self.ply = ply
  
    def __str__(self):
        ''' returns what token the AI is using along with it's tiebreaker method and ply value'''
        return f' AI Token: {self.player} using {self.tie_breaker}' + \
        f' tiebreaking at {self.ply} ply'
    
    def other_player(self, player):
        ''' returns opposite player of whatever player has been passed in'''
        if player == 'X':
            return 'O'
        return'X'
  
    def next_move(self, board):
        ''' calculates the next move of the AI given the current board'''
		# get list of scores for input and highest val of all
        scores = self._scores_for(board, self.player, self.ply)
        highscore = max(scores)

        # get index of all highscores in scores
        highscores = [i for i, j in enumerate(scores) if j == highscore]

        # Tiebreak (first, last, and random elem respectively)
        if self.tiebreaker == "Left":
            return highscores[0]
        if self.tiebreaker == "Right":
            return highscores[-1]
        return random.choice(highscores)

    def _scores_for(self, board, player, ply):
        ''' return list of scores of each column for player given current 
        game board and depth of look ahead (ply)'''
        scores = []
        for col in range(board.width):
            # -1 if illegal move
            if board.is_legal_move(col) == False:
                scores.append(-1)
                continue
            # Add move in col. If win, append 100
            else:
                board.add_move(col, player)
                if (board.is_win_for(player)):
                    scores.append(100)
                else:
                    if ply > 1:
                        # If ply > 1, check scores of other player in ply -1, set to 0 if col move
                        # would result in loss, set to 50 if continues game.
                        opp_scores = self._scores_for(board, self.other_player(player), ply -1)
                        max_opp_score = max(opp_scores)
                        scores.append(100 - max_opp_score)
                    else:
                        scores.append(50)
                # Clean up and return final    
                board.del_move(col)
                    
        return scores
        

class Gui:
    def __init__(self, board, ai):
        ''' Creates Graphical user interface given board object and an AI opponent'''
        self.window = Tk()
        self.board = board
        self.ai = ai
        self.width = board.width # This feels so wrong
        self.height = board.height
        self.diameter = 100
        self.gap = 10
        self.can_width = self.width * self.diameter + self.gap * (self.width + 1)
        self.can_height = self.height * self.diameter + self.gap * (self.height + 1)

    def run_game(self):
        ''' Sets up general size for window that contains the board. Contains mainloop'''
        frame = Frame(self.window)
        frame.pack()

        # setup entire (blank) canvas that can react to left click
        self.canvas = Canvas(self.window, height = self.can_height + 50, 
                             width = self.can_width, bg='#F2EEB8')
        self.x = self.canvas.bind('<Button-1>', self._click)
        self.canvas.pack()

        # Setup buttons
        self._setup_butts(frame)

        # Setup circles (and catch return value at same time)
        self.gui_board = self._setup_circs()

        # Setup status
        self.message = self.canvas.create_text(self.can_width / 2, self.can_height + 25, 
                                               text="Your turn! Click a column to place your token", 
                                               fill='black', font=('Comic Sans MS', 20), justify="left")

        # Mainloop should always be at the very end (test cases right before)
        self.canvas.mainloop()

    def _quit_game(self):
        ''' Closes gui window object killing entire window'''
        self.window.destroy()

    def _new_game(self):
        ''' Clears game board used for scoring as well as gui board by deleting canvas and remaking it'''
        self.board.clear()
        self.canvas.delete('all')
        self.gui_board = self._setup_circs()
        self.message = self.canvas.create_text(self.can_width / 2, self.can_height + 25, 
                                               text="Your turn! Click a column to place your token", 
                                               fill='black', font=('Comic Sans MS', 20), justify="left")

    # register click (and fill correct col)
    def _click(self, event):
        ''' Registers user clicks, updates board, and runs AI turn (technically main loop for game)'''
        #Identify clicked col
        col = int(event.x / (self.can_width / self.width))

        #Ignore illegal moves
        if not self.board.is_legal_move(col):
            print("Illegal move")
            return
    
        # Add move if all is good
        coords = self.board.add_move(col, 'X')
        self.canvas.itemconfig(self.gui_board[coords[1]] [coords[0]], fill='red')
        print(self.board)
        self._update_message("AI's turn! please wait")
        self.canvas.update()

        # Check for win for human and react if necessary
        if self.board.is_win_for('X'):
            self._update_message("Game Over! You Win!")
            messagebox.showinfo('Connect4', 'Game Over, You Wins!')
            return
        if self.board.is_full():
            self._update_message("Tie Game!")
            messagebox.showinfor('Connect4', 'Board is full, tie game!')
            return

        # AI moves now (once I figure out how to end game I can move this)
        ai_col = self.ai.next_move(self.board)
        ai_coords = self.board.add_move(ai_col, 'O')
        self.canvas.itemconfig(self.gui_board[ai_coords[1]][ai_coords[0]], fill='blue')
        self._update_message("Your turn! Click a column to place your token")

        # Check for win for AI, and react if necessary
        if self.board.is_win_for('O'):
            self._update_message("Game Over! AI wins")
            messagebox.showinfo('Connect4', 'Game Over, AI Wins!')
            return
        if self.board.is_full():
            self._update_message("Tie Game!")
            messagebox.showinfo('Connect4', 'Board is full, tie game!')
            return

    def _setup_circs(self):
        ''' Sets up board by making circles evenly spaced within window and makes 2D array of oval
        objects in which the elements can be manipulated later'''
        board = []
        row_gap = 0
        for row in range(self.height):
            row_gap += self.gap
            col_gap = 0
            board_row = []
            for col in range(self.width):
                col_gap += self.gap
                x = col * self.diameter + col_gap
                y = row * self.diameter + row_gap
                circle = self.canvas.create_oval(x, y, x + self.diameter, y + self.diameter, 
                                                 fill = 'white')
                board_row.append(circle)
            board.append(board_row)
        return board

    def _setup_butts(self, parent):
        ''' sets up buttons at top of screen'''
        quit_button = Button(parent, text='Quit', command=self._quit_game)
        quit_button.pack(side='right', padx=10)

        new_game_button = Button(parent, text='New Game', command=self._new_game)
        new_game_button.pack(side='right')

    def _update_message(self, message):
        ''' Updates message at bottom of screen'''
        self.canvas.delete(self.message)
        self.message = self.canvas.create_text(self.can_width / 2, self.can_height + 25, 
                                               text=message, fill='black', 
                                               font=('Comic Sans MS', 20), justify="left")
        self.canvas.update()


def main():
    
    board = Connect4(7,6)
    ply = 7
    bot = Player('O', 'rand', ply)
    window = Gui(board, bot)
    #board.play_gbame_with(bot)
    window.run_game()
    

    
    #Testing code here:
    '''
    test = Connect4(7,6)
    p1 = Player('O', 'Left', 6)
    p2 = Player('X', 'Left', 6)
    print(test)
    # Filling board
    test.add_move(0, 'O')
    test.add_move(0, 'O')
    test.add_move(0, 'O')
    test.add_move(0, 'X')
    test.add_move(0, 'O')
    test.add_move(0, 'O')
    test.add_move(3, 'O')
    test.add_move(4, 'X')
    test.add_move(4, 'X')
    test.add_move(5, 'X')
    test.add_move(5, 'X')
    test.add_move(6, 'X')
    test.add_move(6, 'X')
    test.add_move(6, 'X')
    test.add_move(6, 'O')
    test.add_move(3, 'O')
    print(test)
    print(p1.next_move(test))
    print("DONE")
    '''
    
    
    


if __name__ == '__main__':
  main()
