import subprocess
import numpy as np
import random


def interact_with_minesweeper():
    executable_path = './minesweeper'

    process = subprocess.Popen(
        executable_path,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
  
    while True:
        output = []
        lost = False
        for _ in range(10):
            output_line = process.stdout.readline().strip()

            if not output_line:  # Check if output_line is empty
                break

            if output_line[0] == "G":
                output_line = process.stdout.readline().strip()
            if output_line[0] == "Y":
                lost = True

            if "flag" in output_line:
                print(output_line)
                return 'flag'
              
            output.append(output_line)

            if "flag" in output_line:  # Check if the flag is found
                break

        if lost or "flag" in output_line:
            break

        next_input = process_output_and_get_input(output)

        if next_input == "break":
            break

        process.stdin.write(next_input + '\n')
        process.stdin.flush()

    process.stdin.close()

# Rest of the code remains the same...

def output_to_array(output):
    gamestate = np.full((9, 9), -1, dtype=int)

    for i in range(9):
        for j in range(17):
            if j % 2 == 0:
                char = output[i][j]
                if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8"]:
                    gamestate[i][int(j/2)] = char

    return gamestate


def adjacent_unknowns(gamestate, i, j):
    count = 0
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            if 0 <= x < 9 and 0 <= y < 9 and gamestate[x][y] == -1:
                count += 1
    return count


def adjacent_mines(gamestate, i, j):
    count = 0
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            if 0 <= x < 9 and 0 <= y < 9 and gamestate[x][y] == -2:
                count += 1
    return count


def mark_mines(gamestate, i, j):
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            if 0 <= x < 9 and 0 <= y < 9 and gamestate[x][y] == -1:
                gamestate[x][y] = -2


def find_adjacent_unknown(gamestate, i, j):
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            if 0 <= x < 9 and 0 <= y < 9 and gamestate[x][y] == -1:
                return x, y
    return -1, -1


def process_output_and_get_input(output):
    gamestate = output_to_array(output)

    for i in range(9):
        for j in range(9):
            if gamestate[i][j] == (adjacent_unknowns(gamestate, i, j) + adjacent_mines(gamestate, i, j)):
                mark_mines(gamestate, i, j)

    for i in range(9):
        for j in range(9):
            if gamestate[i][j] == adjacent_mines(gamestate, i, j):
                valid_move = find_adjacent_unknown(gamestate, i, j)
                if valid_move != (-1, -1):
                    return f"{valid_move[0]},{valid_move[1]}"

    valid_moves = []
    for i in range(9):
        for j in range(9):
            if gamestate[i][j] == -1:
                valid_moves.append([i, j])
    valid_move = random.choice(valid_moves)

    return f"{valid_move[0]},{valid_move[1]}"


# Call the function
while True:
 res =  interact_with_minesweeper()
 if res :
    break

