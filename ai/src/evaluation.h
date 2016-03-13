#ifndef AI_EVALUATION_H
#define AI_EVALUATION_H


namespace Evaluation {
    const int dogStepThreshld = 5;
    const int soulGetScore = 100;
    const int doppelThreshold = 50;
    const int speedPowerThreshold = 3;

    int speedThreshold (int power);
    int dogDistScore(int dist);
    int soulDistScore(int dist);
};


#endif //AI_EVALUATION_H
