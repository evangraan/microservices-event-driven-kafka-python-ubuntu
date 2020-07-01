def room_distance(room):
    floor_adder = 0
    room_value = 0
    if room.startswith('A'):
        floor_adder = 1
    if room.startswith('B'):
        floor_adder = 2
    if room.startswith('C'):
        floor_adder = 3
    if room.endswith('1'):
        room_value = 1
    if room.endswith('2'):
        room_value = 2
    if room.endswith('3'):
        room_value = 3

    return floor_adder + room_value
