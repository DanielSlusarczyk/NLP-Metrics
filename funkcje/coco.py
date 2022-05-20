from cocoCaption.pycocotools.coco import COCO
from cocoCaption.pycocoevalcap.eval import COCOEvalCap
import skimage.io as io
import pylab
import json
from json import encoder

def prepareCoco():
    
    encoder.FLOAT_REPR = lambda o: format(o, '.3f')

    # set up file names and pathes
    dataDir='.'
    dataType='val2014'
    algName = 'fakecap'
    annFile='%s/cocoCaption/annotations/captions_%s.json'%(dataDir,dataType)
    subtypes=['results', 'evalImgs', 'eval']
    [resFile, evalImgsFile, evalFile]= \
    ['%s/cocoCaption/results/captions_%s_%s_%s.json'%(dataDir,dataType,algName,subtype) for subtype in subtypes]

    # create coco object and cocoRes object
    coco = COCO(annFile)
    cocoRes = coco.loadRes(resFile)

    cocoEval = COCOEvalCap(coco, cocoRes)

    cocoEval.params['image_id'] = cocoRes.getImgIds()

    cocoEval.evaluate()
    
    return (coco, cocoRes, cocoEval)
