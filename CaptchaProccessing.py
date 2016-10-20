from PIL import Image
import ImageEnhance

def CrackCaptcha(imgpath):
    im = Image.open(imgpath)
    nx, ny = im.size
    im2 = im.resize((int(nx * 5), int(ny * 5)), Image.BICUBIC)
    im2.save("temp2.jpg")
    enh = ImageEnhance.Contrast(im)
    enh.enhance(5.0)


def ImageDenoising(imgpath, black_chop, white_chop):
    b_chop = black_chop
    w_chop = white_chop
    image = Image.open(imgpath).convert('1')
    width, height = image.size
    data = image.load()
    print width, height

    # iterate row first:
    for y in range(height):
        total_b = 0
        total_w = 0
        white_col_index_all = []
        black_col_index_all = []
        white_col_index = []
        black_col_index = []

        # do black noises
        for x in range(width):
            if data[x,y] < 128: # black
                total_b += 1
                black_col_index.append(x)
            else:
                if total_b <= b_chop:
                    black_col_index_all.append(black_col_index)
                black_col_index = []
                total_b = 0

        # do white noises
        for x in range(width):
            if data[x,y] > 128: # white
                total_w += 1
                white_col_index.append(x)
            else:
                if total_w <= w_chop:
                    white_col_index_all.append(white_col_index)
                white_col_index = []
                total_w = 0

        for cell_white in white_col_index_all:
            if len(cell_white) != 0:
                for element_white in cell_white:
                    data[element_white, y] = 0 # change white noises to black

        for cell_black in black_col_index_all:
            if len(cell_black) != 0:
                for element_black in cell_black:
                    data[element_black, y] = 255 # change black noises to white



    # iterate column:
    for x in range(width):
        total_b = 0
        total_w = 0
        white_row_index_all = []
        black_row_index_all = []
        white_row_index = []
        black_row_index = []

        # do black noises
        for y in range(height):
            if data[x, y] < 128:  # black
                total_b += 1
                black_row_index.append(y)
            else:
                if total_b <= b_chop:
                    black_row_index_all.append(black_row_index)
                black_row_index = []
                total_b = 0

        # do white noises
        for y in range(height):
            if data[x, y] > 128:  # white
                total_w += 1
                white_row_index.append(y)
            else:
                if total_w <= w_chop:
                    white_row_index_all.append(white_row_index)
                white_row_index = []
                total_w = 0

        for cell_white in white_row_index_all:
            if len(cell_white) != 0:
                for element_white in cell_white:
                    data[x, element_white] = 0  # change white noises to black

        for cell_black in black_row_index_all:
            if len(cell_black) != 0:
                for element_black in cell_black:
                    data[x, element_black] = 255  # change black noises to white




    image.save('result.jpg')