def last_occurrence(pattern, alphabet):
    occurrences = dict()
    for letter in alphabet:
        occurrences[letter] = pattern.rfind(letter)

    return occurrences

def boyer_moore(text, pattern):
    """Find occurrence of pattern in text."""
    results = []
    alphabet = set(text)
    print(alphabet)
    last = last_occurrence(pattern, alphabet)
    #print("last:", last)
    m = len(pattern)
    n = len(text)
    i = m - 1
    j = m - 1
    while i < n:
        if pattern[j] == text[i]:
            if j == 0:
                results.append(i)
                l = last[text[i]]
                i = i + m - min(j, 1+l)
                j = m - 1
            else:
                i -= 1
                j -= 1
        else:
            l = last[text[i]]
            i = i + m - min(j, 1+l)
            j = m - 1 
    
    return results



### TEST FUNCTION ###

if __name__ == '__main__':
        
    def show_match(text, pattern):
        #print('Text:  %s' % text)
        results = boyer_moore(text, pattern)
        print("results: ", results)
        # for p in results:
        #     print('Match: %s%s' % ('.'*p, pattern))

    fname = "seneca.txt"
    with open(fname) as f:
       text = f.read().replace('\n', ' ')
    
    #text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
    pattern = 'omne'
    show_match(text, pattern)
