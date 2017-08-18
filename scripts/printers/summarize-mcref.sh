 sed 's/^\(.*\) Mref=\(.*\) timestamp.*$/Q\1Mref=\2/' | tr "\n" " " | tr "Q" "\n" | \
	sed 's/^\([^[:space:]]*\)\ .*harmonic_mean/\1 harmonic_mean/' | \
	tr "},{':" "  _"   | \
	awk '{ \
		if($3=="__ln_mean__") { print $1, $4,$6;} \
		else                  { print $1, $6,$4;} \
		if($8=="__ln_mean__") { print $9, $11; } \
		else                  { print $11, $9; } \
		print "Q"; \
	}' | \
	tr "\n" " " |  tr "Q" "\n"
