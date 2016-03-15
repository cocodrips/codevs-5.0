#include "evaluation.h"

int Evaluation::speedThreshold(int power) {
    return 60 / power;
}

int Evaluation::deleteStoneThreshold(int power) {
    return 40 * power;
}

int Evaluation::closedDirectionScore(float closedDirectionNum) {
    if (closedDirectionNum <= 2) { return 0; }
    if (closedDirectionNum < 3) { return -20; }
    if (closedDirectionNum < 4) { return -100; }
    if (closedDirectionNum == 4) { return -1000; }
    return -1000;
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