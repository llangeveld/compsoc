from cvoting import voter as V
from svoting import voter_sv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def ret_shares(num_voters):
    votes = np.random.uniform(0.5, 1, num_voters)
    votes = votes/sum(votes)
    votes = votes*100
    votes = votes.astype('int')

    if sum(votes) != 100:
        remain_votes = 100 - sum(votes)

        for i in range(remain_votes):
            rand_voter = np.random.randint(0,num_voters)
            votes[rand_voter] += 1

    return votes

def cv(n_voters, quadratic = False):
    # n_voters = 2
    n_candidates = 5

    shares = ret_shares(n_voters)

    voters = []
    for i in range(n_voters):
        total_votes = shares[i] * n_candidates
        voters.append(V(total_votes, n_candidates, quadratic))
    
    decisions = np.zeros((n_voters, n_candidates))

    votes = np.zeros((n_voters, n_candidates))
    for i, v in enumerate(voters):
        votes[i] = v.vote()
    
    max_val = np.argmax(votes, axis = 0)
    for i in range(n_candidates):
        decisions[:, i][max_val[i]] = 1

    utility = np.zeros((n_voters))

    for i, v in enumerate(voters):
        utility[i] = v.calculate_utility(decisions[i])
    
    mean = np.mean(utility)
    ste = np.std(utility) / n_voters**0.5

    return mean, ste

def asv(n_v, n_d, quadratic = False):
    n_d = 12

    votes = np.zeros((n_v, n_d))
    voters = []
    for i in range(n_v):
        sv = voter_sv(n_d)
        voters.append(sv)
        sv.vote_asv()
        votes[i] = sv.get_vote_vector()

    final_decision = np.sum(votes,axis = 0)
    final_decision[final_decision> 0] = 1
    final_decision[final_decision < 0] = 0

    utilities = []
    for i in range(n_v):
        utilities.append(voters[i].calculate_utility(final_decision))

    mean = np.mean(utilities)
    ste = np.std(utilities) / n_v**0.5

    return mean, ste

def bsv(n_v, n_d, quadratic = False):
    n_d = 12

    votes = np.zeros((n_v, n_d))
    voters = []
    for i in range(n_v):
        sv = voter_sv(n_d)
        voters.append(sv)
        sv.vote_bsv()
        votes[i] = sv.get_vote_vector()

    final_decision = np.sum(votes,axis = 0)
    final_decision[final_decision> 0] = 1
    final_decision[final_decision < 0] = 0

    utilities = []
    for i in range(n_v):
        utilities.append(voters[i].calculate_utility(final_decision))

    mean = np.mean(utilities)
    ste = np.std(utilities) / n_v**0.5

    return mean, ste


if __name__ == "__main__":
    
    mean_map = {"cv": [], "cvq": [], "asv": [], "asvq": [], "bsv": [], "bsvq": []}
    ste_map = {"cv": [], "cvq": [], "asv": [], "asvq": [], "bsv": [], "bsvq": []}

    quadratic = [True, False]
    run = 30
    nv = 2
    nd = 12

    for i in range(run):
        for q in quadratic:
            cm, cs = cv(nv, quadratic=q)
            Am, As = asv(nv, nd, quadratic=q)
            bm, bs = bsv(nv, nd, quadratic=q)

            if q:
                mean_map["cv"].append(cm)
                mean_map["asv"].append(Am)
                mean_map["bsv"].append(bm)

                ste_map["cv"].append(cs)
                ste_map["asv"].append(As)
                ste_map["bsv"].append(bs)
            else:
                mean_map["cvq"].append(cm)
                mean_map["asvq"].append(Am)
                mean_map["bsvq"].append(bm)

                ste_map["cvq"].append(cs)
                ste_map["asvq"].append(As)
                ste_map["bsvq"].append(bs)
    

    mean_map = {x: np.mean(mean_map[x]) for x in mean_map}
    ste_map = {x: np.mean(ste_map[x]) for x in ste_map}

    mean = list(mean_map.values())
    ste = list(ste_map.values())
    ste = [x + mean[i] for i, x in enumerate(mean)]
    d_len = len(mean_map.keys())
    x = np.linspace(0, d_len - 1, d_len)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    markers = ["o", "v", "*", "s", "D", "^"]
    keys = list(mean_map.keys())

    for i in range(d_len):
        ax.errorbar(x[i], mean[i], ste[i], capsize=2, marker = markers[i], color = "black", label = keys[i])
    
    ax.set_ylabel("Utility")
    plt.legend(loc = "upper left")
    plt.show()