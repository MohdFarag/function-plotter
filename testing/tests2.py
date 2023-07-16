import matplotlib.pyplot as plt

# I want to make functions that print matplotlib texts but with different fonts
def printTextOnMpl(text, fontsize=16, fontname="LATIN MODERN ROMAN", color="black", ha="left", va="bottom"):
    
    fig = plt.figure(1)
    plt.title("Y vs X", fontsize='16',fontname=fontname)	#title
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_facecolor('none')

    plt.text(0, 0, text, ha='left', va='bottom', fontsize=fontsize, fontname=fontname)
    plt.show()
    

printTextOnMpl('2x + 10x + e + cos(x) + log(x)',fontname='cursive')