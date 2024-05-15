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
  "test_cases": [
    {
      "case_index": 1,
      "id": "DDbDP/cde.85.247/1/1",
      "number_alternatives": 1,
      "max_length": 1,
      "min_length": 1,
      "mode_length": 1,
      "test_case": "ἔτους ἐβδ?μου Ἀ.τωνείνου\nΚαίσαξος τοῦ κυρίου Μεχεὶρ κγ\n Ἀρείῳ   \nἙριεῦς   Ἑριέως\n ὑπὲρ  τοῦ\nπέμπτου      \nὀκτώ,   η",
      "alternatives": [
        "ό"
      ]
    },
    {
      "case_index": 2,
      "id": "DDbDP/cde.85.247/1/2",
      "number_alternatives": 1,
      "max_length": 1,
      "min_length": 1,
      "mode_length": 1,
      "test_case": "ἔτους ἐβδ.μου Ἀ?τωνείνου\nΚαίσαξος τοῦ κυρίου Μεχεὶρ κγ\n Ἀρείῳ   \nἙριεῦς   Ἑριέως\n ὑπὲρ  τοῦ\nπέμπτου      \nὀκτώ,   η",
      "alternatives": [
        "ν"
      ]
    }
  ]
}

For each record, create a SQLite record that looks like this:

CREATE TABLE IF NOT EXISTS case_stats (
  min_length INTEGER,
  max_length INTEGER,
  mode_length INTEGER,
  number_alternatives INTEGER
);


"""

import json
import sqlite3
import sys

# Create a new SQLite database
conn = sqlite3.connect("case_stats.db")
c = conn.cursor()
c.execute(
    """
    DROP TABLE IF EXISTS case_stats;
    """
)
c.execute(
    """
    CREATE TABLE IF NOT EXISTS case_stats (
        min_length INTEGER,
        max_length INTEGER,
        mode_length INTEGER,
        number_alternatives INTEGER
    ) ;
    """
)

# Read in the JSONL records from sys.stdin
# and create a new record in the SQLite database for each record one by one

for line in sys.stdin:
    record = json.loads(line)
    for case in record["test_cases"]:
        min_length = case["min_length"]
        max_length = case["max_length"]
        mode_length = case["mode_length"]
        number_alternatives = case["number_alternatives"]
        c.execute(
            """
            INSERT INTO case_stats
            (min_length, max_length, mode_length, number_alternatives)
            VALUES (?, ?, ?, ?)
            """,
            (min_length, max_length, mode_length, number_alternatives),
        )


conn.commit()
