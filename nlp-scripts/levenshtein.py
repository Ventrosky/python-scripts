
synonyms = {
    "annullo" : ["dichiaro nullo","cancello","sopprimo","invalido","revoco","estinguo","abrogo","infirmo","casso","anniento","distruggo","sparisco","svanisco","dissolvo","annichilisco"],
    "saldo" : ["pagamento finale","ultima quota","ultima rata","resto","residuo","quietanza"]
    }

def minimumEditDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]

def findSynonyms(word):
    if word in synonyms.keys():
        return word
    findings = []
    for key, value in synonyms.items():
        findings.append((key, min(list(map(lambda x: minimumEditDistance(word, x), value)))))
    return min(findings, key=lambda p: p[1])    

print("annullo", findSynonyms("annullo"))
print("cancello", findSynonyms("cancelo"))
print("rata", findSynonyms("rata"))
print("cammello", findSynonyms("cammello"))
