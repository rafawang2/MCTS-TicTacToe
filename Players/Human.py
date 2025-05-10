from GameUtils import ANSI_string
class Human():
    def get_move(self, board, player):
        print("Enter coordinate")
        pos = str(input()).split(' ')
        r = int(pos[0])
        c = int(pos[1])
        if r>=3 or c >=3 or r<0 or c<0:
            print(ANSI_string("Wrong Input",color='red', bold=True))
            return self.get_move()
        return r, c