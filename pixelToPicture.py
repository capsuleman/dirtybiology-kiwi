from math import sqrt, floor
import numpy as np
import requests

from kiwi import kiwi, starting_x, starting_y
from creds import USERNAME, PASSWORD


FLAG_API = 'https://api-flag.fouloscopie.com/flag'


def get_pixels_with_id():
    flag_data = requests.get(FLAG_API).json()
    return (
        list(map(lambda datum: (datum['hexColor']), flag_data)),
        list(map(lambda datum: (datum['entityId']), flag_data)))


def get_diag(pixels):
    return floor(sqrt(len(pixels) / 2))


def hex_to_pixel(hex_value):
    try:
        return np.array([
            int(hex_value[1:3], 16),
            int(hex_value[3:5], 16),
            int(hex_value[5:7], 16),
        ])
    except:
        print(f'Error parsing hexadecimal value {hex_value}.')
        return np.zeros((3))


def update_pixel(pixel_id, color):
    login_response = requests.post(
        'https://api.fouloscopie.com/auth/login',
        json={'email': USERNAME, 'password': PASSWORD}).json()
    access_token = login_response['access_token']

    user_response = requests.get(
        'https://admin.fouloscopie.com/users/me',
        headers={'Authorization': f'Bearer {access_token}'}).json()
    fouloscopie_token = user_response['data']['token']
    print(fouloscopie_token)

    print(requests.put(
        'https://api-flag.fouloscopie.com/pixel',
        json={'hexColor': color, 'pixelId': pixel_id},
        headers={'Authorization': fouloscopie_token}).json())


pixels, pixels_id = get_pixels_with_id()
totalDiag = get_diag(pixels)
full_flag = np.zeros((2 * totalDiag, totalDiag, 3), dtype=np.uint8)
full_flag_pixel_ids = np.zeros((2 * totalDiag, totalDiag), dtype=object)

full_flag[0, 0] = hex_to_pixel(pixels[0])
full_flag_pixel_ids[0, 0] = pixels_id[0]
full_flag[1, 0] = hex_to_pixel(pixels[1])
full_flag_pixel_ids[1, 0] = pixels_id[1]
currentPix = 2

for diag in range(1, totalDiag):
    for x in range(2 * diag):
        full_flag[x, diag] = hex_to_pixel(pixels[currentPix])
        full_flag_pixel_ids[x, diag] = pixels_id[currentPix]
        currentPix += 1

    for y in range(diag + 1):
        full_flag[2 * diag, y] = hex_to_pixel(pixels[currentPix])
        full_flag_pixel_ids[2 * diag, y] = pixels_id[currentPix]
        currentPix += 1

    for y in range(diag + 1):
        full_flag[2 * diag + 1, y] = hex_to_pixel(pixels[currentPix])
        full_flag_pixel_ids[2 * diag + 1, y] = pixels_id[currentPix]
        currentPix += 1


clipped_flag = full_flag[
    starting_x:starting_x + len(kiwi),
    starting_y:starting_y + len(kiwi[0])]

diff = np.zeros((len(kiwi), len(kiwi[0])), dtype=np.uint32)

for x, line in enumerate(kiwi):
    for y, pixel in enumerate(line):
        if pixel != None:
            diff[x, y] = sum(
                abs(clipped_flag[x, y] - hex_to_pixel(pixel))) // 3

biggest_diff = np.where(diff == np.amax(diff))
pixel_to_change = full_flag_pixel_ids[
    starting_x + biggest_diff[0][0],
    starting_y + biggest_diff[1][0]]
new_color = kiwi[biggest_diff[0][0]][biggest_diff[1][0]]
print(pixel_to_change, new_color)

update_pixel(pixel_to_change, new_color)
