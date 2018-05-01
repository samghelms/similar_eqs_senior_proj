import numpy as np
from numba import jit
import pickle
import time
from scipy.sparse.linalg import svds


@jit(nopython=True)
def _inner_log_lik(e, f, T):
    cur_log_lik = 0
    for e_t in e:
        log_sum = 0
        for f_t in f:
            log_sum += T[e_t, f_t]
        cur_log_lik += np.log(log_sum)
    return cur_log_lik


def compute_log_lik(T, pairs):
    cur_log_lik = 0
    # e list = f _list len
    for e, f in pairs:
        cur_log_lik += _inner_log_lik(e, f, T)
    return cur_log_lik


@jit(nopython=True)
def _estimate_numba_inner(T, e, f, s_total, counts, total):
    for e_t in e:
        for f_t in f:
            s_total[e_t] += T[e_t, f_t]

    # counts
    for e_t in e:
        for f_t in f:
            counts[e_t, f_t] += T[e_t, f_t] / s_total[e_t]
            total[f_t] += T[e_t, f_t] / s_total[e_t]


@jit(nopython=True)
def _fill_T(T, counts, total):
    for e_t in range(T.shape[0]):
        for f_t in range(T.shape[1]):
            T[e_t, f_t] = counts[e_t, f_t] / total[f_t]


def _estimate(T, pairs, start_log_lik, tol):
    prev_log_lik = -np.inf
    it_counter = 0
    cur_log_lik = start_log_lik
    print("starting log likelihood: {cur_log_lik}".format(cur_log_lik=cur_log_lik))
    while (cur_log_lik - prev_log_lik) > tol:
        start_it_time = time.clock()
        counts = np.zeros(T.shape)
        total = np.zeros(T.shape[1])
        for e, f in pairs:
            # compute normalization
            s_total = np.zeros(T.shape[0])
            _estimate_numba_inner(T, e, f, s_total, counts, total)

        _fill_T(T, counts, total)

        prev_log_lik = cur_log_lik
        cur_log_lik = compute_log_lik(T, pairs)

        print("current log likelihood (end of loop): {cur_log_lik}".format(cur_log_lik=cur_log_lik))

        print("time taken for loop {it}: {time}".format(it=str(it_counter),
            time=str(time.clock() - start_it_time)))
        # serialize
        pickle.dump(T, open('T_'+str(it_counter)+'.pkl', 'wb+'))
        it_counter += 1
    return T


@jit(nopython=True)
def _calculate_embeds(E, T, token_ids, doc_len, doc_idx):
    for i in range(T.shape[0]):
        temp = 0
        for token_id in token_ids:
            temp += T[i, token_id]
        temp /= doc_len + 1
        E[doc_idx, i] = temp


class TREmbed:
    def __init__(self, vocab, pairs, tol=1000):
        """Short summary.

        Parameters
        ----------
        vocab : type
            Description of parameter `vocab`.

        Returns
        -------
        type
            Description of returned object.

        """
        self.T = np.ones(vocab.shape) * 1.0 / vocab.shape[0]
        self.pairs = pairs
        self.start_log_lik = compute_log_lik(self.T, self.pairs)
        self.tol = tol
        self.vocab = vocab


    def estimate(self, test=None):
        self.T = _estimate(self.T, self.pairs, self.start_log_lik, self.tol)


    def construct_embeds(self, doc_list, name='raw_tr_embed.pkl', k=100):
        E = np.zeros((len(doc_list), self.T.shape[0]))
        for doc_idx, doc in enumerate(doc_list):
            if doc_idx % 1000 == 0:
                print(doc_idx)
            _calculate_embeds(E, self.T, [self.vocab.ftoint(token) for token in doc if self.vocab.ftoint(token) is not None], len(doc), doc_idx)
        # TODO: remove this
        pickle.dump(E, open(name, 'wb+'))
        print("embeds constructed, projecting")
        U, s, V = svds(E, k=k)
        proj_E = U.dot(np.diag(s))
        pickle.dump(proj_E, open('raw_tr_embed_proj.pkl', 'wb+'))
        return proj_E
