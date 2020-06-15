from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 
INF = float('inf')
NEG_INF = -INF

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modifying this __init__ function
    def __init__(self, state, current_depth, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])
        # to store a list of (direction, node) tuples
        self.children = []
        self.depth = current_depth
        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        if not self.children:
            return True
        else:
            return False

# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modifying this __init__ function
    def __init__(self, root_state, depth): 
        self.root = Node(root_state, 0, MAX_PLAYER)
        self.depth = depth
        self.simulator = Game()
        self.simulator.board_size = len(root_state[0])

    # recursive function to build a game tree
    def build_tree(self, node=None):
        if node == None:
            #print('tree, node == none')
            node = self.root

        if node.depth == self.depth: 
            #print('tree, if node depth == depth')
            return

        if node.player_type == MAX_PLAYER:
            #print('tree, max player')
            i = 0
            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)
            # NOTE: the following calls may be useful:
            #self.simulator.reset(*(node.state))
            for direction in MOVES:
                #print('tree, maxplayer, moves loop', i)
                i += 1
                self.simulator.reset(*(node.state))
                if self.simulator.move(direction):
                    #print('tree, max move, if move possible')
                    child_state = self.simulator.get_state()
                    child = Node(child_state, node.depth+1, CHANCE_PLAYER)
                    node.children.append((direction, child))

        elif node.player_type == CHANCE_PLAYER:
            #print('tree, chance player')
            i = 0
            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            open_tiles =  self.simulator.get_open_tiles()
            for tile in open_tiles:
                #print('tree, chance, in loop', i)
                #print('tile', tile)
                i += 1

                self.simulator.reset(*(node.state))
                curr_state = self.simulator.get_state()
                curr_matrix = curr_state[0]
                curr_matrix[tile[0]][tile[1]] = 2
                new_state = (curr_matrix, curr_state[1])
                child = Node(new_state, node.depth+1, MAX_PLAYER)
                node.children.append((None,child))

        # TODO: build a tree for each child of this node
        # if node.children:
        
        for child in node.children:
            self.simulator.reset(*(child[1].state))
            self.build_tree(child[1])


    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        if node == None:
            #print('Node == none')
            node = self.root

        if node.is_terminal():
            #print('terminal')
            return None, node.state[1]

        elif node.player_type == MAX_PLAYER:
            #print('max player')
            value = NEG_INF
            direction = None
            for n in node.children:
                new_val = self.expectimax(n[1])[1]
                if new_val > value:
                    value = new_val
                    direction = n[0]
                #direction, value = n[0], max(value, self.expectimax(n[1])[1])
            #print('direction', direction)
            #print('value', value)
            return direction, value

        elif node.player_type == CHANCE_PLAYER:
            #print('chance player')
            value = 0
            chance = 1/(len(node.children))
            for n in node.children:
                value = value + (self.expectimax(n[1])[1]*chance)
            return None, value

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): implement method for extra credits
    def compute_decision_ec(self):
        # TODO delete this
        return random.randint(0, 3)
