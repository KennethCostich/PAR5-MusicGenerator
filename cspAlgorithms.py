import util
import copy
import random

class CSPSolver:
    "Contains functions to solve a given CSP"

    def revise(self, csp, x, y):
        """
        Given a CSP csp and two variables x and y, enforces arc consistency on the
        arc (x, y) with the domains and constraints outlined in the CSP.
        Returns True if the domain of x is revised, or changed.
        Returns False otherwise.
        """
        # separate and store the components of a CSP
        (V, D, C) = csp

        # initialize revised to False
        revised = False

        # initialize the arc
        arc = (x, y)

        # check if there is a constraint for this arc
        if arc in C:
            # get the domain of possible values for variable x
            Dx = D[x]

            # get the domain of possible values for variable y
            Dy = D[y]

            # iterate through values in the domain of x
            for x_val in Dx:
                # initialize satisfies to False
                satisfies = False

                # iterate through values in the domain of y
                for yVal in Dy:
                    # get the function defining the constraint on (x, y)
                    constraint = C[arc]

                    # check if the constraint is satisfied for this x_val and yVal
                    satisfied_here = constraint(x_val, yVal)

                    # if this x_val and yVal satisfy the constraint
                    if satisfied_here:
                        # set satisfies to True
                        satisfies = True

                # if no yVal allows (x_val, yVal) to satisfy the constraint
                if not satisfies:
                    # remove this x_val from the domain of x
                    Dx.remove(x_val)

                    # set revised to True
                    revised = True

        # return whether the domain of X has been revised (changed)
        return revised


    def ac3(self, csp):
        """
        Implementation of the AC-3 algorithm based on the psuedocode given in Lecture.
        Given a CSP csp, enforces complete arc consistency across all arcs in the CSP.
        Returns True if csp is consistent (meaning if all variables have non-empty
        domains after arc-consistency is enforced).
        Returns False if an inconsistency is found (meaning a variable's domain has
        become empty).
        """
        # separate and store the components of a CSP
        (V, D, C) = csp

        # initialize the list of arcs
        arcs = []

        # iterate through pairs of distinct variables to find arcs
        for x in V:
            for y in V:
                # if two variables are not the same, add an arc (x, y) to arcs
                if not (x == y):
                    arc = (x, y)
                    arcs.append(arc)

        # initialize a queue using the Queue structure in util.py
        queue = util.Queue()

        # add each arc to the queue
        for arc in arcs:
            queue.push(arc)

        # We will now enforce arc consistency of each arc in the queue
        # check if there are any arcs in the queue
        while (not (queue.isEmpty())):
            # pop an arc (x, y) from the queue
            (x, y) = queue.pop()

            # call revise(csp, x, y) to enforce arc consistency on (x, y)
            # will return True if the domain of x was revised
            if (self.revise(csp, x, y)):
                # check if the domain of x has been revised to be empty
                if (len(D[x]) == 0):
                    # if it has, there's an inconsistency
                    # return False
                    return False
                
                # initialize list of arcs (n, x), where n is a neighbor of x
                neighbor_arcs = []

                # iterate through arcs
                for arc in arcs:
                    # if arc is of the form (n, x) such that n != y
                    if ((not (arc[0] == y)) and (arc[1] == x)):
                        # add the arc to neighbor_arcs
                        neighbor_arcs.append(arc)

                # push each arc in neighbor_arcs to the queue
                for arc in neighbor_arcs:
                    queue.push(arc)

        # if the queue is empty, no inconsistency has been found
        # return True
        return True

    def mrv(self, csp):
        """
        Heuristic function for the Minimum Remaining Value (MRV) ordering heuristic.
        Given a CSP csp, returns a variable with a domain of minimum size,
        i.e. a variable with the minimum number of remaining values in its domain.

        NOTE: only variables with domain sizes of 2 or greater are considered,
        since 1 remaining value equates to an assignment and 0 remaining values 
        equates to an inconsistent CSP
        NOTE: ties are broken by order of iteration through the set of variables
            TODO: break ties by degree heuristic?? maybe??
            but, all variables might have same degree, so save for later if useful
        """
        # separate and store the components of a CSP
        (V, D, C) = csp

        # initialize a priority queue using the PriorityQueue structure in util.py
        p_queue = util.PriorityQueue()

        # iterate through variables
        for variable in list(V):
            # get the domain size (# of remaining values) for this variable
            domain_size = len(D[variable])

            # if the variable isn't already assigned
            if (domain_size) > 1:
                # push this variable to p_queue with priority domain_size
                p_queue.push(variable, domain_size)
        
        if (p_queue.isEmpty()):
            print("THIS SHIT IS EMPTY")
            print(D)

        # get the variable to expand next
        next_var = p_queue.pop()

        # return the selected variable with MRV
        return next_var

    def lcv(self, csp, x):
        """
        Heuristic function for the Least Constraining Value (LCV) ordering heuristic.
        Given a CSP csp and a variable x, returns a least constraining value from the
        domain of x, i.e. a value which reduces the sum of the sizes of the domains 
        of other variables by the minimum amount.

        NOTE: ties are broken by randomness
        NOTE: comments above lines of code which determine this start with ####
        """
        # separate and store the components of a CSP
        (V, D, C) = csp

        # initialize sum to 0
        init_sum = 0

        # get the sum of the current domain sizes
        for domain in D.values():
            # get the size of this domain
            d_size = len(domain)

            # add this to the sum
            init_sum = init_sum + d_size

        # initialize a priority queue using the PriorityQueue structure in util.py
        """p_queue = util.PriorityQueue()"""

        #### CREATE A LIST OF NUMS OF DEPLETED VALUES
        nums = []

        #### CREATE A DICTIONARY x_val TO NUM
        val_to_depleted = {}

        # get the domain of possible values for variable x
        Dx = D[x]

        # iterate through values in the domain of x Dx
        for x_val in Dx:
            # make a copy of the current domains
            D_copy = copy.deepcopy(D)

            # assign value x_val to variable x in the copy
            D_copy[x] = [x_val]

            # create a csp using the modified copy of domains
            csp_copy = (V, D_copy, C)

            # enforce arc consistency on the prospective CSP
            csp_is_valid = self.ac3(csp_copy)

            # if the assignment didn't create inconsistencies
            if csp_is_valid:
                # initialize the remaining sum to 0
                remaining_sum = 0

                # get the sum of the remaining domain sizes
                for domain in D_copy.values():
                    # get the size of this domain
                    d_size = len(domain)

                    # add this to the sum
                    remaining_sum = remaining_sum + d_size

                # get the difference between the initial sum and remaining sum
                values_depleted = init_sum - remaining_sum

                #### ADD TO LIST
                nums.append(values_depleted)

                #### ADD TO DICTIONARY
                val_to_depleted[x_val] = values_depleted

                # push x_val to p_queue with priority values_depleted
                """p_queue.push(x_val, values_depleted)"""
        
        # get the value to assign to x
        """selected_val = p_queue.pop()"""

        #### GET THE MIN VAL
        min_val = min(nums)

        #### CREATE LIST OF MIN x_valS
        possible_x_vals = []

        #### ADD KEYS TO POSSIBLE X VALS LIST
        for key in val_to_depleted.keys():
            if (val_to_depleted[key] == min_val):
                possible_x_vals.append(key)

        #### SELECT A LCV AT RANDOM
        selected_val = random.choice(possible_x_vals)

        # return the selected LCV
        return selected_val

    def is_solved(self, csp):
        """
        Given a CSP csp, determined whether the CSP is solved.
        If a CSP is solved, no domain has a size greater than 1.
        """
        # separate and store the components of a CSP
        (V, D, C) = csp

        # iterate through new domains
        for domain in D.values():
            # get the length of the domain
            d_size = len(domain)

            # if the domain has size greater than 1
            if (d_size > 1):
                # return False
                return False

        # if you made it this far, return True 
        return True


    def exists_valid_assignment(self, csp):
        """
        Given a CSP csp, finds a valid assignment to variables in csp
        which is a solution to the CSP.
        If a valid assignment exists, returns True.
        If no valid assignment exists, returns False.
        """
        # determine whether the CSP is solved initially
        solved = self.is_solved(csp)

        # enforce initial arc consistency on the CSP
        solvable = self.ac3(csp)

        # if the CSP is not solvable, return false
        if (not solvable):
            return False

        # check if CSP is solved after arc consistency enforced a single time
        solved = self.is_solved(csp)

        # while the CSP is not solved
        while (not solved):
            # separate and store the components of a CSP
            (V, D, C) = csp

            # use MRV to find the next variable to expand
            next_var = self.mrv(csp)
            
            # use LCV to determine the optimal value assignment for next_var
            next_var_val = self.lcv(csp, next_var)

            # assign the found value to relevant variable by reducing the domain
            # of next_var to only contain next_var_val
            D[next_var] = [next_var_val]

            # enforce arc consistency on the updated CSP
            solvable_here = self.ac3(csp)

            # if the CSP is not solvable here, return false
            if (not solvable_here):
                return False

            # update whether CSP is solved
            solved = self.is_solved(csp)

        # return whether or not the CSP is solved
        return solved

    def solve(self, csp):
        """
        Given a CSP csp, solves the CSP and returns a dictionary:
            variable -> value assignment
        If the given CSP is not solvable, returns an empty dictionary.
        """
        # separate and store the components of a CSP
        (V, D, C) = csp

        # initialize the solution map
        solutions = {}

        # find the assignments for the variables in the CSP
        assignment_exists = self.exists_valid_assignment(csp)

        # iterate through variables
        for variable in V:
            # check if an assignment exists
            if assignment_exists:
                # get domain of value:
                this_domain = D[variable]

                # get value from assignment
                value = this_domain[0]

                # put it in the dictionary
                solutions[variable] = value
        
        # return the solutions dictionary
        return solutions
