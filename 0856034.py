#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import sys 
from termcolor import colored, cprint 
import time as t
import random
import copy


# In[2]:


def check(board):
    check_board = np.zeros((board_size,board_size))
    pad_board =  np.pad(board.reshape(board_size,board_size), pad_width=((1,1),(1,1)), mode='constant', constant_values=0)
    #print("&",board)
    #print(pad_board)
    for row in range(1,board_size+1):
        for col in range(1,board_size+1):
            sum_point = 0
            if pad_board[row][col] !=0 and pad_board[row][col]!=-1:
                for i in range(row-1,row+2):
                    for j in range(col-1,col+2):
                        if pad_board[i][j] <-1:
                            sum_point -= pad_board[i][j]
                        elif pad_board[i][j] >-1:
                            sum_point += pad_board[i][j]
                #print(sum_point)
                if sum_point>15:
                    check_board[row-1][col-1] = 1
    return check_board.reshape(board_size*board_size)


# In[3]:


def remove(check_board,board):
    for pos in range(board_size*board_size):
        if check_board[pos] ==1:
            board[pos] = -1
    return board


# In[4]:


def total_point(board):
    user = []
    AI = []
    for point in board:
        if point < -1:
            user.append(-point)
        if point > 0:
            AI.append(point)
            
    return user, AI


# In[5]:


def result_(board):
    #user win return 1
    #AI win return -1
    #Tie return 0
    user_l, AI_l = total_point(board)
    
    if sum(user_l) > sum(AI_l):
        return True
    elif sum(user_l)<sum(AI_l):
        return False
    else:
        if len(user_l) < len(AI_l):
            return True
        elif len(user_l) > len(AI_l):
            return False
        else:
            return None


# In[6]:


def evaluation(board,user_chess_available,AI_chess_available):
    user_e, AI_e = total_point(board)
    point = 0
    
    for i in user_e:
        if i == 3:
            point-=1
        elif i ==5:
            point-=2
        elif i==8:
            point-=4
        elif i == 13:
            point-=7
            
    for i in AI_e:
        if i == 3:
            point+=1
        elif i ==5:
            point+=2
        elif i==8:
            point+=4
        elif i == 13:
            point+=7
            
    for i in user_chess_available:
        if i == 3:
            point-=1/2
        elif i ==5:
            point-=2/2
        elif i==8:
            point-=4/2
        elif i == 13:
            point-=7/2
            
    for i in AI_chess_available:
        if i == 3:
            point+=1/2
        elif i ==5:
            point+=2/2
        elif i==8:
            point+=4/2
        elif i == 13:
            point+=7/2
    
    point += (sum(AI_e) - sum(user_e))*2
    
    L = list(board)
    if 13 in L:
        if 3 in user_chess_available:
            point -=30
        elif 5 in user_chess_available:
            point -=28
        elif 8 in user_chess_available:
            point -=25
        elif 13 in user_chess_available:
            point -=20
    
    return point
    


# In[7]:


def is_end(board):
    if board_size == 6:
        if np.count_nonzero(board) == 22:
            #print("&",np.count_nonzero(tup))
            return True
        else:
            return False
    else:
        if np.count_nonzero(board) == 10:
            #print("&",np.count_nonzero(tup))
            return True
        else:
            return False    


# In[8]:


def min_(board, alpha, beta, user_chess_available, AI_chess_available,count):
    
    #print("min",board)
    #print(count)
    if count>=3:
        return evaluation(board,user_chess_available,AI_chess_available), 0, 0
        
    
    minv = 1000
    qi = None
    put = None
    user_chess = user_chess_available.copy()
    
    if is_end(board):
        return evaluation(board,user_chess_available,AI_chess_available), 0, 0
    
    for chess in user_chess:
        n = random.randint(0,board_size*board_size-1)
        L = INDEX[n:]+INDEX[:n] 
        for i in L:
            if board[i] == 0:
                board_recover = np.copy(board)
                board[i] = -chess
                board = remove(check(board),board)
                
                user_chess_available = user_chess.copy()
                user_chess_available.remove(chess)

                m, max_i, chess_i = max_(board, alpha, beta, user_chess_available, AI_chess_available, count+1)
                if m < minv:
                    minv = m
                    qi = i
                    put = chess
                board = board_recover.copy()
                
                if minv <= alpha:
                    #print("purn")
                    return (minv, qi, put)

                if minv < beta:
                    beta = minv
                
    return minv, qi, put    


# In[9]:


def max_(board, alpha, beta, user_chess_available, AI_chess_available,count):
    
    #print("max",board)
    #print(count)
    if count>=3:
        #print(count)
        return evaluation(board,user_chess_available,AI_chess_available), 0, 0
    
    maxv = -1000
    pi = None
    put = None
    AI_chess = AI_chess_available.copy()
    
    if is_end(board):
        return evaluation(board,user_chess_available,AI_chess_available), 0, 0
    
    for chess in AI_chess:
        n = random.randint(0,board_size*board_size-1)
        L = INDEX[n:]+INDEX[:n] 
        for i in L:
            
            if board[i] == 0:
                board_recover = np.copy(board)
                
                board[i] = chess
                board = remove(check(board),board)
                
                AI_chess_available = AI_chess.copy()
                AI_chess_available.remove(chess)
                
                m, min_i, chess_i = min_(board, alpha, beta, user_chess_available, AI_chess_available,count+1)
                if m > maxv:
                    #print("score",m)
                    maxv = m
                    pi = i
                    put = chess
                
                board = board_recover.copy()
                
                if maxv >= beta:
                    #print("purn")
                    return (maxv, pi, put)

                if maxv > alpha:
                    alpha = maxv
                    
    return maxv, pi, put


# In[10]:


def play(board,user_turn):

    user_chess_available = [13,8,5,3,2]
    AI_chess_available = [2,3,5,8,13]
    show = np.copy(board)
    count_4 = 0
    round_no = 0
    
    
    while True:
        
        #show = np.copy(board)
        for i in range(board_size):
            for j in range(board_size):
                if board[i*board_size+j] == -1:
                    cprint('%-3s'%'X' , "red",end='')
                elif board[i*board_size+j] < -1:
                    cprint('%-3s'%str(-board[i*board_size+j]), "green",end='')
                elif board[i*board_size+j] >0:
                    cprint('%-3s'%str(board[i*board_size+j]), "blue",end='')
                else:
                    cprint('%-3s'%str(board[i*board_size+j]) ,end='')
            print()
            
        print()
        
        if is_end(board):
            result = result_(board)
            if result == True:
                print("user win")
            elif result == False:
                print("AI win")
            else:
                print("Tie")
            return
        
        if user_turn == 1:
            
            while True:
                
                #show = np.copy(board)
                #m,qi, put = min_(board, -46, 46, user_chess_available, AI_chess_available,count)
                
                #print('Recommended move: pos = {}, chess = {}'.format(qi,put))
                show_user_chess_available = user_chess_available.copy()
                show_user_chess_available.reverse()
                
                cprint("user chess", on_color = "on_green" , end = '')
                print(":", show_user_chess_available)
                cprint("AI chess", on_color = 'on_blue', end = '')
                print(":", AI_chess_available)
                
                try:
                    pos_x, pos_y, chess = map(int, input("Input (row, col, weight): ").split())
       
                    print("[User]: ({}, {}, {})".format(pos_x, pos_y, chess))
                    if board[pos_x*board_size+pos_y] == 0 and chess in user_chess_available and pos_x<board_size and pos_y<board_size :
                        board[pos_x*board_size+pos_y] = -chess
                        user_turn = 0
                        user_chess_available.remove(chess)
                        show = remove(check(board),board)
                        break
                    else:
                            print('The move is not valid! Try again.')
                except ValueError:
                    print('Input Error! Try again.')
                except IndexError:
                    print('Index Error! Try again.')


        else:
            start = t.time()
            
            show = np.copy(board)
            m,qi, chess = max_(board, -1000, 1000, user_chess_available, AI_chess_available,count_4)
            end = t.time()
            #print('Evaluation time: {}s'.format(round(end - start, 7)))
            
            show[qi] = chess
            show = remove(check(show),show)
            board = np.copy(show)
            
            AI_chess_available.remove(chess)
            user_turn = 1
            
            
            if round_no ==1:
                count_4 = -2
            elif round_no ==2:
                count_4 = -4
            elif round_no >=3:
                count_4 = -8

            round_no+=1
            
            print("[AI]: ({}, {}, {})".format(int(qi/board_size), qi%board_size, chess))


# In[11]:


from abc import ABC, abstractmethod
from collections import defaultdict
import math
import numpy as np
from termcolor import colored, cprint 
import time as t
import time as t1


class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.finish():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        path = self._select(node)
        #print("path")
        #for i in path:
            #print(i.tup)
        #print("e")
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        #print(reward)
        self._backpropagate(path, reward)

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._UCB_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()
        #for i in self.children[node]:
            #print(i.tup)

    def _simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        #invert_reward = True
        while True:
            if node.finish():
                reward = node.reward()
                return reward
                #return 1 - reward if invert_reward else reward
            node = node.find_random_child()
            #invert_reward = not invert_reward

    def _backpropagate(self, path, reward):
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            #reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _UCB_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def UCB(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=UCB)


# In[12]:


from collections import namedtuple
from random import choice

class sum_15:
    
    def __init__(self, tup, turn, winner, terminal, user_chess, AI_chess, index, chess):

        self.tup= tup
        self.turn= turn 
        self.winner=winner
        self.terminal=terminal
        self.user_chess = user_chess
        self.AI_chess = AI_chess
        self.index = index
        self.chess = chess
        
    def find_children(board):
        if board.terminal:  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        if board.turn:
            L = []
            for chess in board.user_chess:
                for i in range(board_size*board_size):
                    if board.tup[i] == 0:
                        L.append(board.make_move(i, chess))
            return set(L)
        else:
            L = []
            for chess in board.AI_chess:
                if chess ==13:
                    continue
                for i in range(board_size*board_size):
                    if board.tup[i] == 0:
                        L.append(board.make_move(i, chess))
            return set(L)
        

    def find_random_child(board):
        #print(board.user_chess,board.AI_chess)
        if board.terminal or (len(board.user_chess)==2 and len(board.AI_chess)==0):
            return None  # If the game is finished then no moves can be made
        empty_spots = [i for i, value in enumerate(board.tup) if value == 0]
        if board.turn:
            return board.make_move(choice(empty_spots),choice(board.user_chess))
        else:
            chess_avail = board.AI_chess.copy()
            if 13 in board.AI_chess and len(board.AI_chess)>1:
                chess_avail.remove(13)
           # print(board.make_move(choice(empty_spots),choice(board.AI_chess)).tup)
            return board.make_move(choice(empty_spots),choice(chess_avail))

    def reward(board):
        user = []
        AI = []
        for point in board.tup:
            if point < -1:
                user.append(-point)
            if point > 0:
                AI.append(point)
                
        point = (sum(AI) - sum(user))
        return point
    

    def finish(board):
        if board_size == 6:
            if np.count_nonzero(board.tup) == 20:
                #print("&",np.count_nonzero(tup))
                return True
            else:
                return False
        else:
            if np.count_nonzero(board.tup) == 10:
                #print("&",np.count_nonzero(tup))
                return True
            else:
                return False

    def make_move(board, index,chess):
        tup = np.copy(board.tup)
        if board.turn:
            tup[index] = -chess
            turn =False
        else:
            tup[index] = chess
            turn = True
            
        tup = remove(check(tup),tup)
        #print(tup)
            
        winner = result_(tup)
        
        is_terminal = is_end_MCTS(tup)
        
        user_chess = board.user_chess.copy()
        AI_chess = board.AI_chess.copy()
        
        if board.turn:
            user_chess.remove(chess)
            return sum_15(tup, turn, winner, is_terminal, user_chess, AI_chess, index, chess)
        else:
            AI_chess.remove(chess)
            return sum_15(tup, turn, winner, is_terminal, user_chess, AI_chess, index, chess)


# In[13]:


def new_board():
    if board_size == 6:
        return sum_15(tup= np.zeros(36,dtype='int'), turn=bool(user_turn), winner=None, terminal=False, user_chess = [13,13,8,8,8,5,5,3,3,2,2] , AI_chess =  [2,2,3,3,5,5,8,8,8,13,13], index =0, chess = 0)
    else:
        return sum_15(tup= np.zeros(16,dtype='int'), turn=bool(user_turn), winner=None, terminal=False, user_chess = [13,8,5,3,2] , AI_chess =  [2,3,5,8,13], index =0, chess = 0)

def is_end_MCTS(board):
    if board_size == 6:
        if np.count_nonzero(board) == 20:
            #print("&",np.count_nonzero(tup))
            return True
        else:
            return False
    else:
        if np.count_nonzero(board) == 10:
            #print("&",np.count_nonzero(tup))
            return True
        else:
            return False 


# In[14]:


def play_6():
    
    def draw(board):
        for i in range(board_size):
            for j in range(board_size):
                if board[i*board_size+j] == -1:
                    cprint('%-3s'%'X' , "red",end='')
                elif board[i*board_size+j] < -1:
                    cprint('%-3s'%str(-board[i*board_size+j]), "green",end='')
                elif board[i*board_size+j] >0:
                    cprint('%-3s'%str(board[i*board_size+j]), "blue",end='')
                else:
                    cprint('%-3s'%str(board[i*board_size+j]) ,end='')
            print()
        print()
        
    tree = MCTS()
    board = new_board()
    draw(board.tup)
    #print(board.tup.reshape(board_size,board_size))
    
    round_no = 0
    count= 1
    while True:
        
        if board.turn:
            while True:
                show_user_chess_available = board.user_chess.copy()
                show_user_chess_available.reverse()
                cprint("user chess", on_color = "on_green" , end = '')
                print(":", show_user_chess_available)
                cprint("AI chess", on_color = 'on_blue', end = '')
                print(":", board.AI_chess)
                print()
            
                try:
                    pos_x, pos_y, chess = map(int, input("Input (row, col, weight): ").split())
                    
                    print("[User]: ({}, {}, {})".format(pos_x, pos_y, chess))
                    index = board_size * pos_x + pos_y
                    if board.tup[index] ==0 and chess in board.user_chess :
                        board = board.make_move(index,chess)
                        draw(board.tup)
                        break
                    else:
                        print("invaild move")
                except ValueError:
                    print('Input Error! Try again.')
                except IndexError:
                    print('Index Error! Try again.')
                
        else:
            start_all = t1.time()
        
            if round_no <6:
                
                if round_no == 0 and user_turn==0:
                    index_r = random.randint(0,board_size*board_size-1)
                    chess_r = choice([2,3,5])
                    board = board.make_move(index_r,chess_r)
                else:
            
                    start = t.time()
                    tree.do_rollout(board)
                    end = t.time()
        
                    n = int(22/(end-start))
                    #n = 2
                    for i in range(n):  
                        tree.do_rollout(board)

                    board = tree.choose(board)
                
            else:
                
                show = copy.deepcopy(board)
                #print(board.AI_chess)
                m, index, chess = max_(board.tup, -1000, 1000, board.user_chess, board.AI_chess, count)
                show.tup[index] = chess
                show.index = index
                show.chess = chess 
                show.AI_chess.remove(chess)
                board = copy.deepcopy(show)
                board.tup = remove(check(board.tup),board.tup)
                board.turn = 1
                
            end_all = t1.time()
            #print('Evaluation time: {}s'.format(round(end_all - start_all, 7)))
            print("[AI]: ({}, {}, {})".format(board.index//board_size, board.index%board_size, board.chess))
            draw(board.tup)
            
            if round_no >=6:
                count-=1
            
            round_no +=1
        
        if is_end(board.tup):
            if result_(board.tup):
                print("user win")
            elif not result_(board.tup):
                print("AI win")
            else:
                print("TIe")
            break


# In[18]:


while True:
    user_turn = int(input("User first? (0/1; -1 can quit game): ")) 
    if user_turn == -1:
        break
    elif user_turn !=1 and user_turn!=0:
        print("please input 0 or 1")
        continue
    board_size = int(input("Board Size? (4 or 6) : "))
    INDEX = [i for i in range(board_size*board_size)]
    if board_size==4:
        a = np.zeros(board_size* board_size,dtype = 'int')
        play(a,user_turn)
    elif board_size==6:
        play_6()
    else:
        print("wrong board size")


# In[ ]:





# In[ ]:





# In[ ]:




