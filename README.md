# Lacuna Metric

Example: https://papyri.info/ddbdp/aegyptus;89;240 (also in data directory)

Data is sourced from https://github.com/papyri/idp.data

Goal: Convert `<ab>` elements; anonymous blocks

In the idp.data directory, there are 165,660 `ab` tags.

Here are the child elements of `ab` elements found in the data:

| Tag                                                                                    | Count   | How to Process                                                                                                                                                                                    |
|----------------------------------------------------------------------------------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [`abbr`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-abbr.html)           | 33568   | Supply the abbreviation in the context; only eval on abbreviation in context                                                                                                                      |
| [`add`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-add.html)             | 17961   | provide for context; do not consider for evaluation                                                                                                                                               |
| [`app`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-app.html)             | 39261   | type="alternative" -- 'any' of the lem or rdg (readings). Note you'll have to deal with reading groups.                                                                                           |
| [`certainty`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-certainty.html) | 54      | drop                                                                                                                                                                                              |
| [`choice`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-choice.html)       | 159345  | Use the `orig` version in context. Are there cases where this shows up inside `supplied` text? Use the `orig` text.                                                                               |
| [`del`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-del.html)             | 12718   | provide for context; do not consider for evaluation                                                                                                                                               |
| [`expan`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-expan.html)         | 779351  | Use the 'original' text.                                                                                                                                                                          |
| [`figure`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-figure.html)       | 594     | drop                                                                                                                                                                                              |
| [`foreign`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-foreign.html)     | 4121    | provide text only                                                                                                                                                                                 |
| [`g`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-g.html)                 | 71996   | Most likely just ignore all `g`. Might want to                                                                                                                                                    |
| [`gap`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-gap.html)             | 756277  | supply the gap 'as is', except move all gaps outside any `supplied` element                                                                                                                       |
| [`handShift`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-handShift.html) | 22287   | ignore                                                                                                                                                                                            |
| [`hi`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-hi.html)               | 38240   | Worth investigating some more, probably just use the text.                                                                                                                                        |
| [`lb`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-lb.html)               | 1071351 | Might see [paragraphoi](https://en.wikipedia.org/wiki/Paragraphos). Just use a \n |
| [`milestone`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-milestone.html) | 8036    | provide for context                                                                                                                                                                               |
| [`note`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-note.html)           | 2849    | drop                                                                                                                                                                                              |
| [`num`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-num.html)             | 531081  | Give the text                                                                                                                                                                                     |
| [`orig`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-orig.html)           | 4048    | when is this used at the top level? But probably just the text                                                                                                                                    |
| [`q`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-q.html)                 | 2886    | text only                                                                                                                                                                                         |
| [`seg`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-seg.html)             | 316     | use content                                                                                                                                                                                       |
| [`sic`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-sic.html)             | 4       | keep                                                                                                                                                                                              |
| [`space`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-space.html)         | 14592   | provide for context; do not consider for evaluation                                                                                                                                               |
| [`subst`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-subst.html)         | 9856    | provide for context; do not consider for evaluation                                                                                                                                               |
| [`supplied`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-supplied.html)   | 616540  | This is what is being supplied. Look for `app` blocks. Note that not all alternative readings are actually supplied.                                                                              |
| [`surplus`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-surplus.html)     | 3987    | drop all                                                                                                                                                                                          |
| [`unclear`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-unclear.html)     | 586518  | Give the text                                                                                                                                                                                     |


Evaluating on "what other scholars have done."

Do an analysis for support/material.
