from bs4 import BeautifulSoup
from datetime import datetime
import requests
from time import sleep


def get_arxiv_page(query: str,
                   baseURL: str = "http://export.arxiv.org/api/query?",
                   start: int = 0,
                   max_results: int = 10,
                   sortBy: str = "relevance",
                   sortOrder: str = "descending",
                   columns: list = [],
                   timeout: float = 10.) -> list:
    """
    Function processes the query and returns a list of data rows.

    Parameters
    ----------
    query : str
        Query to be requested
    baseURL : str, optional, default : "http://export.arxiv.org/api/query?"
        Base URL of the arxiv API
    start : int, optional, default : 0
        Starting index for page
    max_results : int, optional, default : 10
        Maximum number of page entries
    sortBy : str, optional, default : "relevance"
        Sort entries by
    sortOrder : str, optional, default : "descending"
        Order of sorting
    columns : list, optional, default : []
        List of columns to be returned
    timeout : float, optional, default : 10.
        Timeout in seconds for HTTP requests

    Returns
    -------
    rows : list
        List of data rows
    """

    # Check if columns are valid
    valid_columns = ["id", "title", "summary", "authors", "primary_category",
                     "categories", "comments", "updated", "published", "doi", "links"]
    for c in columns:
        if c not in valid_columns:
            raise ValueError(
                "{:s} is not a valid column name.\nValid column names are {}.".format(c, valid_columns))
    # Renaming map of columns for arxiv query
    col_map = {
        "id": "id",
        "title": "title",
        "summary": "summary",
        "authors": "author",
        "primary_category": "arxiv:primary_category",
        "categories": "category",
        "comments": "arxiv:comment",
        "updated": "updated",
        "published": "published",
        "doi": "arxiv:doi",
        "links": "link",
    }

    # Build and request query URL
    url = '{:s}{:s}&start={:d}&max_results={:d}&sortBy={:s}&sortOrder={:s}'.format(
        baseURL,
        query,
        start,
        max_results,
        sortBy,
        sortOrder
    )

    # Retry on server errors or timeouts
    retries = requests.adapters.Retry(total=5, backoff_factor=0.5,
                                      status_forcelist=[429, 500, 502, 503, 504])
    adapter = requests.adapters.HTTPAdapter(max_retries=retries)

    http = requests.Session()
    http.mount("http://", adapter)

    # The arXiv API can return an empty data set, even though there should be more pages.
    # Since it does not return an error code, we try again after one second.
    # Only after 5 tries with empty data sets, we assume that the query is done.
    i = 0
    while i < 5:
        response = http.get(url, timeout=timeout)

        # Read data and get entries
        data = BeautifulSoup(response.text, "xml")
        entries = data.find_all("entry")
        if entries != []:
            break
        sleep(1.)
        i += 1

    # Loop over entries and build rows of data frame
    rows = []
    for entry in entries:

        d = {}

        # Parse the requested columns
        for c in columns:
            if c in ["authors", "categories", "primary_category", "links"]:
                tmp = entry.find_all(col_map[c])
                if tmp is not None:
                    v = []
                    for t in tmp:
                        if c == "authors":
                            v.append(t.find("name").text.strip())
                        elif c in ["categories", "primary_category"]:
                            v.append(t["term"].strip())
                        elif c == "links":
                            v.append(t["href"].strip())
                    val = "; ".join(v)
            else:
                tmp = entry.find(col_map[c])
                tmp_stripped = tmp.text.strip() if tmp is not None else ""
                if c == "id":
                    val = tmp_stripped[21:]
                elif c == "summary":
                    val = tmp_stripped.replace("\n", " ")
                elif c in ["published", "updated"]:
                    val = datetime.strptime(tmp_stripped, "%Y-%m-%dT%H:%M:%SZ")
                else:
                    val = tmp_stripped
            d[c] = val

        rows.append(d)

    return rows
