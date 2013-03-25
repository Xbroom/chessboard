eco:
	mkdir -p dist
	./ecotool.py resources/full.eco --lookup dist/eco-lookup.json --classification dist/eco-classification.json

.PHONY: test
test:
	nosetests
