def ppu(frac, const):
	return (const/(const+0.0000001 + frac))**2
def pdo(frac, const):
	return (frac/(const+0.0000001 + frac))**2

if __name__=="__main__":
	for i in range(3, 48):
		print(str(round(float(i)/150, 2)) + " H PU:" + str(round(ppu(35.0/150, float(i)/150), 3)))
		print(str(round(float(i)/150, 2)) + " H DO:" + str(round(pdo(35.0/150, float(i)/150), 3)))
		print(str(round(float(i)/150, 2)) + " L PU:" + str(round(ppu(3.0/150, float(i)/150), 3)))
		print(str(round(float(i)/150, 2)) + " L DO:" + str(round(pdo(3.0/150, float(i)/150), 3))+"\n")