# EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks
[![Conference](http://img.shields.io/badge/EMNLP-2019-4b44ce.svg)](https://arxiv.org/abs/1901.11196)


# 改成中文的EDA
近义词获取的工具, 使用工具synonyms获取近义词或分次
pip install -U synonyms
# 测试方法
python code/augment_cn.py --input=zhongwen.txt --output=zhongwen_out.txt --num_aug=6


这是EMNLP-IJCNLP论文的代码 [EDA: Easy Data Augmentation techniques for boosting performance on text classification tasks.](https://arxiv.org/abs/1901.11196) 

介绍 EDA博客 [[here]](https://medium.com/@jason.20/these-are-the-easiest-data-augmentation-techniques-in-natural-language-processing-you-can-think-of-88e393fd610). 

By [Jason Wei](https://jasonwei20.github.io/research/) and Kai Zou.

我们介绍了EDA：轻松的数据增强技术，可提高文本分类任务的性能。这些是一组通用的数据增强技术，易于实施，并且在五个NLP分类任务上已显示出改进，对大小N <500的数据集也进行了很大提升。而其他技术则要求您仅在外部数据集上训练语言模型为了获得小幅提升，我们发现使用EDA进行简单的文本编辑操作可带来良好的性能提升。给定训练集中的句子，我们执行以下操作：

- 同义词替换（SR）：从句子中随机选择n个非停用词。用随机选择的一个同义词替换这些单词中的每个单词。
- 随机插入（RI）：在句子中找到不是停用词的随机词的随机同义词。将该同义词插入句子中的随机位置。这样做n次。
- 随机交换（RS）：在句子中随机选择两个单词并交换其位置。这样做n次。
- 随机删除（RD）：对于句子中的每个单词，以概率p随机删除它。

<p align="center"> <img src="eda_figure.png" alt="drawing" width="400" class="center"> </p>
关于使用和未使用EDA的5个数据集的平均性能对比（相对于所用训练数据的百分比）。
# 使用方法

您可以在不到5分钟的时间内运行EDA任何文本分类数据集。仅需两个步骤：

### 安装NLTK:

```bash
pip install -U nltk
```

下载 WordNet.
```bash
python
>>> import nltk; nltk.download('wordnet')
```

### 运行 EDA

您可以轻松地编写自己的实现，但是该实现采用label\tsentence（请注意\ t）格式的输入文件。因此，例如，您的输入文件应如下所示:

```
1   neil burger here succeeded in making the mystery of four decades back the springboard for a more immediate mystery in the present 
0   it is a visual rorschach test and i must have failed 
0   the only way to tolerate this insipid brutally clueless film might be with a large dose of painkillers
...
```

现在，将此输入文件放入data文件夹. 运行如下命令 

```bash
python code/augment.py --input=<insert input filename>
```

默认的输出文件名将eda_附加到输入文件名的前面，但是您可以使用--output指定自己的文件名。您还可以使用--num_aug（默认值为9）指定每个原始句子生成的扩充句子的数量。此外，您可以指定alpha参数，该参数大约表示将要更改的句子中单词的百分比（默认值为0.1或10％）。因此，例如，如果您的输入文件是sst2_train.txt，而您想输出到sst2_augmented.txt，并且每个原始句子生成16个增强句子，且alpha = 0.05，则可以执行以下操作：

```bash
python code/augment.py --input=sst2_train.txt --output=sst2_augmented.txt --num_aug=16 --alpha=0.05
```


注意，不论alpha设置为多少，每个增强的语句至少应用一个增强操作。因此，如果您执行alpha = 0.001并且句子只有四个单词，那么将仍然执行一个增强操作。即EDA的4个操作中的一个。

# Citation
如果您在论文中使用EDA，请引用我们：
```
@inproceedings{wei-zou-2019-eda,
    title = "{EDA}: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks",
    author = "Wei, Jason  and
      Zou, Kai",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)",
    month = nov,
    year = "2019",
    address = "Hong Kong, China",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/D19-1670",
    pages = "6383--6389",
    abstract = "We present EDA: easy data augmentation techniques for boosting performance on text classification tasks. EDA consists of four simple but powerful operations: synonym replacement, random insertion, random swap, and random deletion. On five text classification tasks, we show that EDA improves performance for both convolutional and recurrent neural networks. EDA demonstrates particularly strong results for smaller datasets; on average, across five datasets, training with EDA while using only 50{\textbackslash}{\%} of the available training set achieved the same accuracy as normal training with all available data. We also performed extensive ablation studies and suggest parameters for practical use.",
}
```

# Experiments

The code is not documented, but is [here](https://github.com/jasonwei20/eda_nlp/tree/master/experiments) for all experiments used in the paper. See [this issue](https://github.com/jasonwei20/eda_nlp/issues/10) for limited guidance.



