import glob
import math
import itertools
from operator import itemgetter

def read_data(folder_name):
    '''
    Input: folder_name - the name of the directory in which to look for txt files
    Output: list of emails (represetned as list of strings)
    '''
    res = []
    for file_name in glob.glob(folder_name + '/*.txt'):
        fh = open(file_name, 'r')
        data = fh.readline()
        fh.close()
        # email contains a list of words
        email = data.split(" ")
        res.append(email)
    return res



def create_dictionary(emails_list):
    '''
    Input: emails_list - list of emails (each email is a list of strings)
    Output: dictionary with all words and their respective count (integers) in
            that particular emails_list
    Note: I will use this function again for Problem 4 (estimated_word_probs)
    '''
    dic = {}
    list_of_words = list(itertools.chain(*emails_list))
    for word in list_of_words:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1
    return dic



def find_common_words(emails_list, M):
    '''
    Input: emails_list - list of emails (each email is a list of strings)
           M - number of common keywords to extract
    Output: list of M most common words in the email list
    '''
    
    vocab_dict = create_dictionary(emails_list)
                
    #dictionary to list and filtered by len(word)
    filtered_vocab = filter(lambda (word,count): len(word)>1, vocab_dict.items())

    #list in descending order and in word-only format
    vocab = map(lambda (word,count): word,
                sorted(filtered_vocab, key=itemgetter(1), reverse=True))
    
    return vocab[:M]



'''
Let |L| = |{spam, non-spam}| = 2 , and suppose |V| = M and 
n_max = length of longest email


Problem 2:
Assumtion: Assume (for a moment) that every word in an email is one of
the M vobulary words. 
Goal: Ensure that for every word in V there exists an email that has v
in every position of n_max

*** Under this assumption, the minimum number of training samples needed 
to train classifier is 2 * M. 

Consider the example of M = |{a,b,c,d,e,f}| = 6 and n_max = 2. 
For some arbitrary class y in L, 
            (a,a); (b,b); (c,c); (d,d); (e,e); (f,f)

Every word in V appears in all i-th positions of n_max. Therefore, 
for this class y, the Pr(X,y) is nonzero. Since there are two classes 
{spam, non-spam}, we multiply by 2. 



Problem 3:
*** Under the "bag of words" model, the minimum number of training sample 
needed to train classifier is 2 * [M / n_max]. 

Consider the example of M = |{a,b,c,d,e,f}| = 6 and n_max = 2.
For some arbitrary class y in L, 
                        (a,b); (c,d); (e,f)    

Because we ignore the position of words in an email, we do not have to
account for emails like (b,a), (d,c), (f,e) in calculating minimum number 
of traning samples. Since every word in V appears at least once, Pr(w|y) is 
non-zero. Finally because the probability of all possible w's in V has
to be non-zero for both classes y {spam and non-spam}, we multiply by 2.

'''



def estimate_class_probs(spam_train_emails, nonspam_train_emails):
    '''
    Input: spam_train_emails - list of training emails classified as spam
           nonspam_train_emails - list of training emails classified as nonspam
    Output: a tuple (p_spam, p_nonspam) corresponding to the estimated probability
            for a given email to be spam and nonspam respectively
    '''

    spam_emails = len(spam_train_emails)
    total_emails = spam_emails + len(nonspam_train_emails)
    p_spam = float(spam_emails)/float(total_emails)

    return p_spam, 1.-p_spam



def estimate_word_probs(vocab, spam_train_emails, nonspam_train_emails):
    ''' 
    Input: vocab - a vocabulary of key words
           spam_train_emails - list of training emails classified as spam
           nonspam_train_emails - list of training emails classified as nonspam
    Output: two lists of probabilities (p_w_given_spam, p_w_given_nonspam)
            where p_w_given_spam[i] is the estimated probability for word
            vocab[i] to appear in a spam email and similarly p_w_given_nonspam[i]
            for nonspam email
    '''
    M = len(vocab)
    p_w_given_spam = [ 0.0 for i in range(M) ]
    p_w_given_nonspam = [ 0.0 for i in range(M) ] 
   
    num_of_spam_words = sum([len(email) for email in spam_train_emails])
    num_of_nonspam_words = sum([len(email) for email in nonspam_train_emails])

    spam_words_and_counts = create_dictionary(spam_train_emails)
    nonspam_words_and_counts = create_dictionary(nonspam_train_emails)

    idx = 0
    for word in vocab:
        s_word_count = spam_words_and_counts[word] if word in spam_words_and_counts else 0
        ns_word_count = nonspam_words_and_counts[word] if word in nonspam_words_and_counts else 0

        p_w_given_spam[idx] += (s_word_count + 1.0)/(num_of_spam_words + M)
        p_w_given_nonspam[idx] += (ns_word_count + 1.0)/(num_of_nonspam_words + M)
        idx += 1

    return p_w_given_spam, p_w_given_nonspam



def classify(email, vocab, p_w_given_spam, p_w_given_nonspam, p_spam, p_nonspam):
    '''
    Input: email - an email to classify
           vocab - vocab - a vocabulary of key words
           p_w_given_spam - list of probabilities where p_w_given_spam[i]
                          is the estimated probability for word vocab[i]
                          to appear in a spam email  
           p_w_given_nonspam - similar to p_w_given_spam for nonspam
           p_spam - probability of a given email being spam
           p_nonspam - probability of a given email being nonspam
    Output: class label of the given email, either 'spam' or 'nonspam'
    '''

    log_p_x_given_spam = math.log(p_spam)
    log_p_x_given_nonspam = math.log(p_nonspam)

    for word in email:
        if word in vocab:
            idx = vocab.index(word)

            log_p_x_given_spam += math.log(p_w_given_spam[idx])
            log_p_x_given_nonspam += math.log(p_w_given_nonspam[idx])

    if log_p_x_given_spam > log_p_x_given_nonspam:
        return 'spam'
    return 'nonspam'

'''
Problem 6:
Out of the 260 test emails, 254 were classified correctly; 6 emails were 
classified incorrectly. 97.69% Success Rate
'''
