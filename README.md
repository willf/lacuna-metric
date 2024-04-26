# Lacuna Metric

Example: https://papyri.info/ddbdp/aegyptus;89;240 (also in data directory)

Data is sourced from https://github.com/papyri/idp.data

Goal: Convert `<ab>` elements; anonymous blocks

In the idp.data directory, there are around 950k `ab` tags.

Here are the child elements of `ab` elements found in the data:

| Tag                                                                                    | Count   | How to Process                                                                                                       |
|----------------------------------------------------------------------------------------|---------|----------------------------------------------------------------------------------------------------------------------|
| [`abbr`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-abbr.html)           | 33568   | Supply the abbreviation in the context; only eval on abbreviation in context                                         |
| [`add`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-add.html)             | 17961   | provide for context; do not consider for evaluation                                                                  |
| [`app`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-app.html)             | 39261   | type="alternative" -- 'any' of the lem or rdg (readings). Note you'll have to deal with reading groups.              |
| [`certainty`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-certainty.html) | 54      | drop                                                                                                                 |
| [`choice`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-choice.html)       | 159345  | Use the `orig` version in context. Are there cases where this shows up inside `supplied` text? Use the `orig` text.  |
| [`del`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-del.html)             | 12718   | provide for context; do not consider for evaluation                                                                  |
| [`expan`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-expan.html)         | 779351  | Use the 'original' text.                                                                                             |
| [`figure`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-figure.html)       | 594     | drop                                                                                                                 |
| [`foreign`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-foreign.html)     | 4121    | provide text only                                                                                                    |
| [`g`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-g.html)                 | 71996   | Most likely just ignore all `g`. Might want to                                                                       |
| [`gap`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-gap.html)             | 756277  | supply the gap 'as is', except move all gaps outside any `supplied` element                                          |
| [`handShift`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-handShift.html) | 22287   | ignore                                                                                                               |
| [`hi`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-hi.html)               | 38240   | Worth investigating some more, probably just use the text.                                                           |
| [`lb`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-lb.html)               | 1071351 | Might see [paragraphoi](https://en.wikipedia.org/wiki/Paragraphos). Just use a \n                                    |
| [`milestone`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-milestone.html) | 8036    | provide for context                                                                                                  |
| [`note`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-note.html)           | 2849    | drop                                                                                                                 |
| [`num`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-num.html)             | 531081  | Give the text                                                                                                        |
| [`orig`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-orig.html)           | 4048    | when is this used at the top level? But probably just the text                                                       |
| [`q`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-q.html)                 | 2886    | text only                                                                                                            |
| [`seg`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-seg.html)             | 316     | use content                                                                                                          |
| [`sic`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-sic.html)             | 4       | keep                                                                                                                 |
| [`space`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-space.html)         | 14592   | provide for context; do not consider for evaluation                                                                  |
| [`subst`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-subst.html)         | 9856    | provide for context; do not consider for evaluation                                                                  |
| [`supplied`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-supplied.html)   | 616540  | This is what is being supplied. Look for `app` blocks. Note that not all alternative readings are actually supplied. |
| [`surplus`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-surplus.html)     | 3987    | keep text all                                                                                                             |
| [`unclear`](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/ref-unclear.html)     | 586518  | Give the text                                                                                                        |

## Analysis by corpus, language, support material

## Number of ab blocks

| Corpus    |  Count  |
|-----------|---------|
| DDbDP     |  85,628 |
| EDH       |  80,793 |
| DCLP      |  11,581 |
| **TOTAL** | 952,002 |

## Language

| Language | Count |
|----------|-------|
| grc      | 94374 |
| la       | 81326 |
| cop      | 2300  |

## Corpus + Language

| Corpus | Language | Count |
|--------|----------|-------|
| DDbDP  | grc      | 80895 |
| EDH    | la       | 78586 |
| DCLP   | grc      | 11272 |
| DDbDP  | la       | 2459  |
| DDbDP  | cop      | 2272  |
| EDH    | grc      | 2207  |
| DCLP   | la       | 281   |
| DCLP   | cop      | 28    |

## Material (10 or more)

| Material                        | Count |
|---------------------------------|-------|
| papyrus                         | 69591 |
| unknown                         | 46962 |
| ostrakon                        | 20600 |
| kalkstein                       | 10591 |
| sandstein                       | 6294  |
| marmor                          | 3930  |
| gesteine                        | 3849  |
| holz                            | 3798  |
| ton                             | 3363  |
| bronze                          | 1665  |
| marmor, weiß                    | 1227  |
| blei                            | 776   |
| marmor, geädert / farbig        | 590   |
| stone                           | 482   |
| pergament                       | 392   |
| silber                          | 286   |
| parchment                       | 284   |
| tuff                            | 202   |
| pottery                         | 190   |
| gesteine unbestimmt             | 167   |
| granit                          | 160   |
| gold                            | 115   |
| travertin                       | 113   |
| oolith                          | 107   |
| wood                            | 104   |
| holz (?)                        | 103   |
| schiefer                        | 97    |
| muschelkalk                     | 97    |
| wachstafel                      | 87    |
| steatit                         | 83    |
| glas                            | 81    |
| trachyt                         | 76    |
| leinen                          | 76    |
| konglomerat                     | 70    |
| basalt                          | 61    |
| speckstein                      | 55    |
| ostracon (poterie)              | 53    |
| kupfer                          | 52    |
| holztafel                       | 52    |
| putz                            | 51    |
| leder                           | 48    |
| eisen                           | 44    |
| knochen                         | 42    |
| vulkantuff                      | 35    |
| gesteine?                       | 34    |
| bronze, silber                  | 31    |
| kalkstein?                      | 29    |
| andesit                         | 28    |
| kalkmergel / mergel             | 27    |
| marmor?                         | 26    |
| metalle                         | 23    |
| lead                            | 23    |
| graffito                        | 23    |
| jaspis                          | 22    |
| sandstein?                      | 20    |
| zinn                            | 19    |
| silber, gold                    | 18    |
| karneol                         | 18    |
| gneis                           | 17    |
| marmor (farbe unbestimmt)       | 15    |
| onyx                            | 14    |
| wood: painted white             | 13    |
| paper                           | 13    |
| messing                         | 13    |
| kalktuff                        | 13    |
| elfenbein                       | 13    |
| quarzit                         | 12    |
| holz, wachs                     | 12    |
| 1                               | 12    |
| mumienleinwand                  | 10    |
| gips                            | 10    |
| bronze?                         | 10    |

## Corpus + Material (ten or more instances)

| Corpus | Material                        | Count |
|--------|----------------------------------|-------|
| DDbDP  | papyrus                         | 59187 |
| EDH    | unknown                         | 45397 |
| DDbDP  | ostrakon                        | 20600 |
| EDH    | kalkstein                       | 10585 |
| DCLP   | papyrus                         | 10404 |
| EDH    | sandstein                       | 6294  |
| EDH    | marmor                          | 3930  |
| EDH    | gesteine                        | 3849  |
| EDH    | ton                             | 3336  |
| DDbDP  | holz                            | 3305  |
| EDH    | bronze                          | 1663  |
| DDbDP  | unknown                         | 1561  |
| EDH    | marmor, weiß                    | 1227  |
| EDH    | blei                            | 775   |
| EDH    | marmor, geädert / farbig        | 590   |
| EDH    | holz                            | 493   |
| DCLP   | stone                           | 482   |
| DDbDP  | pergament                       | 392   |
| EDH    | silber                          | 285   |
| DCLP   | parchment                       | 284   |
| EDH    | tuff                            | 202   |
| DCLP   | pottery                         | 189   |
| EDH    | gesteine unbestimmt             | 167   |
| EDH    | granit                          | 160   |
| EDH    | gold                            | 115   |
| EDH    | travertin                       | 113   |
| EDH    | oolith                          | 107   |
| DCLP   | wood                            | 104   |
| DDbDP  | holz (?)                        | 103   |
| EDH    | schiefer                        | 97    |
| EDH    | muschelkalk                     | 97    |
| DDbDP  | wachstafel                      | 87    |
| EDH    | steatit                         | 82    |
| EDH    | glas                            | 81    |
| EDH    | trachyt                         | 76    |
| DDbDP  | leinen                          | 76    |
| EDH    | konglomerat                     | 70    |
| EDH    | basalt                          | 61    |
| EDH    | speckstein                      | 55    |
| DDbDP  | ostracon (poterie)              | 53    |
| EDH    | kupfer                          | 52    |
| DDbDP  | holztafel                       | 52    |
| EDH    | putz                            | 51    |
| EDH    | eisen                           | 43    |
| EDH    | vulkantuff                      | 35    |
| EDH    | knochen                         | 34    |
| EDH    | gesteine?                       | 34    |
| EDH    | bronze, silber                  | 31    |
| EDH    | leder                           | 29    |
| EDH    | kalkstein?                      | 29    |
| EDH    | andesit                         | 28    |
| EDH    | kalkmergel / mergel             | 27    |
| DDbDP  | ton                             | 27    |
| EDH    | marmor?                         | 26    |
| EDH    | metalle                         | 23    |
| DDbDP  | graffito                        | 23    |
| DCLP   | lead                            | 23    |
| EDH    | jaspis                          | 22    |
| EDH    | sandstein?                      | 20    |
| EDH    | zinn                            | 19    |
| DDbDP  | leder                           | 19    |
| EDH    | silber, gold                    | 18    |
| EDH    | karneol                         | 18    |
| EDH    | gneis                           | 17    |
| EDH    | marmor (farbe unbestimmt)       | 15    |
| EDH    | onyx                            | 14    |
| EDH    | messing                         | 13    |
| EDH    | kalktuff                        | 13    |
| EDH    | elfenbein                       | 13    |
| DCLP   | wood: painted white             | 13    |
| DCLP   | paper                           | 13    |
| EDH    | quarzit                         | 12    |
| EDH    | holz, wachs                     | 12    |
| DCLP   | 1                               | 12    |
| EDH    | bronze?                         | 10    |
| DDbDP  | mumienleinwand                  | 10    |
| DDbDP  | gips                            | 10    |
