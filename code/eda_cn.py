# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou

import random
from random import shuffle
from typing import List
import synonyms

random.seed(1)

# 停止词列表
#synonyms包含停止词处理, synonyms/data/stopwords.txt

# 清理文本
import re

def get_only_chars(s):
    """
    :param s: 清洗爬取的中文语料格式
    :return:
    """
    import re
    from string import digits, punctuation
    rule = re.compile(u'[^a-zA-Z.,;《》？！“”‘’@#￥%…&×（）——+【】{};；●，。&～、|\s:：' + digits + punctuation + '\u4e00-\u9fa5]+')
    s = re.sub(rule, '', s)
    ###处理文本重复符号的表达，如替换多个。！.
    s = re.sub('[、]+', '，', s)
    s = re.sub('\'', '', s)
    s = re.sub('[#]+', '，', s)
    s = re.sub('[?]+', '？', s)
    s = re.sub('[;]+', '，', s)
    s = re.sub('[,]+', '，', s)
    s = re.sub('[!]+', '！', s)
    s = re.sub('[.]+', '.', s)
    s = re.sub('[，]+', '，', s)
    s = re.sub('[。]+', '。', s)
    s = s.strip().lower()
    return s


########################################################################
# Synonym replacement 近义词替换
# 通过wordnet替换近义词
########################################################################

# 近义词替换，需要安装synonyms
#pip install synonyms

def synonym_replacement(words, n, sim_alpha):
    """
    替换近义词
    :param words: 单词列表
    :param n: 替换n个单词
    :return:
    """
    new_words = words.copy()
    #去重后的单词列表
    random_word_list = list(set(words))
    #混淆打乱
    random.shuffle(random_word_list)
    num_replaced = 0
    for random_word in random_word_list:
        synonyms = get_synonyms(random_word, sim_alpha)
        if len(synonyms) >= 1:
            #获取近义词
            synonym = random.choice(list(synonyms))
            #对原始的句子中的单词进行近义词替换
            new_words = [synonym if word == random_word else word for word in new_words]
            # print("replaced", random_word, "with", synonym)
            num_replaced += 1
        # 只替换n个单词
        if num_replaced >= n:
            break
    return new_words


def get_synonyms(word, sim_alpha)-> List:
    """
    获取近义词,返回近义词列表
    :param word: 输入一个单词
    :param sim_alpha: 相似度阈值
    :return: 如果没找到近义词，直接返回
    """
    synonyms_words = []
    #获取近义词，我们筛选，获取相似度大于90%的单词
    words = synonyms.nearby(word)
    for word, simliary in zip(words[0], words[1]):
        if simliary > sim_alpha:
            synonyms_words.append(word)
    #若果近义词列表不为空
    if synonyms_words:
        #如果单词在近义词中，那么，从近义词列表中删除
        if word in synonyms_words:
            synonyms_words.remove(word)
        return list(synonyms_words)
    else:
        return [word]


########################################################################
# Random deletion 随机删除
# 以概率p的形式随机删除句子中的单词
########################################################################

def random_deletion(words, p):
    # 只有一个单词时，不删除
    if len(words) == 1:
        return words

    # 以概率p的形式随机删除句子中的单词
    new_words = []
    for word in words:
        #均匀分布，返回0到1之间的数
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    # 如果删掉了所有单词，随机返回一个单词
    if len(new_words) == 0:
        rand_int = random.randint(0, len(words) - 1)
        return [words[rand_int]]

    return new_words


########################################################################
# Random swap 随机交换
#随机交换句子中的单词n次
########################################################################

def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    return new_words


def swap_word(new_words):
    random_idx_1 = random.randint(0, len(new_words) - 1)
    random_idx_2 = random_idx_1
    counter = 0
    while random_idx_2 == random_idx_1:
        random_idx_2 = random.randint(0, len(new_words) - 1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1]
    return new_words


########################################################################
# Random insertion 随机插入
# 随机插入n个词到句子中
########################################################################

def random_insertion(words, n, sim_alpha):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words, sim_alpha)
    return new_words

def add_word(new_words, sim_alpha):
    """
    插入的是近义词
    :param new_words: 新的单词列表
    :param sim_alpha: 余弦相似度
    :return:
    """
    synonyms = []
    counter = 0
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words) - 1)]
        synonyms = get_synonyms(random_word, sim_alpha)
        counter += 1
        if counter >= 10:
            return
    random_synonym = synonyms[0]
    random_idx = random.randint(0, len(new_words) - 1)
    new_words.insert(random_idx, random_synonym)


########################################################################
# 数据增强主函数
########################################################################

def eda(sentence, alpha_sr=0.1, alpha_ri=0.1, alpha_rs=0.1, p_rd=0.1, num_aug=9, sim_alpha=0.8):
    """

    :param sentence:  输入句子
    :param alpha_sr: 随机替换的每个句子单词变更的百分比
    :param alpha_ri: 随机插入的每个句子单词变更的百分比
    :param alpha_rs:  随机交换的每个句子单词变更的百分比
    :param p_rd:   随机删除的概率
    :param num_aug:   生成的增强句子的个数
    :return:
    """
    # 句子清理
    sentence = get_only_chars(sentence)
    #分词, 只获取分词结果
    words = synonyms.seg(sentence)[0]
    #过滤掉空字符
    words = [word for word in words if word != '']
    num_words = len(words)

    #增强后的句子存储列表
    augmented_sentences = []
    num_new_per_technique = int(num_aug / 4) + 1
    #计算出每种的操作的数字
    n_sr = max(1, int(alpha_sr * num_words))
    n_ri = max(1, int(alpha_ri * num_words))
    n_rs = max(1, int(alpha_rs * num_words))

    # sr 随机替换
    for _ in range(num_new_per_technique):
        a_words = synonym_replacement(words, n_sr, sim_alpha)
        augmented_sentences.append(' '.join(a_words))

    # ri 随机插入
    for _ in range(num_new_per_technique):
        a_words = random_insertion(words, n_ri, sim_alpha)
        augmented_sentences.append(' '.join(a_words))

    # rs 随机交换
    for _ in range(num_new_per_technique):
        a_words = random_swap(words, n_rs)
        augmented_sentences.append(' '.join(a_words))

    # rd 随机删除
    for _ in range(num_new_per_technique):
        a_words = random_deletion(words, p_rd)
        augmented_sentences.append(' '.join(a_words))

    #对生成后的句子也做清理
    augmented_sentences = [get_only_chars(sentence) for sentence in augmented_sentences]
    shuffle(augmented_sentences)

    # 保留num_aug个增强的句子，或者按比例保存
    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    # 把原始句子也加入进去，最后返回
    augmented_sentences.append(sentence)

    return augmented_sentences