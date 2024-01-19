from PIL import Image

def image_to_matrix(image_path):
    image = Image.open(image_path)
    width, height = image.size
    matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel = image.getpixel((x, y))
            if pixel == (156, 90, 60, 255):  # Deep water
                row.append(1)
            if pixel == (61, 156, 65, 255):  # Deep water
                row.append(2)
            if pixel == (0, 162, 232, 255):  # Deep water
                row.append(3)
            if pixel == (33, 150, 243, 255):  # Deep water
                row.append(4)
            else:
                row.append(0)  # Unknown color
        matrix.append(row)

    return matrix

def save_matrix_to_file(matrix, output_file):
    with open(output_file, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')

image_path = 'objects_map.png'
result_matrix = image_to_matrix(image_path)
save_matrix_to_file(result_matrix, 'objects_map.txt')
