TARGET := outlay
LTX := pdflatex -interaction=nonstopmode -halt-on-error

GENERATE := python3 generator/generate-latex-source.py
JQ := generator/jq
SRC := data.yml
BUILDDIR := _build
DATA := $(BUILDDIR)/data.json
JSONSRC := $(BUILDDIR)/src.json
TOTAL := $(BUILDDIR)/total.json
EMPTYJSONFILE := $(BUILDDIR)/empty.json
RATESDIR := $(BUILDDIR)/rates
MONTHS := $(shell yaml2json data.yml | jq -r -f $(JQ)/find-months.jq)
RATES := $(MONTHS:%=$(RATESDIR)/%.json)
ALLRATES := $(BUILDDIR)/rates.json

# see http://ec.europa.eu/budget/contracts_grants/info_contracts/inforeuro/index_fr.cfm
define getrates
	curl "http://ec.europa.eu/budg/inforeuro/api/public/monthly-rates?year=$(1)&month=$(2)"
endef

all: $(TARGET).pdf
	killall -HUP mupdf || true

$(TARGET).pdf: $(BUILDDIR)/$(TARGET).pdf
	cp $< $@

$(BUILDDIR)/$(TARGET).pdf: $(BUILDDIR)/$(TARGET).tex
	cd $(dir $@); \
		$(LTX) $(TARGET).tex

$(BUILDDIR)/$(TARGET).tex: $(DATA) $(TOTAL)
	$(GENERATE) $^ > $@

$(TOTAL): $(DATA)
	cat $< | jq -f $(JQ)/total.jq > $@

$(DATA): $(JSONSRC) $(ALLRATES)
	cat $^ | jq -s -f $(JQ)/convert-currency.jq > $@

$(JSONSRC): $(SRC)
	mkdir -p $(shell dirname $@)
	yaml2json $< > $@

$(ALLRATES): $(EMPTYJSONFILE) $(RATES)
	cat $^ | jq -s add > $@

$(EMPTYJSONFILE):
	echo '{}' > $@

$(RATESDIR)/%.json:
	mkdir -p $(shell dirname $@)
	echo '{"$(*F)": ' > $@
	$(call getrates,$(shell cut -d'-' -f1 $(*F)),$(shell cut -d'-' -f2 $(*F))) >> $@
	echo '}' >> $@

clean:
	rm -rf $(BUILDDIR)
	rm -f $(TARGET).pdf
