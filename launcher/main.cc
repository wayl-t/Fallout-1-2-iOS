#include <SDL.h>
#include <unistd.h>
#include <sys/stat.h>
#include <string>
#include <cstdio>
#include <cstdarg>
const char* iOSGetDocumentsPath();
namespace fallout { int gnw_main(int argc, char** argv); }
namespace fallout2 { int falloutMain(int argc, char** argv); }
namespace fallout2 { bool gProgramIsActive = false; }
namespace fallout { bool GNW95_isActive = false; char GNW95_title[256] = {}; }
static FILE* gLauncherLog = nullptr;
static void launcherLog(const char* fmt, ...) {
  if (!gLauncherLog) return;
  va_list args; va_start(args, fmt);
  vfprintf(gLauncherLog, fmt, args);
  va_end(args);
  fputc(10, gLauncherLog);
  fflush(gLauncherLog);
}
static int pickGame() {
  if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) != 0) { launcherLog("pickGame SDL_Init failed: %s", SDL_GetError()); return 1; }
  launcherLog("pickGame SDL_Init ok");
  SDL_Window* w = SDL_CreateWindow("Fallout", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 640, 480, SDL_WINDOW_FULLSCREEN | SDL_WINDOW_ALLOW_HIGHDPI);
  if (!w) { launcherLog("pickGame CreateWindow failed: %s", SDL_GetError()); return 1; }
  int winW = 0; int winH = 0; SDL_GetWindowSize(w, &winW, &winH);
  launcherLog("pickGame window size=%dx%d", winW, winH);
  SDL_Renderer* r = SDL_CreateRenderer(w, -1, SDL_RENDERER_ACCELERATED);
  if (!r) launcherLog("pickGame CreateRenderer failed: %s", SDL_GetError());
  int choice = 0;
  while (!choice) {
    SDL_Event e;
    while (SDL_PollEvent(&e)) {
      if (e.type == SDL_QUIT) { launcherLog("event QUIT -> choice=1"); choice = 1; }
      if (e.type == SDL_MOUSEBUTTONDOWN) { int wh = 480; SDL_GetWindowSize(w, nullptr, &wh); int c = (e.button.y < wh / 2) ? 1 : 2; launcherLog("event MOUSEBUTTONDOWN x=%d y=%d button=%d winH=%d -> choice=%d", e.button.x, e.button.y, (int)e.button.button, wh, c); choice = c; }
      if (e.type == SDL_MOUSEBUTTONUP) { launcherLog("event MOUSEBUTTONUP x=%d y=%d", e.button.x, e.button.y); }
      if (e.type == SDL_FINGERDOWN) { int c = (e.tfinger.y < 0.5f) ? 1 : 2; launcherLog("event FINGERDOWN fingerId=%lld x=%.4f y=%.4f pressure=%.3f -> choice=%d", (long long)e.tfinger.fingerId, (double)e.tfinger.x, (double)e.tfinger.y, (double)e.tfinger.pressure, c); choice = c; }
      if (e.type == SDL_FINGERUP) { launcherLog("event FINGERUP x=%.4f y=%.4f", (double)e.tfinger.x, (double)e.tfinger.y); }
    }
    if (r) { int width = 0; int height = 0; SDL_GetWindowSize(w, &width, &height); SDL_SetRenderDrawColor(r, 20, 16, 10, 255); SDL_RenderClear(r); SDL_SetRenderDrawColor(r, 190, 130, 40, 255); SDL_Rect top = {40, 40, width - 80, height / 2 - 60}; SDL_RenderFillRect(r, &top); SDL_SetRenderDrawColor(r, 90, 110, 60, 255); SDL_Rect bottom = {40, height / 2 + 20, width - 80, height / 2 - 60}; SDL_RenderFillRect(r, &bottom); SDL_RenderPresent(r); }
    SDL_Delay(16);
  }
  launcherLog("pickGame done choice=%d", choice);
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
  std::string logPath = docs + "/launcher.log";
  gLauncherLog = fopen(logPath.c_str(), "a");
  launcherLog("=== launcher start docs=%s ===", docs.c_str());
  std::string dir1 = docs + "/Fallout1";
  std::string dir2 = docs + "/Fallout2";
  int mk1 = mkdir(dir1.c_str(), 0755);
  int mk2 = mkdir(dir2.c_str(), 0755);
  launcherLog("mkdir Fallout1=%d Fallout2=%d", mk1, mk2);
  int choice = pickGame();
  launcherLog("main choice=%d", choice);
  std::string dir = choice == 2 ? dir2 : dir1;
  int cd = chdir(dir.c_str());
  launcherLog("chdir %s -> %d", dir.c_str(), cd);
  char prog[16] = "Fallout";
  char* args[2] = {prog, nullptr};
  if (choice == 2) { launcherLog("starting fallout2 engine"); SDL_Init(SDL_INIT_AUDIO | SDL_INIT_VIDEO | SDL_INIT_EVENTS); int rc = fallout2::falloutMain(1, args); launcherLog("fallout2 engine returned %d", rc); return rc; }
  launcherLog("starting fallout1 engine");
  int rc = fallout::gnw_main(1, args);
  launcherLog("fallout1 engine returned %d", rc);
  return rc;
}
