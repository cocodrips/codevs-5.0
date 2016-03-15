#include "evaluation.h"

int Evaluation::speedThreshold(int power) {
    return 60 / power;
}

int Evaluation::deleteStoneThreshold(int power) {
    return 40 * power;
}

int Evaluation::dogDistScore(int dist) {
    if (dist == 0) {
        return -10000;
    }
    if (dist < Evaluation::dogStepThreshld) return 0 / (dist * dist);
    return 0;
}

int Evaluation::soulDistScore(int dist) {
    if (dist == 0) {
        return Evaluation::soulGetScore;
    }
    return Evaluation::soulGetScore / 2 / dist;
}

int Evaluation::dropStoneEnemyThreshold(int power) {
    return 80 * power;
}

int Evaluation::doppelThreshold(int power) {
    return 40 * power; //もとは50
}