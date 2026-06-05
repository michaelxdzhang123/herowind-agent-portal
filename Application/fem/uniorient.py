import fire


def unior(inpfile):
    """读取 Abaqus .inp 文件，将 shell section 中的方向定义统一替换为 or1，并输出到新文件。

    :param inpfile: 输入的 Abaqus .inp 文件路径
    """
    lns = open(inpfile, "r").readlines()
    out = ""

    shellsec = False
    for i in lns:
        if not shellsec:
            shellsec = i.find("shell section") != -1

        if shellsec and i.find("or") != -1:
            sp = i.split(",")
            out += ",".join(sp[:-1])
            out += ",or1\n"
        else:
            out += i
    of = inpfile.replace(".inp", "_unior.inp")
    open(of, "w").write(out)
    print(f"Wrote to {of}")


def main():
    """主函数，通过 fire 模块暴露 unior 命令行接口。"""
    fire.Fire(unior)


if __name__ == "__main__":
    main()
