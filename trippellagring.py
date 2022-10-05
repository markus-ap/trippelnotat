from rdflib import SKOS, Graph, Literal, RDF, RDFS, DC, URIRef, Namespace, DCTERMS
from rdflib.namespace import FOAF, XSD
from datetime import datetime

def tilfeldig_suffix(lengde=4):
    from random import choice
    alfabet = "abcdefghijklmnopqrstuvwxyzæøå0123456789"
    alfabet += alfabet.upper()
    suffix = "".join([choice(alfabet) for i in range(lengde)])

    return suffix if suffix[0] != "-" else suffix[1:]

def lag_forfatter(namn):
    namn_literal = Literal(namn)
    forfatter_id = f"{tnd}{namn.replace(' ', '-')}"

    forfattar_type = URIRef(tnp.Forfattar)
    forfattar = URIRef(forfatter_id)

    g.add((forfattar, RDF.type, forfattar_type))
    g.add((forfattar, SKOS.prefLabel, namn_literal))

    return forfatter_id


def lag_notat(forfatter, tittel):
    no = datetime.now()
    
    notat_id = f"{tnd.notat}-{tilfeldig_suffix(8)}"
    notat = URIRef(notat_id)

    g.add((notat, DCTERMS.creator, URIRef(forfatter)))
    g.add((notat, DC.title, Literal(tittel)))
    g.add((notat, RDF.type, tnp.Notat))
    g.add((notat, DCTERMS.created, Literal(no, datatype=XSD.dateTime)))
    
    return notat_id

def skriv_notat(notat, tekst):
    notat_node = URIRef(notat)

    if (notat_node, None, None) in g:
        g.add((notat_node, RDFS.comment, Literal(tekst)))
    else:
        raise Exception(f"{notat} fins ikkje i graf.")

def lagre_graf():
    fil = open("rdf.ttl", "w", encoding="utf8")
    fil.write(g.serialize(format="ttl"))

if __name__ == "__main__":
    g = Graph()

    tnp = Namespace("https://tnp.example.com/ontologi#")
    tnd = Namespace("https://tnp.example.com/data#")

    g.bind("tnp", "https://tnp.example.com/ontologi#")
    g.bind("tnd", "https://tnp.example.com/data#")
    g.bind("dc", DC)
    g.bind("dcterms", DCTERMS)
    g.bind("skos", SKOS)

    forfatter = lag_forfatter("Markus AP")
    notat = lag_notat(forfatter, "Kult notat!")
    skriv_notat(notat, "#Kult notat\nDette er eit skikkeleg kult notat!")

    lagre_graf()