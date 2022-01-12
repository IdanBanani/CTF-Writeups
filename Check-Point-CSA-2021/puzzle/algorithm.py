from pprint import pprint


# def translate(src,dst):
#     if dst[1]-src[1] == 2:
#         step = 'v'
#     if dst[1]-src[1] == -2:
#         step = '^'
#     if dst[0]-src[0] == 2:
#         step = '>'
#     if dst[0]-src[0] == -2:
#         step = '<'
#     return [*src,step]

class Node:
    def __init__(self, matrix, parent, move):
        self.matrix = matrix
        self.parent = parent
        self.move = move

    def getMatrix(self):
        return self.matrix

    def getParent(self):
        return self.parent

    def getMove(self):
        return self.move

    def showMatrix(self):
        print("\n".join("".join(elem) for elem in self.matrix))

    def isWinningState(self):
        # return "".join(list(map(lambda item: "".join(item), self.matrix))).count('O') == 1 and self.matrix[3][3] == 'O'
        return self.matrix == Solver.dest_mat

    def isEmptySpot(self, x, y):
        length = len(self.matrix)
        return (0 <= x < Solver.COLS) and (0 <= y < Solver.ROWS) and (self.matrix[y][x] == '.')

    def locateAllPlayers_O(self):

        positions = [(x, y) for x in range(Solver.COLS) for y in range(Solver.ROWS) if self.matrix[y][x] == 'O']
        return positions


    def getValidMovesForPosition(self, x, y):
        getValidMovesNodes = []

        if self.isEmptySpot(x, y - 2) and self.matrix[y-1][x] == 'O':
            newMatrix = [[self.matrix[i][j] for j in range(Solver.COLS)] for i in range(Solver.ROWS)]
            newMatrix[y][x], newMatrix[y-2][x] = '.', 'O'
            newMatrix[y-1][x] = '.'
            move = [x, y,'^']
            node = Node(newMatrix, self, move)
            getValidMovesNodes.append(node)

        #move down
        if self.isEmptySpot(x + 2, y) and self.matrix[y][x + 1] == 'O':
            newMatrix = [[self.matrix[i][j] for j in range(Solver.COLS)] for i in range(Solver.ROWS)]
            newMatrix[y][x], newMatrix[y][x + 2] ='.','O'
            newMatrix[y][x + 1] = '.'
            move = [x, y, '>']
            node = Node(newMatrix, self, move)
            getValidMovesNodes.append(node)

        if self.isEmptySpot(x, y + 2) and self.matrix[y + 1][x] == 'O':
            newMatrix = [[self.matrix[i][j] for j in range(Solver.COLS)] for i in range(Solver.ROWS)]
            newMatrix[y][x], newMatrix[y + 2][x] = '.', 'O'
            newMatrix[y + 1][x] = '.'
            move = [x, y,"v"]
            node = Node(newMatrix, self, move)
            getValidMovesNodes.append(node)

        #move up
        if self.isEmptySpot(x - 2, y) and self.matrix[y][x - 1] == 'O':
            newMatrix = [[self.matrix[i][j] for j in range(Solver.COLS)] for i in range(Solver.ROWS)]
            newMatrix[y][x], newMatrix[y][x - 2] = '.', 'O'
            newMatrix[y][x - 1] = '.'
            move = [x, y,"<"]
            node = Node(newMatrix, self, move)
            getValidMovesNodes.append(node)
        return getValidMovesNodes



    def generateChildren(self):
        children = []
        positions = self.locateAllPlayers_O()
        for position in positions:
            x = position[0] # row idx
            y = position[1] # col  idx
            validPositions = self.getValidMovesForPosition(x, y)
            children.extend(validPositions)
        return children




class Solver:
    ROWS = -1
    COLS = -1
    dest_mat = None
    dest_total_O = None
    curr_total_O = -1
    def __init__(self,src_borad,dst_board):
        self.matrix = src_borad
        Solver.dest_mat = dst_board #TODO : check
        Solver.dest_total_O = sum(sum(1 for c in line if c == 'O') for line in dst_board)
        Solver.curr_total_O = sum(sum(1 for c in line if c == 'O') for line in src_borad)
        # pprint(self.matrix)
        self.startNode = Node(self.matrix, None, None)
        self.finalStateAchieved = False
        self.moves = []

    def calcPath(self, endNode):
        path = []
        currentNode = endNode
        while True:
            if currentNode.getParent() is None:
                break
            else:
                path.append(currentNode)
                currentNode = currentNode.getParent()
        path = path[::-1]
        # print('Total moves: ' + str(len(path)), end='\n\n')
        counter = 1
        for node in path:
            self.moves.append(node.getMove())
            # print('Step ' + str(counter) + ' :')
            # node.showMatrix()
            # print()
            counter += 1

    def getMoves(self):
        # pprint(self.moves)
        ans = []
        for move in self.moves:
            # src,dst = move
            ans.append(move)
        # print(ans)
        return ans

    def calcNumOfPlayers(self,node):
        ans = sum(sum(1 for c in line if c == 'O') for line in node.getMatrix())
        return ans

    def dfs(self, node):
        if self.finalStateAchieved:
            return

        if Solver.curr_total_O == Solver.dest_total_O:
            if node.isWinningState():
                # print('Winning state achieved.')
                final = node.getMatrix()
                # print([''.join(l) for l in list(final)])
                self.calcPath(node)

                self.finalStateAchieved = True
                return
            else:
                self.matrix = node.getParent()
                return

        children = node.generateChildren()
        if len(children) > 0:
            for child in children:
                Solver.curr_total_O -= 1
                self.dfs(child)
                if self.finalStateAchieved:
                    return
                else:
                    self.matrix = node.getParent()
                    Solver.curr_total_O +=1

        return


    def solve(self):
        self.dfs(self.startNode)


class Bot:
    def solvePegSolitaire(self, src_board,dst_board ):
        Solver.ROWS = len(src_board)
        Solver.COLS = len(src_board[0])
        solver = Solver(src_board,dst_board)
        solver.solve()
        moves = solver.getMoves()
        return moves

if __name__ == "__main__":
    bot = Bot()
    bot.solvePegSolitaire()
