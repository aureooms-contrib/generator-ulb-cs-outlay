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
        - id: 1
          date: 2018-07-05 -- 2018-07-09
          title: Aller-retour Brussels -- Utrecht
          km: 360

## Add travel expenses

Edit the file `data.yml` 

    travel:
        - id: 2
          date: 2018-07-05 -- 2018-07-09
          title: Aller-retour BRU -- PRG
          currency: CZK 3395
          eur: 133.19

        - id: 3
          date: 2018-07-05
          title: Taxi vers BRU
          eur: 38.5

        - id: 4
          date: 2018-07-05
          title: Uber de PRG
          currency: CZK 275.79
          eur: 10.60

        - id: 5
          date: 2018-07-09
          title: Taxi vers PRG
          currency: CZK 600

        - id: 6
          date: 2018-07-09
          title: Taxi de BRU
          eur: 50.6


## Add other expenses

Edit the file `data.yml` 

    other:
        - id: 7
          date: 2018-07-05 -- 2018-07-09
          title: Per diem (30 EUR x 4 jours FRIA)
          eur: 120
