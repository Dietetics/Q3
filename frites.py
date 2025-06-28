# Nom, Matricule
# Nom, Matricule

import sys


def read(input_file):
    """Fonctions pour lire dans les fichier. Vous pouvez les modifier,
    faire du parsing, rajouter une valeur de retour, mais n'utilisez pas
    d'autres librairies.
    Functions to read in files. you can modify them, do some parsing,
    add a return value, but don't use other librairies"""

    file = open(input_file, "r")
    lines = file.readlines()
    file.close()

    # Parse the input
    n = int(lines[0].strip())
    points = []
    for i in range(1, n + 1):
        x, y = map(int, lines[i].strip().split())
        points.append((x, y))

    return n, points


def write(str_content, output_file):
    """Fonctions pour écrire dans un fichier. Vous pouvez la modifier,
    faire du parsing, rajouter une valeur de retour, mais n'utilisez pas
    d'autres librairies.
    Functions to read in files. you can modify them, do some parsing,
    add a return value, but don't use other librairies"""

    file = open(output_file, "w")
    file.write(str_content)
    file.close()


def can_place_fries(points, k):
    """Check if fries of half-length k can be placed on all points"""
    n = len(points)

    if n > 20:  # For large inputs, use greedy approach
        return can_place_fries_greedy(points, k)

    # Try all possible orientations (0 = horizontal, 1 = vertical)
    for mask in range(1 << n):
        valid = True

        # Check if this orientation assignment is valid
        for i in range(n):
            for j in range(i + 1, n):
                x1, y1 = points[i]
                x2, y2 = points[j]

                orientation_i = (mask >> i) & 1
                orientation_j = (mask >> j) & 1

                # If same orientation, check for overlap
                if orientation_i == orientation_j:
                    if orientation_i == 0:  # Both horizontal
                        if y1 == y2 and abs(x1 - x2) < 2 * k + 1:
                            valid = False
                            break
                    else:  # Both vertical
                        if x1 == x2 and abs(y1 - y2) < 2 * k + 1:
                            valid = False
                            break

            if not valid:
                break

        if valid:
            return True

    return False


def can_place_fries_greedy(points, k):
    """Greedy approach for large inputs"""
    n = len(points)

    # Build conflict graph
    conflicts = [[] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]

            # Check if they conflict when both horizontal
            h_conflict = (y1 == y2 and abs(x1 - x2) < 2 * k + 1)
            # Check if they conflict when both vertical
            v_conflict = (x1 == x2 and abs(y1 - y2) < 2 * k + 1)

            if h_conflict and v_conflict:
                return False  # No valid assignment possible
            elif h_conflict:
                conflicts[i].append((j, 'h'))  # Can't both be horizontal
                conflicts[j].append((i, 'h'))
            elif v_conflict:
                conflicts[i].append((j, 'v'))  # Can't both be vertical
                conflicts[j].append((i, 'v'))

    # Try to assign orientations greedily
    orientation = [-1] * n  # -1: unassigned, 0: horizontal, 1: vertical

    def is_valid_assignment(point, orient):
        for neighbor, conflict_type in conflicts[point]:
            if orientation[neighbor] != -1:
                if conflict_type == 'h' and orient == 0 and orientation[neighbor] == 0:
                    return False
                if conflict_type == 'v' and orient == 1 and orientation[neighbor] == 1:
                    return False
        return True

    def backtrack(point):
        if point == n:
            return True

        # Try horizontal first
        if is_valid_assignment(point, 0):
            orientation[point] = 0
            if backtrack(point + 1):
                return True
            orientation[point] = -1

        # Try vertical
        if is_valid_assignment(point, 1):
            orientation[point] = 1
            if backtrack(point + 1):
                return True
            orientation[point] = -1

        return False

    return backtrack(0)



def find_max_k(points):
    """Find the maximum k for which fries can be placed"""
    n = len(points)


    # Cas 1: if only one point, infinite is possible
    if n <= 1:
        return "infini"


    # Cas 2: si k=0
    # Check if k=0 is possible
    if not can_place_fries(points, 0):
        return "0"


    # Cas 3: si infini, checked
    # Try increasingly large k values until we find one that doesn't work
    # But first check if infinite is possible by trying a very large k
    large_k = 1000  # Large enough k to test if infinite is possible

    if can_place_fries(points, large_k):
        return "infini"


    # Cas 4: trouver k, checked
    # Binary search for maximum k
    # Find the largest k that works
    left, right = 0, large_k
    result = 0

    while left <= right:
        mid = (left + right) // 2
        if can_place_fries(points, mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1

    return str(result)


def main(args):
    """Fonction main/Main function"""
    input_file = args[0]
    output_file = args[1]
    n, points = read(input_file)

    result = find_max_k(points)
    write(result, output_file)


# NE PAS TOUCHER
# DO NOT TOUCH
if __name__ == "__main__":
    main(sys.argv[1:])
