from MCTSNode import MCTSNode
from GomokuGameState import GomokuGameState

class MonteCarloTreeSearch:

    def __init__(self, iteration_number, game_state):
        self.iterate_number = iteration_number
        self.root_node = MCTSNode(game_state = game_state)
        self.root_node.set_new_available_move()

    def max_RAVE(self, children):
        node_max = children[0]
        max_rave = node_max.RAVE()

        for node in children[1:]:
            rave = node.RAVE()
            if rave > max_rave:
                max_rave = rave
                node_max = node
        return node_max

    def search(self):
        if self.root_node.is_terminal:
            return 

        i = 0

        while i < self.iterate_number:
            select_node = self.select()
            expand_node = self.expand(select_node)
            winner, x_simulate_move, o_simulate_move = self.simulate(expand_node)
            self.back_propagate(expand_node, winner, x_simulate_move, o_simulate_move)
            i += 1
        return self.chose_best_move()


    def select(self):
        node = self.root_node
        while not node.is_expandable() and not node.is_terminal:
            node = self.max_RAVE(node.children)
        return node

    def expand(self, node):
        if node.is_terminal:
            return node

        move = node.pop_random_expand_move()
        expand_node = MCTSNode(parent = node, game_state = node)
        expand_node.play(move)
        node.add_child(expand_node)

        return expand_node

    def simulate(self, node):

        simulate_node = GomokuGameState(game_state = node)

        x_simulate_move = []
        o_simulate_move = []
        
        while not simulate_node.is_terminal:
            move = simulate_node.random_choice_available_move()
            
            if simulate_node.turn == 1:
                x_simulate_move.append(move)          
            else:
                o_simulate_move.append(move)

            simulate_node.play(move)

        return simulate_node.winner, x_simulate_move, o_simulate_move

    def back_propagate(self, node, winner, x_simulate_move, o_simulate_move):
        while node:
            if node.children:
                if node.turn == 1:
                    for child in node.children:
                        if child.last_move in x_simulate_move:
                            child.q_AMAF += 0.5 if winner == -1 else (1 if winner == child.player_make_move else -5)
                            child.n_AMAF += 1
                elif node.turn == 0:
                    for child in node.children:
                        if child.last_move in o_simulate_move:
                            child.q_AMAF += 0.5 if winner == -1 else (1 if winner == child.player_make_move else -5)
                            child.n_AMAF += 1
 
            node.q_UCT += 0.5 if winner == -1 else (1 if winner == node.player_make_move else -5)
            node.n_UCT += 1
            node = node.parent
        
    def chose_best_move(self):
        return max(self.root_node.children, key = lambda node: node.n_UCT).last_move