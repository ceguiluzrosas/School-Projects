from NBC_methods import *
                        
class Consts:
    M = 2500

if __name__ == '__main__':

    # read training data
    spam_train_emails = read_data('EmailsData/spam-train')
    nonspam_train_emails = read_data('EmailsData/nonspam-train')

    # read testing data
    spam_test_emails = read_data('EmailsData/spam-test')
    nonspam_test_emails = read_data('EmailsData/nonspam-test')

    # Problem 1 -- find M most common words in the entire dataset
    vocab = find_common_words(spam_train_emails + \
                              nonspam_train_emails + \
                              spam_test_emails + \
                              nonspam_test_emails, Consts.M)
    assert len(vocab) == Consts.M  
    
    # Problem 4 -- estimate the probabilities p(w | spam), p(w | nonspam)
    #              for every word w in the vocabulary
    p_w_given_spam, p_w_given_nonspam = estimate_word_probs(vocab, spam_train_emails, \
                                                                   nonspam_train_emails)
    for i in xrange(Consts.M):
        assert p_w_given_spam[i] <= 1 and p_w_given_spam[i] >= 0
        assert p_w_given_nonspam[i] <= 1 and p_w_given_nonspam[i] >= 0

    # Problem 5 -- estimate the probability of being in each class
    #              (spam and nonspam) from the training data
    p_spam, p_nonspam = estimate_class_probs(spam_train_emails, nonspam_train_emails)
    assert p_spam <= 1 and p_spam >= 0
    assert p_nonspam <= 1 and p_nonspam >= 0   
 
    # Problem 6 -- classify test data and record the number of incorrect classifications
    incorrect = 0
    for email in spam_test_emails: 
        if classify(email, vocab, p_w_given_spam, p_w_given_nonspam, p_spam, p_nonspam) == 'nonspam':
            incorrect += 1
    for email in nonspam_test_emails:
        if classify(email, vocab, p_w_given_spam, p_w_given_nonspam, p_spam, p_nonspam) == 'spam':
            incorrect += 1

    print ("incorrect", incorrect)
