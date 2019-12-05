#Library import
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from nltk.corpus import wordnet as wn
from spacy_wordnet.__utils__ import *
from spacy_wordnet.wordnet_domains import get_domains_for_synset

def findDefinition(word: str,phrase: str,word_index: int):

    # Loading the supported spacy model (between "es" and "en")
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(WordnetAnnotator(nlp.lang))

    # Define the token that is the user's keyword that he wants to know the definition (in the particular context)
    token = nlp(word)[0]
    # Define the sentence that is the user's phrase in which there is the token
    sentence = nlp(phrase)

    # From WordNet Domains retrieve all the token's domains
    token_domains = token._.wordnet.wordnet_domains()
    token_syn = wn.synsets(token.text)
    if (len(token_domains) == 0):
        if(len(token_syn) == 0):
            return [['No definition found'],1]
        return [[token_syn[0]._pos.upper() + ' - ' + token_syn[0].definition()],0]
    #Support structures
    token_domains_dict = {token_domains[i]: 0 for i in range(0, len(token_domains), 1)}     # Convert the list into a dictionary (domain,int)
    max_token_domains = []                                                                  #list of frequent domains
    synset_dict = dict()                                                                    #synsets dictionary
    max_synset_list = []                                                                    #list of frequent synsets
    def_list = []                                                                           #definitions list
    # For each word in the sentence
    for sentence_token in sentence:
        type = sentence_token.pos_
        if word_index == sentence_token.idx:
            type_k = type

        # Retrieve the list of domains of the given token
        list_domains = sentence_token._.wordnet.wordnet_domains()
        # Cicle on the list: if a domain is in the list of the token's list then the integer value is incremented
        encountered_domains = []
        for i in list_domains:
            if i in token_domains and not (i in encountered_domains):
                token_domains_dict[i] += 1
                encountered_domains.append(i)

    # Take the max repeated domain/s
    # Find item with Max Value in Dictionary
    itemMaxValue = max(token_domains_dict.items(), key=lambda x: x[1])
    for key, value in token_domains_dict.items():
        if value == itemMaxValue[1]:
            max_token_domains.append(key)
    # Retrieve the synset that is repeated frequently
    for j in max_token_domains:
        verified_pos = verify_pos(type_k)
        synsets = all_the_synsets(token.text, verified_pos, [j])
        if len(synsets) == 0:
            synsets = all_the_synsets(token.text, None,[j])
            all_syn = wn.synsets(token.text, verified_pos)
            if len(all_syn) != 0:
                synsets.append(all_syn[0])
        for i in synsets:
            if i not in synset_dict:
                synset_dict[i] = 1
            else:
                synset_dict[i] += 1
    #Max value in the dictionary, that we use to search frequent items
    max_synset = max(synset_dict.items(), key=lambda x: x[1])
    for key, value in synset_dict.items():
        if value == max_synset[1]:  #fare controllo tipo sinset e token
            max_synset_list.append(key)
    if (max_synset[1]-1) != 0 and len(max_synset_list) == 1:
        for key, value in synset_dict.items():
            if value == max_synset[1]-1:
                max_synset_list.append(key)

    #List of definitions
    for k in max_synset_list:
        def_list.append(k._pos.upper() + ' - ' + k.definition())
    return [def_list,0]


def has_domains(synset: Synset, domains: List[str]) -> bool:
    return not set(domains).isdisjoint(get_domains_for_synset(synset))


def all_the_synsets(word: str, pos, domains: [str]):
    return [ss for ss in wn.synsets(word, pos) if has_domains(ss, domains)]


def verify_pos(type: str):
    if type == "NOUN":
        return wn.NOUN
    elif type == "VERB":
        return wn.VERB
    elif type == "ADJ":
        return wn.ADJ
    else:
        return None




if __name__ == "__main__":
    word = 'plays'
    phrase = 'Every musician only sees the notes that he or she plays, marco likes to listen plays, she play the guitar'
    definition = findDefinition(word, phrase,17)
    print(definition)
