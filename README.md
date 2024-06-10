# WebCat

![webcat](https://github.com/Samuele95/WebCat/assets/94041647/b1c0afb6-f5b7-4e12-b865-0cd1abcf662f)

## Description
WebCat is a project dedicated to the automated discovery and classification of websites based on content similarities, through an overall unsupervised learning approach using algorithmic models trained as necessary. The activities carried out range from **web crawling** and **web scraping**, for the discovery and the acquisition of the textual content of web pages, up to the use of neural networks for the vectorization of this content and the classification of the findings based on clustering algorithms. Specifically, the vectorization activity is carried out by the transformer-based BERT neural network, while the clustering process is the work of a Self-Organizing Map (SOM) as a form of unsupervised learning based on a neural network.

![gui](https://github.com/Samuele95/WebCat/assets/94041647/ce233b9e-d79f-485c-81ea-a7400c64adb8)

## Installation
Launch Docker compose from the same folder containing the ```compose.yaml``` file, with the following command.
```
docker compose up
```

## Docs
Please refer to the [wiki](https://github.com/Samuele95/WebCat/wiki) for the overall docs and usage instructions.

## Bibliography and references
Bishop, Christopher M. 2006. *Pattern Recognition and Machine Learning*.
Springer.
<https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf>.

Devlin, Jacob, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019.
“BERT: Pre-Training of Deep Bidirectional Transformers for Language
Understanding.” In *Proceedings of the 2019 Conference of the North
American Chapter of the Association for Computational Linguistics: Human
Language Technologies, Volume 1 (Long and Short Papers)*, edited by Jill
Burstein, Christy Doran, and Thamar Solorio, 4171–86. Minneapolis,
Minnesota: Association for Computational Linguistics.
<https://doi.org/10.18653/v1/N19-1423>.

Goodfellow, Ian, Yoshua Bengio, and Aaron Courville. 2016. *Deep
Learning*. The Mit Press.
<http://imlab.postech.ac.kr/dkim/class/csed514_2019s/DeepLearningBook.pdf>.

Grootendorst, Maarten. 2020. “KeyBERT: Minimal Keyword Extraction with
BERT.” Zenodo. <https://doi.org/10.5281/zenodo.4461265>.

Kohonen, T. 1990. “The Self-Organizing Map.” *Proceedings of the IEEE*
78: 1464–80. <https://doi.org/10.1109/5.58325>.

Kohonen, Teuvo. 2013. “Essentials of the Self-Organizing Map.” *Neural
Networks* 37 (January): 52–65.
<https://doi.org/10.1016/j.neunet.2012.09.018>.

Mitchell, Tom M. 1997. *Machine Learning*. Mcgraw Hill.

Raschka, Sebastian, and Vahid Mirjalili. 2017. *Python Machine Learning
: Machine Learning and Deep Learning with Python, Scikit-Learn, and
TensorFlow*. Packt Publishing.

Russell, Peter. 2021. *ARTIFICIAL INTELLIGENCE : A Modern Approach,
Global Edition.* Pearson Education Limited.

Vaswani, Ashish, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion
Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017.
“Attention Is All You Need.” In *Advances in Neural Information
Processing Systems*, edited by I. Guyon, U. Von Luxburg, S. Bengio, H.
Wallach, R. Fergus, S. Vishwanathan, and R. Garnett. Vol. 30. Curran
Associates, Inc.
<https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf>.

Vettigli, Giuseppe. 2018. “MiniSom: Minimalistic and NumPy-Based
Implementation of the Self Organizing Map.”
<https://github.com/JustGlowing/minisom/>.
