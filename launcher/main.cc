#include <SDL.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string>
const char* iOSGetDocumentsPath();
namespace fallout { int gnw_main(int argc, char** argv); }
namespace fallout2 { int falloutMain(int argc, char** argv); }
namespace fallout2 { bool gProgramIsActive = false; }
namespace fallout { bool GNW95_isActive = false; char GNW95_title[256] = {}; }
static int pickGame() {
  if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) != 0) return 1;
  SDL_Window* w = SDL_CreateWindow("Fallout", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 640, 480, SDL_WINDOW_FULLSCREEN | SDL_WINDOW_ALLOW_HIGHDPI);
  if (!w) return 1;
  SDL_Renderer* r = SDL_CreateRenderer(w, -1, SDL_RENDERER_ACCELERATED);
  int choice = 0;
  while (!choice) {
    SDL_Event e;
    while (SDL_PollEvent(&e)) {
      if (e.type == SDL_QUIT) choice = 1;
      if (e.type == SDL_MOUSEBUTTONDOWN) { int wh = 480; SDL_GetWindowSize(w, nullptr, &wh); choice = (e.button.y < wh / 2) ? 1 : 2; }
      if (e.type == SDL_FINGERDOWN) choice = (e.tfinger.y < 0.5f) ? 1 : 2;
    }
    if (r) { int width = 0; int height = 0; SDL_GetWindowSize(w, &width, &height); SDL_SetRenderDrawColor(r, 20, 16, 10, 255); SDL_RenderClear(r); SDL_SetRenderDrawColor(r, 190, 130, 40, 255); SDL_Rect top = {40, 40, width - 80, height / 2 - 60}; SDL_RenderFillRect(r, &top); SDL_SetRenderDrawColor(r, 90, 110, 60, 255); SDL_Rect bottom = {40, height / 2 + 20, width - 80, height / 2 - 60}; SDL_RenderFillRect(r, &bottom); SDL_RenderPresent(r); }
    SDL_Delay(16);
  }
  if (r) SDL_DestroyRenderer(r);
  SDL_DestroyWindow(w);
  SDL_Quit();
  return choice;
}
int main(int argc, char** argv) {
  (void)argc; (void)argv;
  SDL_SetHint(SDL_HINT_MOUSE_TOUCH_EVENTS, "0");
  SDL_SetHint(SDL_HINT_TOUCH_MOUSE_EVENTS, "0");
  std::string docs = iOSGetDocumentsPath();
  std::string dir1 = docs + "/Fallout1";
  std::string dir2 = docs + "/Fallout2";
  mkdir(dir1.c_str(), 0755);
  mkdir(dir2.c_str(), 0755);
  int choice = pickGame();
  std::string dir = choice == 2 ? dir2 : dir1;
  chdir(dir.c_str());
  char prog[16] = "Fallout";
  char* args[2] = {prog, nullptr};
  if (choice == 2) { SDL_Init(SDL_INIT_AUDIO | SDL_INIT_VIDEO | SDL_INIT_EVENTS); return fallout2::falloutMain(1, args); }
  return fallout::gnw_main(1, args);
}

