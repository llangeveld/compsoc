from cvoting import voter as V
from svoting import voter_sv

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

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


def plot_figure(mean_map, ste):
    # Categorize data
    mean_cv = [mean_map['cv'], mean_map['cvq']]
    se_cv = [ste[0], ste[1]]
    mean_asv = [mean_map['asv'], mean_map['asvq']]
    se_asv = [ste[2], ste[3]]
    mean_bsv = [mean_map['bsv'], mean_map['bsvq']]
    se_bsv = [ste[4], ste[5]]

    # Set up plot
    x=np.arange(0,2)
    legend = [Line2D([0], [0], color='lightsalmon', lw='3', label='No QV'),
              Line2D([0], [0], color='lightskyblue', lw='3', label='With QV'),
              Line2D([0], [0], marker='o', color='w', label='Mean',
                     markerfacecolor='black', markersize=7)]

    fig, (ax1, ax2, ax3) = plt.subplots(1,3, sharey=True)
    fig.suptitle("Mean utility with SE")

    # First subplot
    ax1.errorbar(x, mean_cv, yerr=se_cv, fmt='o',
                 ecolor=['lightsalmon', 'lightskyblue'],
                 elinewidth=3, color="black")
    ax1.set_xticks([-0.5, 1.5])
    ax1.set_xticklabels(["", ""])
    ax1.grid(axis='y', color='silver', linestyle='-')
    ax1.set_title("CV")
    ax1.set_ylabel("Utility")
    ax1.legend(handles=legend, loc='upper left')

    # Second subplot
    ax2.errorbar(x, mean_asv, yerr=se_asv, fmt='o',
                 ecolor=['lightsalmon', 'lightskyblue'],
                 elinewidth=3, color="black")
    ax2.set_xticks([-0.5, 1.5])
    ax2.set_xticklabels(["", ""])
    ax2.grid(axis='y', color='silver', linestyle='-')
    ax2.set_title("ASV")

    # Third subplot
    ax3.errorbar(x, mean_bsv, yerr=se_bsv, fmt='o',
                 ecolor=['lightsalmon', 'lightskyblue'],
                 elinewidth=3, color="black")
    ax3.set_xticks([-0.5, 1.5])
    ax3.set_xticklabels(["", ""])
    ax3.grid(axis='y', color='silver', linestyle='-')
    ax3.set_title("BSV")

    # Build figure
    fig.tight_layout()
    plt.show()


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

    plot_figure(mean_map, ste)