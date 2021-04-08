import random
import numpy as np


class voter_sv(object):
    def __init__(self, nr_decisions, quadratic=False):
        self.votes = 0
        self.vote_vector = np.zeros((nr_decisions))
        self.nr_decisions = nr_decisions
        self.quadratic = quadratic
        self.preference = [x/100 for x in random.sample(range(-100, 100), nr_decisions)]
        self.threshold = 0.1
        self.utility = 0

    def vote_asv(self):
        for d in range(self.nr_decisions):
            self.votes = self.votes + 1
            self.vote_vector[d] = self.how_many_votes_asv(d)
            self.votes = self.votes - abs(self.vote_vector[d])

    def vote_bsv(self):
        self.votes = self.votes + self.nr_decisions
        for d in range(self.nr_decisions):
            self.votes = self.votes + 1
            self.vote_vector[d] = self.how_many_votes_bsv(d)
            self.votes = self.votes - abs(self.vote_vector[d])

    def how_many_votes_asv(self, decision_index):
        remaining_decisions = self.nr_decisions - decision_index
        pref = self.preference[decision_index]

        if self.quadratic:
            multiplier = np.sqrt(abs(pref)/0.5)
        else:
            multiplier = abs(pref)/0.5 
        votes_cast = int(round(multiplier*((self.votes + remaining_decisions) / remaining_decisions)))

        if votes_cast > self.votes:
            votes_cast = self.votes

        if self.quadratic:
            votes_cast = np.sqrt(votes_cast)

        if pref > 0:
            return votes_cast
        else:
            return -votes_cast
    
    def how_many_votes_bsv(self, decision_index):
        remaining_decisions = self.nr_decisions - decision_index
        pref = self.preference[decision_index]

        if self.quadratic:
            multiplier = np.sqrt(abs(pref)/0.5)
        else:
            multiplier = abs(pref)/0.5 
        votes_cast = int(round(multiplier*((self.votes + remaining_decisions) / remaining_decisions)))

        if votes_cast < 1:
            votes_cast = 1
        if votes_cast > self.votes:
            votes_cast = self.votes
        
        if self.quadratic:
            votes_cast = np.sqrt(votes_cast)
        if pref > 0:
            return votes_cast
        else:
            return -votes_cast
    
    def calculate_utility(self, final_decisions):
        for d in range(self.nr_decisions):
            self.utility = self.utility + final_decisions[d]*self.preference[d]
        
        return self.utility 
    
    def get_vote_vector(self):
        return self.vote_vector

    def get_utility(self):
        return self.utility

# n_v = 7
# n_d = 12

# votes = np.zeros((n_v, n_d))
# voters = []
# for i in range(n_v):
#     sv = voter_sv(n_d)
#     voters.append(sv)
#     sv.vote_asv()
#     votes[i] = sv.get_vote_vector()

# print(votes)
# final_decision = np.sum(votes,axis = 0)
# final_decision[final_decision> 0] = 1
# final_decision[final_decision < 0] = 0
# print(final_decision)

# utilities = []
# for i in range(n_v):
#     utilities.append(voters[i].calculate_utility(final_decision))

# mean = np.mean(utilities)
# std = np.std(utilities)

# x = np.arange(0, n_v, 1)
# print(utilities)
# plt.scatter(x, utilities)
# print(mean)
# print(std)
# print(votes)
# print(final_decision)

# plt.show()
