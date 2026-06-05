import pandas as pd
import argparse
from matplotlib import pyplot as plt


def load_st_file(fname):
    """加载 HAWC2 的 .st 文件并返回 pandas DataFrame。

    :param fname: .st 文件路径
    :return: 包含截面属性的 DataFrame
    """
    l = open(fname, "r").readlines()
    keys = l[1].split()

    dat = {}
    key = None
    for i in l[2:]:
        if i.startswith("$"):
            key = i.split()[0]
            dat[key] = []
        elif key != None:
            dat[key].append([float(j) for j in i.split()])

    return pd.DataFrame(dat["$1"], columns=keys)


# plot all columns in the dataframe in a single plot, keep the plot open
def plot_df(ax, axmap, df, name):
    """在子图上绘制 DataFrame 中指定的列。

    :param ax: matplotlib 子图数组
    :param axmap: 列名到子图索引的映射字典
    :param df: 要绘制的 DataFrame
    :param name: 图例标签名称
    """

    for i in axmap:
        a = ax[axmap[i]]
        a.plot(df["r"], df[i], label=name)
        a.set_title(i)
        if i == "mass":
            a.legend(loc="upper left")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("file1", help="file1")
    p.add_argument("file2", help="file2")
    p.add_argument("--out", default="out.png", help="output file")
    args = p.parse_args()

    df1 = load_st_file(args.file1)
    df2 = load_st_file(args.file2)

    # df2[[i for i in df2.columns if i not in ["r", "mass"]]] *= 1e-6
    fig, ax = plt.subplots(3, 3, figsize=(12, 12))

    axmap = {
        "mass": (0, 0),
        "K11": (1, 0),
        "K22": (2, 0),
        "K33": (0, 1),
        "K44": (1, 1),
        "K55": (2, 1),
        "K66": (0, 2),
    }
    plot_df(ax, axmap, df1, args.file1)
    plot_df(ax, axmap, df2, args.file2)

    plt.savefig(args.out)
    print("saved to", args.out)
