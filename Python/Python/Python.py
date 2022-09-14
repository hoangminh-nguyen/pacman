import operator as op
import copy
import numpy as np
import random
class Agent:
    def __init__(self):
        self.returnedPath = []
        self.score = 0
        self.curPos = ()
        self.startPos =()
        
        
class Game:
    def __init__(self):
        self.map = []
        self.mazeSize = (0,0)
        self.pacman = Agent()
        self.ghosts = []
        self.foods = []
        self.level = 0
        
    def ReadInput(self):
        inputPath = input("Enter input file path: ")
        self.level = int(input("Level: "))
        f = None
        try:
            f = open(inputPath, 'r')
        except IOError:
            print("Couldn't open the file")
            return False
        else:
            # First line is size of maze
            self.mazeSize = tuple(int(i) for i in f.readline().split())
            print("maze size: " + str(self.mazeSize))

            # Next lines are graph info
            for i in range(0, self.mazeSize[0]):
                self.map.append(f.readline().split())
#             print("map: " + str(self.map))
            
            # Last line is pacman init pos
            self.pacman.curPos = tuple(int(i) for i in f.readline().split())
            
            # 
            for i in range(self.mazeSize[0]):
#                 print("i: " + str(i))
                for j in range(self.mazeSize[1]):
#                     print("j: " + str(j))
#                     if (self.map[i][j] == "0"): # blank
#                     if (self.map[i][j] == "1"): # wall
                    if (self.map[i][j] == '2'): # food
#                         print("debug")
                        self.foods.append((i,j))
                        
                    elif (self.map[i][j] == '3'): # ghost
                        self.ghosts.append(Agent())
                        self.ghosts[-1].curPos = (i,j) 
                        self.ghosts[-1].startPos = (i,j) 
        finally:
            if f: 
                f.close()
                return True
              
    def GenerateSuccessors(self,map, i, j):
        legalPos = []
        if (self.level == 4) or (self.level == 3):
            legalPos = ["0", "2", "3"]
        else: # level 1, 2
            legalPos = ["0", "2"]

        successors = []
        
        #level 3 nha 
        # map = blindmap
        if self.level == 3:
            #print("helooo")
            if i+1 < len(map) and map[i+1][j][0] in [0,2,3] and map[i+1][j][1] == 1:
                successors.append((i+1, j))
            if i > 0 and map[i-1][j][0] in [0,2,3] and map[i-1][j][1] == 1:
                successors.append((i-1, j))
            if j+1 < len(map[0]) and map[i][j+1][0] in [0,2,3] and map[i][j+1][1] == 1:
                successors.append((i, j+1))
            if j > 0 and map[i][j-1][0] in [0,2,3] and map[i][j-1][1] == 1: 
                successors.append((i, j-1))
                        
        else:
#         print("GenerateS: " + str((i,j)))
            if i+1 < self.mazeSize[0] and self.map[i+1][j] in legalPos:
                successors.append((i+1, j))
            if i > 0 and self.map[i-1][j] in legalPos:
                successors.append((i-1, j))
            if j+1 < self.mazeSize[1] and self.map[i][j+1] in legalPos:
                successors.append((i, j+1))
            if j > 0 and self.map[i][j-1] in legalPos:
                successors.append((i, j-1))
        
        return successors
    
    def ManhattanDis(self, x, y):
        return abs(x[0]-y[0]) + abs(x[1] - y[1])
    
    def A_Start_Graph_Search(self, map, goal, state):
        if (state==goal):
            return []
        frontier=[[state,-1,self.ManhattanDis(goal,state),0,self.ManhattanDis(goal,state)]] #[node,father,f(n),g(n),h(n)]
        expanded_node=[]
        while(frontier):
            node=frontier.pop(0)
            expanded_node.append(node)
            
            if node[0] == goal:
                path_returned=self.return_path(expanded_node)
                return path_returned
            for x in self.GenerateSuccessors(map ,node[0][0], node[0][1]):
                if self.check_Existed(frontier,x)==False and self.check_Existed(expanded_node,x)==False:
                    frontier.append([x,node[0],self.ManhattanDis(x,goal) +node[3]+1,node[3]+1,self.ManhattanDis(x,goal)]) #[node,father,f(n),g(n),h(n)]
#               
                    frontier.sort(key=op.itemgetter(2))
                    continue
                if self.check_Existed(frontier,x)==True:
                    for y in frontier:
                        if y[0]==x and y[2]>node[2]+1:
                            frontier.pop(frontier.index(y))
                            frontier.append([x,node[0],self.ManhattanDis(x,goal)+node[3]+1,node[3]+1,self.ManhattanDis(x,goal)])
                            frontier.sort(key=op.itemgetter(2))
                            break
        return []
                
    def myFunc(self, e):
        return e[2]

    def sort(self, a):
        for x in range(len(a)-1):
            for y in range(x+1,len(a)):
                if a[x][2]>a[y][2]:
                    b=a[x]
                    a[x]=a[y]
                    a[y]=b
        for x in range(len(a)-1):
            for y in range(x+1,len(a)):
                if a[x][2]==a[y][2] and a[x][0]>a[y][0]:
                    b=a[x]
                    a[x]=a[y]
                    a[y]=b
        return a

    def check_Existed(self, listt,x):
#         print("listt:" + str(listt))
        for y in listt:
            if x==y[0]:
                return True
        return False
    
    def return_path(self, explorded):
        path = []
        current = explorded[-1]
        while(current[1] != -1):
            path.insert(0, current[0])
            for i in explorded:
                if i[0] == current[1]:
                    current = i
                    break
        path.insert(0, current[0])
        return path

    def ToAnim(self): # For animation
        # pacman path        
        pacmanPath = self.GetDirectionPath(self.pacman.returnedPath)                    
                   
        # ghosts path
        ghostsPaths = [" ".join(self.GetDirectionPath(a.returnedPath)) for a in self.ghosts]
        
        # Save file
        #  First line is pacman path
        f = open('path.txt','w')
        f.write(" ".join(pacmanPath) + "\n")
        
        #  Next line is the number of ghosts
        f.write(str(len(self.ghosts))+ "\n")
        
        #  Next lines is ghosts paths 
        for i in pacmanPath:
            print(i, end=" ")
        print(ghostsPaths)
        for path in ghostsPaths:
            f.write(path + "\n")
                            
        f.close()
        
    def GetDirectionPath(self, returnedPath):
        path = []
        curPos = returnedPath[0]
        
        for a in returnedPath[1:]:
            if (a[0] > curPos[0]):
                path.append("D")
            elif ((a[0] < curPos[0])):
                path.append("U")
            elif ((a[1] < curPos[1])):
                path.append("L")    
            elif ((a[1] > curPos[1])):
                path.append("R")
            curPos = a 
        
        return path
    #----------------------------------------------------------LEVEL3--------------------------------------------------------
    def level_three(self):
        # khoi tao
        Blindmap=[[[0,0] for _ in range(self.mazeSize[1])] for _ in range(self.mazeSize[0])]
        self.pacman.returnedPath.append(self.pacman.curPos)
        for a in range(len(self.ghosts)):
            self.ghosts[a].returnedPath.append(self.ghosts[a].startPos)
        dem = 250
        dangerous_step, dangerous_zone,memory_food = [],[],[]
        check_loop = 0
        temp_wall = []
        cell = (0,0)
        flag = 3
        while(dem):
            self.look_around(Blindmap, memory_food)
            dangerous_step = self.dangerous_step(Blindmap, dangerous_zone) #nhung o quai vat co the vao
            self.setWall(Blindmap, dangerous_zone, temp_wall,flag)

            moveF = []
            close_food = self.look_closestfood_in_range(Blindmap)
            unexplorded_cell = self.find_unexplorded(Blindmap)

            if close_food: #có đồ ăn trong tầm nhìn
                moveF = self.find_min_distance(Blindmap, close_food)
            if memory_food and moveF==[]: #có đồ ăn trong trí nhớ
                moveF = self.find_min_distance(Blindmap, memory_food)
            if unexplorded_cell and moveF==[]: #còn ô chưa khám phá
                moveF = self.find_min_distance(Blindmap, unexplorded_cell)
            
            

            if (moveF and cell != moveF[0]):# kiem tra neu di qua lai quai ma khong thoat ra duoc thi tưởng tượng đó là bức tường r đi đường khác
                check_loop +=1
                if check_loop == 2:
                    Blindmap[cell[0]][cell[1]][0] = 1
                    temp_wall.append(cell)
                    check_loop = 0
            print(moveF)
            if moveF:
                cell = moveF[1]
                moveF = moveF[1]
            
            
            if moveF in dangerous_step and moveF in dangerous_zone:
                a = [x for x in self.GenerateSuccessors(Blindmap, self.pacman.curPos[0],self.pacman.curPos[1]) if x not in dangerous_step]
                if a == []:
                    return
                moveF = random.choice(a)

            if moveF == []:#het duong dau hang
                if flag:
                    print("break")
                    self.break_wall(Blindmap,temp_wall,memory_food)
                    flag-=1
                    continue
                else:
                    return
                
            self.pacman.curPos = tuple(moveF)
            self.monster_step()

            #kiem tra co dung quai vat khong
            for i in range(len(self.ghosts)):
                if self.pacman.curPos == self.ghosts[i].curPos:
                    self.pacman.returnedPath.append(self.pacman.curPos)
                    return

            #xoa food sau khi an
            if(self.pacman.curPos in self.foods):
                self.map[self.pacman.curPos[0]][self.pacman.curPos[1]] = '0'
                Blindmap[self.pacman.curPos[0]][self.pacman.curPos[1]][0] = 0
                for i in self.foods:
                    if i == (self.pacman.curPos[0],self.pacman.curPos[1]):
                        self.foods.remove(i)
                for i in memory_food:
                    if i[0] == self.pacman.curPos[0] and i[1] == self.pacman.curPos[1]:
                        memory_food.remove(i)

            self.pacman.returnedPath.append(self.pacman.curPos)
            dem-=1
      
    def dangerous_step(self, Blindmap, dangerous_zone):
        suc = []
        x = self.pacman.curPos[0]-3
        y = self.pacman.curPos[1]-3
        for i in range(7):
            for j in range(7):
                if (x+i) >= 0 and (y+j) >= 0 and (x+i) < len(Blindmap) and (y+j) < len(Blindmap[0]):
                    if Blindmap[x+i][y+j][0] == 3:
                        if (x+i, y+j) not in dangerous_zone:
                            dangerous_zone.append((x+i, y+j))
                        suc.append((x+i, y+j))
                        suc += self.GenerateSuccessors(Blindmap, x+i, y+j)
        #return list of tuple  
        return suc

    def setWall(self, Blindmap, dangerous_zone, temp_wall, flag):
        if flag == 3:
            for x in dangerous_zone:
                Blindmap[x[0]][x[1]][0] = 1
                if x not in temp_wall:
                    temp_wall.append(x)
        else:
            for x in temp_wall:
                Blindmap[x[0]][x[1]][0] = 1

    def break_wall(self, Blindmap, temp_wall, memory_food):
        for x in temp_wall:
            Blindmap[x[0]][x[1]][0] = 0
        for x in memory_food:
            Blindmap[x[0]][x[1]][0] = 2
        temp_wall.clear()

    def monster_step(self):
        oldposition = []
        for a in range(len(self.ghosts)):
            step = []
            i = self.ghosts[a].curPos[0]
            j = self.ghosts[a].curPos[1]
            oldposition.append([i,j])
            starti = lambda x : abs(x-self.ghosts[a].startPos[0])
            startj = lambda y : abs(y-self.ghosts[a].startPos[1])
            if i+1 < self.mazeSize[0] and (starti(i+1) + startj(j)) <= 1 and self.map[i+1][j] in ['0','2','3']:
                step.append((i+1, j))
            if i > 0 and (starti(i-1)+ startj(j)) <= 1 and self.map[i-1][j] in ['0','2','3']:
                step.append((i-1, j))
            if j+1 < self.mazeSize[1] and (starti(i) + startj(j+1)) <= 1 and self.map[i][j+1] in ['0','2','3']:
                step.append((i, j+1))
            if j > 0 and (starti(i) +startj(j-1)) <= 1 and self.map[i][j-1] in ['0','2','3']:
                step.append((i, j-1)) 
            self.ghosts[a].curPos = random.choice(step)
        #xoa quai vat khoi vi tri cu
        for a in range(len(self.ghosts)):
            self.map[oldposition[a][0]][oldposition[a][1]] = '0'
        #them quai vat vao vi tri moi
        for a in range(len(self.ghosts)):
            self.map[self.ghosts[a].curPos[0]][self.ghosts[a].curPos[1]] = '3'
            self.ghosts[a].returnedPath.append(self.ghosts[a].curPos)
        #them thuc an vao vi tri cu trong map, vi hoi nay bi quai vat de len
        for a in range(len(self.foods)):
            self.map[self.foods[a][0]][self.foods[a][1]] = '2'

    def find_unexplorded(self, Blindmap):
        unexplorded_cell=[]
        for i in range(len(Blindmap)):
            for j in range(len(Blindmap[0])):
                if Blindmap[i][j][1] == 1:
                    a = 0
                    if i+1 < len(Blindmap) and Blindmap[i+1][j][1] == 0:
                        a = 1
                    if i > 0 and Blindmap[i-1][j][1] == 0:
                        a = 1
                    if j+1 < len(Blindmap[0]) and Blindmap[i][j+1][1] == 0:
                        a = 1
                    if j > 0 and Blindmap[i][j-1][1] == 0: 
                        a = 1
                    if (a == 1): 
                        unexplorded_cell.append([i,j])
        return unexplorded_cell                          
                
    def look_monster_in_range(self, map):
        x = self.pacman.curPos[0]-3
        y = self.pacman.curPos[1]-3
        monster = []
        for i in range(7):
            for j in range(7):
                if (x+i) >= 0 and (y+j) >= 0 and (x+i) < len(map) and (y+j) < len(map[0]):
                    if (map[x+i][y+j] == '3'):
                        monster.append([x+i,y+j])
        return monster
    
    def look_around(self, Blindmap, memory_food):
        x = self.pacman.curPos[0]-3
        y = self.pacman.curPos[1]-3
        for i in range(7):
            for j in range(7):
                if (x+i) >= 0 and (y+j) >= 0 and (x+i) < len(Blindmap) and (y+j) < len(Blindmap[0]):
                    if Blindmap[x+i][y+j][1] == 0:
                        Blindmap[x+i][y+j][1] = 1
                    Blindmap[x+i][y+j][0] = int(self.map[x+i][y+j])
                    if Blindmap[x+i][y+j][0] == 2 and [x+i,y+j] not in memory_food:
                        memory_food.append([x+i,y+j])
    
    def look_closestfood_in_range(self, Blindmap):
        food_in_range=[]
        x = self.pacman.curPos[0]-3
        y = self.pacman.curPos[1]-3
        for i in range(7):
            for j in range(7):
                if (x+i) >= 0 and (y+j) >= 0 and (x+i) < len(Blindmap) and (y+j) < len(Blindmap[0]):
                    if Blindmap[x+i][y+j][0] == 2:
                        food_in_range.append([x+i, y+j])
        return food_in_range
    
    def find_min_distance(self, Blindmap, listPosition):
        lenpath = []
        for i in range(len(listPosition)):
            lenpath.append(len(self.A_Start_Graph_Search(Blindmap,tuple(listPosition[i]), self.pacman.curPos))) 
        minpath=0
        for i in range(len(lenpath)):
            if lenpath[i] == 0:
                continue
            elif lenpath[i]!=0:
                minpath=i
                for j in range(i, len(lenpath)):
                    if lenpath[j]<lenpath[minpath] and lenpath[j]!=0:
                        minpath=j
                break
        a = self.A_Start_Graph_Search(Blindmap,tuple(listPosition[minpath]), self.pacman.curPos)
        return a
    
    def Run(self):
        # LEVEL 1
        if (self.level == 1):            
            result = self.A_Start_Graph_Search(self.map, self.foods[0], tuple(self.pacman.curPos))
 #           result = self.A_Start_Graph_Search([], [], [])
#             print(result[0])
            print(result)
            self.pacman.returnedPath = result
        
        
        if (self.level == 3):
            self.level_three()
        # LEVEL 4
        if (self.level == 4):
            pacmanPath = []
            ghostPaths = [[] for _ in range(len(self.ghosts))]
            depth = [10,0]
            gameState = {}
            gameState['map'] = self.map
            gameState['pacmanPos'] = self.pacman.curPos
            gameState['ghostsPos'] = [ghost.curPos for ghost in self.ghosts]
            gameState['gameScore'] = 0
            gameState['nFoods'] = len(self.foods)
            
#             miniMaxValue, pacmanPath, ghostPaths, currentGameState = self.MiniMax(0, depth, gameState, pacmanPath, ghostPaths)
#             
            
            count = 0
            while (True):
                miniMaxValue, pacmanPathTmp, ghostPathsTmp, gameState = self.MiniMax(0, [10,0], gameState, [], [[] for _ in range(len(self.ghosts))], -999999, 999999) 
                if len(pacmanPath) == 0:
                    pacmanPath += pacmanPathTmp
                else: 
                    pacmanPath += pacmanPathTmp[1::]
                for i in range(len(self.ghosts)):
                    if len(ghostPaths[i]) == 0:
                        ghostPaths[i] += ghostPathsTmp[i]
                    else:
                        ghostPaths[i] += ghostPathsTmp[i][1::]
                    
                count +=1
                print("COUNT: " + str(count))
#                 if (count == 3):
#                     break
                
                if self.IsLose(gameState) or self.IsWin(gameState):
                    break
            
            print("COUNT: " + str(count))
            print(miniMaxValue)
            print(pacmanPath)
            print(ghostPaths)
            print(gameState)
            
            self.pacman.returnedPath = pacmanPath
            for i in range(len(self.ghosts)):
                self.ghosts[i].returnedPath = ghostPaths[i]            
    
    
    #----------------------------------------------------------LEVEL4--------------------------------------------------------
    def MiniMax(self, agent, depth, gameState, pacmanPath, ghostPaths, alpha, beta):
        '''
        agent: (int) turn of Pacman or ghost  
        Each node in the search tree has its own game state
        gameState: a dict containing 2d array map of current game state, where is the left foods, current pos of pacman and ghosts)
        gameState = {"map": [a 2d array map], "pacmanPos": (x,y), "ghostsPos": [(x,y)] "gameScore": int, "nFoods": int}
        depth = [depthLimit, currentDepth]            
        '''
        if self.IsLose(gameState) or self.IsWin(gameState) or depth[0] == depth[1]:           
#             print("pacmanPath before insert:" + str(pacmanPath))
            pacmanPath.insert(0, gameState['pacmanPos'])
#             print("pacmanPath after insert:" + str(pacmanPath))
#             print("pacmanPath at stop:" + str(pacmanPath))           
            for i in range(len(self.ghosts)):        
                ghostPaths[i].insert(0, gameState['ghostsPos'][i])         
            
            return [self.EvaluationFunctionLV4(gameState), pacmanPath, ghostPaths, gameState]
        
        if agent == 0:  # maximize for pacman
            nextGameStates = self.GetNextGameStates(0, gameState)             
            traceback = []
            va = -999999
            for nextGameState in nextGameStates:                                
                l = self.MiniMax(1, depth.copy(), nextGameState, copy.deepcopy(pacmanPath), copy.deepcopy(ghostPaths), alpha, beta)
                traceback.append(l)
                va = max(va, traceback[-1][0])
                
                if va >= beta:
                    break
                alpha = max(alpha, va)
                            
            values = [v[0] for v in traceback]
            idxMax = np.argmax(values)
            pacmanPath = traceback[idxMax][1]          
            pacmanPath.insert(0, gameState['pacmanPos'])
            ghostPaths = traceback[idxMax][2]
                    
            
#             if depth[1] == 6:  
#                 print("Max: " + str(values[idxMax]))
#                 print(values)      

#             if values[idxMax] == -600 and depth[1] == 0:
#                 print("-600 DEPTH: " + str(traceback[idxMax]))              
                
#             if depth[1] == 0:
#                 print("Max: " + str(values[idxMax]))
#                 print(values)  
            
            return [values[idxMax], pacmanPath, ghostPaths, traceback[idxMax][3]]
        
        else:  # minimize for ghosts
            nextAgent = agent + 1  # get the next agent
            if len(self.ghosts) + 1 == nextAgent:
                nextAgent = 0            
               
            if nextAgent == 0:  # increase depth every time all agents have moved
                depth[1] += 1
                
            nextGameStates = self.GetNextGameStates(agent, gameState)       
            traceback = []
            vb = 999999                                                                                 
            for nextGameState in nextGameStates:
                l = self.MiniMax(nextAgent, depth.copy(), nextGameState, copy.deepcopy(pacmanPath), copy.deepcopy(ghostPaths), alpha, beta)
                traceback.append(l)
                vb = min(vb, traceback[-1][0])
                
                if vb <= alpha:
                    break
                beta = min(beta, vb)
                
            values = [v[0] for v in traceback]
            idxMin = np.argmin(values)
            ghostPaths = traceback[idxMin][2]
            ghostPaths[agent-1].insert(0, gameState['ghostsPos'][agent-1])
            pacmanPath = traceback[idxMin][1]           
            
            
#             if (traceback[idxMin][3]['gameScore'] > 80):
#                 print("AGENT: " + str(agent))
#                 print("DEPTH: " + str(depth[1]))
#                 print("EvalValue: "+str(self.EvaluationFunctionLV4(traceback[idxMin][3])))
#                 print("Values: " + str(values))
#                 print(traceback[idxMin][3])
            
            
            return [values[idxMin], pacmanPath, ghostPaths, traceback[idxMin][3]]                 
       
    def GetLeftFoods(self, gameState):        
        return [(i,j) for i in range(len(gameState['map'])) for j in range(len(gameState['map'][i])) if gameState['map'][i][j] == "2"]
                 
    def EvaluationFunctionLV4(self, gameState):
#         print("debug1")
#         if (self.IsLose(gameState)):
#             print("Debug: lose")
#         elif self.IsWin(gameState):
#             print("Debug: win")
#         else:
#             print("Debug: limit depth")
#         print(gameState)
        
#         ghostsOptimalPath = [self.A_Start_Graph_Search(gameState['map'], gameState['pacmanPos'], ghostPos) ]
#         distanceToGhosts = [len(ghostPath[1::]) for ghostPath in ghostsOptimalPath]
        distanceToGhosts = [self.ManhattanDis(gameState['pacmanPos'], ghostPos) for ghostPos in gameState['ghostsPos']]
        sumOfDistanceToGhosts = sum(distanceToGhosts)
        
        
#         listFoods = self.GetLeftFoods(gameState)
#         manhattanDistanceToFoods = [self.ManhattanDis(pos, gameState['pacmanPos']) for pos in listFoods]       
#         returnedPath = self.A_Start_Graph_Search(gameState['map'], listFoods[np.argmin(manhattanDistanceToFoods)], gameState['pacmanPos'])       
#         nearestFoodDistance = len(returnedPath)
        
        
#         # Foods in circle of radius 10
#         AStartDistanceToFoods = [len(self.A_Start_Graph_Search(gameState['map'], food, gameState['pacmanPos'])[1::]) for food in listFoods]
#         foodsInCircle = [i for i in AStartDistanceToFoods if i<=10]
#         distanceToFoodsInCircle = sum(foodsInCircle)
        
        # Foods left
        nFoods = gameState['nFoods']
        
        a = 10
        b = 4000
        c = -3000
#         d = 1500*len(foodsInCircle)
        
        if (nFoods == 0):
            nFoods = 0.1
#             d = 1
#             distanceToFoodsInCircle = 1
            
#         if len(foodsInCircle) != 0:
#             d = 1500*len(foodsInCircle)
#         else:
#             distanceToFoodsInCircle = 1
#             d = 1
            
        evalValue = a*gameState['gameScore'] + b*(1/nFoods) + c*(1/sumOfDistanceToGhosts)
        
        if any([distance <= 2 for distance in distanceToGhosts]):
            evalValue -= 5000
            
        return evalValue
        
        
        
    def IsFood(self, currentState, pos):
        return currentState['map'][pos[0]][pos[1]] == "2"
    
    def IsLose(self, gameState):
        return any([gameState['pacmanPos'] == ghostPos for ghostPos in gameState['ghostsPos']])
    
    def IsWin(self, gameState):
        return gameState['nFoods'] == 0
    
    def GetNextGameStates(self, agent, currentState):
        nextGameStates = []
        if (agent == 0): # If pacman
            curPos = currentState['pacmanPos']
            successors = self.GenerateSuccessors(curPos[0], curPos[1])
                        
            for i in range(len(successors)):
                gameState = copy.deepcopy(currentState)                
                curPos = successors[i]
                gameState['pacmanPos'] = curPos
                
                if self.IsFood(gameState, curPos): # increase game score if there is food
                    gameState['nFoods'] -= 1
                    gameState['map'][curPos[0]][curPos[1]] = '0'
                    gameState['gameScore'] += 20                    
                
                gameState['gameScore'] -= 1
                nextGameStates.append(gameState)
                
        else:
            returnedPath = self.A_Start_Graph_Search(currentState['map'], currentState['pacmanPos'], currentState['ghostsPos'][agent-1])
            gameState = copy.deepcopy(currentState)
            gameState['ghostsPos'][agent-1] = returnedPath[1]                                                            
            nextGameStates.append(gameState)            
                                                                                
        return nextGameStates
                        
game = Game() 
game.ReadInput() 
game.Run() 
game.ToAnim()