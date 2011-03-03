### Matt Caldwell
### References: http://www.cs.princeton.edu/courses/archive/fall04/cos126/assignments/markov.html
### 2004

from Graph import *
from random import uniform
from nltk.probability import FreqDist

class MarkovChain(Graph):
    """Graph representation of a Markov Chain.  The implementation is generic in order to
       provide scalable usage."""

    # define static class variables here
    MOST_LIKELY = 1
    LEAST_LIKELY = 2
    WEIGHTED = 3
    
    def __init__(self):
        Graph.__init__(self)

    def __repr__(self):
        return Graph.__repr__(self)

    def next(self, s, method = MOST_LIKELY):
        # Pick a transition leaving state s and return a state that would
        # likely follow.  The next state is chosen according to the method
        # specified.  The default is to choose and return the most likely
        # transition state.

        # determine all states adjacent to s
        transitions = self._adjacentVertices[s]
        freqDist = FreqDist()

        # determine the weights of the edges between state s and all adjacent states
        for state in transitions:
            freqDist.inc(state)

        if method == MarkovChain.MOST_LIKELY:
            return freqDist.max()

        elif method == MarkovChain.LEAST_LIKELY:
            # NLTK provides no built-in method to return the minimum of a
            # frequency distribution so for now, we get a list of samples
            # sorted in decreasing order and grab the last one.

            return freqDist.sorted_samples()[-1]

        else:
            # choose a real number between 0 and 1
            x = uniform(0,1)
            
            # choose next state based on weights of the edges.  Randomness plays a part here.
            for i in range(len(transitions)):
                probability = freqDist.freq(transitions[i])
             
                if x < probability:
                    return transitions[i]

                x = x - probability

            exc = "Error in MarkovChain.next().  Did not find next state.\n"
            raise exc
                    
# For testing and debugging purposes only
if __name__ == "__main__":
    chain = MarkovChain()
    chain.add('the','hes')
    chain.add('the','hes')
    chain.add('the','hes')
    chain.add('the','her')
    chain.add('the','her')
    print chain
    print chain.next('the', MarkovChain.MOST_LIKELY)
    print chain.next('the', MarkovChain.LEAST_LIKELY)
    print chain.next('the', MarkovChain.WEIGHTED)
