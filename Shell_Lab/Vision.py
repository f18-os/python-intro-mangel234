arr = [1, 1, 2, 3, 4, 5, 6, 45, 23, 37, 155]


def Gray_Image(I):
    H = {}

    for pix in I:
        H[pix] = H.get(pix, 0) + 1
        print(H)
    return H


Gray_Image(arr)
# print(Final)
