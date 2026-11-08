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
static SDL_Texture* loadBg(SDL_Renderer* r, const char* name) { std::string base = SDL_GetBasePath() ? SDL_GetBasePath() : ""; std::string p = base + name; SDL_Surface* sf = SDL_LoadBMP(p.c_str()); if (!sf) { launcherLog("bg load failed %s: %s", p.c_str(), SDL_GetError()); return nullptr; } SDL_Texture* tx = SDL_CreateTextureFromSurface(r, sf); SDL_FreeSurface(sf); launcherLog("bg loaded %s", p.c_str()); return tx; }
static void drawBtn(SDL_Renderer* r, SDL_Rect b, bool first) { SDL_SetRenderDrawColor(r, 0, 0, 0, 150); SDL_RenderFillRect(r, &b); SDL_SetRenderDrawColor(r, first ? 255 : 120, first ? 176 : 200, first ? 46 : 235, 255); for (int i = 0; i < 4; i++) { SDL_Rect f = { b.x + i, b.y + i, b.w - 2 * i, b.h - 2 * i }; SDL_RenderDrawRect(r, &f); } SDL_SetRenderDrawColor(r, first ? 255 : 120, first ? 176 : 200, first ? 46 : 235, 255); int cx = b.x + b.w / 2; int cy = b.y + b.h / 2; SDL_Rect dot = { cx - 14, cy - 14, 28, 28 }; SDL_RenderFillRect(r, &dot); }
static int pickGame() {
  if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_EVENTS) != 0) { launcherLog("pickGame SDL_Init failed: %s", SDL_GetError()); return 1; }
  SDL_Window* w = SDL_CreateWindow("Fallout", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 640, 480, SDL_WINDOW_FULLSCREEN | SDL_WINDOW_ALLOW_HIGHDPI);
  if (!w) { launcherLog("pickGame CreateWindow failed: %s", SDL_GetError()); return 1; }
  SDL_Renderer* r = SDL_CreateRenderer(w, -1, SDL_RENDERER_ACCELERATED);
  if (!r) { launcherLog("pickGame CreateRenderer failed: %s", SDL_GetError()); return 1; }
  SDL_Texture* bg1 = loadBg(r, "fallout1_bg.bmp"); SDL_Texture* bg2 = loadBg(r, "fallout2_bg.bmp");
  int choice = 0; int pressed = 0;
  auto halves = [&](int W, int H, SDL_Rect& h1, SDL_Rect& h2, SDL_Rect& b1, SDL_Rect& b2) { bool land = W >= H; if (land) { h1 = {0, 0, W / 2, H}; h2 = {W / 2, 0, W - W / 2, H}; } else { h1 = {0, 0, W, H / 2}; h2 = {0, H / 2, W, H - H / 2}; } int bw = (land ? W / 2 : W) * 56 / 100; int bh = 84; b1 = { h1.x + (h1.w - bw) / 2, h1.y + h1.h - bh - 44, bw, bh }; b2 = { h2.x + (h2.w - bw) / 2, h2.y + h2.h - bh - 44, bw, bh }; };
  auto drawScene = [&](SDL_Rect* focus, float t) { int W = 0, H = 0; SDL_GetWindowSize(w, &W, &H); SDL_Rect h1, h2, b1, b2; halves(W, H, h1, h2, b1, b2); SDL_SetRenderDrawColor(r, 10, 8, 5, 255); SDL_RenderClear(r); if (focus && t >= 0.0f) { SDL_Texture* tx = (choice == 2 ? bg2 : bg1); SDL_Rect from = (choice == 2 ? h2 : h1); SDL_Rect dst = { (int)(from.x + (0 - from.x) * t), (int)(from.y + (0 - from.y) * t), (int)(from.w + (W - from.w) * t), (int)(from.h + (H - from.h) * t) }; if (tx) SDL_RenderCopy(r, tx, nullptr, &dst); else { SDL_SetRenderDrawColor(r, 40, 30, 16, 255); SDL_RenderFillRect(r, &dst); } } else { if (bg1) SDL_RenderCopy(r, bg1, nullptr, &h1); if (bg2) SDL_RenderCopy(r, bg2, nullptr, &h2); SDL_SetRenderDrawColor(r, 0, 0, 0, 255); if (W >= H) { SDL_Rect div = { W / 2 - 2, 0, 4, H }; SDL_RenderFillRect(r, &div); } else { SDL_Rect div = { 0, H / 2 - 2, W, 4 }; SDL_RenderFillRect(r, &div); } drawBtn(r, b1, true); drawBtn(r, b2, false); (void)pressed; } SDL_RenderPresent(r); };
  while (!choice) { SDL_Event e; while (SDL_PollEvent(&e)) { int W = 0, H = 0; SDL_GetWindowSize(w, &W, &H); bool land = W >= H; if (e.type == SDL_QUIT) choice = 1; if (e.type == SDL_MOUSEBUTTONDOWN) { choice = land ? (e.button.x < W / 2 ? 1 : 2) : (e.button.y < H / 2 ? 1 : 2); pressed = choice; launcherLog("pick mouse %d,%d -> %d", e.button.x, e.button.y, choice); } if (e.type == SDL_FINGERDOWN) { choice = land ? (e.tfinger.x < 0.5f ? 1 : 2) : (e.tfinger.y < 0.5f ? 1 : 2); pressed = choice; launcherLog("pick finger %.3f,%.3f -> %d", (double)e.tfinger.x, (double)e.tfinger.y, choice); } } if (!choice) { drawScene(nullptr, -1.0f); SDL_Delay(16); } }
  launcherLog("expand animation choice=%d", choice); Uint32 t0 = SDL_GetTicks(); while (true) { float t = (SDL_GetTicks() - t0) / 650.0f; if (t >= 1.0f) { drawScene((SDL_Rect*)1, 1.0f); break; } float ease = 1.0f - (1.0f - t) * (1.0f - t); drawScene((SDL_Rect*)1, ease); SDL_Delay(16); } SDL_Delay(250);
  if (bg1) SDL_DestroyTexture(bg1); if (bg2) SDL_DestroyTexture(bg2); SDL_DestroyRenderer(r); SDL_DestroyWindow(w); SDL_Quit(); launcherLog("pickGame done choice=%d", choice); return choice;
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
