#include "brain.h"

bool Brain::canMove(const State &state, const Point me, const Point direction) {
    Point nextPos = me + direction;
    Cell cell = state.field[nextPos.y][nextPos.x];

    if (cell.isWall()) return false;
    if (cell.isBlock()) {
        Point nextBlock = nextPos + direction;
        Cell nextBlockCell = state.field[nextBlock.y][nextBlock.x];
        if (!nextBlockCell.isEmpty()) return false;

        // 忍者のマスに石が行くなら駄目
        set<int> dists = state.distToNinja(nextBlock);
        if (dists.find(0) != dists.end()) return false;
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
        Character &dog = dogPair.second; // copy
        idSortDogSet.insert(dog);
    }


    for (Character _dog : idSortDogSet) {
        Character dog = _dog; // copy

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
                                      const Point &direction, int step,
                                      set<Point> *outGetSouls) {

    State state = _state;
    vector<Point> bestPath;
    vector<Point> bestGetSouls;
    int bestScore = -INF;

    for (vector<Point> path : Path::destinations[2].at(direction)) {
        Point me = _me;
        int score = 0;
        vector<Point> getSouls;
        for (Point p : path) {
            auto field = state.field;

            if (!canMove(state, me, p)) continue;
            me = move(&state, me, p);

            // 中継地点にソウルがあるか
            if (state.souls.find(me) != state.souls.end()) {
                if (outGetSouls->find(me) == outGetSouls->end()) {
                    getSouls.push_back(me);
                    score += Evaluation::soulGetScore;
                }
            }
        }

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


void Brain::setBestPath(const State &_state, int step, vector<Point> *outPath0, vector<Point> *outPath1) {
    int bestScore = -INF;
    vector<Point> bestPath0;
    vector<Point> bestPath1;

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

            // 移動する
            set<Point> getSouls;
            vector<Point> path0 = tryAllRelayPoint(state, state.ninjas[0].point, d0, step, &getSouls);
            vector<Point> path1 = tryAllRelayPoint(state, state.ninjas[1].point, d1, step, &getSouls);

            int soulPoint = getSouls.size() * Evaluation::soulGetScore; // 取得したソウルのポイント
            vector<Point> restSouls;
            set_difference(getSouls.begin(), getSouls.end(),
                           state.souls.begin(), state.souls.end(), back_inserter(restSouls));

            state.setStepsToNinjas();
            // ソウルへの距離
            REP(i, 4) {
                auto itr = restSouls.begin() + i;
                if (itr == restSouls.end()) break;
                Point p = *itr;
                soulPoint += Evaluation::soulDistScore(state.stepsToNinjas[p.y][p.x]);
            }

            score += soulPoint;

            // 犬移動
            setNextDogs(&state);
            int dogPoint = getDogScore(state);
            score += dogPoint;

#ifdef DEBUG
            for (Point p: path0) {
                cerr << p.print();
            }
            cerr << " ";
            for (Point p: path1) {
                cerr << p.print();
            }
            cerr << "score: " << score << endl;
#endif

            if (bestScore < score) {
                bestScore = score;
                bestPath0 = path0;
                bestPath1 = path1;
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
}


void Brain::simulate(State *state, string *outSkill,
                     vector<Point> *outPath0, vector<Point> *outPath1) {
    stringstream ssSkill;

    ssSkill << 2 << endl;
    *outSkill = ssSkill.str();
    setBestPath(*state, 2, outPath0, outPath1);

    return;
}