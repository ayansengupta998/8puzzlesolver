import sys
import puzz
import pdqpq
import random



MAX_SEARCH_ITERS = 100000
GOAL_STATE = puzz.EightPuzzleBoard("012345678")
results = {'path' : [],
               'path_cost':0,
               'frontier_count': 0,
               'expanded_count': 0,
    
    }


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
    elif strategy == "astar-h1":
        results = astar_h1(start_state)
    elif strategy == "astar-h2":
        results = astar_h2(start_state)
    elif strategy == "astar-h3":
        results = astar_h3(start_state)   
    
    
    return results
def bfs_search(start_state):
    
    frontier = []
    explored = []
    frontier.append(("start",start_state))
    if start_state == GOAL_STATE:#edge case to check if start state is the goal state 
        results['path'].append(("start",start_state))
        results['frontier_count'] = 1
        return results
    else:
        while len(frontier) != 0: #check if the frontier is empty 
            node = frontier.pop(0) #pop index 0 of the frontir because bfs uses FIFO strategy
            explored.append(node)#add popped node to explored list
            results['path'].append(node) #add popped node to the path since it the node was taken next
            results['expanded_count'] = results['expanded_count'] +1 #increment expanded count by 1          
            # str_node = str(explored[-1][1])
            # index = str_node.find("0") #index of where the 0 appears
            succ = node[1].successors()#maintain a dictionary of all successors
            #now need to expand popped node 
            nextState_list = [(k,v) for k,v in succ.items()] #make a list of all  the possible successors
            # temp_next_state = str(nextState_list[0][1])
            # cost = int(temp_next_state[index])
            # results['path_cost'] = results['path_cost'] + (cost*cost)
            for i in nextState_list: #expand popped node
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
            #finding cost per move
            print(results)
            str_node = str(node[1])
            index = str_node.find("0")
            nxt_state = str(frontier[0][1])
            tile_movecost = int(nxt_state[index])
            results['path_cost'] = results['path_cost'] + (tile_movecost*tile_movecost)
        return results
            
def astar_h1(start_state):
    results = {'path' : [],
               'path_cost':0,
               'frontier_count': 0,
               'expanded_count': 0,
    }
    q =pdqpq.PriorityQueue()#define a priority queue q which is empty
    #define two sets, frontier and explored
    frontier = set()
    explored = []
    frontier.add(start_state)
    results['path'].append(('start',start_state))
    recurser(start_state, q, results, frontier, explored,'')
    results['frontier_count'] = len(frontier)
    results['expanded_count'] = len(explored)
    return results

def recurser(current_state, q, results, frontier, explored, move):
    if str(GOAL_STATE) == str(current_state) or (str(current_state) in explored and q.empty()):
        return
    if str(current_state) not in explored:
        explored.append(str(current_state))
        #explore the unexplored states
        successors = current_state.successors()
        for key in successors:
            #get each successor
            new_state = successors[key]
            if new_state not in frontier:
                h = heuristic(new_state, 1)
                g = cost(current_state, new_state)
                f = g + h
                #add every expanded state to the frontier
                frontier.add(new_state)
                q.add((new_state, key), f)
    print("Explored is", explored)
    print("Queue is ",q)
    results['path'].append((q.pq[0][2][1],q.pq[0][2][0]))
    moveCost = q.pq[0][0]
    results['path_cost'] += moveCost
    node = q.pop()
    recurser(node[0],q,results,frontier, explored,node[1])

def astar_h2(start_state):
    results = {'path' : [],
               'path_cost':0,
               'frontier_count': 0,
               'expanded_count': 0,
    
    }    
    q =pdqpq.PriorityQueue()
    heuristic(start_state, 2)

    return results

    
def astar_h3(start_state):
    results = {'path' : [],
               'path_cost':0,
               'frontier_count': 0,
               'expanded_count': 0,
    
    }    
    q =pdqpq.PriorityQueue()
    heuristic(start_state, 3)
    return results

#helper funciton to calculate the 3 different heuristics as selected
def heuristic(state, h):
    val = 0
    stateString = str(state)
    goalString = str(GOAL_STATE)
    if h == 1:
        #number of misplaced tiles
        for i in range(0,len(stateString)):
            if stateString[i] != goalString[i]:
                val+=1
    elif h == 2:
        #Manhattan distance
        for i in range(0,len(stateString)):
            tile = stateString[i]
            if stateString[i] != goalString[i]:
                x = state.find(tile)[0]
                y = state.find(tile)[1]
                xg= GOAL_STATE.find(tile)[0]
                yg = GOAL_STATE.find(tile)[1]
                val += abs(x-xg) + abs(y-yg)
    elif h == 3:
        #modified Manhattan distance
        for i in range(0,len(stateString)):
            tile = stateString[i]
            if stateString[i] != goalString[i]:
                x = state.find(tile)[0]
                y = state.find(tile)[1]
                xg= GOAL_STATE.find(tile)[0]
                yg = GOAL_STATE.find(tile)[1]
                val += (abs(x-xg) + abs(y-yg)) * (int(tile)**2)
    return val

def cost(current_state, next_state):
    current_stateString = str(current_state)
    next_stateString = str(next_state)
    for i in range(0,len(current_stateString)):
        if current_stateString[i] != next_stateString[i]:
            if int(current_stateString[i])>0:
                return int(current_stateString[i])**2
            else:
                return int(next_stateString[i])**2
    return 0


            
            

                    
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

