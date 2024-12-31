### PHASE 1: Interaction and payoff
    #To do

###Phase 2 : Reproduction
    #Compute probabilities to pick an individual based on fitness_i/fitness_tot : DONE
    #Pick randomly the indvidual for reproduction (cloning the indvidual) : DONE
    #With probability lamda, the clone migrate to another group

###Phase 3 : Group Conflict
    #Select kappa*self.num_groups groups for the conflicts
    #If selected amount of groups is odd:
        #50% chance to REMOVE a group from the conflict
        #50% chance to ADD an unselected group TO conflict
    #Generate the pairs for the conflict
    #For each conflicts:
        #Compute probability to win based on the group_payoff and the parameter z (check equation)
        #The winner is cloned and replace the loser group
            
###Phase 4 : Group Splitting
    #Check all groups and verify groups getting more than n indivuals (due to reproduction or conflicts)
    #With probability q, split the parent group into 2 daughter groups to fill randomly
        #The first daughter replaces the parent
        #The second daughter replaces another random group
    #If no split, remove random indvidual from the group to respect the size group_size

is_there_fixation = False
###Looping not is_there_fixation