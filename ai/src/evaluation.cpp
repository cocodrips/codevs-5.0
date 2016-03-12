#include "evaluation.h"

int Evaluation::dogDistScore(int dist) {
    if (dist == 0) {
        return -10000;
    }
    if (dist > Evaluation::dogStepThreshld) return 0;
    return 0;
}

int Evaluation::soulDistScore(int dist) {
    if (dist == 0) {
        return Evaluation::soulGetScore;
    }
    return Evaluation::soulGetScore / 2 / dist;
}
