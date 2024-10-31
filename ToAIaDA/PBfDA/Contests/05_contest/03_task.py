import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

months = ['January', 'February', 'March', 'April', 'May', 'November', 'December']
hornberg = [330, 260, 190, 150, 150, 120, 290]
strick = [300, 260, 200, 200, 160, 280, 160]
huetten = [300, 240, 190, 180, 160, 240, 150]


fig, ax = plt.subplots()

width = 0.2
ax.bar(months, hornberg, width, label='Hornberg', color='#F08080', zorder=3)
ax.bar([i + width for i in range(len(months))], strick, width, label='Strick', color='#00B050', zorder=3)
ax.bar([i + 2*width for i in range(len(months))], huetten, width, label='Huetten', color='#87CEEB', zorder=3)

ax.set_xlabel('Month')
ax.set_ylabel('Monthly Precipitation [mm]')
ax.set_xticks([i + width for i in range(len(months))])
ax.set_xticklabels(months)

hornberg_patch = mpatches.Patch(color='#F08080', label='Hornberg')
strick_patch = mpatches.Patch(color='#00B050', label='Strick')
huetten_patch = mpatches.Patch(color='#87CEEB', label='Huetten')

legend = plt.legend(handles=[hornberg_patch, strick_patch, huetten_patch], title='variable', bbox_to_anchor=(1, 0.7), frameon=False, loc='upper left', handletextpad=-0.5)
patches = legend.get_patches()
texts = legend.get_texts()

for patch in patches:
    patch.set_height(15)
    patch.set_width(patch.get_height())

plt.draw()

ax.grid(True, linestyle='-', color='lightgray', zorder=0)

ax.set_zorder(2)

plt.show()