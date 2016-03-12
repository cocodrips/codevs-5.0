#include "codevs.h"
#include "controller.h"
#include "input.h"

class Game {
public:
    const string name = "cocodrips ;)";
    Controller controller;
    Game() {
        controller = Controller();
    }

    void start() {
        cout << name << endl;
        cout.flush();

        while (1) {
            Input::mainInput(&controller, cin);
            controller.myState.dumpField(cerr);
            controller.enemyState.dumpField(cerr);
//            cout << 2 << endl;
//            cout << "NN" << endl;
//            cout << "NN" << endl;
        }

    }

};

int main() {
    Game game = Game();
    game.start();
}