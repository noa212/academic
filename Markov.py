# CS122 W'18: Markov models and hash tables
# Noa Ohcana

import sys
import math
import Hash_Table

HASH_CELLS = 57

class Markov:

    def __init__(self,k,s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        self.ht = Hash_Table.Hash_Table(HASH_CELLS, 0)
        self.k = k
        for i in range(len(s)):
            # should be helper but had trouble implementing
            if (i-self.k) < 0:
                key_front = s[i-self.k:]
                key_end = s[:i]
                key = s[i-self.k:] + s[:i]
                key_plus1 = s[i-self.k:] + s[:i+1]
            if (i-k) >= 0:
                key = s[i-self.k:i]
                key_plus1 = s[i-self.k:i+1]
            value = self.ht.lookup(key)
            value += 1
            value_plus1 = self.ht.lookup(key_plus1)
            value_plus1 += 1
            self.ht.update(key, value)
            self.ht.update(key_plus1, value_plus1)

    def log_probability(self,s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        '''
        # reach into the values, .count
        unique = ''.join(set(s))
        big_S = len(unique)
        total_log_prob = 0
        for i in range(len(s)):
            if (i-self.k) < 0:
                s_k_f = s[i-self.k:]
                s_k_e = s[:i]
                s_k = s_k_f + s_k_e
                little_N = self.ht.lookup(s_k)
                s_k_plus1 = s[i-self.k:] + s[:i+1]
                little_M = self.ht.lookup(s_k_plus1)
                numer = little_M + 1
                denom = little_N + big_S
                prob = math.log(numer/denom)
                total_log_prob += prob
            if (i-self.k) >= 0:
                s_k = s[i-self.k:i]
                little_N = self.ht.lookup(s_k)
                s_k_plus1 = s[i-self.k:i+1]
                little_M = self.ht.lookup(s_k_plus1)
                numer = little_M + 1
                denom = little_N + big_S
                prob = math.log(numer/denom)
                total_log_prob += prob

        return total_log_prob

def identify_speaker(speech1, speech2, speech3, order):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the *normalized* log probabilities of each of the 
    speakers uttering that text under a "order" order character-based Markov 
    model, and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''

    model1 = Markov(order, speech1)
    total_prob1 = model1.log_probability(speech3)
    s1_length = len(speech3)
    normalizedp1 = total_prob1/s1_length

    model2 = Markov(order, speech2)
    total_prob2 = model2.log_probability(speech3)
    s2_length = len(speech3)
    normalizedp2 = total_prob2/s2_length

    if normalizedp1 > normalizedp2:
        more_likely = "A"
    elif normalizedp1 < normalizedp2:
        more_likely = "B"

    return (normalizedp1, normalizedp2, more_likely)

def print_results(res_tuple):
    '''
    Given a tuple from identify_speaker, print formatted results to the screen
    '''
    (likelihood1, likelihood2, conclusion) = res_tuple
    
    print("Speaker A: " + str(likelihood1))
    print("Speaker B: " + str(likelihood2))

    print("")

    print("Conclusion: Speaker " + conclusion + " is most likely")


if __name__=="__main__":
    num_args = len(sys.argv)

    if num_args != 5:
        print("usage: python3 " + sys.argv[0] + " <file name for speaker A> " +
              "<file name for speaker B>\n  <file name of text to identify> " +
              "<order>")
        sys.exit(0)
    
    with open(sys.argv[1], "rU") as file1:
        speech1 = file1.read()

    with open(sys.argv[2], "rU") as file2:
        speech2 = file2.read()

    with open(sys.argv[3], "rU") as file3:
        speech3 = file3.read()

    res_tuple = identify_speaker(speech1, speech2, speech3, int(sys.argv[4]))

    print_results(res_tuple)
