
class Vocab:
    def __init__(self, pairs):
        """Short summary.

        Parameters
        ----------
        pairs : type
            list of (e, f) tuples.

        Constructs Vocab object

        """
        e, f = zip(*pairs)
        e = [item for sublist in e for item in sublist]
        f = [item for sublist in f for item in sublist]
        self.e_d = {tok: id for id, tok in enumerate(set(e))}
        self.f_d = {tok: id for id, tok in enumerate(set(f))}

        self.shape = (len(self.e_d), len(self.f_d))

    def etoint(self, token):
        return self.e_d[token]

    def ftoint(self, token):
        return self.f_d[token]

    def transform(self, pairs):
        e, f = zip(*pairs)
        map2id = lambda tokens, d: [d[t] for t in tokens]
        e_ids = [map2id(tokens, self.e_d) for tokens in e]
        f_ids = [map2id(tokens, self.f_d) for tokens in f]
        pairs = []
        for ix in range(len(e_ids)):
          pairs.append((e_ids[ix],f_ids[ix]))
        return pairs

    def save(self):
        pass
