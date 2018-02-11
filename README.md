## Market Segmentation using Attributed Graph Community Detection

[1]: http://masonporter.blogspot.in/2011/02/facebook100-data-set.html
[2]: https://github.com/Aminoid/market-segmentation/blob/master/Paper.AttributedCommunity.Detection.pdf

Market segmentation divides a broad target market into subsets of consumers or businesses that have or are perceived to have common needs, interests, and priorities. These segments help firms or businesses focus on their target groups effectively and allocate resources efficiently. Traditional segmentation methods are solely based on attribute data such as demographics (age, sex, ethnicity, education, etc.) and psychographic profiles (lifestyle, personality, motives, etc.). However, social networks have recently become important for marketing. Depending on the nature of the market, social relations can even become vital in forming segments. Such social relations combined with demographic properties can be used to find more relevant subsets of consumers or businesses (i.e., communities).

In this project, we aim to find such market segments given social network data. These social relations can be captured in a graph framework where nodes represent customers/users and edges represent some social relationship. The properties belonging to each customer/user can be treated as node attributes. Hence, market segmentation becomes the problem of community detection over attributed graphs, where the communities are formed based on graph structure as well as attribute similarities.

## Datasets
Two small datasets: `fb_caltech_small_edgelist.txt` and `fb_caltech_small_attrlist.csv`. This dataset contains a facebook network of a US university (given as an edgelist) with each node corresponding to a user profile having the following attributes: student/faculty status, gender, major, second major, dorm, and year information. For the similarity convenience, these attribute values have been converted into asymmetric binary variables. The original dataset, which we downsampled to 324 users, can be found [here][1].

## Procedure
1. Implement the SAC-1 method described in the section-IV part-A in the [publication][2]. For the implementation, focus on section III and section IV part-A. The file is called `sac1.py`. It takes one argument as input, the alpha value, and produces a file called `communities.txt` as output which contains one community per line with vertex id’s separated by commas, e.g.,
```
1,4,8,9,12,17,85
2,7,25,66,97,45
```

2. Used cosine similarity to measure attribute similarity.
3. Limit the algorithm convergence to have a maximum of 15 iterations (this is an additional parameter that is not mentioned in the publication, but can be used in the implementation if it takes more than 15 iterations before convergence).
6. Produced separate outputs for different values of α = 0, 0.5, and 1. Final output is saved in the directory under the names `communities_0.txt`, `communities_5.txt`, and `communities_1.txt`, respectively.

## How to run
1. `python sac1.py` to create the files.
2. `Rscript evaluation.R` to do the evaluation of the communities.
