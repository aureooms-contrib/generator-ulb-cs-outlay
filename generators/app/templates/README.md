## Needed

  - make
  - jq (for data management)
  - pdflatex (for pdf generation)
  - python3 (for templating)
  - yaml2json (for nicer data format)
  - curl (for automatic conversion rates)

## Add a personal car expense

Edit the file `data.yml` 

    car:
        - id: CUSTOMLATEXID
          date: 2018-07-05 -- 2018-07-09
          title: Aller-retour Brussels -- Utrecht
          km: 360

## Add travel expenses

Edit the file `data.yml` 

    travel:
        - date: 2018-07-05 -- 2018-07-09
          title: Aller-retour BRU -- PRG
          currency: CZK 3395
          eur: 133.19

        - date: 2018-07-05
          title: Taxi vers BRU
          eur: 38.5

        - date: 2018-07-05
          title: Uber de PRG
          currency: CZK 275.79
          eur: 10.60

        - date: 2018-07-09
          title: Taxi vers PRG
          currency: CZK 600

        - date: 2018-07-09
          title: Taxi de BRU
          eur: 50.6


## Add other expenses

Edit the file `data.yml` 

    other:
        - date: 2018-07-05 -- 2018-07-09
          perdiem: fria

        - date: 2018-07-05 -- 2018-07-09
          perdiem: fnrs

        - date: 2018-04-29 -- 2018-07-10
          perdiem: Hongrie
