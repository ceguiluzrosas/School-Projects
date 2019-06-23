import string
import math
import random

def read_text_from_file(filename):
    '''
    # input:  filename with text (corpus)
    # output: a string containing the text in the file
    '''
    fh = open("MCMC/"+filename, 'r')
    text = fh.read()
    fh.close()
    return text


def text_to_clean_list(text):
    '''
    input:  string
    output: list of all characters in the string, where every character
            that is not a letter is replaced with whitespace
    '''
    alphabet_list = list(string.ascii_lowercase)
    data = list(text.strip())
    for i in range(len(data)):
        data[i] = data[i].lower()
        if data[i] not in alphabet_list and data[i] != " ":
            data[i] = " "
    return data


def calc_bigram_frequencies(corpus):
    '''
    input:  string of text (corpus)
    output: dictionary with bigrams (character pairs) as keys and
            counts (number of times a pair of characters, including
            whitespaces, appears in the text) as values
    '''
    res_dict = {}
    data = text_to_clean_list(corpus)
    for i in range(len(data)-1):
        bigram = data[i]+data[i+1]
        if bigram in res_dict:
            res_dict[bigram] += 1
        else:
            res_dict[bigram] = 1
    return res_dict


def generate_random_key(key):
    '''
    input:  x, encryption key  (as a string of 26 letters)
    output: y, another encryption key obtained by switching a pair of letters in x
    '''
    ch1 = random.randint(0, 25)
    ch2 =  random.randint(0, 25)
    while ch1 == ch2: #the case where x and y are the same
        ch2 = random.randint(0, 25)
    new_key = list(key) #easy method to switch characters of str
    new_key[ch1], new_key[ch2] = new_key[ch2], new_key[ch1]
    return "".join(new_key)


def apply_key_on_text(text, key):
    '''
    input:  a string of text
    output: a string of text where every letter is substituted with its
            mapping acocording to the given key
    '''
    alpha = string.ascii_lowercase 
    mod_alpha = {k:alpha[num] for num, k in enumerate(key.lower())} 
    decoded_text = ""
    for ch in text:
        if ch not in mod_alpha: #mod_alpha has only alphabet, no punct or whitespace
            decoded_text += ch 
        else: 
            decoded_text += mod_alpha[ch]
    return decoded_text


def calc_log_score(encrypted_text, key, bigram_freqs_dict):
    '''
    input:  text (as a string), key (as a string), bigram_freqs_dict
    output: ln(Q(key))
    '''
    decrypted_text = apply_key_on_text(encrypted_text, key)
    log_score = 0
    data = text_to_clean_list(decrypted_text)
    denominator = len(bigram_freqs_dict) + sum([count for count in bigram_freqs_dict.values()])
    #denominator = (unique bigrams) + (Sum of all digrams' count)

    for i in range(len(data)-1): #Using Laplace Smoothing
        bigram = data[i]+data[i+1]
        if bigram not in bigram_freqs_dict:
            log_score += math.log(1/float(denominator))
        else:
            log_score += math.log((bigram_freqs_dict[bigram] + 1)/float(denominator))
    return log_score


def random_coin(p):
    '''
    input:  p between 0 and 1
    output: True with probability p, False with probability 1-p
    '''
    return random.uniform(0,1)<p


def MCMC_decrypt(n_iters, encrypted_text, bigram_freqs_dict):
    '''
    input:  n_iters (number of iterations to simulate the chain), encrypted_text (as a string),  bigram_freqs_dict
    output: decrypted text (as a string)
    '''
    current_key = string.ascii_lowercase # start from the key x=ABCDE...

    for i in range(n_iters):
        proposed_key = generate_random_key(current_key)
        log_score_current_key = calc_log_score(encrypted_text, current_key, bigram_freqs_dict)
        log_score_proposed_key = calc_log_score(encrypted_text, proposed_key, bigram_freqs_dict)
        acceptance_probability = min(1,math.exp(log_score_proposed_key - log_score_current_key))

        if random_coin(acceptance_probability):
            current_key = proposed_key
        if i%500==0:
            print ("iter",i,":",apply_key_on_text(encrypted_text,current_key)[0:99])

    return apply_key_on_text(encrypted_text,current_key)



if __name__ == "__main__":    

    random.seed(5)

    # text from Oliver Twist
    '''
    plain_text = "As Oliver gave this first proof of the free and proper \
action of his lungs, the patchwork coverlet which was carelessly flung \
over the iron bedstead, rustled; the pale face of a young woman was raised \
feebly from the pillow; and a faint voice imperfectly articulated the words, \
Let me see the child, and die. The surgeon had been sitting with his face \
turned towards the fire: giving the palms of his hands a warm and a rub alternately. \
As the young woman spoke, he rose, and advancing to the bed's head, said, \
with more kindness than might have been expected of him"
    '''

    # text from Harry Potter
    plain_text = "October arrived, spreading a damp chill over the grounds and into the castle. \
Madam Pomfrey, the nurse, was kept busy by a sudden spate of colds among the staff and students. \
Her Pepperup potion worked instantly, though it left the drinker smoking at the ears for several hours \
afterward. Ginny Weasley, who had been looking pale, was bullied into taking some by Percy. The steam  \
pouring from under her vivid hair gave the impression that her whole head was on fire. \
Raindrops the size of bullets thundered on the castle windows for days on end; the lake rose, \
the flower beds turned into muddy streams, and Hagrid's pumpkins swelled to the size of garden sheds. \
Oliver Wood's enthusiasm for regular training sessions, however, was not dampened, which was why Harry \
was to be found, late one stormy Saturday afternoon a few days before Halloween, returning to Gryffindor \
Tower, drenched to the skin and splattered with mud."


    encrypted_text = apply_key_on_text(plain_text, "XEBPROHYAUFTIDSJLKZMWVNGQC")

    corpus = read_text_from_file('war_and_peace.txt')

    bigram_freqs_dict = calc_bigram_frequencies(corpus)

    decrypted_text = MCMC_decrypt(10000, encrypted_text, bigram_freqs_dict)

    print (decrypted_text)

