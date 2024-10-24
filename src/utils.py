from matplotlib.patches import Patch


class CustomLegend(Patch):
    def __init__(self, color, label, **kwargs):
        super().__init__(facecolor=color, **kwargs)
        self.label = label

    def set_label_below(self, ax, x, y, **textprops):
        ax.text(
            x,
            y - 0.05,
            self.label,
            horizontalalignment="center",
            verticalalignment="top",
            transform=ax.transAxes,
            **textprops
        )
        return self
