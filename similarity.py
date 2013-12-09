def ppu(frac, const):
	return (const/(const+0.0000001 + frac))**2
def pdo(frac, const):
	return (frac/(const+0.0000001 + frac))**2


def contains(p, q):
	if len(p) > len(q):
		small = q
		big = p
	else:
		small = p
		big = q
	for i in range(len(big)-(len(small)-1)):
		print(big[i:i+len(small)])
		if big[i:i+len(small)] == small:
			return True
	return False



if __name__=="__main__":
	a = list('GTTCACATGATTTATGCCTAGAAGAGTAGCCGCGCCCATTGTTTCACGCGTTAAGACGGAAGAGCTCGTCGTGTGGCGCGCATAGTGTAAGACATGTTTGCCAACTCAAATCGTGCACTAAAGGGCTGATCCGGATATATTGGAACTACACAGACAAGACCAGTCTGACCGATCTCATCCTGCAACGTCTGTGCCGGGAT')
	print(a)
	b = list('GTGCCGGGAT')
	print(b)
	print(contains(a, b))

	# for i in range(3, 48):
	# 	print(str(round(float(i)/150, 2)) + " H PU:" + str(round(ppu(35.0/150, float(i)/150), 3)))
	# 	print(str(round(float(i)/150, 2)) + " H DO:" + str(round(pdo(35.0/150, float(i)/150), 3)))
	# 	print(str(round(float(i)/150, 2)) + " L PU:" + str(round(ppu(3.0/150, float(i)/150), 3)))
	# 	print(str(round(float(i)/150, 2)) + " L DO:" + str(round(pdo(3.0/150, float(i)/150), 3))+"\n")