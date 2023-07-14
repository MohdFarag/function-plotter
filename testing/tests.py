import matplotlib.pyplot as plt

print(
sorted(style for style in plt.style.available if style != 'classic' and not style.startswith('_'))
    
)