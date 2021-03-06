#ifndef AI_EVALUATION_H
#define AI_EVALUATION_H


namespace Evaluation {
const int mySkillThreshld = 70;
const int SendDogScorePerPower = 4;
const int dogStepThreshld = 4;
const int soulGetScore = 100;
const int speedPowerThreshold = 3;
const int dropEnemyBlockMostFar = 5;

const int doppelTestPointY[] = {1, 7, 12, 15};
const int doppelTestPointX[] = {1, 7, 12};

int speedThreshold(int power);

int sendDogThreshold(int power);

int deleteStoneThreshold(int power);

int dropStoneEnemyThreshold(int power);

int doppelThreshold(int power);

int closedDirectionScore(float closedDirectionNum);


int dogDistScore(int dist);

int soulDistScore(int dist);
};


#endif //AI_EVALUATION_H
