from math import sqrt, floor
import numpy as np
import requests
from random import random
from time import sleep
from datetime import datetime
import threading

from kiwi import kiwi, starting_x, starting_y
from creds import ACCOUNTS

GET_FLAG_URL = 'https://api-flag.fouloscopie.com/flag'
FOULOSCOPIE_LOGIN_URL = 'https://api.fouloscopie.com/auth/login'
GET_USER_INFO_URL = 'https://admin.fouloscopie.com/users/me'
UPDATE_PIXEL_URL = 'https://api-flag.fouloscopie.com/pixel'
GET_FLAG_UPDATES_URL = 'https://api-flag.fouloscopie.com/flag/after'


def get_pixels_with_id():
    flag_data = requests.get(GET_FLAG_URL).json()
    return (
        list(map(lambda datum: (datum['hexColor']), flag_data)),
        list(map(lambda datum: (datum['entityId']), flag_data)))


def get_diag(pixels):
    return floor(sqrt(len(pixels) / 2)) + 1


def hex_to_pixel(hex_value):
    try:
        return np.array([
            int(hex_value[1:3], 16),
            int(hex_value[3:5], 16),
            int(hex_value[5:7], 16),
        ])
    except:
        if hex_value != None:
            print(f'Error parsing hexadecimal value {hex_value}.')
        return np.zeros((3))


def get_token(email, password):
    login_response = requests.post(
        FOULOSCOPIE_LOGIN_URL,
        json={'email': email, 'password': password}).json()
    access_token = login_response['access_token']

    user_response = requests.get(
        GET_USER_INFO_URL,
        headers={'Authorization': f'Bearer {access_token}'}).json()
    fouloscopie_token = user_response['data']['token']
    return fouloscopie_token


def update_pixel(pixel_id, color, fouloscopie_token):
    while True:
        response = requests.put(
            UPDATE_PIXEL_URL,
            json={'hexColor': color, 'pixelId': pixel_id},
            headers={'Authorization': fouloscopie_token})
        content = response.json()
        status_code = response.status_code

        if status_code == 200:
            return
        if status_code == 429:
            time_to_wait = content['retryAfter'] / 1000 + 10 * random()
            print('Too short! Next try in {0:.2f}s'.format(time_to_wait))
            sleep(time_to_wait)


def get_index_or_none(list, index):
    if index < len(list):
        return list[index]
    return None


def get_full_flag_with_id():
    pixels, pixels_id = get_pixels_with_id()

    totalDiag = get_diag(pixels)
    full_flag = np.zeros((2 * totalDiag, totalDiag, 3), dtype=np.uint8)
    full_flag_pixel_ids = np.zeros((2 * totalDiag, totalDiag), dtype=object)

    def add_pixel_to_flag(x, y, current_pix):
        full_flag[x, y] = hex_to_pixel(get_index_or_none(pixels, current_pix))
        full_flag_pixel_ids[x, y] = get_index_or_none(pixels_id, current_pix)

    add_pixel_to_flag(0, 0, 0)
    add_pixel_to_flag(1, 0, 1)
    currentPix = 2

    for diag in range(1, totalDiag):
        for x in range(2 * diag):
            add_pixel_to_flag(x, diag, currentPix)
            currentPix += 1

        for y in range(diag + 1):
            add_pixel_to_flag(2 * diag, y, currentPix)
            currentPix += 1

        for y in range(diag + 1):
            add_pixel_to_flag(2 * diag + 1, y, currentPix)
            currentPix += 1

    return full_flag, full_flag_pixel_ids


def get_last_updates(last_update_ts):
    return requests.get(
        f'{GET_FLAG_UPDATES_URL}/{last_update_ts}').json()


def get_datetime():
    return datetime.utcnow().isoformat()[:-3] + 'Z'


def update_flag_thread_function(full_flag, full_flag_pixel_ids):
    print('[UPDATE FLAG] Starting thread')

    last_update_ts = get_datetime()
    while True:
        sleep(30)
        last_updates = get_last_updates(last_update_ts)
        for update in last_updates:
            pixel_id = update['entityId']
            new_color = update['hexColor']
            flag_index = update['indexInFlag']

            where_result = np.where(full_flag_pixel_ids == pixel_id)
            if len(where_result[0]) == 0:
                print('[UPDATE FLAG] Pixel outside initial flag', flag_index)
                continue

            coords = (where_result[0][0], where_result[1][0])
            full_flag[coords] = hex_to_pixel(new_color)

        print(f'[UPDATE FLAG] Updated {len(last_updates)} pixels.')
        last_update_ts = get_datetime()


sem = threading.Semaphore()


def main_thread_function(full_flag, full_flag_pixel_ids, email, password, index):
    print(f'[MAIN {index}] Starting thread')

    token = get_token(email, password)
    time_to_wait = 0

    while True:
        print('[MAIN {}] Next execution in {:.2f}s'.format(index, time_to_wait))
        sleep(time_to_wait)

        sem.acquire()
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
        coord_x = biggest_diff[0][0]
        coord_y = biggest_diff[1][0]
        pixel_to_change = full_flag_pixel_ids[
            starting_x + coord_x,
            starting_y + coord_y]
        new_color = kiwi[coord_x][coord_y]
        sem.release()

        full_flag[coord_x, coord_y] = hex_to_pixel(new_color)
        update_pixel(pixel_to_change, new_color, token)
        print(f'[MAIN {index}] Updated {pixel_to_change} with {new_color}')

        time_to_wait = 120 + 30 * random()


if __name__ == '__main__':
    full_flag, full_flag_pixel_ids = get_full_flag_with_id()

    main_threads = []

    for index, account in enumerate(ACCOUNTS):
        new_main_thread = threading.Thread(
            target=main_thread_function,
            args=(full_flag, full_flag_pixel_ids,
                  account['email'], account['password'], index),
            daemon=True
        )
        main_threads.append(new_main_thread)

    update_thread = threading.Thread(
        target=update_flag_thread_function,
        args=(full_flag, full_flag_pixel_ids),
        daemon=True
    )
    for main_thread in main_threads:
        main_thread.start()
    update_thread.start()

    for main_thread in main_threads:
        main_thread.join()
    update_thread.join()
