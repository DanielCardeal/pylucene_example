"""
PyLucene working example that indexes all text documents in the "documents/"
directory and runs a query on the resulting index.

The index is stored in the file system directory "index/".
"""
import glob
import os

import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import (DirectoryReader, IndexWriter,
                                     IndexWriterConfig)
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import ByteBuffersDirectory, FSDirectory

WORKING_DIR = os.getcwd()
INPUT_DOCS_DIR = os.path.join(WORKING_DIR, "documents/")
INDEX_DIR = os.path.join(WORKING_DIR, "index/")


def documentFromFile(filepath: str) -> Document | None:
    """Create a Lucene document from a filepath."""
    try:
        with open(filepath, "r") as f:
            contentsField = Field("contents", f.read(), TextField.TYPE_STORED)
            fileNameField = Field("filename", f.name, TextField.TYPE_STORED)
            filePathField = Field("filepath", filepath, TextField.TYPE_STORED)
        document = Document()
        document.add(contentsField)
        document.add(fileNameField)
        document.add(filePathField)
        return document
    except FileNotFoundError:
        print(f"File {filepath} does not exist.")
        return None


def indexFiles(idxDirectory, analyzer):
    """Add all text files of `INPUT_DOCS_DIR` to the index."""
    idxConfig = IndexWriterConfig(analyzer)
    idxWriter = IndexWriter(idxDirectory, idxConfig)
    for filepath in glob.glob("*.txt", root_dir=INPUT_DOCS_DIR):
        filepath = os.path.join(INPUT_DOCS_DIR, filepath)
        d = documentFromFile(filepath)
        if d is not None:
            idxWriter.addDocument(d)

    idxWriter.close()


def searchIndex(idxDirectory, analyzer, query, n=5):
    """Run a query in the index."""
    idxReader = DirectoryReader.open(idxDirectory)
    idxSearcher = IndexSearcher(idxReader)

    parser = QueryParser("contents", analyzer)
    query = parser.parse(query)

    # Return a list of documents
    hits = idxSearcher.search(query, n).scoreDocs
    return list(map(lambda hit: idxSearcher.doc(hit.doc), hits))


if __name__ == "__main__":
    # Starts Lucene VM
    lucene.initVM(vmargs=["-Djava.awt.headless=true"])
    print("lucene", lucene.VERSION)

    # Open/read a filesystem directory
    # NOTE: is strictly necessary to use the Paths API from java to open a file
    # system directory
    idxDirectory = FSDirectory.open(Paths.get(INDEX_DIR))

    # Open/create a RAM directory
    # idxDirectory = ByteBuffersDirectory()

    # Use default analyzer
    analyzer = StandardAnalyzer()

    # Add files to the index
    indexFiles(idxDirectory, analyzer)

    # Query some text
    results = searchIndex(idxDirectory, analyzer, query="Weapon whale")

    ## Print results
    for result in results:
        print(result.get("filename"))
