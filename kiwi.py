# https://docs.google.com/spreadsheets/d/1Y3u-ph40jMTpmHqJnsdQnnP6Z2J5CJ0-KBiwkuI8gSQ/edit#gid=0
B0 = "#7E4B15"  # Brown skin
G0 = "#ACDD6F"  # Green
G1 = "#2AB41D"  # Dark green
G2 = "#28D30E"  # Green center
B1 = "#000000"  # Black seed
N0 = None  # Transparent

starting_x = 160
starting_y = 42

kiwi = [
[N0, N0, N0, N0, N0, N0, N0, N0, N0, N0, B0, B0, B0, B0, B0, B0, B0, B0, B0, N0, N0, N0, N0, N0, N0, N0, N0, N0],
[N0, N0, N0, N0, N0, N0, N0, B0, B0, B0, G2, G2, G2, G2, G2, G2, G2, G2, G2, B0, B0, N0, N0, N0, N0, N0, N0, N0],
[N0, N0, N0, N0, N0, B0, B0, B0, G2, G2, G2, G1, G1, G1, G1, G1, G1, G1, G1, G2, G2, B0, B0, N0, N0, N0, N0, N0],
[N0, N0, N0, N0, B0, B0, G2, G2, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G2, G2, B0, N0, N0, N0, N0],
[N0, N0, N0, B0, B0, G2, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G2, B0, N0, N0, N0],
[N0, N0, N0, B0, B0, G2, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G2, B0, N0, N0, N0],
[N0, N0, B0, B0, G2, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G2, B0, N0, N0],
[N0, B0, B0, G2, G1, G1, G1, G1, G1, G1, G1, G2, G2, G2, G2, G2, G2, G2, G1, G1, G1, G1, G1, G1, G1, G2, B0, N0],
[N0, B0, B0, G2, G1, G1, G1, G1, G1, G2, G2, G2, G2, G2, G2, G2, G2, G2, G2, G1, G1, G1, G1, G1, G1, G2, B0, N0],
[N0, B0, B0, G2, G1, G1, G1, G1, G2, G2, G2, B1, G2, G2, G2, G2, G2, B1, G2, G2, G1, G1, G1, G1, G1, G2, B0, N0],
[B0, B0, G2, G1, G1, G1, G1, G1, G2, G2, G2, G2, B1, G0, G0, G0, B1, G2, G2, G2, G2, G1, G1, G1, G1, G1, G2, B0],
[B0, B0, G2, G1, G1, G1, G1, G2, G2, G2, G2, G2, G0, B1, G0, B1, G0, G2, G2, G2, G2, G1, G1, G1, G1, G1, G2, B0],
[B0, B0, G2, G1, G1, G1, G1, G2, G2, G2, G2, G0, G0, G0, G0, G0, G0, G0, G2, G2, G2, G1, G1, G1, G1, G1, G2, B0],
[B0, B0, G2, G1, G1, G1, G1, G2, G2, G2, B1, G0, G0, G0, G0, G0, G0, G0, B1, G2, G2, G1, G1, G1, G1, G1, G2, B0],
[B0, B0, G2, G1, G1, G1, G1, G2, G2, G2, G2, G0, G0, G0, G0, G0, G0, G0, G2, G2, G2, G1, G1, G1, G1, G1, G2, B0],
[B0, B0, G2, G1, G1, G1, G1, G2, G2, G2, G2, G2, G0, B1, G0, B1, G0, G2, G2, G2, G2, G1, G1, G1, G1, G1, G2, B0],
[N0, B0, B0, G2, G1, G1, G1, G1, G2, G2, G2, G2, B1, G0, G0, G0, B1, G2, G2, G2, G2, G1, G1, G1, G1, G2, B0, N0],
[N0, B0, B0, G2, G1, G1, G1, G1, G2, G2, G2, B1, G2, G2, G2, G2, G2, B1, G2, G2, G1, G1, G1, G1, G1, G2, B0, N0],
[N0, B0, B0, G2, G1, G1, G1, G1, G1, G2, G2, G2, G2, G2, G2, G2, G2, G2, G2, G1, G1, G1, G1, G1, G1, G2, B0, N0],
[N0, N0, B0, B0, G2, G1, G1, G1, G1, G1, G1, G2, G2, G2, G2, G2, G2, G2, G1, G1, G1, G1, G1, G1, G2, B0, N0, N0],
[N0, N0, B0, B0, G2, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G2, B0, N0, N0],
[N0, N0, N0, B0, B0, G2, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G2, B0, N0, N0, N0],
[N0, N0, N0, N0, B0, B0, G2, G2, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G1, G2, G2, B0, N0, N0, N0, N0],
[N0, N0, N0, N0, N0, B0, B0, B0, G2, G2, G1, G1, G1, G1, G1, G1, G1, G1, G1, G2, G2, B0, B0, N0, N0, N0, N0, N0],
[N0, N0, N0, N0, N0, N0, B0, B0, B0, B0, G2, G2, G1, G1, G1, G1, G1, G2, G2, B0, B0, N0, N0, N0, N0, N0, N0, N0],
[N0, N0, N0, N0, N0, N0, N0, N0, B0, B0, B0, B0, G2, G2, G2, G2, G2, B0, B0, N0, N0, N0, N0, N0, N0, N0, N0, N0],
[N0, N0, N0, N0, N0, N0, N0, N0, N0, N0, N0, B0, B0, B0, B0, B0, B0, N0, N0, N0, N0, N0, N0, N0, N0, N0, N0, N0],
]
