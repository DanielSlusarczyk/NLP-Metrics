from funkcje.Bleu import *
import warnings

import nltk.translate.bleu_score as BLEU
import matplotlib.pyplot as plt

def test(coco, cocoRes, evals, weights):
    warnings.filterwarnings('ignore')
    nmbOfTests = len(evals)
    epsilon = 0.06
    
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

        bleu = Bleu(weights, references, candidate)
        codeBleu = bleu.result
        
        cocoBleu = evals[test]["Bleu_" + str(len(weights))]

        candidate = candidate.split()
        references = [ref.split() for ref in references]
        ntlkBleu = BLEU.sentence_bleu(references, candidate, weights, smoothing_function=None)

        res1.append(abs(codeBleu - ntlkBleu))
        
        if(abs(codeBleu - cocoBleu) > epsilon):
            res2.append(abs(codeBleu - cocoBleu))
        else:
            res2.append(0)
    
    fig, (ax1,ax2) = plt.subplots(1,2,figsize=(30,10))
    fig.suptitle('Test dla ' + str(nmbOfTests) + ' danych', fontsize=30)
    
    ax1.hist(res1, align="left")
    ax1.set_title('|Moje Bleu - ntlk Bleu|', fontsize=25)
    
    ax2.hist(res2, align="left")
    ax2.set_title('|Moje Bleu - coco Bleu|', fontsize=25)