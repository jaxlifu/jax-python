#!/usr/bin/env python
# -*- coding: utf-8 -*-
import jieba
import gensim


def tranning():
    with open('hlm.txt', 'r', encoding='utf-8') as f:
        data = [line.strip() for line in f.readlines() if line.strip()]
        sentences = []
        for line in data:
            words = list(jieba.cut(line))
            sentences.append(words)
        with open('names.txt','w',encoding='utf-8') as namefile:
            namefile.write(str(sentences))
        model = gensim.models.Word2Vec(
            sentences, size=100, window=5, min_count=5, workers=4)
    return model
    pass


def find_relationship(tranning_model, a, b, c):
    d, _ = tranning_model.most_similar(positive=[c, b], negative=[a])[0]
    print('给定%s与%s的,%s和%s有类似的关系' % (a, b, c, d))
    pass


if __name__ == '__main__':
    model = tranning()
    for k, s in model.most_similar(positive=['宝钗']):
        print('{0}:{1}'.format(k, s))
    find_relationship(model,'王夫人','凤姐','薛姨妈')
