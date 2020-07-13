# Easy data augmentation techniques for text classification
# Jason Wei and Kai Zou

from eda_cn import eda
#arguments to be parsed from command line
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True, type=str, help="要增强的文本文件")
ap.add_argument("--output", required=False, type=str, help="要输出的增强文本文件的名称，非必须")
ap.add_argument("--num_aug", required=False, default=9, type=int, help="对于文本文件，每个句子生成的增强句子的个数")
ap.add_argument("--alpha", required=False, type=float, help="每个句子单词变更的百分比")
ap.add_argument("--sim_alpha", required=False, default=0.8, type=float, help="用于近义词寻找时，2个词的余弦相似度，相似度在这个阈值内才进行替换,或插入")
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

#使用EDA生成数据, 去掉了默认的标签\t加文本的格式，默认都是文本
def gen_eda(train_orig, output_file, alpha, num_aug=9, sim_alpha=0.8):

    lines = open(train_orig, 'r').readlines()
    for i, sentence in enumerate(lines):
        #调用eda生成sentence，生成后得到新的句子aug_sentences,aug_sentences是一个列表
        aug_sentences = eda(sentence, alpha_sr=alpha, alpha_ri=alpha, alpha_rs=alpha, p_rd=alpha, num_aug=num_aug, sim_alpha=sim_alpha)
        for idx, aug_sentence in enumerate(aug_sentences):
            with open(str(idx)+ '_'+ output_file, 'a+') as file:
                file.write(aug_sentence+'\n')

    print("用eda生成的句子 " + train_orig + " 生成至 " + output_file + " 生成个数=" + str(num_aug))

#main function
if __name__ == "__main__":

    #eda生成
    gen_eda(args.input, output, alpha=alpha, num_aug=num_aug, sim_alpha=args.sim_alpha)