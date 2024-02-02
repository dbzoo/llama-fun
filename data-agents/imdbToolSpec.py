"""IMDB Search tool spec."""
from typing import Any, List
from llama_index.tools.tool_spec.base import BaseToolSpec
from llama_index.readers.schema.base import Document

class IMDBToolSpec(BaseToolSpec):
    """Specifies a tool for querying Movies from IMDB"""

    spec_functions = ["search_movie"]
    
    def search_movie(self, movie: str) -> List[Document]:
        """Make a query to the IMDB search engine to receive a list of results

           Args:
              movie (str): Search for a movie        
        """
        import imdb
        ia = imdb.IMDb()
        search_results = ia.search_movie(movie)
        results = []
        for movie in search_results:
            results.append(Document(doc_id=movie.movieID, text=movie.summary(), metadata=movie.data))
        return results
