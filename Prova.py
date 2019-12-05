#Library import
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

#Loading the supported spacy model (between "es" and "en")
nlp = spacy.load('en')
nlp.add_pipe(WordnetAnnotator(nlp.lang))

#Define the token that is the user's keyword that he wants to know the definition (in the particular context)
token = nlp('wood')[0]
#Define the sentence that is the user's phrase in which there is the token
#sentence = nlp('So that cooled them down a little, because the people that’s always the most anxious for to hang a nigger that hain’t done just right is always the very ones that ain’t the most anxious to pay for him when they’ve got their satisfaction out of him.')
#sentence = nlp('The Dormouse had closed its eyes by this time, and was going off into a doze, but, on being pinched by the Hatter, it woke up again with a little shriek, and went on : that begins with an M, such as mousetraps, and the moon, and memory, and muchness—you know you say things are much of a muchness , did you ever see such a thing as a drawing of a muchness?')
sentence = nlp('Two roads diverged in a wood, and I, I took the one less travelled by, and that has made all the difference.')
#sentence = nlp('Marco plays videogames in his room.')

print("Sentence:")
print(sentence)
print("Keyword:")
print(token)

#From WordNet Domains retrieve all the token's domains
token_domains = token._.wordnet.wordnet_domains()

#Convert the list into a dictionary (domain,int)
token_domains_dict = {token_domains[i]: 0 for i in range(0, len(token_domains), 1)}

#For each word in the sentence
for sentence_token in sentence:
    type = sentence_token.pos_
    if type is 'NOUN' or type is 'VERB' or type is 'ADJ':
        #Retrieve the list of domains of the given token
        list_domains = sentence_token._.wordnet.wordnet_domains()
        #Cicle on the list: if a domain is in the list of the token's list then the integer value is incremented
        lista_vuota=[]
        for i in list_domains:
            if i in token_domains and not(i in lista_vuota):
                token_domains_dict[i] += 1
                lista_vuota.append(i)

print("All the domains with their repetitions")
print(token_domains_dict)
print("----------------------------------")

#Take the max repeated domain/s
max_token_domains = []
#Find item with Max Value in Dictionary
itemMaxValue = max(token_domains_dict.items(), key=lambda x: x[1])

for key, value in token_domains_dict.items():
    if value == itemMaxValue[1]:
        max_token_domains.append(key)

print("List of the domains repeated frequently")
print(max_token_domains)
print("----------------------------------")

#Retrieve the synset that is repeated frequently
synset_dict = dict()

for j in max_token_domains:
    synsets = token._.wordnet.all_the_synsets(token.text, [j])
    for i in synsets:
        if i not in synset_dict:
            synset_dict[i] = 1
        else:
            synset_dict[i] += 1

print("Synset Dictionary with repetitions:")
print(synset_dict)

max_synset = max(synset_dict.items(), key=lambda x: x[1])
max_synset_list = []
for key, value in synset_dict.items():
    if value == max_synset[1]:
        max_synset_list.append(key)

print("Frequently repeated Synsets:")
print(max_synset_list)
print("----------------------------------")
print("Possible definitions:")
for k in max_synset_list:
    print(k.definition())