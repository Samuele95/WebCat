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
