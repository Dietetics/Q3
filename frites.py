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


# Global cache for conflict checking
_conflict_cache = {}


def get_conflicts_for_k(points, k):
    """Get cached conflicts for given points and k"""
    points_key = tuple(sorted(points))
    cache_key = (points_key, k)

    if cache_key in _conflict_cache:
        return _conflict_cache[cache_key]

    n = len(points)
    h_conflicts = set()  # pairs that can't both be horizontal
    v_conflicts = set()  # pairs that can't both be vertical
    impossible_pairs = set()  # pairs that can't coexist

    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]

            # Check horizontal conflict
            h_conflict = (y1 == y2 and abs(x1 - x2) < 2 * k + 1)
            # Check vertical conflict
            v_conflict = (x1 == x2 and abs(y1 - y2) < 2 * k + 1)

            if h_conflict and v_conflict:
                impossible_pairs.add((i, j))
            elif h_conflict:
                h_conflicts.add((i, j))
            elif v_conflict:
                v_conflicts.add((i, j))

    result = (h_conflicts, v_conflicts, impossible_pairs)
    _conflict_cache[cache_key] = result
    return result


def can_place_fries(points, k):
    """Check if fries of half-length k can be placed on all points using DP"""
    n = len(points)

    if n > 22:  # For very large inputs, use greedy approach
        return can_place_fries_greedy(points, k)

    # Get cached conflicts
    h_conflicts, v_conflicts, impossible_pairs = get_conflicts_for_k(points, k)

    # If any impossible pairs exist, return False immediately
    if impossible_pairs:
        return False

    # Convert conflicts to bitmasks for faster checking
    h_conflict_masks = {}
    v_conflict_masks = {}

    for i, j in h_conflicts:
        if i not in h_conflict_masks:
            h_conflict_masks[i] = 0
        if j not in h_conflict_masks:
            h_conflict_masks[j] = 0
        h_conflict_masks[i] |= (1 << j)
        h_conflict_masks[j] |= (1 << i)

    for i, j in v_conflicts:
        if i not in v_conflict_masks:
            v_conflict_masks[i] = 0
        if j not in v_conflict_masks:
            v_conflict_masks[j] = 0
        v_conflict_masks[i] |= (1 << j)
        v_conflict_masks[j] |= (1 << i)

    # DP approach: try orientations more intelligently
    memo = {}

    def dp(pos, h_assigned, v_assigned):
        """DP function: pos=current position, h/v_assigned=bitmasks of assigned orientations"""
        if pos == n:
            return True

        state = (pos, h_assigned, v_assigned)
        if state in memo:
            return memo[state]

        # Try horizontal orientation
        can_horizontal = True
        if pos in h_conflict_masks:
            # Check if any conflicting point is already horizontal
            if h_conflict_masks[pos] & h_assigned:
                can_horizontal = False

        if can_horizontal:
            new_h = h_assigned | (1 << pos)
            if dp(pos + 1, new_h, v_assigned):
                memo[state] = True
                return True

        # Try vertical orientation
        can_vertical = True
        if pos in v_conflict_masks:
            # Check if any conflicting point is already vertical
            if v_conflict_masks[pos] & v_assigned:
                can_vertical = False

        if can_vertical:
            new_v = v_assigned | (1 << pos)
            if dp(pos + 1, h_assigned, new_v):
                memo[state] = True
                return True

        memo[state] = False
        return False

    return dp(0, 0, 0)


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


def find_max_k_divide_conquer(points, low, high, depth=0):
    """Divide and conquer approach to find maximum k"""
    # Base case
    if low > high:
        return low - 1

    # Avoid infinite recursion
    if depth > 30:
        return low

    # If range is small, use linear search
    if high - low <= 3:
        result = low - 1
        for k in range(low, high + 1):
            if can_place_fries(points, k):
                result = k
            else:
                break
        return result

    # Divide: find middle point
    mid = (low + high) // 2

    # Conquer: check if mid works
    if can_place_fries(points, mid):
        # If mid works, search in upper half
        return find_max_k_divide_conquer(points, mid + 1, high, depth + 1)
    else:
        # If mid doesn't work, search in lower half
        return find_max_k_divide_conquer(points, low, mid - 1, depth + 1)


def find_max_k(points):
    """Find the maximum k for which fries can be placed using divide-and-conquer"""
    n = len(points)

    # Cas 1: if only one point, infinite is possible
    if n <= 1:
        return "infini"

    # Cas 2: si k=0
    # Check if k=0 is possible
    if not can_place_fries(points, 0):
        return "0"

    # Calculate intelligent upper bound
    max_distance = 0
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]

            # Distance when points are on same line
            if x1 == x2:  # Same column
                max_distance = max(max_distance, abs(y1 - y2))
            elif y1 == y2:  # Same row
                max_distance = max(max_distance, abs(x1 - x2))

    # If no points share same row/column, infinite is possible
    if max_distance == 0:
        return "infini"

    # Set reasonable upper bound
    upper_bound = max_distance // 2 + 1

    # Check if infinite is possible
    if can_place_fries(points, upper_bound):
        return "infini"

    # Use divide and conquer to find maximum k
    result = find_max_k_divide_conquer(points, 0, upper_bound)

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
