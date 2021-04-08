import numpy as np
import random

class voter(object):

    def __init__(self, num_votes, num_candidates, quadratic = False):
        self.num_candidates = num_candidates
        self.num_votes = num_votes
        self.preference = self.get_preference()
        self.quadratic = quadratic
    
    def get_preference(self):
        pref = np.random.uniform(0.5, 1, self.num_candidates)
        pref = pref/sum(pref)
        return pref
    
    def calculate_utility(self, final_decisions):
        utility = 0
        for d in range(self.num_candidates):
            utility = utility + final_decisions[d]*self.preference[d]
        
        return utility 
    
    def vote(self):
        votes = (self.preference*self.num_votes).astype('int')

        if sum(votes) < self.num_votes:
            diff = self.num_votes - sum(votes)
            most_pref = np.argmax(self.preference)
            votes[most_pref] += diff

        if self.quadratic:
            votes = votes ** 0.5

        return votes


# def ret_shares(num_voters):
#     votes = np.random.uniform(0.5, 1, num_voters)
#     votes = votes/sum(votes)
#     votes = votes*100
#     votes = votes.astype('int')

#     if sum(votes) != 100:
#         remain_votes = 100 - sum(votes)

#         for i in range(remain_votes):
#             rand_voter = np.random.randint(0, num_voters)
#             votes[rand_voter] += 1

#     return votes

# if __name__ == "__main__":

#     n_voters = 2
#     n_candidates = 3

#     shares = ret_shares(n_voters)

#     voters = []
#     for i in range(n_voters):
#         total_votes = shares[i] * n_candidates
#         voters.append(voter(total_votes, n_candidates))
    
#     decisions = np.zeros((n_voters, n_candidates))

#     votes = np.zeros((n_voters, n_candidates))
#     for i, v in enumerate(voters):
#         votes[i] = v.vote()
    
#     max_val = np.argmax(votes, axis = 0)
#     for i in range(n_candidates):
#         decisions[:, i][max_val[i]] = 1

#     utility = np.zeros((n_voters))

#     for i, v in enumerate(voters):
#         utility[i] = v.calculate_utility(decisions[i])
    
#     mean = np.mean(utility)
#     ste = np.std(utility) / n_voters**0.5

#     print(mean)
#     print(ste)