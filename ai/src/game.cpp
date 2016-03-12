#include "codevs.h"
#include "controller.h"
#include "input.h"
#include "output.h"

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
            Output::mainOutput(&controller, cout);
        }

    }

};

int main() {
    Game game = Game();
    game.start();
}