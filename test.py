



from collections import defaultdict

# Define the hexagon grid
rows = [
    ['A1'],
    ['B1', 'B2'],
    ['C1', 'C2', 'C3'],
    ['D1', 'D2'],
    ['E1']
]

# Function to assign vertex names based on hexagons sharing them
def hexagon_vertices_names(rows):
    vertices = defaultdict(list)
    
    for r, row in enumerate(rows):
        for c, hex_name in enumerate(row):
            print(f"Hexagon: {hex_name}")
            # Calculate surrounding vertices
            top = f'v{r}_{c}_top'
            bottom = f'v{r}_{c}_bottom'
            top_left = f'v{r}_{c}_top_left'
            top_right = f'v{r}_{c}_top_right'
            bottom_left = f'v{r}_{c}_bottom_left'
            bottom_right = f'v{r}_{c}_bottom_right'
            
            # Assign vertices to the hexagon
            vertices[top].append(hex_name)
            vertices[bottom].append(hex_name)
            vertices[top_left].append(hex_name)
            vertices[top_right].append(hex_name)
            vertices[bottom_left].append(hex_name)
            vertices[bottom_right].append(hex_name)

            # Handle vertex sharing between hexagons
            if c > 0:
                vertices[f'v{r}_{c-1}_top_right'].append(hex_name)
                vertices[f'v{r}_{c-1}_bottom_right'].append(hex_name)
            if r > 0:
                vertices[f'v{r-1}_{c}_bottom'].append(hex_name)
                if c < len(rows[r-1]):
                    vertices[f'v{r-1}_{c}_bottom_left'].append(hex_name)
                    vertices[f'v{r-1}_{c}_bottom_right'].append(hex_name)
                if c > 0:
                    vertices[f'v{r-1}_{c-1}_bottom_right'].append(hex_name)
                    vertices[f'v{r-1}_{c-1}_bottom_left'].append(hex_name)
    
    # Remove empty or single-hexagon vertices
    vertices = {k: v for k, v in vertices.items() if len(v) > 1}

    return vertices

# Get and print the vertices with intersecting hexagons
vertices_with_hexagons = hexagon_vertices_names(rows)
for vertex, hexagons in vertices_with_hexagons.items():
    print(f"Vertex {vertex}: {', '.join(hexagons)}")
