#ifndef AI_EVALUATION_H
#define AI_EVALUATION_H


namespace Evaluation {
    const int dogStepThreshld = 5;
    const int soulGetScore = 100;
    const int doppelThreshold = 50;

    int dogDistScore(int dist);
    int soulDistScore(int dist);
};


#endif //AI_EVALUATION_H
