import spacy
#nlp = spacy.load('en')
nlp = spacy.load("en_core_web_sm")

def addIfNotDuplicate(value, outputs):
    first, *middle, last = value.split()
    alreadyPresentInOutput = False
    for alreadyPresent in outputs:
        if alreadyPresent.endswith(last):
            alreadyPresentInOutput = True
    if not alreadyPresentInOutput:
        outputs.append(value)
    
def handleCompounds(compounds, amod, compoundsTracker):
    currentCompoundText = ""
    firstOne = True
    for token in compounds:
        if firstOne:
            adjectiveString = ""
            for adjectives in amod:
                if adjectives.head == token or adjectives.head == token.head:
                    adjectiveString = adjectiveString + adjectives.text
                    amod.remove(adjectives)
            if adjectiveString == "":        
                currentCompoundText = token.text + " " + token.head.text
            else:
                currentCompoundText = adjectiveString + " " + token.text + " " + token.head.text
            firstOne = False
        else:
            currentCompoundText = currentCompoundText + " " + token.head.text
    if currentCompoundText != "":
        #outputs.append(currentCompoundText)
        compoundsTracker[token.head] = currentCompoundText
    currentCompoundText = ""
    compounds = []

def getCoreIssues(text):
    nsubj = []
    amod = []
    neg = []
    dobj = []
    acomp = []
    compounds = []
    xcomp = []
    outputs = []
    rootWords = []
    importantNouns = []
    phrasalVerbs = {} 
    compoundsTracker = {}
    prt = []
    significantTokensFound = False 
    doc = nlp(text)
    for token in doc:
        if token.dep_ == "ROOT" and token.text == token.head.text:
            rootWords.append(token)
            
        if token.pos_ in ["PROPN"]:
            importantNouns.append(token)
            significantTokensFound = True

        if token.dep_ == "prt" and token.head.pos_ == "VERB" :
            phrasalVerbs[token.head.text] = token.head.text + " " + token.text
            prt.append(token)
            significantTokensFound = True

        if token.dep_ in ["nsubj", "nsubjpass", "nmod", "acl"]:
#            print(token.text, token.dep_, token.head.text, token.head.pos_,
#            [child for child in token.children])
 #       print(token.text, token.head.text)
            nsubj.append(token)
            significantTokensFound = True
            
        if token.dep_ == "amod" or token.dep_ == "advmod":
            amod.append(token)
            significantTokensFound = True
            
        if token.dep_ == "neg":
            neg.append(token)
            significantTokensFound = True
            
        if token.dep_ == "dobj":
            dobj.append(token)
            significantTokensFound = True
            
        if token.dep_ == "acomp":
            acomp.append(token)
            significantTokensFound = True
            
        if token.dep_ == "xcomp":
            dobj.append(token)
            significantTokensFound = True
            
        #Process Compounds directly
        if token.dep_ == "compound":
            compounds.append(token)
            significantTokensFound = True
        else:
            handleCompounds(compounds, amod, compoundsTracker)
            compounds =[]
    handleCompounds(compounds, amod, compoundsTracker)
    
    #Process nsubj nodes
    for token in nsubj:
        intermediateStr = ""
        # Handle negation
        for negToken in neg:
            if token.head == negToken.head: 
                intermediateStr = token.text + " " + negToken.text + " " + token.head.text

        if intermediateStr == "":
            if token.dep_ == "acl":
                intermediateStr = token.head.text + " " + token.text
            else:
                intermediateStr = token.text + " " + token.head.text
            #Check if nsubj related to a Compound
            compoundWord = compoundsTracker.get(token.head)
            if compoundWord is not None:
                for adjective in amod:
                    if adjective.head == token.head:
                        compoundWord = adjective.text + " " + compoundWord
                        amod.remove(adjective)

                intermediateStr = token.text + " " + compoundWord
                del compoundsTracker[token.head]
            #REMOVE DUPLICATE CODE, IF IT WORKS
            compoundWord = compoundsTracker.get(token)
            if compoundWord is not None:
                adjectiveCompoundStr = ""
                for adjective in amod:
                    if adjective.head == token.head:
                        if adjectiveCompoundStr == "":
                            adjectiveCompoundStr = adjective.text
                        else:
                            adjectiveCompoundStr = adjectiveCompoundStr + " " + adjective.text
                        amod.remove(adjective)

                intermediateStr = compoundWord + " " + token.head.text + " " + adjectiveCompoundStr
                del compoundsTracker[token]
                
        #Add Direct Object
        for dObjToken in dobj:
            if token.head == dObjToken.head: 
                #Check if associated with a Compound
                compoundWord = compoundsTracker.get(dObjToken)
                if compoundWord is not None:
                    intermediateStr = intermediateStr + " " + compoundWord
                    del compoundsTracker[dObjToken]
                else:
                #end new code
                    intermediateStr = intermediateStr + " " + dObjToken.text
                dobj.remove(dObjToken)
                
        #Add adjectival complement
        for acompToken in acomp:
            if token.head == acompToken.head: 
                intermediateStr = intermediateStr + " " + acompToken.text
                acomp.remove(acompToken)
                
        #Add adjective Modifiers complement
        for acompToken in amod:
            if token.head == acompToken.head: 
                intermediateStr = intermediateStr + " " + acompToken.text
                amod.remove(acompToken)

        #Add PRT (Phrasal Verbs), if associated with the Subject
        for phrasalVerb in prt:
            if token.head == phrasalVerb.head: 
                intermediateStr = intermediateStr + " " + phrasalVerb.text
                prt.remove(phrasalVerb)

        outputs.append(intermediateStr)

    #Process any standalone DirectObject nodes
    for token in dobj:
        intermediateStr = ""
        intermediateStr = token.head.text + " " + token.text  
        #outputs.append(intermediateStr)
        addIfNotDuplicate(intermediateStr, outputs)

    #Process amod nodes
    for token in amod:
        #Handle Amod only if it is not associated with an Adjective
        compoundWord = compoundsTracker.get(token.head)
        if compoundWord is None:
            #Restrict advmods to those related to a Noun
            if token.dep_ == "advmod" and token.pos_ not in ["NOUN", "PROPN"]:
                continue
            intermediateStr = ""
            intermediateStr = token.text + " " + token.head.text
            #outputs.append(intermediateStr)
            addIfNotDuplicate(intermediateStr, outputs)
        
    #Process Root nodes
    for token in rootWords:
        if significantTokensFound == False:
            outputs.append(token.text)
        
    #Process xcomp nodes
    for token in xcomp:
        intermediateStr = ""
        intermediateStr = token.text + " " + token.head.text
        #outputs.append(intermediateStr)
        addIfNotDuplicate(intermediateStr, outputs)
    
    #Check if Phrasal verbs (like Throwing-up) are in the output
    for key,val in phrasalVerbs.items():
        phrasalVerbFound = False
        for str in outputs:
            if key in str:
                phrasalVerbFound = True
        if not phrasalVerbFound:
            outputs.append(val)

    for key,val in compoundsTracker.items():
        addIfNotDuplicate(val, outputs)
        
    #Check if Proper Nouns are in the output
    for token in importantNouns:
        importantNounFound = False
        properNoun = token.text
        for str in outputs:
            if properNoun in str:
                importantNounFound = True
        if not importantNounFound:
            outputs.append(properNoun)

    return outputs

#print( getCoreIssues("microwave with no power") )
print( getCoreIssues("Cartridge showing bubbles"))