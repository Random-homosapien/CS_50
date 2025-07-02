else:
            for cell in self.cells:
                if cell in MinesweeperAI.safes():
                    Known_safe.add(cell)         
            return Known_safe