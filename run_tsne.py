

if __name__ == '__main__':
    from MulticoreTSNE import MulticoreTSNE as TSNE
    tsne = TSNE(n_jobs=2)
    Y = tsne.fit_transform(embeds)
