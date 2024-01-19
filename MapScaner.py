from PIL import Image

def image_to_matrix(image_path):
    image = Image.open(image_path)
    width, height = image.size
    matrix = []

    for y in range(height):
        row = []
        for x in range(width):
            pixel = image.getpixel((x, y))
            if pixel == (63, 72, 204, 255):  # Deep water
                row.append(0)
            elif pixel == (0, 162, 232, 255):  # Shelf
                row.append(1)
            elif pixel == (153, 217, 234, 255):  # Shallow woter
                row.append(2)
            elif pixel == (239, 228, 176, 255):  # Sandb  
                row.append(3)
            elif pixel == (185, 122, 87, 255):  # Road
                row.append(4)
            elif pixel == (0, 150, 136, 255):  # 
                row.append(5)
            elif pixel == (11, 112, 102, 255):  #
                row.append(6)
            elif pixel == (181, 230, 29, 255):  # Soil
                row.append(9)
            elif pixel == (34, 177, 76, 255):  # Forest floor
                row.append(10)
            elif pixel == (126, 83, 207, 255):  # 
                row.append(13)
            elif pixel == (103, 58, 183, 255):  #
                row.append(14)
            elif pixel == (207, 218, 230, 255):  # 
                row.append(15)
            elif pixel == (184, 204, 224, 255):  #
                row.append(16)
            elif pixel == (255, 87, 34, 255):  # 
                row.append(17)
            elif pixel == (244, 67, 54, 255):  #
                row.append(18)
            elif pixel == (195, 195, 195, 255):  # Town road
                row.append(19)
            else:
                row.append(pixel)  # Unknown color
        matrix.append(row)

    return matrix

def save_matrix_to_file(matrix, output_file):
    with open(output_file, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')

image_path = 'map.png'
result_matrix = image_to_matrix(image_path)
save_matrix_to_file(result_matrix, 'map.txt')
