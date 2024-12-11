import math
def label_catan_hexes(resources):
    vertex_map = []
    vertex_counter = 3

    # Top row exception
    vertex_map.extend([
        {0: [resources[0][0]]},
        {1: [resources[0][1]]},
        {2: [resources[0][2]]}
    ])

    mid_row = math.floor(len(resources) / 2)

    # Process the board layout
    for row in range(len(resources)):
        # need to repeat twice to get all hexes for each row
        for row_counter in range(2):
            for i in range(len(resources[row]) + 1):
                if row_counter == 0:  # Top row of vertices for the hex
                    if i == 0:
                        vertex_map.append({vertex_counter: [resources[row][i]]})
                    elif i == len(resources[row]):
                        adjacent = [resources[row][i - 1]]
                        if row > mid_row:
                            adjacent.insert(0, resources[row - 1][i])
                        vertex_map.append({vertex_counter: adjacent})
                    else:
                        adjacent = [resources[row][i - 1], resources[row][i]]
                        if row > mid_row:
                            adjacent.insert(0, resources[row - 1][i])
                        elif row > 0:
                            adjacent.insert(0, resources[row - 1][i - 1])
                        vertex_map.append({vertex_counter: adjacent})
                else:  # Bottom row of vertices for the hex
                    if row < mid_row:
                        if i == 0:
                            vertex_map.append({vertex_counter: [resources[row][i], resources[row + 1][i]]})
                        elif i == len(resources[row]):
                            vertex_map.append({vertex_counter: [resources[row][i - 1], resources[row + 1][i]]})
                        else:
                            vertex_map.append({vertex_counter: [resources[row][i - 1], resources[row][i], resources[row + 1][i]]})
                    elif row < len(resources) - 1:
                        if i == 0:
                            vertex_map.append({vertex_counter: [resources[row][i]]})
                        elif i == len(resources[row]):
                            vertex_map.append({vertex_counter: [resources[row][i - 1]]})
                        else:
                            vertex_map.append({vertex_counter: [resources[row][i - 1], resources[row][i], resources[row + 1][i - 1]]})
                    else:
                        if i == 0:
                            vertex_map.append({vertex_counter: [resources[row][i]]})
                        elif i == len(resources[row]):
                            vertex_map.append({vertex_counter: [resources[row][i - 1]]})
                        else:
                            vertex_map.append({vertex_counter: [resources[row][i - 1], resources[row][i]]})
                vertex_counter += 1

    # Bottom row exception
    vertex_map.extend([
        {vertex_counter: [resources[-1][0]]},
        {vertex_counter + 1: [resources[-1][1]]},
        {vertex_counter + 2: [resources[-1][2]]}
    ])

    print(vertex_map)

    return vertex_map


# resources = [
#     ['brick', 'forest', 'sheep'],
#     ['forest', 'wheat', 'rock', 'wheat'],
#     ['sheep', 'rock', 'sheep', 'sheep', 'forest'],
#     ['desert', 'brick', 'wheat', 'brick'],
#     ['rock', 'forest', 'wheat']
# ]
resources = [
    ['w', 's', 'f'],
    ['w', 'b', 's', 'b'],
    ['f', 's', 'r', 'r', 'f'],
    ['b', 's', 'w', 'b', 'w', 'f'],
    ['f', 'b', 'd', 'r', 'f'],
    ['w', 'r', 'r', 's'],
    ['s', 'w', 'd']

]


vertex_resource_map = label_catan_hexes(resources)