# W3 生词表 CSV -> 自动生成练习题
# 运行: python vocab_tool.py
import os
import csv
import sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import weekpath  # noqa: E402  统一解析 data/ 路径，换目录也不会找不到文件
DATA = weekpath.data_path("生词表.csv")
def load_words(path=DATA):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))
def filter_by_level(words, level="4"):
    return [w for w in words if str(w["HSK等级"]) == str(level)]
def count_by_pos(words):
    return Counter(w["词性"] for w in words)
def gen_exercises(words, out=None):
    # 产物统一落到代码包根目录
    # 打开文件，注意这里用 with 缩进内部代码
    out =   out or weekpath.root_path("练习.txt")
    with open   (out, "w", encoding="utf-8") as f:
        for w in words:
            # 确保这里的 f.write 在 with 块内（缩进比 for 多一层）
            f.write("用“%s”造一个句子。 [__]\n" % w.get("词语", w.get("word", "未知词汇")))
if __name__ == "__main__":
    words = load_words()
    lv4 = filter_by_level(words, "4")
    print("总词汇 %d 个，其中 HSK4 词汇 %d 个，词性分布：%s"
          % (len(words), len(lv4), count_by_pos(lv4)))
    out = weekpath.root_path("练习.txt")
    gen_exercises(lv4, out)
    print("已生成：%s" % out)
