# flag{wh04m1_15_pr0ud_0f_y0u}
import numpy as np
import random
import subprocess

def play_minesweeper():
    process = subprocess.Popen(
        ['./minesweeper'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    while True:
        result = []
        failed = False
        for _ in range(10):
            read_line = process.stdout.readline().strip()

            if not read_line:
                break

            if "Game" in read_line:
                read_line = process.stdout.readline().strip()
                
            if "lost" in read_line:
                failed = True

            if "flag" in read_line:
                print(read_line)
                return 'flag'
            result.append(read_line)

            if "flag" in read_line:
                break

        if failed or "flag" in read_line:
            break

        next_input = analyze_and_get_input(result)

        if next_input == "break":
            break

        process.stdin.write(next_input + '\n')
        process.stdin.flush()

    process.stdin.close()
def array_result(result):
    current_state = np.full((9, 9), -1, dtype=int)
    i = 0
    while i < 9:
        j = 0
        while j < 17:
            char = result[i][j]
            if char in [str(i) for i in range(9)]:
                current_state[i][j//2] = int(char)
            j += 2
        i += 1

    return current_state

def unknown_neighbours(current_state, i, j):
    count = 0
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if 0 <= x < 9 and 0 <= y < 9 and current_state[x][y] == -1:
                count += 1
    return count


def neighbour_mines(current_state, i, j):
    count = 0
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if 0 <= x < 9 and 0 <= y < 9 and current_state[x][y] == -2:
                count += 1
    return count


def label_mines(current_state, i, j):
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if 0 <= x < 9 and 0 <= y < 9 and current_state[x][y] == -1:
                current_state[x][y] = -2


def  identify_neighbours(current_state, i, j):
    for x in range(i - 1, i + 2):
        for y in range(j - 1, j + 2):
            if 0 <= x < 9 and 0 <= y < 9 and current_state[x][y] == -1:
                return x, y
    return -1, -1


def analyze_and_get_input(result):
    current_state = array_result(result)

    i = 0
    while i < 9:
        j = 0
        while j < 9:
            if current_state[i][j] == (unknown_neighbours(current_state, i, j) + neighbour_mines(current_state, i, j)):
                label_mines(current_state, i, j)
            j += 1
        i += 1

    i = 0
    while i < 9:
        j = 0
        while j < 9:
            if current_state[i][j] == neighbour_mines(current_state, i, j):
                correct_steps = identify_neighbours(current_state, i, j)
                if correct_steps != (-1, -1):
                    return f"{correct_steps[0]},{correct_steps[1]}"
            j += 1
        i += 1

    correct_steps = [(i, j) for i in range(9) for j in range(9) if current_state[i][j] == -1]
    selected_step = random.choice(correct_steps)

    return f"{selected_step[0]},{selected_step[1]}"


# Call play_minesweeper function
while True:
    res = play_minesweeper()
    if res:
        break




