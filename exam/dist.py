pos = [0,0]
health = 5
damage = 3
with open ("map.txt") as file:
    maze = file.readlines()
    maze = [i.strip() for i in maze]
print(maze)


class Maze:

    def __init__(self, maze):
        self.maze = maze


def shape(maze):

    n_rows = len(maze)
    n_cols = len(maze[0])
    return [n_rows, n_cols]

    
def print_maze(maze: Maze, pos):
    """
    Функция выводит лабиринт и текущее положение в нем.
​
    Возможные ходы должны отмечаться 'o', текущее положение 'h',
    стена 'x', монстр 'm', а выход 'f'.
​
    :param maze: Лабиринт
    :param pos: Текущая позиция в лабиринте (строка, столбец)
    """
    n_rows, n_cols = shape(maze)
    for r in range(n_rows):
        print(maze[r])
    print(pos)


def shortest_dist(maze: Maze, pos):
    
    for r in range(1, len(maze)):
        for c in range(1, len(maze[0])):
            for i in range(len(pos)):
                if maze[pos[i] + 1] == 'o':
                    pos[i] == pos[i] + 1
                    maze[pos[i]] = 'h'
                    maze[pos[i] - 1] = '-'
                    if maze[pos[i]] == 'm':
                        health -= damage
                    if health < 0:
                        print ('Вы погибли')
    return maze

output = shortest_dist(maze, pos = [0,0])
for i in range(len(output)): 
    print(output[i])


