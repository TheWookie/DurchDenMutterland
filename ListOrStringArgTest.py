

def test_one(*word_or_words):
    for word in word_or_words:
        print(word)
    print()
        
def test_two(*wordz):
    if "penis" in wordz:
        print("penis in wordz.")
    else:
        print("no d here!")
    print()
    
def test_three(*words):
    print(words)
    words = list(words)
    ''' tuples are immutable. I could remake the touple with list comprehension (which would
    be hella cooler), however, this seems to be a better solution. I can just use '.remove'
    which I hope has better performance than forcing an iteration. '''
    print(words)
    if "penis" in words:
        print("Removing penis.")
        words.remove("penis")
    print(words)
    
def test_four(first, *words):
    print(first)
    print(words)
    words = [x.upper() for x in words]
    '''list comprehension to convert a tupple of lowercase
    words into a list of uppercase words. bamf.''' 
    print(words)

def test_five(list_one, list_two):
    return set(list_one) <= set(list_two)

def test():
    'test_one("Caterwal", "Cantonese")'
    'test_two("cats", "va-gina", "penis")'
    'test_three("pants", "penis")'
    'test_four("lower", "case", "words")'
    print(test_five(["apple", "banana", "orange"], ["apple", "banana", "orange"]))
    print(test_five(["apple", "banana"], ["apple", "banana", "orange"]))
    print(test_five(["apple", "banana", "orange"], ["apple", "banana"]))
    print(test_five(["apple", "banana", "five"], ["apple", "banana", "orange"]))

if __name__ == '__main__':
    test()
