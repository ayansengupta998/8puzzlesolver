import sys
import puzz
import pdqpq
import random
from goto import goto, comefrom, label


MAX_SEARCH_ITERS = 100000
GOAL_STATE = puzz.EightPuzzleBoard("012345678")


def solve_puzzle(start_state, strategy):
    """Perform a search to find a solution to a puzzle.
    
    Args:
        start_state: an EightPuzzleBoard object indicating the start state for the search
        flavor: a string indicating which type of search to run.  Can be one of the following:
            'bfs' - breadth-first search
            'ucost' - uniform-cost search
            'greedy-h1' - Greedy best-first search using a misplaced tile count heuristic
            'greedy-h2' - Greedy best-first search using a Manhattan distance heuristic
            'greedy-h3' - Greedy best-first search using a weighted Manhattan distance heuristic
            'astar-h1' - A* search using a misplaced tile count heuristic
            'astar-h2' - A* search using a Manhattan distance heuristic
            'astar-h3' - A* search using a weighted Manhattan distance heuristic
    
    Returns: 
        A dictionary containing describing the search performed, containing the following entries:
            'path' - a list of 2-tuples representing the path from the start state to the goal state 
                (both should be included), with each entry being a (str, EightPuzzleBoard) pair 
                indicating the move and resulting state for each action.  Omitted if the search 
                fails.
            'path_cost' - the total cost of the path, taking into account the costs associated 
                with each state transition.  Omitted if the search fails.
            'frontier_count' - the number of unique states added to the search frontier at any
                point during the search.
            'expanded_count' - the number of unique states removed from the frontier and expanded 
                (successors generated).
    """
    
    if(strategy == "bfs"):
        results = bfs_search(start_state)

    
    
    return results
def bfs_search(start_state):
    results = {'path' : [],
               'path_cost':0,
               'frontier_count': 0,
               'expanded_count': 0,
    
    }
    frontier = []
    # frontier.append(start_state)
    explored = []
    frontier.append(("start",start_state))
    results['path_cost'] = 0
    results['frontier_count'] = 1
    if start_state == GOAL_STATE:
        return results
    else:
        while len(frontier) != 0: #check if the frontier is empty 
            node = frontier.pop(0) #pop index 0 of the frontir because bfs uses FIFO strategy
            explored.append(node)#add popped node to explored list
            results['path'].append(node)
            results['expanded_count'] = results['expanded_count'] +1 #increment expanded count by 1 
            if(len(frontier)==0):
                goto expand
            str_node = str(node[1])
            index = str_node.find("0") #index of where the 0 appears
            succ = node[1].successors()#maintain a dictionary of all successors
            #now need to expand popped node 
            nextState_list = [(k,v) for k,v in succ.items()] #make a list of all  the possible successors
            random.shuffle(nextState_list)#randomize the order 
            temp_next_state = str(frontier[0][1])
            cost = int(temp_next_state[index])
            results['path_cost'] = results['path_cost'] + (cost*cost)
            label .expand
            for i in nextState_list:
                if(i not in frontier) and (i not in explored):
                    if(i[1] == GOAL_STATE):
                        results['path'].append(i)
                        node_str = str(node[1])
                        print(node_str)
                        char = node_str.find("0")
                        print(char)
                        temp_state = str(i[1])
                        print(temp_state)
                        tile_number = int(temp_state[char])
                        results['path_cost'] = results['path_cost'] + (tile_number*tile_number)
                        return results
                    else:
                        frontier.append(i)
                        results["frontier_count"] = results["frontier_count"] + 1

                    
def print_summary(results):
    if 'path' in results:
        print("found solution of length {}, cost {}".format(len(results['path']), 
                                                            results['path_cost']))
        for move, state in results['path']:
            print("  {:5} {}".format(move, state))
    else:
        print("no solution found")
    print("{} states placed on frontier, {} states expanded".format(results['frontier_count'], 
                                                                    results['expanded_count']))


############################################

if __name__ == '__main__':

    start = puzz.EightPuzzleBoard(sys.argv[1])
    method = sys.argv[2]

    print("solving puzzle {} -> {}".format(start, GOAL_STATE))
    results = solve_puzzle(start, method)
    print_summary(results)

