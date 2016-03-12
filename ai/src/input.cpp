#ifndef AI_INPUT
#define AI_INPUT

#include "input.h"

namespace Input {
void playerInput(State *state, istream& cin) {
    int i, y, x, n;

    state->start();

    int power;
    cin >> power;
    state->power = power;

    // フィールド情報
    int r, c;
    cin >> r >> c;
    string row;
    REP (y, Y) {
        cin >> row;
        REP (x, X) {
            state->field[y][x] = Cell(row[x]);
        }
    }

    // 忍者情報
    cin >> n;
    REP (c, n) {
        cin >> i >> y >> x;
        state->ninjas[i] = Character(i, y, x);
    }

    // 犬情報
    cin >> n;
    REP(c, n) {
        cin >> i >> y >> x;
        Point point = Point(y, x);
        state->dogPoints.insert(Point(y, x));
        state->dogs.insert(make_pair(point, Character(i, y, x)));
    }

    // ソウル情報
    cin >> n;
    REP (c, n) {
        cin >> y >> x;
        state->souls.insert(Point(y, x));
    }

    REP(c, Skill::Max) {
        cin >> x;
        state->skillUsed[c] = x;
    }
}

void mainInput(Controller *controller, istream& cin) {
    int timelimit;
    State &state = controller->myState;

    cin >> timelimit;

    int skillNum;
    cin >> skillNum;

    int skillPower;
    REP(i, skillNum) {
        cin >> skillPower;
        state.skillPower[i] = skillPower;
    }

    playerInput(&controller->myState, cin);
    playerInput(&controller->enemyState, cin);
}
}

#endif
