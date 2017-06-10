import pandas as pd


def save_plot(data_frame: pd.DataFrame, save_path: str, title: str):
    plot = data_frame.plot(title=title)
    plot_figure = plot.get_figure()
    plot_figure.savefig(save_path + ".line.png")

    # hist = data_frame.plot.hist(alpha=0.5, bins=160, normed=True,
    #                             title=plot_name + ' histogram')
    # hist_figure = hist.get_figure()
    # hist_figure.savefig(plot_save_path + ".hist.png")