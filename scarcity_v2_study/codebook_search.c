#define _POSIX_C_SOURCE 200809L
/* Exact codebook branch-and-bound for the unpaid S-DIRECT certificate.
   Rewards and weights are nonnegative integers on a common scale.
   Objective is sum_s weight[s] * max_{w in S} reward[s][w].
   Deterministic: combinations are taken in increasing word-index order
   after a fixed score permutation (score, then index). */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_S 96
#define MAX_W 32

static int nS, nW, K, collect_limit;
static long time_limit_ms;
static int64_t reward[MAX_S][MAX_W];
static int64_t weight[MAX_S];
static int order[MAX_W];
static __int128 best;
static int have_best;
static long nodes;
static int timed_out;
static int nopt;
static int truncated;
static int *opt_store; /* collect_limit * K */

static long cpu_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts);
    return (long)ts.tv_sec * 1000L + ts.tv_nsec / 1000000L;
}

static void print_i128(__int128 x) {
    if (x == 0) {
        putchar('0');
        return;
    }
    if (x < 0) {
        putchar('-');
        x = -x;
    }
    char buf[64];
    int n = 0;
    while (x > 0) {
        buf[n++] = (char)('0' + (int)(x % 10));
        x /= 10;
    }
    while (n--) putchar(buf[n]);
}

static __int128 word_score(int w) {
    __int128 s = 0;
    for (int i = 0; i < nS; i++) s += (__int128)weight[i] * reward[i][w];
    return s;
}

static void rec(int start, int64_t *cur, int *chosen, int slots, long t0) {
    nodes++;
    if ((nodes & 65535L) == 0 && cpu_ms() - t0 > time_limit_ms) {
        timed_out = 1;
        return;
    }
    if (slots == 0) {
        __int128 v = 0;
        for (int s = 0; s < nS; s++) v += (__int128)weight[s] * cur[s];
        if (!have_best || v > best) {
            best = v;
            have_best = 1;
            nopt = 0;
            truncated = 0;
        }
        if (v == best) {
            if (nopt < collect_limit) {
                memcpy(opt_store + nopt * K, chosen, (size_t)K * sizeof(int));
            } else {
                truncated = 1;
            }
            nopt++;
        }
        return;
    }
    if (nW - start < slots) return;

    /* Upper bound: sum of the best `slots` single-word gains over `cur`. */
    __int128 pots[MAX_W];
    int np = 0;
    for (int i = start; i < nW; i++) {
        int w = order[i];
        __int128 pot = 0;
        for (int s = 0; s < nS; s++) {
            int64_t d = reward[s][w] - cur[s];
            if (d > 0) pot += (__int128)weight[s] * d;
        }
        pots[np++] = pot;
    }
    for (int i = 1; i < np; i++) {
        __int128 key = pots[i];
        int j = i - 1;
        while (j >= 0 && pots[j] < key) {
            pots[j + 1] = pots[j];
            j--;
        }
        pots[j + 1] = key;
    }
    __int128 curv = 0;
    for (int s = 0; s < nS; s++) curv += (__int128)weight[s] * cur[s];
    __int128 gain = 0;
    int take = slots < np ? slots : np;
    for (int i = 0; i < take; i++) gain += pots[i];
    if (have_best && curv + gain < best) return;

    for (int i = start; i <= nW - slots; i++) {
        int w = order[i];
        int64_t next[MAX_S];
        for (int s = 0; s < nS; s++) {
            int64_t rw = reward[s][w];
            next[s] = rw > cur[s] ? rw : cur[s];
        }
        chosen[K - slots] = w;
        rec(i + 1, next, chosen, slots - 1, t0);
        if (timed_out) return;
    }
}

int main(void) {
    if (scanf("%d %d %d %ld %d", &nS, &nW, &K, &time_limit_ms, &collect_limit) != 5) {
        fprintf(stderr, "bad header\n");
        return 2;
    }
    if (nS < 1 || nS > MAX_S || nW < 1 || nW > MAX_W || K < 1 || K > nW || collect_limit < 1) {
        fprintf(stderr, "bad dims\n");
        return 2;
    }
    for (int s = 0; s < nS; s++) {
        if (scanf("%lld", (long long *)&weight[s]) != 1) return 2;
    }
    for (int s = 0; s < nS; s++) {
        for (int w = 0; w < nW; w++) {
            if (scanf("%lld", (long long *)&reward[s][w]) != 1) return 2;
        }
    }
    for (int w = 0; w < nW; w++) order[w] = w;
    for (int i = 1; i < nW; i++) {
        int key = order[i];
        __int128 ks = word_score(key);
        int j = i - 1;
        while (j >= 0) {
            __int128 js = word_score(order[j]);
            if (js > ks || (js == ks && order[j] < key)) break;
            order[j + 1] = order[j];
            j--;
        }
        order[j + 1] = key;
    }
    /* Greedy seed so the bound prunes from the first node. */
    {
        int64_t gcur[MAX_S];
        memset(gcur, 0, sizeof(gcur));
        int used[MAX_W];
        memset(used, 0, sizeof(used));
        for (int t = 0; t < K; t++) {
            int bw = -1;
            __int128 bv = 0;
            int have = 0;
            for (int w = 0; w < nW; w++) {
                if (used[w]) continue;
                __int128 v = 0;
                for (int s = 0; s < nS; s++) {
                    int64_t m = reward[s][w] > gcur[s] ? reward[s][w] : gcur[s];
                    v += (__int128)weight[s] * m;
                }
                if (!have || v > bv || (v == bv && w < bw)) {
                    bv = v;
                    bw = w;
                    have = 1;
                }
            }
            used[bw] = 1;
            for (int s = 0; s < nS; s++) if (reward[s][bw] > gcur[s]) gcur[s] = reward[s][bw];
            best = bv;
            have_best = 1;
        }
    }
    opt_store = calloc((size_t)collect_limit * (size_t)K, sizeof(int));
    if (!opt_store) return 2;
    int64_t cur0[MAX_S];
    memset(cur0, 0, sizeof(cur0));
    int chosen[MAX_W];
    long t0 = cpu_ms();
    rec(0, cur0, chosen, K, t0);
    long elapsed = cpu_ms() - t0;
    printf("%s\n", timed_out ? "timeout" : "complete");
    print_i128(have_best ? best : 0);
    printf("\n%d\n%d\n%ld\n%ld\n", nopt, truncated, nodes, elapsed);
    int show = nopt < collect_limit ? nopt : collect_limit;
    if (truncated) show = collect_limit;
    /* nopt counts all; stored min(nopt, collect_limit) */
    if (nopt < show) show = nopt;
    printf("%d\n", show);
    for (int i = 0; i < show; i++) {
        for (int k = 0; k < K; k++) {
            if (k) putchar(' ');
            printf("%d", opt_store[i * K + k]);
        }
        putchar('\n');
    }
    free(opt_store);
    return 0;
}
