# Направления векторов. Используются в check_winner
directions = [(1, 0), (0, 1), (1, -1), (1, 1)]

# Направления векторов. Используются в определение пустых пространств
# Это связано с логикой ходов бота ;)
point_around_directions = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]

# Константы для метода define_position в window
indent_from_the_edge = 9
size_of_one_cell = 25
