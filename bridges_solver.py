import os
import math


def try_int(s):
    try:
        return int(s)
    except ValueError:
        return False


def read_board(path):
    f = open(path, 'r')
    lines = f.read().splitlines()
    board = [l.split() for l in lines]

    lengthy = set([len(r) for r in board])
    assert len(lengthy) == 1

    stats = dict()
    stats['vertices'] = dict()
    for i in range(len(board)):
        for j in range(len(board[0])):
            x = try_int(board[i][j])
            if x is not False:
                stats['vertices'][(i, j)] = x
    stats['current'] = {k: [] for k in stats['vertices']}
    return board, stats


def get_row(board, j):
    return board[j]


def get_col(board, i):
    return [c[i] for c in board]


def get_up(board, stats, i, j):
    is_blocked = get_col(board, j)[:i]
    b1 = 0
    b2 = 0
    if '-' in is_blocked:
        b1 = i - is_blocked[::-1].index('-')
    if '=' in is_blocked:
        b2 = i - is_blocked[::-1].index('=')
    n = [v[0] for v in stats['vertices'] if v[1] == j and v[0] < i]
    if len(n) == 0:
        # print('no vertices above', i, j)
        return None
    else:
        n = max(n)
    if b1 > n or b2 > n:
        # print('n was',n,'and was blocked by', max(b1, b2))
        # print(easy_board[b1][j])
        # print(easy_board[b2][j])
        # print(is_blocked)
        return None
    return n, j


def get_down(board, stats, i, j):
    is_blocked = get_col(board, j)[i + 1:]
    b1 = len(board[0])
    b2 = len(board[0])
    if '-' in is_blocked:
        b1 = i + is_blocked.index('-')
    if '=' in is_blocked:
        b2 = i + is_blocked.index('=')
    n = [v[0] for v in stats['vertices'] if v[1] == j and v[0] > i]
    if len(n) == 0:
        # print('no vertices below',i,j)
        return None
    else:
        n = min(n)
    if b1 < n or b2 < n:
        # print('was blocked by',b1,b2)
        return None
    return n, j


def get_right(board, stats, i, j):
    is_blocked = get_row(board, i)[j + 1:]
    b1 = len(board)
    b2 = len(board)
    if '|' in is_blocked:
        b1 = j + is_blocked.index('|')
    if '║' in is_blocked:
        b2 = j + is_blocked.index('║')
    n = [v[1] for v in stats['vertices'] if v[0] == i and v[1] > j]
    if len(n) > 0:
        n = min(n)
    else:
        # print(is_blocked)
        return None
    if b1 < n or b2 < n:
        # print('n',n,'b1',b1,'b2',b2)
        # print(is_blocked)
        return None
    return i, n


def get_left(board, stats, i, j):
    is_blocked = get_row(board, i)[:j]
    b1 = 0
    b2 = 0
    if '|' in is_blocked:
        b1 = j - is_blocked[::-1].index('|')
    if '║' in is_blocked:
        b2 = j - is_blocked[::-1].index('║')
    n = [v[1] for v in stats['vertices'] if v[0] == i and v[1] < j]
    if len(n) > 0:
        n = max(n)
    else:
        return None
    if b1 > n or b2 > n:
        return None
    return i, n


def get_ns(board, stats, i, j):
    return list(filter(lambda x: x is not None, [get_up(board, stats, i, j),
                                                 get_right(board, stats, i, j),
                                                 get_down(board, stats, i, j),
                                                 get_left(board, stats, i, j)]))


def set_bridge(board, stats, i1, j1, i2, j2):
    if stats['vertices'][(i1, j1)] == 1 and stats['vertices'][(i2, j2)] == 1:
        return board, stats
    elif stats['vertices'][(i1, j1)] == 2 and stats['vertices'][(i2, j2)] == 2 and (i2, j2) in stats['current'][
        (i1, j1)]:
        return board, stats
    if i1 == i2:
        for j in range(min(j1, j2) + 1, max(j1, j2)):
            board[i1][j] = '-' if (i2, j2) not in stats['current'][(i1, j1)] else '='
    else:
        for i in range(min(i1, i2) + 1, max(i1, i2)):
            board[i][j1] = '|' if (i2, j2) not in stats['current'][(i1, j1)] else "║"
    stats['current'][(i1, j1)].append((i2, j2))
    stats['current'][(i2, j2)].append((i1, j1))
    return board, stats


def minimum_needed_islands(n):
    return math.ceil(n / 2)


def solve(board, stats):
    keep_on = True
    while keep_on:
        keep_on = False
        for v in stats['vertices']:
            # print('in solve for', v)
            if len(stats['current'][v]) == stats['vertices'][v]:
                continue
            ns = get_ns(board, stats, v[0], v[1])
            possible_connection = [n for n in ns if
                                   len(stats['current'][n]) < stats['vertices'][n] and stats['current'][v].count(n) < 2]
            # print(possible_connection)

            if minimum_needed_islands(stats['vertices'][v] - len(stats['current'][v])) >= len(possible_connection):
                keep_on = True
                for n in possible_connection:
                    board, stats = set_bridge(board, stats, v[0], v[1], n[0], n[1])

            possible_connection = [n for n in possible_connection if
                                   len(stats['current'][n]) < stats['vertices'][n] and stats['current'][v].count(n) < 2]
            # print(possible_connection)
            more_connection = []

            for c in possible_connection:
                other_current = stats['vertices'][c] - len(stats['current'][c])
                if stats['current'][v].count(c) < 2:
                    if other_current > 0:
                        more_connection.append(c)
                    if other_current > 1 and stats['current'][v].count(c) == 0:
                        more_connection.append(c)

            # print(more_connection)
            if len(more_connection) == stats['vertices'][v] - len(stats['current'][v]):
                keep_on = True
                for n in more_connection:
                    board, stats = set_bridge(board, stats, v[0], v[1], n[0], n[1])
            # print_board(board)
            # print(stats)
    return board, stats


def backtrack(board, stats, tries=0):
    not_done = [v for v in stats['vertices'] if stats['vertices'][v] > len(stats['current'][v])]
    for v in not_done:
        ns = get_ns(board, stats, v[0], v[1])
        possible_connection = [n for n in ns if
                               len(stats['current'][n]) < stats['vertices'][n] and stats['current'][v].count(n) < 2]
        print(possible_connection)
        for p in possible_connection:
            board1, stats1 = set_bridge(board, stats, v[0], v[1], p[0], p[1])
            board1, tempstats1 = solve(board1, stats1)
            if is_solved(stats):
                return board1, stats1


def is_connected(stats):
    visited = set()
    to_visit = list()
    to_visit.append(list(stats['vertices'].keys())[0])
    while len(to_visit)>0:
        v=to_visit.pop()
        visited.add(v)
        ns = set(stats['current'][v])
        to_visit.extend(list(ns - visited))
    if len(visited)==len(stats['vertices']):
        return True
    return False


def is_solved(stats):
    return sum([stats['vertices'][v] for v in stats['vertices']]) == sum(
        [len(bs) for v, bs in stats['current'].items()]) and is_connected(stats)


def print_board(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '.':
                print(' ', end='')
            else:
                print(board[i][j], end='')
        print()


if __name__ == '__main__':
    board, stats = read_board(os.path.join(os.getcwd(), 'test'))
    # board, stats = read_board(os.path.join(os.getcwd(), 'hard_board'))
    print('input:')
    print_board(board)

    print('output:')
    solved, solved_stats = solve(board, stats)
    print(solved_stats)
    print_board(solved)
    if is_solved(stats):
        print('SOLVED!')
    else:
        print('BACKTRACK')
        solved, solved_stats = backtrack(solved, solved_stats)
        print(solved_stats)
        print_board(solved)
