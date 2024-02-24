from collections import deque

def find_paths(n):
    start = (0, 0, 0, 1)  # (x, y, direction, rotation_count)
    visited = set([(0, 0, 0, 1)])
    queue = deque([start])
    paths = []

    while queue:
        x, y, direction, rotation_count = queue.popleft()

        if rotation_count == n:
            paths.append((x, y, direction))
            continue

        # 우회전
        new_direction_r = (direction + 1) % 4
        new_position_r = (x, y, new_direction_r, rotation_count + 1)
        if new_position_r not in visited:
            queue.append(new_position_r)
            visited.add(new_position_r)

        # 좌회전
        new_direction_l = (direction - 1) % 4
        new_position_l = (x, y, new_direction_l, rotation_count + 1)
        if new_position_l not in visited:
            queue.append(new_position_l)
            visited.add(new_position_l)

    return paths

def main():
    for z in range(3):
        
        paths = find_paths(z)
        unique_paths = set(paths)

        print(f"Number of unique paths for n={z}: {len(unique_paths)}")
        print("Paths:", unique_paths)

if __name__ == "__main__":
    main()
