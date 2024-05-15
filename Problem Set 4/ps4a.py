# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    n = len(sequence)
    solutions = []

    #start with a base case
    # if n == 1:
    #     solutions.append(sequence)
        

    # #next is our recursive case
    # else:
    #     sequence_minus_letter = sequence.replace(sequence[0],'')
    #     get_permutations(sequence_minus_letter)
    #     for perms in get_permutations(sequence_minus_letter):
    #         for i in range(len(perms)):
    #             solutions.append(perms[:i] + perms[i] + perms[n-i:])
    
    # return solutions

    # Base case: if the sequence is a single character, return it as the only permutation
    if len(sequence) == 1:
        return [sequence]
    
    # Recursive case
    permutations = []
    for i, char in enumerate(sequence):
        # Exclude the current character and get permutations of the remaining characters
        first = sequence[:i]
        second = sequence[i+1:]
        remaining_sequence = first + second
        for perm in get_permutations(remaining_sequence):
            # Prepend the current character to each permutation of the remaining characters
            permutations.append(char + perm)
    
    return permutations


    

if __name__ == '__main__':
#    #EXAMPLE
   example_input = 'abc'
   print('Input:', example_input)
   print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
   print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)

    

