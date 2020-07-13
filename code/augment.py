# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou

from eda import *

#arguments to be parsed from command line
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="要增强的文本文件")
ap.add_argument("--output", required=False, type=str, help="要输出的增强文本文件的名称，非必须")
ap.add_argument("--num_aug", required=False, type=int, help="对于文本文件，每个句子生成的增强句子的个数")
ap.add_argument("--alpha", required=False, type=float, help="每个句子单词变更的百分比")
args = ap.parse_args()

#如果不指定输出格式，默认为eda_ 加上原始文件名
output = None
if args.output:
    output = args.output
else:
    from os.path import dirname, basename, join
    output = join(dirname(args.input), 'eda_' + basename(args.input))

#默认每个句子增强的句子个数是9个
num_aug = 9 #default
if args.num_aug:
    num_aug = args.num_aug

#默认每个句子中单词的更改的百分比是10%
alpha = 0.1#default
if args.alpha:
    alpha = args.alpha

#使用EDA生成数据
def gen_eda(train_orig, output_file, alpha, num_aug=9):

    writer = open(output_file, 'w')
    lines = open(train_orig, 'r').readlines()
    #对于是label \t sentence格式的文件进行处理，只处理sentence部分
    for i, line in enumerate(lines):
        parts = line[:-1].split('\t')
        label = parts[0]
        sentence = parts[1]
        #调用eda生成sentence，生成后得到新的句子aug_sentences,aug_sentences是一个列表
        aug_sentences = eda(sentence, alpha_sr=alpha, alpha_ri=alpha, alpha_rs=alpha, p_rd=alpha, num_aug=num_aug)
        for aug_sentence in aug_sentences:
            writer.write(label + "\t" + aug_sentence + '\n')

    writer.close()
    print("用eda生成的句子 " + train_orig + " to " + output_file + " with num_aug=" + str(num_aug))

#main function
if __name__ == "__main__":

    #eda生成
    gen_eda(args.input, output, alpha=alpha, num_aug=num_aug)