from rdflib import SKOS, Graph, Literal, RDF, RDFS, URIRef, Namespace
from rdflib.namespace import FOAF , XSD
from uuid import uuid4

def lag_forfatter(namn):
    namn_literal = Literal(namn)
    forfatter_id = f"{tnd}{namn.replace(' ', '-')}"

    forfattar_type = URIRef(tnp.Forfattar)
    forfattar = URIRef(forfatter_id)

    g.add((forfattar, RDF.type, forfattar_type))
    g.add((forfattar, SKOS.prefLabel, namn_literal))

    return forfatter_id


def lag_notat(forfatter, tittel):
    notat_id = f"{tnd.notat}-{uuid4()}"
    notat = URIRef(notat_id)

    g.add((notat, tnp.skrevetAv, URIRef(forfatter)))
    g.add((notat, SKOS.prefLabel, Literal(tittel)))
    g.add((notat, RDF.type, tnp.Notat))
    
    return notat_id

def skriv_notat(notat, tekst):
    g.add((URIRef(notat), RDFS.comment, Literal(tekst)))

if __name__ == "__main__":
    g = Graph()

    tnp = Namespace("https://tnp.example.com/ontologi#")
    tnd = Namespace("https://tnp.example.com/data#")

    g.bind("tnp", "https://tnp.example.com/ontologi#")
    g.bind("tnd", "https://tnp.example.com/data#")
    g.bind("skos", SKOS)

    forfatter = lag_forfatter("Markus AP")
    notat = lag_notat(forfatter, "Kult notat!")
    skriv_notat(notat, "#Kult notat\nDette er eit skikkeleg kult notat!")

    print(g.serialize(format="ttl"))