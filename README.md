# arXiv Loader

[![GitHub](https://img.shields.io/github/license/stammler/arxivloader) ](https://github.com/stammler/arxivloader/blob/master/LICENSE) [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/stammler/arxivloader/blob/master/.github/CODE_OF_CONDUCT.md)  
[![PyPI - Downloads](https://img.shields.io/pypi/dm/arxivloader?label=PyPI%20downloads)](https://pypistats.org/packages/arxivloader)

This tool is a wrapper of the [arXiv API](https://arxiv.org/help/api/) that allows you to retrieve metadata of articles published on arXiv.  
Please abide by the [Terms of Usage](https://arxiv.org/help/api/tou) of the arXiv API.

## Installation

`pip install arxivloader`

## Usage

Please consult the [arXiv API documentation](https://arxiv.org/help/api/user-manual#_query_interface) for help in constructing a valid query string.

### Searching by keyword

To search for a keyword the query needs to start with `search_query=` followed by a prefix and the search word.  
Possible prefixes are 

| Prefix | Explanation       |
|:-------|:------------------|
| ti     | Title             |
| au     | Author            |
| abs    | Abstract          |
| co     | Comments          |
| jr     | Journal Reference |
| cat    | Subject Category  |
| rn     | Report Number     |
| id     | arXiv ID          |
| all    | All of the above  |

Please have a look at the [arXiv API documentation](https://arxiv.org/help/api/user-manual#query_details) for details.

```
import arxivloader

keyword = "DustPy"
prefix = "all"
query = "search_query={prefix}:{keyword}".format(prefix, keyword)
columns = ["id", "title", "authors"]

df = arxivloader.load(query, columns=columns)
print(df)
```

|    | id           | title                                                               | authors                                                                              |
|---:|:-------------|:--------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
|  0 | 2207.00322v2 | DustPy: A Python Package for Dust Evolution in Protoplanetary Disks | Sebastian Markus Stammler; Tilman Birnstiel                                          |
|  1 | 2110.04007v1 | The formation of wide exoKuiper belts from migrating dust traps     | E. Miller; S. Marino; S. M. Stammler; P. Pinilla; C. Lenz; T. Birnstiel; Th. Henning |

### Searching by id

To search for a specific arXiv ID the query needs to start with `id_list=` followed by a comma-separated list of arXiv IDs:

```
import arxivloader

IDs = ["1909.04674", "1909.10526"]
query = "id_list={}".format(",".join(IDs))
columns = ["id", "title", "authors"]

df = arxivloader.load(query, columns=columns)

print(df)
```

|    | id           | title                                                               | authors                                                                                                       |
|---:|:-------------|:--------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------|
|  0 | 1909.04674v1 | The DSHARP Rings: Evidence of Ongoing Planetesimal Formation?       | Sebastian M. Stammler; Joanna Drazkowska; Til Birnstiel; Hubert Klahr; Cornelis P. Dullemond; Sean M. Andrews |
|  1 | 1909.10526v1 | Including Dust Coagulation in Hydrodynamic Models of Protoplanetary Disks: Dust Evolution in the Vicinity of a Jupiter-mass Planet  | Joanna Drazkowska; Shengtai Li; Til Birnstiel; Sebastian M. Stammler; Hui Li                                  |

### Filtering specific articles by keywords

If both, `search_query=` and `id_list=` are present, the given arXiv articles are filtered by the give key word.

```
import arxivloader

keyword = "DSHARP"
prefix = "ti"
IDs = ["1909.04674", "1909.10526"]
query = "search_query={pf}:{kw}&id_list={ids}".format(pf=prefix, kw=keyword, ids=",".join(IDs))
columns = ["id", "title", "authors"]

df = arxivloader.load(query, columns=columns)

print(df)
```

|    | id           | title                                                         | authors                                                                                                       |
|---:|:-------------|:--------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------|
|  0 | 1909.04674v1 | The DSHARP Rings: Evidence of Ongoing Planetesimal Formation? | Sebastian M. Stammler; Joanna Drazkowska; Til Birnstiel; Hubert Klahr; Cornelis P. Dullemond; Sean M. Andrews |

### Searching by category

It is possible to search large number of articles by category. Please be responsible with the traffic this query causes.

```
import arxivloader

keyword = "astro-ph.EP"
prefix = "cat"
query = "search_query={pf}:{kw}".format(pf=prefix, kw=keyword)
columns = ["id", "title", "primary_category", "categories", "published"]

df = arxivloader.load(query, columns=columns, sortBy="submittedDate", sortOrder="descending", num=1000, page_size=100)

print(df.head(5))
```

|    | id           | title                                                                  | primary_category   | categories                 | published           |
|---:|:-------------|:-----------------------------------------------------------------------|:-------------------|:---------------------------|:--------------------|
|  0 | 2210.11357v1 | The Key Factors Controlling the Seasonality of Planetary Climate       | physics.ao-ph      | physics.ao-ph; astro-ph.EP | 2022-10-20 15:45:43 |
|  1 | 2210.11305v1 | On the origin of the dichotomy of stellar activity cycles              | astro-ph.SR        | astro-ph.SR; astro-ph.EP   | 2022-10-20 14:34:33 |
|  2 | 2210.11207v1 | $\texttt{KOBEsim}$: a Bayesian observing strategy algorithm for planet detection in radial velocity blind-search | astro-ph.EP        | astro-ph.EP; astro-ph.IM   | 2022-10-20 12:33:03 |
|  3 | 2210.11103v1 | Lower-than-expected flare temperatures for TRAPPIST-1                  | astro-ph.SR        | astro-ph.SR; astro-ph.EP   | 2022-10-20 08:55:47 |
|  4 | 2210.10909v1 | TOI-3884 b: A rare 6-R$_{\oplus}$ planet that transits a low-mass star with a giant and likely polar spot | astro-ph.EP        | astro-ph.EP                | 2022-10-19 22:19:15 |

## Acknowledgements

Thank you to arXiv for use of its open access interoperability.