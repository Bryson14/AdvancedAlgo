"""
Here is a variant of one of the best known google interview questions: Given a dictionary D which contains a set of
 words (strings) and a string S, determine how many ways S can be made from concatenating any subset of words contained
  within D.
If D = {“cat”, “dog”, “jim”, “fred”, “jimmy”, “my”, ”ed”, ”ment”, “em”, “body”, “embodiment”, “ i”}
And S = “jimmy”, your code would return 2.
"""

def concat_set_dp(goal, D):
    if goal >= len(S):
        return 1
    pass


def concat_set(goal, D):
    # goal is met
    if goal == "":
        return 1
    # there's no more words in the list
    if not D:
        return 0

    sum = 0
    for i in range(len(D)):
        item = D[i]
        if goal.startswith(item):
            sum += concat_set(goal[len(item):], D[0: i] + D[i+1:])

    return sum


D = ["cat", "dog", "jim", "fred", "jimmy", "my", "ed", "ment", "em", "body", "embodiment", "i", "happy", 'h', 'app', 'y']
S = 'happy'
print(concat_set(S, D))
print(concat_set_dp(0, D))