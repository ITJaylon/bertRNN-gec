from torch.utils.data import Dataset


def parse_m2(gold_path, err_path, cor_path):
    file = open(gold_path)
    m2 = file.read().strip().split("\n\n")
    out1 = open(err_path, "w")
    out2 = open(cor_path, "w")
    # Do not apply edits with these error types
    skip = {"noop", "UNK", "Um"}

    for sent in m2:
        sent = sent.split("\n")
        cor_sent = sent[0].split()[1:]  # Ignore "S "
        out1.write(" ".join(cor_sent) + "\n")
        edits = sent[1:]
        offset = 0
        for edit in edits:
            edit = edit.split("|||")
            if edit[1] in skip: continue  # Ignore certain edits
            coder = int(edit[-1])
            if coder != 0: continue  # Ignore other coders
            span = edit[0].split()[1:]  # Ignore "A "
            start = int(span[0])
            end = int(span[1])
            cor = edit[2].split()
            cor_sent[start + offset:end + offset] = cor
            offset = offset - (end - start) + len(cor)
        out2.write(" ".join(cor_sent) + "\n")

def makeData(err_path, cor_path):
    err_text = []
    cor_text = []
    with open(err_path, encoding='utf-8') as f1:
        for line in f1.readlines():
            err_text.append(line.strip())

    with open(cor_path, encoding='utf-8') as f2:
        for line in f2.readlines():
            cor_text.append(line.strip())

    f1.close()
    f2.close()
    return err_text, cor_text


class MyDataSet(Dataset):
    def __init__(self,err_text,cor_text):
        self.err_text = err_text
        self.cor_text = cor_text
        self.size = len(err_text)

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        if (idx > self.size):
            print('index out of boundary!')
            return None
        return self.err_text[idx], self.cor_text[idx]

if __name__ == '__main__':
    # 原始的m2格式数据 gold_path , 输出error_text和correct_text
    gold_path = "../data/fce.train.gold.bea19.m2"
    err_path = "../data/fce_train_err_text.txt"
    cor_path = "../data/fce_train_cor_text.txt"
    parse_m2(gold_path,err_path,cor_path)