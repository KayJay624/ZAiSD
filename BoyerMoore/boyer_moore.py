def last_occurrence(pattern, text):
    occurrences = {}
    for i, letter in enumerate(text):
        if (letter in pattern):
            if (not letter in occurrences):
                occurrences[letter] = i
        else:
            occurrences[letter] = -1

    return occurrences

def boyer_moore(text, pattern):
    results = []
    last = last_occurrence(pattern, text)
    #print("last:", last)
    m = len(pattern)
    n = len(text)
    i = m - 1
    j = m - 1
    while i < n:
        if pattern[j] == text[i]:
            if j == 0:
                results.append(i)  #jest dopasowanie
                i = i + m - min(j, 1 + last[text[i]])
                j = m - 1
            else:
                i -= 1
                j -= 1
        else:
            i = i + m - min(j, 1 + last[text[i]])
            j = m - 1 
    
    return results

def get_word(index, pattern, text):
    i = index
    while text[i] != ' ':
        i -= 1

    j = index + len(pattern)
    while text[j] != ' ':
        j +=1

    return text[i:j]

#################################################################

fname = "seneca.txt"
with open(fname) as f:
    text = f.read().replace('\n', ' ')
pattern = 'omne'

# text = 'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.'
# pattern = "lo"

results = boyer_moore(text, pattern)
print("Liczba wystąpień '",pattern,"': ", len(results))
#print("results: ", results)

for r in results:
    print(r, ":", get_word(r, pattern, text))

