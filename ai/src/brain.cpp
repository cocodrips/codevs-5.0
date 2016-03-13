#include "brain.h"

bool Brain::canMove(const State &state, const Point me, const Point direction) {
    Point nextPos = me + direction;
    if (!nextPos.isInsideField()) return false;
    Cell cell = state.field[nextPos.y][nextPos.x];

    if (cell.isWall()) return false;
    if (cell.isBlock()) {
        Point nextBlock = nextPos + direction;
        Cell nextBlockCell = state.field[nextBlock.y][nextBlock.x];
        if (!nextBlockCell.isEmpty()) return false;
        if (state.dogPoints.find(nextBlock) != state.dogPoints.end()) return false;

        // 忍者のマスに石が行くなら駄目
        set<int> dists = state.distToNinja(nextBlock);
//        if (dists.find(0) != dists.end()) return false;
    }
    return true;
}

Point Brain::move(State *state, const Point me, const Point direction) {
    Point nextPos = me + direction;
    Cell &cell = state->field[nextPos.y][nextPos.x];

    if (cell.isBlock()) {
        Point nextBlock = nextPos + direction;
        Cell &nextBlockCell = state->field[nextBlock.y][nextBlock.x];

        nextBlockCell.type = Cell::Block;
        cell.type = Cell::Empty;
    }
    return nextPos;
}

int Brain::moveToDestination(State *state, Point *outMe, const vector<Point> &path,
                             vector<Point> *outGetSouls, const set<Point> &souls) {
    int score = 0;
    for (Point p : path) {
        auto field = state->field;

        if (!canMove(*state, *outMe, p)) {
            return -INF;
        }
        *outMe = move(state, *outMe, p);

        // 中継地点にソウルがあるか
        if (state->souls.find(*outMe) != state->souls.end()) {
            if (souls.find(*outMe) == souls.end()) {
                outGetSouls->push_back(*outMe);
                score += Evaluation::soulGetScore;
            }
        }
    }
    return score;
}

void Brain::setNextDogs(State *state) {
    vector<vector<int> > stepsFromNinja = state->stepsToNinjas;
    if (state->doppelganger.isInsideField()) {
        stepsFromNinja = state->stepsToDopperl;
    }

    set<Point> newDogPoints;
    map<Point, Character> newDogs;

    int size = state->dogs.size();

    set<Character> idSortDogSet;
    for (pair<Point, Character> dogPair : state->dogs) {
        Character dog = dogPair.second; // copy
        dog.dist = stepsFromNinja[dog.point.y][dog.point.x];
        idSortDogSet.insert(dog);
    }

    for (Character dog : idSortDogSet) {
        Point bestDirection = Direction::directions[4];
        int bestStep = INF;

        REP (i, DIRECTION_NUM) {
            Point direction = Direction::directions[i];
            Point point = dog.point + direction;
            int step = stepsFromNinja[point.y][point.x];
            if (newDogPoints.find(point) != newDogPoints.end()) continue;
            if (step < bestStep) {
                bestDirection = direction;
                bestStep = step;
            }
        }

        dog.point += bestDirection;
        newDogPoints.insert(dog.point);
        newDogs[dog.point] = dog;
    }

    vector<Point> v(newDogPoints.begin(), newDogPoints.end());
    state->dogs = newDogs;
    state->dogPoints = newDogPoints;
}



int Brain::getDogScore(const State &state) {
    // int directionScore[4] = {};
    int score = 0;
    for (auto point : state.dogPoints) {
        int step = state.stepsToNinjas[point.y][point.x];
        score += Evaluation::dogDistScore(step);
    }
    return score;
}

vector<Point> Brain::tryAllRelayPoint(const State &_state,
                                      const Point &_me,
                                      const Point &destination, int step,
                                      set<Point> *outGetSouls) {

    vector<Point> bestPath;
    vector<Point> bestGetSouls;
    int bestScore = -INF;
    for (vector<Point> path : Path::destinations[step].at(destination)) {
        State state = _state;
        Point me = _me;
        int score = 0;
        vector<Point> getSouls;

        score = moveToDestination(&state, &me, path, &getSouls, *outGetSouls);
        if (bestScore < score) {
            bestScore = score;
            bestPath = path;
            bestGetSouls = getSouls;
        }
    }
    for (auto p : bestGetSouls) {
        outGetSouls->insert(p);
    }
    return bestPath;
}


int Brain::setBestPath(const State &_state, const int step,
                       vector<Point> *outPath0, vector<Point> *outPath1, int initScore) {
    int bestScore = initScore;
    vector<Point> bestPath0;
    vector<Point> bestPath1;

    State doppelState = _state;


    for (auto destPair0 : Path::destinations[step]) {
        for (auto destPair1 : Path::destinations[step]) {

            int score = 0;
            State state = _state; // Copy

            Point d0 = destPair0.first;
            Point d1 = destPair1.first;

            state.ninjas[0].point += d0;
            state.ninjas[1].point += d1;

            if (!state.ninjas[0].point.isInsideField()) continue;
            if (!state.ninjas[1].point.isInsideField()) continue;

            if (!state.field[state.ninjas[0].point.y][state.ninjas[0].point.x].isEmpty()) continue;
            if (!state.field[state.ninjas[1].point.y][state.ninjas[1].point.x].isEmpty()) continue;


            // 移動する
            set<Point> getSouls;
            vector<Point> path0 = tryAllRelayPoint(state, _state.ninjas[0].point, d0, step, &getSouls);
            vector<Point> path1 = tryAllRelayPoint(state, _state.ninjas[1].point, d1, step, &getSouls);

            Point p0 = _state.ninjas[0].point;
            Point p1 = _state.ninjas[1].point;

            REP(i, step) {
                if (i < path0.size()) {
                    if (canMove(state, p0, path0[i])) p0 = move(&state, p0, path0[i]);
                }
                if (i < path1.size()) {
                    if (canMove(state, p1, path1[i])) p1 = move(&state, p1, path1[i]);
                }
            }
            state.ninjas[0].point = p0;
            state.ninjas[1].point = p1;

            state.setStepsToNinjas();

            int soulPoint = getSouls.size() * Evaluation::soulGetScore; // 取得したソウルのポイント
            vector<Point> restSouls;
            set_difference(state.souls.begin(), state.souls.end(),
                           getSouls.begin(), getSouls.end(),
                           back_inserter(restSouls));

            // ソウルへの距離
            int soulDistPoint = 0;
            REP(i, 8) {
                auto itr = restSouls.begin() + i;
                if (itr == restSouls.end()) break;
                Point p = *itr;
                soulDistPoint += Evaluation::soulDistScore(state.stepsToNinjas[p.y][p.x]);
            }


            score += soulPoint + soulDistPoint;

            // 犬移動
            if (state.doppelganger.isInsideField()) {
                state.setStepsToDoppel(state.doppelganger);
            }
            setNextDogs(&state);
            int dogPoint = getDogScore(state);
            score += dogPoint;

#ifdef DEBUG
            cerr << getSouls.size() << " ";
            for (Point p: path0) {
                cerr << p.print();
            }
            cerr << " ";
            for (Point p: path1) {
                cerr << p.print();
            }

            cerr << " score: " << score << " dog:" << dogPoint << " soul:" <<
            soulPoint << " soulDist:" << soulDistPoint << endl;
#endif

            if (bestScore < score) {
                bestScore = score;
                bestPath0 = path0;
                bestPath1 = path1;
#ifdef DEBUG
                cerr << bestScore << endl;
                state.dumpField(cerr);
                state.dumpStepsToNinjas(cerr);
                if (state.doppelganger.isInsideField()) {
                    state.dumpStepsToDoppel(cerr);
                }
#endif
            }

        }
    }
#ifdef DEBUG
    cerr << "====" << endl;
    for (Point p: bestPath0) {
        cerr << p.print();
    }
    cerr << " ";
    for (Point p: bestPath1) {
        cerr << p.print();
    }
#endif

    *outPath0 = bestPath0;
    *outPath1 = bestPath1;
    return bestScore;
}


void Brain::simulate(const State &_state, const State &enemyState,  string *outSkill,
                     vector<Point> *outPath0, vector<Point> *outPath1) {


    int defaultScore = setBestPath(_state, 2, outPath0, outPath1, -INF);
    int bestScore = defaultScore;


    // doppel
    State state = _state;
    if (state.power > state.skillPower[Skill::DoppelMe]) {
        REP(i, NINJA_NUM){
            vector<Point> path0;
            vector<Point> path1;
            state.doppelganger = state.ninjas[i].point;
            int score = setBestPath(state, 2, &path0, &path1, defaultScore);
            if (bestScore < score &&
                    defaultScore + Evaluation::doppelThreshold < score) {
                bestScore = score;
                *outPath0 = path0;
                *outPath1 = path1;
                stringstream ss;
                ss << 3 << endl;
                ss << Skill::DoppelMe << " " << state.doppelganger.y << " " << state.doppelganger.x;
                *outSkill = ss.str();
            }
        }
    }

    // speed
    state = _state;
    if (state.skillPower[Skill::Speed] <= Evaluation::speedPowerThreshold) {
        if (state.power > state.skillPower[Skill::Speed] &&
                state.power > state.skillPower[Skill::DoppelMe] * 3) {
            vector<Point> path0;
            vector<Point> path1;
            int score = setBestPath(state, 3, &path0, &path1, defaultScore);
            if (bestScore < score &&
                    defaultScore + Evaluation::speedThreshold(state.skillPower[Skill::Speed]) < score) {
                bestScore = score;
                *outPath0 = path0;
                *outPath1 = path1;
                stringstream ss;
                ss << 3 << endl;
                ss << Skill::Speed;
                *outSkill = ss.str();
            }
        }
    }

    if (state.power)

    if (*outSkill == "") {
        stringstream ssSkill;
        ssSkill << 2;
        *outSkill = ssSkill.str();
    }

    return;
}