from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Lemma, _WordNetObject
from nltk.stem.wordnet import WordNetLemmatizer
import graph, shortest_paths


def nuovo_equal(self, other):
    if isinstance(other, str) or isinstance(self, str):
        return False
    return self._name == other._name

_WordNetObject.__eq__ = nuovo_equal


#funzione modificata nell'integrazione con 1 2 e 3 al posto di low medium e high
def inner_function2(parola1, parola2, flag, level=2):
    if level == 1 and flag:
        num_iter = 5
        relazioni = restituisci_tutte(parola1, parola2, num_iter)
    elif level == 2 and flag:
        num_iter = 10
        relazioni = restituisci_tutte(parola1, parola2, num_iter)
    elif level == 3 and flag:
        num_iter = 15
        relazioni = restituisci_tutte(parola1, parola2, num_iter)
    elif level == 1 and not flag:
        num_iter = 5
        relazioni = restituisci_relazione(parola1, parola2, num_iter)
    elif level == 2 and not flag:
        num_iter = 10
        relazioni = restituisci_relazione(parola1, parola2, num_iter)
    elif level == 3 and not flag:
        num_iter = 15
        relazioni = restituisci_relazione(parola1, parola2, num_iter)
    else:
        relazioni = ""

    return relazioni


def restituisci_tutte(parola1, parola2, num_iter = 10):
    G, partenza, arrivo = crea_grafo(parola1, parola2, num_iter)
    risultati = []
    frase_finale = []

    print("Numero vertici Grafo: " + str(G.vertex_count()))
    print("Numero archi Grafo: " + str(G.edge_count()))

    f = ""
    for edge in  G.incident_edges(arrivo):
        cloud = shortest_paths.shortest_path_lengths(G, partenza, arrivo)
        tree = shortest_paths.shortest_path_tree(G, partenza, cloud)
        frase, ultimo_arco = costruisci_frase(tree, partenza, arrivo)

        for parola in frase:
            f += parola + " "

        if ultimo_arco is not None:
            ultimo_arco._element = float("inf")

        risultati.append(f)
        f = ""

    for frase in risultati:
        frase_finale += [frase + "\n\n"]

    if risultati == []:
        frase_finale = ["No relations between these words."]

    return frase_finale


def restituisci_relazione(parola1, parola2, num_iter=6):
    G, partenza, arrivo = crea_grafo(parola1, parola2, num_iter)
    frase_finale = []

    print("Numero vertici Grafo: " + str(G.vertex_count()))
    print("Numero archi Grafo: " + str(G.edge_count()))

    #dijkstra
    cloud = shortest_paths.shortest_path_lengths(G, partenza, arrivo)
    tree = shortest_paths.shortest_path_tree(G, partenza, cloud)
    frase, tmp = costruisci_frase(tree, partenza, arrivo)

    for parola in frase:
        frase_finale += [parola + "\n"]

    return frase_finale


def crea_grafo(parola1, parola2, num_iter):
    #creo i primi collegamenti, i sinonimi
    all_ss = wn.synsets(parola1)

    #calcoliamo il fattore di normalizzazione per il calcolo dei pesi dei collegamenti
    fattore_di_normalizzazione = calcola_fattore_normalizzazione(all_ss, parola1);
    #print("fattore di normalizzazione: " + str(fattore_di_normalizzazione))

    G = graph.Graph()

    partenza = G.insert_vertex(parola1)
    arrivo = G.insert_vertex(parola2)

    for ss in all_ss:
        nodo = G.insert_vertex(ss)
        G.insert_edge(partenza, nodo, calcola_peso(ss, parola1), "that means") #SINONIMO
        find_target(G, nodo, arrivo)

    #funzione ricorsiva
    popola_grafo(G, all_ss, arrivo ,num_iter, fattore_di_normalizzazione**(1/3))

    return G, partenza, arrivo


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


def popola_grafo(G, all_ss, arrivo, num_iter, fattore_di_normalizzazione):

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
            tutti_collegamenti(G, precedente, arrivo, da_analizzare, analizzati, fattore_di_normalizzazione)
            da_analizzare.remove(ss)
            analizzati.add(ss)
        i += 1

    return


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


def calcola_peso(ss_partenza, parola):
    all_lemma = ss_partenza.lemmas()
    p = calcola_posizione_lemma(ss_partenza, parola)

    if p == -1:
        return 10 #valore di default che in teoria non capita mai

    c = all_lemma[p].count()
    if c == 0:
        c = 0.1
    peso = 1 / (c**(1/3))

    return peso


def find_target(G, nodo, arrivo):
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
             elif lemma._synset._pos == "v":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as verb: " + verbo)
             elif lemma._synset._pos == "r":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adverb: " + nome)
             else:
                 G.insert_edge(nodo, arrivo, 0.01, "intended as noun: " + nome)
             break
         elif lemma.name().lower() == verbo:
             if lemma._synset._pos == "a" or lemma._synset._pos == "s":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adjective: " + aggettivo)
             elif lemma._synset._pos == "r":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adverb: " + avverbio)
             else:
                G.insert_edge(nodo, arrivo, 0.01, "intended as verb: " + verbo)
             break
         elif lemma.name().lower() == aggettivo:
             if lemma._synset._pos == "r":
                 G.insert_edge(nodo, arrivo, 0.01, "intended as adverb: " + avverbio)
             else:
                G.insert_edge(nodo, arrivo, 0.01, "intended as adjective: " + aggettivo)
             break
         elif lemma.name().lower() == avverbio:
             G.insert_edge(nodo, arrivo, 0.01, "intended as adverb: " + avverbio)
             break
    return


def nuovo_collegamento(G, arrivo, precedente, new_ss, peso, stringa):
    nodo = G.insert_vertex(new_ss)
    G.insert_edge(precedente, nodo, peso, stringa)
    find_target(G, nodo, arrivo)
    return


def tutti_collegamenti(G, precedente, arrivo, da_analizzare, analizzati, fattore_di_normalizzazione):
    for new_ss in precedente.element().hypernyms():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 2/5*fattore_di_normalizzazione, "that is a particularization of")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().hyponyms():   #ANCHE TROPONYM
        nuovo_collegamento(G, arrivo, precedente, new_ss, 2/5*fattore_di_normalizzazione, "that generalizes")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().member_holonyms():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 1/5*fattore_di_normalizzazione, "that is a member of")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().part_holonyms():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 1/5*fattore_di_normalizzazione, "that is a part of")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().substance_holonyms():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 1/5*fattore_di_normalizzazione, "that is a component of")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().substance_meronyms():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 1/5*fattore_di_normalizzazione, "that is composed by")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().part_meronyms():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 1/5*fattore_di_normalizzazione, "that has in part a")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().member_meronyms():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 1/5*fattore_di_normalizzazione, "that has as a member a")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().entailments():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 1/5*fattore_di_normalizzazione, "that, as a verb, involves a")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().causes():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 2/5*fattore_di_normalizzazione, "that causes")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().also_sees():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 3/5*fattore_di_normalizzazione, "that has a correlation with")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().verb_groups():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 3/5*fattore_di_normalizzazione, "verb group")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    for new_ss in precedente.element().similar_tos():
        nuovo_collegamento(G, arrivo, precedente, new_ss, 3/5*fattore_di_normalizzazione, "that has a similar meaning to")
        if not analizzati.__contains__(new_ss):
            da_analizzare.add(new_ss)

    #Collegamenti lessicali
    if isinstance(precedente.element(), Lemma):
        array = [precedente.element()]
    else:
        array = precedente.element().lemmas()

    for lemma in array:
        for contrario in lemma.antonyms():
            nuovo_collegamento(G, arrivo, precedente, contrario, 1/5*fattore_di_normalizzazione, "that is the opposite of")
            if not analizzati.__contains__(contrario):
                da_analizzare.add(contrario)
        for rel_form in lemma.derivationally_related_forms():
            nuovo_collegamento(G, arrivo, precedente, rel_form, 1/5*fattore_di_normalizzazione, "that is a lexical form derived from")
            if not analizzati.__contains__(rel_form):
                da_analizzare.add(rel_form)


def costruisci_frase(tree, partenza, arrivo):
     if arrivo not in tree:
         print("There aren't any relations between these words")
         return ["There aren't any relations between these words."], None

     arco = tree[arrivo]
     path = ["to which the searched word refers: " + arrivo.element() + " (" +arco.label() +")"]

     ultimo_arco = arco
     curr = arco.opposite(arrivo)
     while curr in tree:
         if isinstance(curr.element(), Lemma):
             path.append(curr.element().name())
         else:
             path.append(curr.element().definition())
         arco = tree[curr]
         path.append(arco.label())
         curr = arco.opposite(curr)

     path.append(partenza.element())
     path.reverse()
     return path, ultimo_arco



#print(inner_function2("wet", "dry", True, 3))
#print(inner_function2("reserved", "engaged", True, 1))
