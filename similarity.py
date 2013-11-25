def ppu(frac, const):
	return (const/(const+0.0000001 + frac))**2
def pdo(frac, const):
	return (frac/(const+0.0000001 + frac))**2

if __name__=="__main__":
	print(str(float(i)/100) + " PU:" + str(round(ppu(0.0, float(i)/100), 3)))