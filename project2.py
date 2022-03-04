# ENPM661 Project2 Dijkstra Algorithm Implementation
import numpy as np
import cv2 as cv
import math
import copy

# function for calculate linear equation
def linear_eq(i,j,x1,y1,x2,y2):
    f = ((y2-y1)/(x2-x1))*(i-x1) + y1 - j
    return f

# function for backtrack optimal route
def backtrack(closed_list):
    route = [goal_node]
    while True:
        parent = copy.deepcopy(closed_list[route[0]][1])
        if parent == None:
            break
        else:
            route.insert(0,parent)
    return route

# function for getting priority queue
def get_priority(open_list):
    min = math.inf
    min_node = None
    for node in open_list:
        if open_list[node][0] < min:
            min = copy.deepcopy(open_list[node][0])
            min_node = node
    return min_node    

# functions for all 8 actions
def ActionMoveUp(current_node):
    i = copy.deepcopy(current_node[0])
    j = copy.deepcopy(current_node[1])
    if j==map.shape[0]-1:
        status = False
        next_node = (i,j)
    else:
        if any(map[j+1,i]!=obstracle_cspace): 
            status = True
            next_node = (i,j+1)
        else:
            status = False
            next_node = (i,j)
    return [status,next_node]

def ActionMoveDown(current_node):
    i = copy.deepcopy(current_node[0])
    j = copy.deepcopy(current_node[1])
    if j==0:
        status = False
        next_node = (i,j)
    else:
        if any(map[j-1,i]!=obstracle_cspace): 
            status = True
            next_node = (i,j-1)
        else:
            status = False
            next_node = (i,j)
    return [status,next_node]

def ActionMoveLeft(current_node):
    i = copy.deepcopy(current_node[0])
    j = copy.deepcopy(current_node[1])
    if i==0:
        status = False
        next_node = (i,j)
    else:
        if any(map[j,i-1]!=obstracle_cspace): 
            status = True
            next_node = (i-1,j)
        else:
            status = False
            next_node = (i,j)
    return [status,next_node]

def ActionMoveRight(current_node):
    i = copy.deepcopy(current_node[0])
    j = copy.deepcopy(current_node[1])
    if i==map.shape[1]-1:
        status = False
        next_node = (i,j)
    else:
        if any(map[j,i+1]!=obstracle_cspace): 
            status = True
            next_node = (i+1,j)
        else:
            status = False
            next_node = (i,j)
    return [status,next_node]

def ActionMoveUpRight(current_node):
    i = copy.deepcopy(current_node[0])
    j = copy.deepcopy(current_node[1])
    if (j==map.shape[0]-1) or (i==map.shape[1]-1):
        status = False
        next_node = (i,j)
    else:
        if any(map[j+1,i+1]!=obstracle_cspace): 
            status = True
            next_node = (i+1,j+1)
        else:
            status = False
            next_node = (i,j)
    return [status,next_node]

def ActionMoveUpLeft(current_node):
    i = copy.deepcopy(current_node[0])
    j = copy.deepcopy(current_node[1])
    if (j==map.shape[0]-1) or (i==0):
        status = False
        next_node = (i,j)
    else:
        if any(map[j+1,i-1]!=obstracle_cspace): 
            status = True
            next_node = (i-1,j+1)
        else:
            status = False
            next_node = (i,j)
    return [status,next_node]

def ActionMoveDownLeft(current_node):
    i = copy.deepcopy(current_node[0])
    j = copy.deepcopy(current_node[1])
    if (j==0) or (i==0):
        status = False
        next_node = (i,j)
    else:
        if any(map[j-1,i-1]!=obstracle_cspace): 
            status = True
            next_node = (i-1,j-1)
        else:
            status = False
            next_node = (i,j)
    return [status,next_node]

def ActionMoveDownRight(current_node):
    i = copy.deepcopy(current_node[0])
    j = copy.deepcopy(current_node[1])
    if (j==0) or (i==map.shape[1]-1):
        status = False
        next_node = (i,j)
    else:
        if any(map[j-1,i+1]!=obstracle_cspace): 
            status = True
            next_node = (i+1,j-1)
        else:
            status = False
            next_node = (i,j)
    return [status,next_node]

# define colors of obstracles
clearance = 5
obstracle = (255,0,0)
obstracle_cspace = (0,255,0)
visited = (255,255,255)

# initialize map
map = np.zeros((250,400,3))

# create obstracles
for i in range(map.shape[1]): # x-axis
    for j in range(map.shape[0]): # y-axis
        # circle obstracle
        if (i-300)**2 + (j-185)**2 - (40)**2 <= 0 :
            map[j,i] = obstracle
        # V obstracle
        V1 = linear_eq(i,j,*(36,185),*(105,100)) <= 0 and linear_eq(i,j,*(105,100),*(80,180)) >= 0 and linear_eq(i,j,*(80,180),*(36,185)) >= 0
        V2 = linear_eq(i,j,*(36,185),*(80,180),) <= 0 and linear_eq(i,j,*(80,180),*(115,210)) <= 0 and linear_eq(i,j,*(115,210),*(36,185)) >= 0
        if V1 or V2:
            map[j,i] = obstracle
        # hexagon obstracle
        if (linear_eq(i,j,*(200,60),*(235,80)) <= 0 and i<235 and linear_eq(i,j,*(235,120),*(200,140)) >= 0
            and linear_eq(i,j,*(200,140),*(165,120)) >=0 and i>165 and linear_eq(i,j,*(165,80),*(200,60)) <=0):
            map[j,i] = obstracle 

# display map with original obstracles            
map = cv.flip(map,0)
cv.imshow('map',map)
cv.waitKey(1000) 
map = cv.flip(map,0)

# inflate obstracles with circle of radius=5
for i in range(map.shape[1]): # x-axis
    for j in range(map.shape[0]): # y-axis
        if all(map[j,i] == obstracle):
            cv.circle(map, (i,j), clearance, obstracle_cspace, -1)
            
# get start and goal node from user input
while True:
    x_start, y_start = input("Input start node (x_start, y_start) seperated by space : ").split()
    x_goal, y_goal = input("Input goal node (x_goal, y_goal) seperated by space : ").split()
    x_start, y_start = int(x_start), int(y_start)
    x_goal, y_goal = int(x_goal), int(y_goal)
    if (x_start>=map.shape[1] or x_start<0 or y_start>=map.shape[0] or y_start<0) and (x_goal>=map.shape[1] or x_goal<0 or y_goal>=map.shape[0] or y_goal<0):
        print('Both start and goal node is in out of map, please try again')
    elif (x_start>=map.shape[1] or x_start<0 or y_start>=map.shape[0] or y_start<0) and not (x_goal>=map.shape[1] or x_goal<0 or y_goal>=map.shape[0] or y_goal<0):
        print('Start node is in out of map, please try again')
    elif not (x_start>=map.shape[1] or x_start<0 or y_start>=map.shape[0] or y_start<0) and (x_goal>=map.shape[1] or x_goal<0 or y_goal>=map.shape[0] or y_goal<0):
        print('Goal node is in out of map, please try again')
    elif all(map[y_start,x_start]==obstracle_cspace) and any(map[y_goal,x_goal]!=obstracle_cspace):
        print('Start node is in obstracle, please try again')
    elif any(map[y_start,x_start]!=obstracle_cspace) and all(map[y_goal,x_goal]==obstracle_cspace):
        print('Goal node is in obstracle, please try again')
    elif all(map[y_start,x_start]==obstracle_cspace) and all(map[y_goal,x_goal]==obstracle_cspace):
        print('Both start and goal node is in obstracle, please try again')
    else:
        break      
        
# initialize lists and points for Dijkstra
start_node = (x_start,y_start)
goal_node = (x_goal,y_goal)
open_list = {} # dictionary format (x,y):[C2C,parent] 
open_list[start_node] = [0, None]
closed_list = {} # dictionary format (x,y):[C2C,parent] 

# Dijskstra algorithm
while open_list != {}:
    # pop node with minimum C2C from open list, set as current node, and add to closed list
    current_node = get_priority(open_list)
    current_c2c = copy.deepcopy(open_list[current_node][0])
    closed_list[current_node] = open_list.pop(current_node)
    map[current_node[1],current_node[0]] = visited
    # check if current node is goal node
    if current_node == goal_node:
        route = backtrack(closed_list)
        print('Success')
        # plot optimal route  
        for node in route:
            map[node[1],node[0]] = (0,0,255) 
            map = cv.flip(map,0)             
            cv.imshow('map',map)
            cv.waitKey(10) 
            map = cv.flip(map,0)
        # display final map
        map = cv.flip(map,0)
        cv.imshow('map',map)
        cv.waitKey(0) 
        break
    # visit surrounding nodes and update their C2C, add them to open list if not already there
    else:
        up_empty, up_node = ActionMoveUp(current_node)
        upright_empty, upright_node = ActionMoveUpRight(current_node)
        right_empty, right_node = ActionMoveRight(current_node)
        downright_empty, downright_node = ActionMoveDownRight(current_node)
        down_empty, down_node = ActionMoveDown(current_node)
        downleft_empty, downleft_node = ActionMoveDownLeft(current_node)
        left_empty, left_node = ActionMoveLeft(current_node)
        upleft_empty, upleft_node = ActionMoveUpLeft(current_node)
        # check up node
        if (up_empty == True) and (up_node not in closed_list):
            if up_node not in open_list:
                open_list[up_node] = [current_c2c+1, current_node]
            else:
                if open_list[up_node][0] > current_c2c+1:
                    open_list[up_node] = [current_c2c+1,current_node]
        # check up-right node
        if (upright_empty == True) and (upright_node not in closed_list):
            if upright_node not in open_list:
                open_list[upright_node] = [current_c2c+1.4, current_node]
            else:
                if open_list[upright_node][0] > current_c2c+1.4:
                    open_list[upright_node] = [current_c2c+1.4,current_node]
        # check right node
        if (right_empty == True) and (right_node not in closed_list):
            if right_node not in open_list:
                open_list[right_node] = [current_c2c+1, current_node]
            else:
                if open_list[right_node][0] > current_c2c+1:
                    open_list[right_node] = [current_c2c+1,current_node]    
        # check down-right node
        if (downright_empty == True) and (downright_node not in closed_list):
            if downright_node not in open_list:
                open_list[downright_node] = [current_c2c+1.4, current_node]
            else:
                if open_list[downright_node][0] > current_c2c+1.4:
                    open_list[downright_node] = [current_c2c+1.4,current_node]  
        # check down node
        if (down_empty == True) and (down_node not in closed_list):
            if down_node not in open_list:
                open_list[down_node] = [current_c2c+1, current_node]
            else:
                if open_list[down_node][0] > current_c2c+1:
                    open_list[down_node] = [current_c2c+1,current_node]      
        # check down-left node
        if (downleft_empty == True) and (downleft_node not in closed_list):
            if downleft_node not in open_list:
                open_list[downleft_node] = [current_c2c+1.4, current_node]
            else:
                if open_list[downleft_node][0] > current_c2c+1.4:
                    open_list[downleft_node] = [current_c2c+1.4,current_node]   
        # check left node
        if (left_empty == True) and (left_node not in closed_list):
            if left_node not in open_list:
                open_list[left_node] = [current_c2c+1, current_node]
            else:
                if open_list[left_node][0] > current_c2c+1:
                    open_list[left_node] = [current_c2c+1,current_node]                     
        # check up-left node
        if (upleft_empty == True) and (upleft_node not in closed_list):
            if upleft_node not in open_list:
                open_list[upleft_node] = [current_c2c+1.4, current_node]
            else:
                if open_list[upleft_node][0] > current_c2c+1.4:
                    open_list[upleft_node] = [current_c2c+1.4,current_node]
                
    # display current map
    cv.circle(map, start_node, 5, (0,0,255), -1)
    cv.circle(map, goal_node, 5, (0,0,255), -1)
    map = cv.flip(map,0)               
    cv.imshow('map',map)
    cv.waitKey(1) 
    map = cv.flip(map,0)
else:
    print('Failure') 

