#include "ai.cpp"

int main() {
    // AIの名前を出力
    cout << "SampleAI.cpp" << endl;
    cout.flush();

    while (codevs::input()) {
        codevs::think();
        cout.flush();
    }

    return 0;
}