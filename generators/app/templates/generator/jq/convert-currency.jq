.[1] as $rates |
.[0] |
with_entries(
	if .key == "travel" or .key == "other"
	then
		({
			key: .key,
			value: (
				.value |
				map(
					if .currency
					then
						if .eur
						then
							(
								.currency |= . + " (taux carte)"
							)
						else
							. as $x |
							(
								.eur |=
									($x.currency[4:] | tonumber)
									/
									(
										$rates[$x.date[:7]] |
										map(select(.isoA3Code==$x.currency[:3])) |
										first.value
									)
							) |
							(
								.currency |= . + " (taux EU)"
							)
						end
					else
						.
					end
				)
			)
		})
	else
		.
	end
)
