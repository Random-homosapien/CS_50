import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count
    
    def neighbourhood(self, cell):
        '''
        Returns a set of all cells around given cell
        '''
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    cells.add((i,j))
        return cells
                
    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"
    
    def __repr__(self):
        return f"{self.cells} = {self.count}"    

    def known_mines(self):          #USER
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if (self.count != 0):
            if len(self.cells) == self.count:
                # print(f"Mines = {self.cells}")
                return self.cells


    def known_safes(self):          #USER
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        if self.count == 0:
            return self.cells 


    def mark_mine(self, cell):      #USER
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        new_cells = set()
        if cell in self.cells:
            new_cells.add(cell)
            new_cells = self.cells.difference(new_cells)
            self.cells = new_cells
            self.count -= 1
            # print(f"Mine = {self.cells}")

    def mark_safe(self, cell):      #USER
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        new_cells = set()
        if cell in self.cells:
            new_cells.add(cell)
            new_cells = self.cells.difference(new_cells)
            self.cells = new_cells
            # print(f"Safe: {cell}")


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge : list[Sentence] = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)
            print(f"mine = {cell}")

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1
        self.moves_made.add(cell)
        # print(f"\n\n{cell} added to moves made")
        # print(f"{self.moves_made = }\n")

        #2
        if cell not in self.safes:
            self.mark_safe(cell)
            # print(f"{cell} added to Safes")
            # print(f"{self.safes = }\n")
        # else:
            # print(f"{cell} already in Safes")

        #3
        cells: set = self.neighbourhood(cell)
        cells.difference_update(self.safes)
        NewSentence = Sentence(cells, count)
        
        for cell in NewSentence.cells:
            if cell in self.mines:
                NewSentence.mark_mine(cell)
                
        self.knowledge.append(NewSentence)
        # print(f"{NewSentence = }")

        #4
        for sentence in self.knowledge:
            if sentence.known_mines():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)
        
        
        self.check_knowledge(NewSentence)
        for i in range(2):
            for sentence in self.knowledge:
                # print(f"checking Knowledge for {sentence}")
                self.check_knowledge(sentence)


        # raise NotImplementedError

    def check_knowledge(self, sentence: Sentence):
        # print(sentence)
        if len(sentence.cells) == 0:                    #Empty sentence
            self.knowledge.remove(sentence) 
        elif sentence.count == 0:
            for cell in sentence.cells:                 #All cells are safe
                self.mark_safe(cell) 
            self.knowledge.remove(sentence)
        elif len(sentence.cells) == sentence.count:     #All cells are mines
            for cell in sentence.cells:
                self.mark_mine(cell)
            self.knowledge.remove(sentence)

        for sentence2 in self.knowledge:
            if sentence2.cells < sentence.cells:        # sentence2 is subset of sentence 
                sentence.cells.difference_update(sentence2.cells)
                sentence.count -= sentence2.count
                # self.knowledge.remove(sentence2)
                # print(f"After removing subset {sentence = }")
            if sentence2.cells > sentence.cells:        # sentence2 is superset of sentence
                sentence2.cells.difference_update(sentence.cells)
                sentence2.count -= sentence.count
                # self.knowledge.remove(sentence2)  
                # print(f"After removing subset {sentence = }")

    def neighbourhood(self, cell):
        '''
        Returns a set of all cells around given cell
        '''
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    cells.add((i,j))
        return cells

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes.difference(self.moves_made):
            return cell
        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #Compute probability for all cells
        for sentence in self.knowledge:
            print (sentence)
            single_probability = sentence.count/len(sentence.cells)
            for cell in sentence.cells:
                if cell not in Cell_stat.all_cell.keys():
                    Cell_stat.all_cell[cell] = single_probability
                elif cell in Cell_stat.all_cell.keys():
                    Cell_stat.all_cell[cell] += single_probability
        print(Cell_stat.all_cell)

        if Cell_stat.all_cell:
            min_key = min(Cell_stat.all_cell, key=Cell_stat.all_cell.get)
            print(f"Min key = {min_key} \n min value = {Cell_stat.all_cell[min_key]} ")
            return min_key
        else:                           #If no probability exists, play random
            for i in range(self.height):
                for j in range(self.width):
                    if (i,j) not in self.mines.union(self.moves_made):
                        return(i,j)

class Cell_stat():

    all_cell = {}
    def __init__(self, cell_location, probability) -> None:
        self.cell_location = cell_location
        self.probability = probability


    

def main():
    mn = Minesweeper()
    mn.print()
    print(mn.board)

if __name__ == "__main__":
    main()