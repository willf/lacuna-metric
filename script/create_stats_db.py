"""
Read in a bunch of JSONL records that look like this:

{
  "corpus_id": "DDbDP",
  "file_id": "cde.85.377",
  "block_index": 2,
  "id": "DDbDP/cde.85.377/2",
  "title": "cde.85.377",
  "material": "papyrus",
  "language": "grc",
  "training_text": "<gap/>.ρ<gap/>\n<gap/>ζομ<gap/>\n<gap/>τη.<gap/>",
  "test_cases": []
}

For each record, create a SQLite record that looks like this:

CREATE TABLE IF NOT EXISTS stats (
  corpus_id TEXT,
  file_id TEXT,
  block_index INTEGER,
  id TEXT,
  material TEXT,
  language TEXT,
  test_cases_length INTEGER,
);


"""

import json
import sqlite3
import sys

# Create a new SQLite database
conn = sqlite3.connect("stats.db")
c = conn.cursor()
c.execute(
    """
    DROP TABLE IF EXISTS stats;
    """
)
c.execute(
    """
    CREATE TABLE IF NOT EXISTS stats (
        corpus_id TEXT,
        file_id TEXT,
        block_index INTEGER,
        id TEXT,
        material TEXT,
        language TEXT,
        training_text_length INTEGER,
        test_cases_length INTEGER
    );
    """
)

# Read in the JSONL records from sys.stdin
# and create a new record in the SQLite database for each record one by one

for line in sys.stdin:
    record = json.loads(line)
    corpus_id = record["corpus_id"]
    file_id = record["file_id"]
    block_index = record["block_index"]
    id = record["id"]
    material = record["material"]
    language = record["language"]
    training_text_length = len(record["training_text"])
    test_cases_length = len(record["test_cases"])

    c.execute(
        """
        INSERT INTO stats
        (corpus_id, file_id, block_index, id, material, language, training_text_length, test_cases_length)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            corpus_id,
            file_id,
            block_index,
            id,
            material,
            language,
            training_text_length,
            test_cases_length,
        ),
    )

conn.commit()
