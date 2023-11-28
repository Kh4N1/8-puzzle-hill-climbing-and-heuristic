import copy
import streamlit as st

def create_initial_state():
    initial_state = [[0] * 3 for _ in range(3)]
    index = 0
    for i in range(3):
        for j in range(3):
            num = st.number_input(f"Enter a number between 0 and 8 for z[{i},{j}]: ", min_value=0, max_value=8, key=f"num_{i}_{j}")
            if 0 <= num <= 8 and num not in initial_state:
                initial_state[i][j] = num
            else:
                st.error("❌Invalid input❌. Please enter a number between 0 and 8 for the next try! 👀")
                st.stop()
            index += 1
    return initial_state

def print_table(state):
    custom_css = """
           <style>
               .tabless {
                   text-align: center;
               }
               td, th {
                text-align: center;
            }
           </style>
       """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.table(state)

def heuristic_1(state, goal_state):
    count = sum(1 for i in range(3) for j in range(3) if state[i][j] != goal_state[i][j] and state[i][j] != 0)
    return count

def heuristic_2(state, goal_state):
    distance = sum(abs(row - i) + abs(col - j) for i in range(3) for j in range(3) if state[i][j] != 0
                   for row, col in [divmod(state[i][j] - 1, 3)])
    return distance

def generate_neighbors(current_state):
    neighbors = []
    zero_row, zero_col = next((i, j) for i, row in enumerate(current_state) for j, val in enumerate(row) if val == 0)
    for move in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        new_row, new_col = zero_row + move[0], zero_col + move[1]
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = copy.deepcopy(current_state)
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], \
                new_state[zero_row][zero_col]
            neighbors.append(new_state)
    return neighbors

def hill_climbing(state, heuristic, goal_state):
    current_state = state
    path = [current_state]
    moves = 0
    while True:
        neighbors = generate_neighbors(current_state)
        neighbor_scores = [(neighbor, heuristic(neighbor, goal_state)) for neighbor in neighbors]
        neighbor_scores.sort(key=lambda x: x[1])
        if neighbor_scores[0][1] >= heuristic(current_state, goal_state):
            break
        else:
            current_state = neighbor_scores[0][0]
            path.append(current_state)
            moves += 1
    return current_state, moves, path

def main():
    st.title("Puzzle Solver with hill climbing")
    st.header("Goal State:")
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    print_table(goal_state)

    st.header("Template Puzzle:")
    template_state = [["z[0,0]", "z[0,1]", "z[0,2]"], ["z[1,0]", "z[1,1]", "z[1,2]"], ["z[2,0]", "z[2,1]", "z[2,2]"]]
    print_table(template_state)

    st.write("\n---------------------------\n")
    st.header("Initial puzzle:")
    initial_state = create_initial_state()
    print_table(initial_state)
    initial_state_h1 = copy.deepcopy(initial_state)
    result_h1, moves_h1, path_h1 = hill_climbing(initial_state_h1, heuristic_1, goal_state)
    st.write("\n---------------------------\n")
    st.header("Results for h1 heuristic:")
    st.write("Final puzzle mode:")
    print_table(result_h1)
    st.write("Number of moves made:", moves_h1)
    st.write("Path:")
    for i, state in enumerate(path_h1):
        st.write(f"step {i}:")
        print_table(state)

    initial_state_h2 = copy.deepcopy(initial_state)
    result_h2, moves_h2, path_h2 = hill_climbing(initial_state_h2, heuristic_2, goal_state)
    st.write("\n---------------------------\n")
    st.header("Results for h2 heuristic:")
    st.write("Final puzzle mode:")
    print_table(result_h2)
    st.write("Number of moves made:", moves_h2)
    st.write("The path obtained:")
    for i, state in enumerate(path_h2):
        st.write(f"step {i}:")
        print_table(state)

if __name__ == "__main__":
    main()
