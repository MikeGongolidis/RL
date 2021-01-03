import random


class simple21env():

    def __init__(self):

        self.deck = self.create_deck()
        self.dealers_deck = [i for i in range(1,11)]
        self.agents_hand = -1
        self.dealers_hand = -1
        self.completed_episodes = 0
        self.done = False
        self.number_of_actions = 2
        

    def create_deck(self):
        deck = [i for i in range(-10,11)]
        deck.remove(0)
        for i in range(1,11):
            deck.append(i)
        
        return deck


    def reset(self):
        starting_reward = 0
        self.done = False
        self.agents_hand = -1
        self.dealers_hand = -1
        while self.agents_hand<0:
            self.agents_hand = random.choice(self.deck)
        while self.dealers_hand<0:
            self.dealers_hand = random.choice(self.deck)
        
        return self.agents_hand,self.dealers_hand,starting_reward,self.done


    def check_if_bust(self,dealer=False):
        bust = False
        hand = self.agents_hand
        if dealer:
            hand = self.dealers_hand
        if hand<1 or hand>21:
            bust = True
        return bust

    def check_goal(self,dealer_bust):

        reward = 0
        if dealer_bust or self.agents_hand>self.dealers_hand:
            reward = 1
        elif self.dealers_hand> self.agents_hand:
            reward = -1

        return reward


    def dealer_game(self):

        bust = self.check_if_bust(dealer=True)

        while self.dealers_hand <= 17 and not bust:
            if not bust:
                self.dealers_hand += random.choice(self.dealers_deck)
            else:
                break
            bust = self.check_if_bust(dealer=True)

        return bust

    def step(self,action):
        if not self.done == True:
            
            reward = 0
            if action == 0: # hit

                self.agents_hand += random.choice(self.deck)
                agent_bust = self.check_if_bust()
                if agent_bust:
                    reward = -1
                    self.done = True
                    self.completed_episodes+=1
            else: # stick
                self.done = True
                self.completed_episodes+=1
                dealer_bust = self.dealer_game()
                reward = self.check_goal(dealer_bust)
            state = (self.agents_hand,self.dealers_hand,reward,self.done)
        else:
            print("Episode is over, reset environment")
            state = None

        return state
