from django.shortcuts import render
from django.http import HttpResponse
import json
import time
# Create your views here.

def solve(request):
    start = time.time()
    if request.method == 'GET':
        if request.GET.get('board'):
            board = json.loads(request.GET.get('board'))
            note = {}
            for i in range(1, 10):
                note[i] = []
            ########### note creation #######################################################################
            for i in range(len(board)):
                if board[i] == 0:
                    quo = i // 9
                    rem = i % 9
                    possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    numbers_in_row = []
                    numbers_in_column = []
                    numbers_in_block = []
                    for j in range(9):
                        row = (quo * 9) + j
                        column = (j * 9) + rem
                        block = ((((quo // 3) * 3) + (j // 3)) * 9) + (((rem // 3) * 3) + (j % 3))
                        board_list = board
                        if board[row] != 0:
                            numbers_in_row.append(board_list[row])
                        if board[column] != 0:
                            numbers_in_column.append(board_list[column])
                        if board[block] != 0:
                            numbers_in_block.append(board_list[block])
                    if len(numbers_in_row) != len(set(numbers_in_row)) or len(numbers_in_column) != len(set(numbers_in_column)) or len(numbers_in_block) != len(set(numbers_in_block)):# or len(numbers_in_row) == 0 or len(numbers_in_column) == 0 or len(numbers_in_block) == 0:
                        return HttpResponse("Invalid board", content_type="text/plain")
                    possible_numbers = list(set(possible_numbers) - set(numbers_in_row) - set(numbers_in_column) - set(numbers_in_block))
                    for j in possible_numbers:
                        note[j].append(i)
                else:
                    note[board[i]].append(i)
            #################################################################################################
            ############ note solving #######################################################################
            condition = True
            while condition:
                for i in note:
                    length = len(note[i])
                    l = len(note[i]) - 1
                    while l < length and l >= 0:
                        address = note[i][l]
                        quo = address // 9
                        rem = address % 9
                        row_list = []
                        column_list = []
                        block_list = []
                        for k in range(9):
                            row = (quo * 9) + k
                            column = (k * 9) + rem
                            block = ((((quo // 3) * 3) + (k // 3)) * 9) + (((rem // 3) * 3) + (k % 3))
                            if row != address:
                                row_list.append(row)
                            if column != address:
                                column_list.append(column)
                            if block != address:
                                block_list.append(block)
                        if (not set(row_list).intersection(set(note[i]))) or (not set(column_list).intersection(set(note[i]))) or (not set(block_list).intersection(set(note[i]))):
                            for j in note:
                                if j == i:
                                    note[j] = list(set(note[j]) - set(row_list) - set(column_list) - set(block_list))
                                else:
                                    if address in note[j]:
                                        note[j].remove(address)
                        if len(note[i]) < length:
                            l = l - (length - len(note[i]))
                        else:
                            l -= 1
                        length = len(note[i])
                stop_cond = True
                for i in note:
                    if len(note[i]) > 9:
                        stop_cond = False
                if stop_cond:
                    condition = False
            solved_board = [0 for e in range(81)]
            for i in note:
                for j in note[i]:
                    solved_board[j] = i
            end = time.time()
            elapsed = end - start
            printable_solved_board = " | "
            for j in range(9 * 2 + 3):
                    printable_solved_board += "-"
            printable_solved_board += " | \n"
            for i in range(9):
                if (i + 1) % 3 == 1:
                    printable_solved_board += " | "
                for j in range(9):
                    printable_solved_board += str(solved_board[i * 9 + j])
                    if (j + 1) % 3 == 0:
                        printable_solved_board += " | "
                    else:
                        printable_solved_board += " "
                printable_solved_board += "\n | "
                if (i + 1) % 3 == 0:
                    for j in range(9 * 2 + 3):
                        printable_solved_board += "-"
                    printable_solved_board += " | \n"
            content = {"solved_board_list": solved_board, "printable_solved_board": printable_solved_board, "time": elapsed}
            return HttpResponse(json.dumps(content), content_type="text/json")
        else:
            return HttpResponse("No board provided", status=400, reason='board not provided')
    else:
        return HttpResponse(status=405, reason='Method Not Allowed', allowed_methods=['GET'])