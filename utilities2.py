from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Lemma, _WordNetObject
from nltk.stem.wordnet import WordNetLemmatizer
import tkinter as tk
import graph, shortest_paths
import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from nltk.corpus import wordnet as wn
import operator
from spacy_wordnet.wordnet_domains import get_domains_for_synset, Wordnet
from gerarchia_domini import lista_domini_padre

def nuovo_equal(self, other):
    if isinstance(other, str) or isinstance(self, str):
        return False
    return self._name == other._name

_WordNetObject.__eq__ = nuovo_equal


#funzione modificata nell'integrazione con 1 2 e 3 al posto di low medium e high
def inner_function2_second(parola1, parola2, pos1, pos2,index_list, paragraph_list, level = 2):
    paragrafo = recupera_paragrafo(pos1, pos2,index_list,paragraph_list)
    if paragrafo is None:
        return ["please select two words of the same paragraph"]
    relazioni = restituisci_relazione(parola1, parola2, paragrafo, level*5)
    return relazioni


def recupera_paragrafo(start_index_word1,start_index_word2,index_list,paragraph_list):

    paragrafo = None
    start_index_word1 = int(start_index_word1.split('.')[0])
    start_index_word2 = int(start_index_word2.split('.')[0])

    if start_index_word1 <= start_index_word2:
        minor = start_index_word1
        major = start_index_word2
    else:
        minor = start_index_word2
        major = start_index_word1


    for i in range(0, index_list.__len__()-1):
        string_index_prev = index_list[i]
        string_index_succ = index_list[i+1]
        index_prev = int(string_index_prev.split('.')[0])
        index_succ = int(string_index_succ.split('.')[0])
        if index_prev <= minor <= index_succ:
            if index_prev <= major <= index_succ:
                #paragrafo trovato all'indice i
                paragrafo = paragraph_list[i]
                break
            else:
                #le due parole non fanno parte dello stesso paragrafo
                print("Parole non dello stesso paragrafo")

    if paragrafo is not None:
         print("\n----------PARAGRAFO----------------\n" + paragrafo + "\n---------------------------\n")

    return paragrafo



def restituisci_relazione(parola1, parola2, paragrafo, num_iter):
    flag = False
    G, partenza, arrivo = None, None, None
    domini_parole = calcola_domini(parola1,parola2, paragrafo)

    print(domini_parole[0])
    if domini_parole[0] is None:
        frase_finale = ["There aren't any relations between these words, no domains found."]
    else:
        for d in domini_parole:
            print(d)
            G, partenza, arrivo, flag = crea_grafo(parola1, parola2, num_iter, d)
            if flag:
                break

        if flag:
            frase_finale = ["Domain of interest: " + G.restituisci_max_dominio() + "\n"]

            print("Numero vertici Grafo: " + str(G.vertex_count()))
            print("Numero archi Grafo: " + str(G.edge_count()))

            #dijkstra
            cloud = shortest_paths.shortest_path_lengths(G, partenza, arrivo)
            tree = shortest_paths.shortest_path_tree(G, partenza, cloud)
            frase, tmp = costruisci_frase(tree, partenza, arrivo)

            # for parola in frase:
            #     frase_finale += parola
            frase_finale += frase

        else:
            frase_finale = ["There aren't any relations between these words."]

    return frase_finale


def crea_grafo(parola1, parola2, num_iter, dominio):
    flag = False

    #creo i primi collegamenti, i sinonimi
    all_ss = wn.synsets(parola1)

    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(WordnetAnnotator(nlp.lang))

    G = graph.Graph()

    partenza = G.insert_vertex(parola1)
    arrivo = G.insert_vertex(parola2)

    valid_ss = []

    print(dominio)
    for ss in all_ss:
        domini_ss = get_domains_for_synset(ss)
        padri_dominio = lista_domini_padre(dominio)
        for d in padri_dominio:
            if d not in domini_ss:
                continue
            nodo = G.insert_vertex(ss, dominio=d)
            valid_ss.append(ss)
            G.insert_edge(partenza, nodo, 1, "that means") #SINONIMO
            flag = find_target(G, nodo, arrivo)
            break

    #funzione ricorsiva
    flag2 = popola_grafo(G, valid_ss, arrivo, num_iter, dominio)
    return G, partenza, arrivo, flag or flag2


def calcola_fattore_normalizzazione(all_ss, parola):
    nome = WordNetLemmatizer().lemmatize(parola, 'n')
    verbo = WordNetLemmatizer().lemmatize(parola, 'v')
    aggettivo = WordNetLemmatizer().lemmatize(parola, 'a')
    avverbio = WordNetLemmatizer().lemmatize(parola, 'r')

    fattore = 0.1
    for ss in all_ss:
        for l in ss.lemmas():
            if l.name().lower() == nome.lower() or l.name().lower() == verbo.lower() \
                    or l.name().lower() == aggettivo.lower() or l.name().lower() == avverbio.lower():
                if l.count() > fattore:
                    fattore = l.count()

    return fattore


def popola_grafo(G, all_ss, arrivo, num_iter, dominio):
    flag = False
    analizzati = set()
    da_analizzare = set()
    for ss in all_ss:
        da_analizzare.add(ss)

    i = 0
    while i < num_iter:
        supporto = []
        for tmp in da_analizzare:
            supporto.append(tmp)

        for ss in supporto:
            precedente = G.insert_vertex(ss)
            if tutti_collegamenti(G, precedente, arrivo, da_analizzare, analizzati, dominio):
                flag = True
            da_analizzare.remove(ss)
            analizzati.add(ss)
        i += 1

    return flag


def calcola_posizione_lemma(ss, parola):

    nome =  WordNetLemmatizer().lemmatize(parola,'n')
    verbo =  WordNetLemmatizer().lemmatize(parola,'v')
    aggettivo =  WordNetLemmatizer().lemmatize(parola,'a')
    avverbio =  WordNetLemmatizer().lemmatize(parola,'r')

    i = 0
    for l in ss.lemmas():
        if l.name().lower() == nome.lower() or l.name().lower() == verbo.lower()\
                or l.name().lower() == aggettivo.lower() or l.name().lower() == avverbio.lower():
            return i
        i += 1

    return -1


def find_target(G, nodo, arrivo):
    flag = False

    if isinstance(nodo.element(), Lemma):
        array = [nodo.element()]
    else:
        array = nodo.element().lemmas()

    nome = WordNetLemmatizer().lemmatize(arrivo.element(), 'n').lower()
    verbo = WordNetLemmatizer().lemmatize(arrivo.element(), 'v').lower()
    aggettivo = WordNetLemmatizer().lemmatize(arrivo.element(), 'a').lower()
    avverbio = WordNetLemmatizer().lemmatize(arrivo.element(), 'r').lower()

    for lemma in array:
         if lemma.name().lower() == nome:
             if lemma._synset._pos == "a" or lemma._synset._pos == "s":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adjective: " + aggettivo)
                 flag = True
             elif lemma._synset._pos == "v":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as verb: " + verbo)
                 flag = True
             elif lemma._synset._pos == "r":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adverb: " + nome)
                 flag = True
             else:
                 G.insert_edge(nodo, arrivo, 0.01, "intended as noun: " + nome)
                 flag = True
             break
         elif lemma.name().lower() == verbo:
             if lemma._synset._pos == "a" or lemma._synset._pos == "s":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adjective: " + aggettivo)
                 flag = True
             elif lemma._synset._pos == "r":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adverb: " + avverbio)
                 flag = True
             else:
                G.insert_edge(nodo, arrivo, 0.01, "intended as verb: " + verbo)
                flag = True
             break
         elif lemma.name().lower() == aggettivo:
             if lemma._synset._pos == "r":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adverb: " + avverbio)
                 flag = True
             else:
                G.insert_edge(nodo, arrivo, 0.01, "intended as adjective: " + aggettivo)
                flag = True
             break
         elif lemma.name().lower() == avverbio:
             G.insert_edge(nodo, arrivo, 0.01, "intended as adverb: " + avverbio)
             flag = True
             break
    return flag


def nuovo_collegamento(G, arrivo, precedente, new_ss, peso, stringa, dominio, analizzati, da_analizzare):
    flag = False

    if isinstance(new_ss, Lemma):
        nodo = G.insert_vertex(new_ss)
        G.insert_edge(precedente, nodo, peso, stringa)
        flag = find_target(G, nodo, arrivo)
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)
    else:
        domini_ss = get_domains_for_synset(new_ss)
        padri_dominio = lista_domini_padre(dominio)

        for d in padri_dominio:
            if d in domini_ss:
                nodo = G.insert_vertex(new_ss, dominio=d)
                G.insert_edge(precedente, nodo, peso, stringa)
                flag = find_target(G, nodo, arrivo)
                if not analizzati.__contains__(new_ss):
                    da_analizzare.add(new_ss)

                break

    return flag


def tutti_collegamenti(G, precedente, arrivo, da_analizzare, analizzati, dominio):
    flag = False
    for new_ss in precedente.element().hypernyms():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that is a particularization of", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().hyponyms():   #ANCHE TROPONYM
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that generalizes", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().member_holonyms():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that is a member of", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().part_holonyms():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that is a part of", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().substance_holonyms():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that is a component of", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().substance_meronyms():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that is composed by", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().part_meronyms():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that has in part a", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().member_meronyms():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that has as a member a", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().entailments():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that, as a verb, involves a", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().causes():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that causes", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().also_sees():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that has a correlation with", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().verb_groups():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "verb group", dominio, analizzati, da_analizzare):
            flag = True

    for new_ss in precedente.element().similar_tos():
        if nuovo_collegamento(G, arrivo, precedente, new_ss, 1, "that has a similar meaning to", dominio, analizzati, da_analizzare):
            flag = True

    #Collegamenti lessicali
    if isinstance(precedente.element(), Lemma):
        array = [precedente.element()]
    else:
        array = precedente.element().lemmas()

    for lemma in array:
        for contrario in lemma.antonyms():
            if nuovo_collegamento(G, arrivo, precedente, contrario, 1, "that is the opposite of", dominio, analizzati, da_analizzare):
                flag = True

        for rel_form in lemma.derivationally_related_forms():
            if nuovo_collegamento(G, arrivo, precedente, rel_form, 1, "that is a lexical form derived from", dominio, analizzati, da_analizzare):
                flag = True

    return flag


def costruisci_frase(tree, partenza, arrivo):
     if arrivo not in tree:
         print("There aren't any relations between these words")
         return [], None

     arco = tree[arrivo]
     path = ["to which the searched word refers: " + arrivo.element() + " (" +arco.label() +")"]

     ultimo_arco = arco
     curr = arco.opposite(arrivo)
     while curr in tree:
         if isinstance(curr.element(), Lemma):
             path.append(curr.element().name() + "\n")
         else:
             path.append(curr.element().definition() + "\n")
         arco = tree[curr]
         path.append(arco.label() + "\n")
         curr = arco.opposite(curr)

     path.append("\n" + partenza.element() + "\n")
     path.reverse()
     return path, ultimo_arco





def calcola_domini(word1: str,word2:str,phrase: str):

    # Loading the supported spacy model (between "es" and "en")
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe(WordnetAnnotator(nlp.lang))

    # Define the token that is the user's keyword that he wants to know the definition (in the particular context)
    token1 = nlp(word1)[0]
    type1_k = token1.pos_
    #if not (type1_k is 'NOUN' or type1_k is 'VERB' or type1_k is 'ADJ' or type1_k is 'INTJ' or type1_k is 'PROPN'):
    #    return [None,1]
    token2 = nlp(word2)[0]
    type2_k = token2.pos_
    #if not (type2_k is 'NOUN' or type2_k is 'VERB' or type2_k is 'ADJ' or type2_k is 'INTJ' or type2_k is 'PROPN'):
    #    return [None, 1]


    # Define the sentence that is the user's phrase in which there is the token
    sentence = nlp(phrase)

    #domains 1
    token1_domains = token1._.wordnet.wordnet_domains()
    if (len(token1_domains) == 0):
        return [None, 1]
    #domains 2
    token2_domains = token2._.wordnet.wordnet_domains()
    if (len(token2_domains) == 0):
        return [None, 1]

    print(token2_domains)
    print(token1_domains)

    #common domains
    c_domains = []
    for d in token1_domains:
        if d in token2_domains:
            c_domains.append(d)

    token_domains_dict = {c_domains[i]: 0 for i in range(0, len(c_domains), 1)}

    # For each word in the sentence
    for sentence_token in sentence:
        type = sentence_token.pos_
        #if type is 'NOUN' or type is 'VERB' or type is 'ADJ' or type is 'INTJ' or type is 'PROPN':
        # Retrieve the list of domains of the given token
        list_domains = sentence_token._.wordnet.wordnet_domains()
        # Cicle on the list: if a domain is in the list of the token's list then the integer value is incremented
        encountered_domains = []
        for i in list_domains:
            if i in c_domains and not (i in encountered_domains):
                token_domains_dict[i] += 1
                encountered_domains.append(i)

    final_dict = sorted(token_domains_dict.items(), key=operator.itemgetter(1), reverse=True)

    print("________________________________________________________")
    print(token_domains_dict.items())

    list = []
    for i in final_dict:
        list.append(i[0])


    return list


