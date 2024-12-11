from random import shuffle
import math

def generate_board(resources, number_of_resources, desert, number_of_deserts, extra_resources, setup):
    total_hexes = []
    for resource in resources:
        total_hexes += number_of_resources * [resource]
    total_hexes += number_of_deserts * desert
    for resource in extra_resources:
        total_hexes += 1 * [resource]
    board_setup = [hex for hex in total_hexes]
    shuffle(board_setup)

    start_index = 0
    rows = []
    for row in setup:
        end_index = start_index + row
        row_items = board_setup[start_index:end_index]
        rows.append(row_items)
        start_index = end_index

    return board_setup, rows

def label_catan_hexes(rows):
    vertex_map = []
    vertex_counter = 3

    # Top row exception
    vertex_map.extend([
        {0: [rows[0][0]]},
        {1: [rows[0][1]]},
        {2: [rows[0][2]]}
    ])

    mid_row = math.floor(len(rows) / 2)

    # Process the board layout
    for row in range(len(rows)):
        # need to repeat twice to get all hexes for each row
        for row_counter in range(2):
            for i in range(len(rows[row]) + 1):
                if row_counter == 0:  # Top row of vertices for the hex
                    if i == 0:
                        vertex_map.append({vertex_counter: [rows[row][i]]})
                    elif i == len(rows[row]):
                        adjacent = [rows[row][i - 1]]
                        if row > mid_row:
                            adjacent.insert(0, rows[row - 1][i])
                        vertex_map.append({vertex_counter: adjacent})
                    else:
                        adjacent = [rows[row][i - 1], rows[row][i]]
                        if row > mid_row:
                            adjacent.insert(0, rows[row - 1][i])
                        elif row > 0:
                            adjacent.insert(0, rows[row - 1][i - 1])
                        vertex_map.append({vertex_counter: adjacent})
                else:  # Bottom row of vertices for the hex
                    if row < mid_row:
                        if i == 0:
                            vertex_map.append({vertex_counter: [rows[row][i], rows[row + 1][i]]})
                        elif i == len(rows[row]):
                            vertex_map.append({vertex_counter: [rows[row][i - 1], rows[row + 1][i]]})
                        else:
                            vertex_map.append({vertex_counter: [rows[row][i - 1], rows[row][i], rows[row + 1][i]]})
                    elif row < len(rows) - 1:
                        if i == 0:
                            vertex_map.append({vertex_counter: [rows[row][i]]})
                        elif i == len(rows[row]):
                            vertex_map.append({vertex_counter: [rows[row][i - 1]]})
                        else:
                            vertex_map.append({vertex_counter: [rows[row][i - 1], rows[row][i], rows[row + 1][i - 1]]})
                    else:
                        if i == 0:
                            vertex_map.append({vertex_counter: [rows[row][i]]})
                        elif i == len(rows[row]):
                            vertex_map.append({vertex_counter: [rows[row][i - 1]]})
                        else:
                            vertex_map.append({vertex_counter: [rows[row][i - 1], rows[row][i]]})
                vertex_counter += 1

    # Bottom row exception
    vertex_map.extend([
        {vertex_counter: [rows[-1][0]]},
        {vertex_counter + 1: [rows[-1][1]]},
        {vertex_counter + 2: [rows[-1][2]]}
    ])

    return vertex_map

def generate_spiral_order_of_hexes(rows, number_of_items):
    spiral_order = []
    top = 0
    right = max(len(row) for row in rows) - 1
    bottom = len(rows) - 1
    left = 0
    right_most = -1
    most_right = 3
    most_left = 0
    position_order = []

    # if there is place to move ahead and place to move at the bottom
    while  top <= bottom and left <= right and number_of_items > 0:
        # move left to right on the top row
        if most_left > most_right:
            spiral_order.append(rows[top][most_left])
            number_of_items -= 1
        else:
            spiral_order.extend(rows[top][most_left:most_right+1])
            number_of_items -= len(rows[top][most_left:most_right+1])
        top += 1

        # move from top to bottom, adding all items in the right most
        for i in range(top, bottom ):
            spiral_order.append(rows[i][right_most])
            number_of_items -= 1
        # move right (left) by one
        right -= 1
        right_most -=1

        # move from right to left on the bottom row (and bottom row is below the top row)
        if top < bottom:
            if most_left > most_right:
                spiral_order.append(rows[bottom][most_left])
                number_of_items -= 1
            else:
                items = rows[bottom][most_left:most_right+1][::-1]
                spiral_order.extend(items)
                number_of_items -= len(items)
            bottom -= 1

        # move from bottom to top, adding all items in the left most
        if left <= right:
            for i in range(bottom, top - 1, -1):
                if left < len(rows[i]):
                    spiral_order.append(rows[i][left])
                    number_of_items -= 1
            # move left (right) by one
            left += 1
        most_right -= 1
        most_left += 1

    return spiral_order


def get_dots_for_number(number):
    if number == 2 or number == 12:
        return 1
    elif number == 3 or number == 11:
        return 2
    elif number == 4 or number == 10:
        return 3
    elif number == 5 or number == 9:
        return 4
    elif number == 6 or number == 8:
        return 5
    else:
        return 0

def assign_number_to_hexes(spiral_order, number_order):
    hex_assignment = []
    number_index = 0

    for i in range(len(spiral_order)):
        if spiral_order[i] == 'D':
            hex_assignment.append({'resource': 'D', 'number': 7, 'dots': 0, 'dots_as_stars': get_dots_as_stars(0)})
        else:
            if number_index < len(number_order):
                dots = get_dots_for_number(number_order[number_index])
                hex_assignment.append({'resource': spiral_order[i], 'number': number_order[number_index], 'dots': dots, 'dots_as_stars': get_dots_as_stars(dots)})
                number_index += 1
            else:
                hex_assignment.append({'resource': spiral_order[i], 'number': None, 'dots': 0, 'dots_as_stars': get_dots_as_stars(0)})
    return hex_assignment

def get_dots_as_stars(dots):
    return '*' * dots

def print_custom_catan_board(hexes, setup):
    if sum(setup) != len(hexes):
        print("Setup does not match the number of hexes.")
        return
    all_rows = []
    # Define indentation levels for the setup
    start_index= 0
    for row in setup:
        end_index = start_index + row
        row_items = hexes[start_index:end_index]
        row_items_filtered = []
        for item in row_items:
            row_items_filtered.append(f"{item['resource']}({get_dots_as_stars(item['dots'])})")
        row_display = "   " * (len(setup) - row) + "   ".join([f"[{item}]" for item in row_items_filtered])
        print(row_display)
        start_index = end_index
        all_rows.append(row_items_filtered)
    return all_rows


def generate_complete_board(number_of_players):
    resources = ['W', 'L', 'B', 'O', 'G']
    desert = ['D']
    commodities = ['paper', 'coin', 'cloth']
    extra_resource = ['L', 'O', 'W']
    if number_of_players == 3 or number_of_players == 4:
        number_of_deserts = 1
        number_of_resources = 3
        setup = [3, 4, 5, 4, 3]
        number_order = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
        number_of_items = 19
        print('normal')

    elif number_of_players == 5 or number_of_players == 6:
        number_of_deserts = 2
        number_of_resources = 5
        setup = [3, 4, 5, 6, 5, 4, 3]
        number_order = [4, 5, 2, 8, 4, 8, 3, 6, 10, 11, 11, 8, 9, 3, 6, 11, 10, 9, 5, 9, 4, 5, 10, 12, 12, 6, 12, 3]
        number_of_items = 30
        print('expansion')
    
    board_setup, rows = generate_board(resources, number_of_resources, desert, number_of_deserts, extra_resource, setup)

    spiral_order = generate_spiral_order_of_hexes(rows, number_of_items)

    labelled_hex = label_catan_hexes(rows)

    print(spiral_order)

    hex_assignment = assign_number_to_hexes(spiral_order, number_order)
    print(hex_assignment)

    rows = print_custom_catan_board(hex_assignment, setup)

    hex_placement = []
    start_index = 0
    for row in setup:
        end_index = start_index + row
        row_items = hex_assignment[start_index:end_index]
        # row_size = hex_assignment[row]
        hex_placement.append(row_items)
        start_index = end_index


    return hex_placement, setup, labelled_hex
