from arxivloader.api import get_arxiv_page
import numpy as np
import pandas as pd
from time import sleep
from tqdm.auto import tqdm
import warnings


def load(query: str,
         num: int = 10,
         start: int = 0,
         page_size: int = 10,
         delay: float = 3.,
         sortBy: str = "relevance",
         sortOrder: str = "descending",
         columns: list = ["id", "title", "summary", "authors", "primary_category",
                          "categories", "comments", "updated", "published", "doi", "links"],
         timeout: float = 10.,
         verbosity: int = 2) -> pd.DataFrame:
    """
    Function returns a Pandas DataFrame with arXiv data for the given query.
    Please see the arXiv API documentation to build a valid query:
    https://arxiv.org/help/api/user-manual#_query_interface

    Please be responsible and abide by the arXiv API Terms of Usage:
    https://arxiv.org/help/api/tou

    Thank you to arXiv for use of its open access interoperability.

    Parameters
    ----------
    query : str
        Query to be requested
    num : int, optional, default : 10
        Number of entries to be returned
    start : int, optional, default : 0
        Starting index for page
    page_size : int, optional, defaul : 10
        Maximum number of page entries. Maximum is 30000.
    delay : float, optional, default : 3.
        Delay in seconds between page requests. Has to at least 3.
    sortBy : str, optional, default : "relevance"
        Sort entries by
    sortOrder : str, optional, default : "descending"
        Order of sorting
    columns : list, optional, default : ["id", "title", "summary", "authors", "primary_category", "categories", "comments", "updated", "published", "doi", "links"]
        Data columns to be retrieved
    timeout : float, optional, default : 10.
        Timeout in seconds for HTTP requests
    verbosity : int, optional, default : 2
        Level of verbosity

    Returns
    -------
    df : pandas.DataFrame
        Pandas DataFrame with the requested arXiv data
    """

    if query == "":
        raise ValueError("Positional argument query is empty string.")

    if delay < 3:
        warnings.warn("Delay has to be at least 3 seconds. Setting delay=3.")
        delay = 3.

    if page_size > 30_000:
        warnings.warn("Maximum page size is 30000. Setting page_size=30000.")
        page_size = 30_000

    if sortBy not in ["relevance", "lastUpdatedDate", "submittedDate"]:
        raise ValueError(
            "Keyword argument sortBy can only be 'relevance', 'lastUpdatedDate', or 'submitedDate'.")

    if sortOrder not in ["ascending", "descending"]:
        raise ValueError(
            "Keyword argument sortOrder can only be 'ascending' or 'descending'.")

    hide_progress = False
    # Set verbosity of progressbar
    if(verbosity < 2):
        hide_progress = True

    start_ids = np.arange(start, start+num, page_size)

    rows = []
    start_ids = np.arange(start, start+num, page_size)
    is_done = False
    with tqdm(start_ids, desc="Downloading pages", disable=hide_progress) as iterator:
        for start_id in iterator:
            if not is_done:
                if start_id > start_ids[0]:
                    sleep(delay)
                maxres = np.minimum(page_size, start+num-start_id)
                r = get_arxiv_page(
                    query, start=start_id, max_results=maxres, sortBy=sortBy, sortOrder=sortOrder, columns=columns, timeout=timeout)
                if r == []:
                    is_done = True
                    continue
                if len(r) != maxres:
                    is_done = True
                rows += r

    df = pd.DataFrame(rows, columns=columns)

    # Dropping duplicate rows
    df.drop_duplicates(inplace=True, ignore_index=True)

    # Printing success message
    if(verbosity > 0):
        msg = "Retrieved {N_rows} entries.".format(N_rows=len(df))
        print(msg)

    return df
