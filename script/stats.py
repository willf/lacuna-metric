import json
import sqlite3
import sys

# Create a new SQLite database
conn = sqlite3.connect("stats.db")

c = conn.cursor()


def create_stats(statement, cursor, filename):
    """
    Execute the statement on the cursor, then write the results to the filename
    """
    cursor.execute(statement)
    with open(filename, "w") as f:
        f.write("\t".join([d[0] for d in cursor.description]) + "\n")
        for row in cursor.fetchall():
            f.write("\t".join(map(str, row)) + "\n")


# Get the distinct number of blocks and the number of test cases by corpus_id

create_stats(
    """

  SELECT
    corpus_id AS 'Corpus',
    COUNT(distinct file_id) AS 'Editions',
    COUNT(block_index) AS 'Blocks',
    SUM(test_cases_length) AS 'Cases'
    FROM stats
    GROUP BY corpus_id
    ORDER BY corpus_id
    """,
    c,
    "corpus_stats.tsv",
)

create_stats(
    """

  SELECT
    language AS 'Language',
    COUNT(distinct file_id) AS 'Editions',
    COUNT(block_index) AS 'Blocks',
    SUM(test_cases_length) AS 'Cases'
    FROM stats
    GROUP BY language
    ORDER BY 3 DESC
    """,
    c,
    "language_stats.tsv",
)


# Do the same for materials

create_stats(
    """

  SELECT
    material AS 'Material',
    COUNT(distinct file_id) AS 'Editions',
    COUNT(block_index) AS 'Blocks',
    SUM(test_cases_length) AS 'Cases'
    FROM stats
    GROUP BY material
    HAVING COUNT(block_index) >= 100
    ORDER BY 3 DESC
    """,
    c,
    "material_stats.tsv",
)


# Close the connection
conn.close()

conn = sqlite3.connect("case_stats.db")
c = conn.cursor()

# Get the counts of the number of alternatives
create_stats(
    """

  SELECT
    number_alternatives AS 'Alternatives',
    COUNT(*) AS 'Cases'
    FROM case_stats
    GROUP BY number_alternatives
    ORDER BY number_alternatives
    """,
    c,
    "alternatives_stats.tsv",
)

# Get the counts of the mode length
create_stats(
    """

  SELECT
    mode_length AS 'Mode',
    COUNT(*) AS 'Cases'
    FROM case_stats
    GROUP BY mode_length
    ORDER BY mode_length
    """,
    c,
    "mode_stats.tsv",
)
