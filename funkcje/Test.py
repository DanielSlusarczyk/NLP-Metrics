from funkcje.Bleu import *
import warnings

import nltk.translate.bleu_score as BLEU
import matplotlib.pyplot as plt

def test(coco, cocoRes, evals, weights):
    warnings.filterwarnings('ignore')
    nmbOfTests = len(evals)
    
    # codeBleu - ntlkBleu
    res1 = []
    # codeBleu - cocoBleu
    res2 = []
    
    for test in range(0, nmbOfTests):
        imgId = evals[test]['image_id']

        annIds = coco.getAnnIds(imgIds=imgId)
        anns = coco.loadAnns(annIds)

        references = []
        for ann in anns:
            references.append(ann['caption'])

        annIds = cocoRes.getAnnIds(imgIds=imgId)
        anns = cocoRes.loadAnns(annIds)
        candidate = anns[0]['caption']

        # Własna implementacja
        bleu = Bleu(weights, references, candidate)
        codeBleu = round(bleu.result, 4)
        
        # COCO
        cocoBleu = round(evals[test]["Bleu_" + str(len(weights))], 4)
        
        # NTLK
        candidate = candidate.split()
        references = [ref.split() for ref in references]
        nltkBleu = round(BLEU.sentence_bleu(references, candidate, weights, smoothing_function=None), 4)

        res1.append(abs(codeBleu - nltkBleu))
        res2.append(abs(codeBleu - cocoBleu))

    
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(30,10))
    fig.suptitle('Test dla ' + str(nmbOfTests) + ' danych', fontsize=30)
    
    ax1.hist(res1, align="left")
    ax1.set_title('|Implementacja Bleu - NLTK Bleu|', fontsize=25)
    
    ax2.hist(res2, align="left")
    ax2.set_title('|Moje Bleu - coco Bleu|', fontsize=25)