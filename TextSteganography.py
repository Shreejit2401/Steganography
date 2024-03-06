<<<<<<< HEAD
import json

with open('merged_dictionary.json', 'r') as file:
    d = json.load(file)
# print(len(list(d.items())))
new_pairs = {
        "this": "apple",
        "that": "dog",
        "there": "tree",
        "on": "table",
        "in": "box",
        "under": "bed",
        "above": "clouds",
        "between": "two",
        "among": "friends",
        "behind": "door",
        "below": "surface",
        "beneath": "ground",
        "beside": "tree",
        "at": "home",
        "by": "the",
        "for": "you",
        "from": "here",
        "to": "there",
        "with": "friends",
        "where": "here",
        "who": "me",
        "whom": "him",
        "whose": "mine",
        "when": "now",
        "which": "one",
        "why": "reason",
        "how": "way",
        "what": "thing",
        "while": "waiting",
        "before": "now",
        "after": "now",
        "since": "then",
        "during": "time",
        "until": "then",
        "upon": "arrival",
        "about": "topic",
        "across": "river",
        "against": "wall",
        "along": "road",
        "amid": "chaos",
        "around": "world",
        "as": "such",
        "before": "after",
        "behind": "front",
        "below": "above",
        "beneath": "above",
        "beside": "away",
        "between": "among",
        "beyond": "reach",
        "by": "with",
        "despite": "efforts",
        "down": "up",
        "except": "exclude",
        "for": "against",
        "from": "to",
        "in": "out",
        "inside": "outside",
        "into": "out",
        "like": "dislike",
        "near": "far",
        "of": "with",
        "off": "on",
        "on": "off",
        "out": "in",
        "outside": "inside",
        "over": "under",
        "past": "future",
        "regarding": "matter",
        "round": "square",
        "since": "before",
        "through": "around",
        "throughout": "limited",
        "to": "from",
        "toward": "away",
        "under": "over",
        "until": "after",
        "unto": "onto",
        "up": "down",
        "upon": "under",
        "with": "without",
        "within": "outside",
        "without": "with",
        # Add more prepositions and words as needed
    }
d.update(new_pairs)
# print(len(list(d.items())))


# with open('merged_dictionary.json', 'w') as file:
#     json.dump(d, file)

def first_replace_words(input_str):
    words = input_str.split()
    word_dict = d

    replaced_words = [word_dict.get(word, word) for word in words]  
    return ' '.join(replaced_words)  

def revert_words(input_str):
    reverse_word_dict = {v: k for k, v in d.items()}
    words = input_str.split()  
    replaced_words = [reverse_word_dict.get(word, word) for word in words]  
    return ' '.join(replaced_words)  


input_str = input()

output_str = first_replace_words(input_str)
print("first encrypted(Cover generated)::--> ",output_str)

recovered = revert_words(output_str)
print("Got orginial back::--> ",recovered)
=======
import json

with open('merged_dictionary.json', 'r') as file:
    d = json.load(file)
# print(len(list(d.items())))
new_pairs = {
        "this": "apple",
        "that": "dog",
        "there": "tree",
        "on": "table",
        "in": "box",
        "under": "bed",
        "above": "clouds",
        "between": "two",
        "among": "friends",
        "behind": "door",
        "below": "surface",
        "beneath": "ground",
        "beside": "tree",
        "at": "home",
        "by": "the",
        "for": "you",
        "from": "here",
        "to": "there",
        "with": "friends",
        "where": "here",
        "who": "me",
        "whom": "him",
        "whose": "mine",
        "when": "now",
        "which": "one",
        "why": "reason",
        "how": "way",
        "what": "thing",
        "while": "waiting",
        "before": "now",
        "after": "now",
        "since": "then",
        "during": "time",
        "until": "then",
        "upon": "arrival",
        "about": "topic",
        "across": "river",
        "against": "wall",
        "along": "road",
        "amid": "chaos",
        "around": "world",
        "as": "such",
        "before": "after",
        "behind": "front",
        "below": "above",
        "beneath": "above",
        "beside": "away",
        "between": "among",
        "beyond": "reach",
        "by": "with",
        "despite": "efforts",
        "down": "up",
        "except": "exclude",
        "for": "against",
        "from": "to",
        "in": "out",
        "inside": "outside",
        "into": "out",
        "like": "dislike",
        "near": "far",
        "of": "with",
        "off": "on",
        "on": "off",
        "out": "in",
        "outside": "inside",
        "over": "under",
        "past": "future",
        "regarding": "matter",
        "round": "square",
        "since": "before",
        "through": "around",
        "throughout": "limited",
        "to": "from",
        "toward": "away",
        "under": "over",
        "until": "after",
        "unto": "onto",
        "up": "down",
        "upon": "under",
        "with": "without",
        "within": "outside",
        "without": "with",
        # Add more prepositions and words as needed
    }
d.update(new_pairs)
# print(len(list(d.items())))


# with open('merged_dictionary.json', 'w') as file:
#     json.dump(d, file)

def first_replace_words(input_str):
    words = input_str.split()
    word_dict = d

    replaced_words = [word_dict.get(word, word) for word in words]  
    return ' '.join(replaced_words)  

def revert_words(input_str):
    reverse_word_dict = {v: k for k, v in d.items()}
    words = input_str.split()  
    replaced_words = [reverse_word_dict.get(word, word) for word in words]  
    return ' '.join(replaced_words)  


input_str = input()

output_str = first_replace_words(input_str)
print("first encrypted(Cover generated)::--> ",output_str)

recovered = revert_words(output_str)
print("Got orginial back::--> ",recovered)
>>>>>>> b503a805319117794273aa6f3e241a7149913ca4
