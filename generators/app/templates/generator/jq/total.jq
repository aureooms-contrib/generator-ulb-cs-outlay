{
	car: (if .car == null then 0 else .car | map(.eur) | add end),
	travel: (if .travel == null then 0 else .travel | map(.eur) | add end),
	other: (if .other == null then 0 else .other | map(.eur) | add end),
	all: (([[{"eur": 0}],.car,.travel,.other] | add | map(.eur) | add) - (if .advance == null then 0 else .advance end))
}
