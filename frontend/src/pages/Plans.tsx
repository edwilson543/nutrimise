import { useMemo, useState } from "react";
import { recipes } from "@/data/recipes";
import { useMealPlanner } from "@/contexts/MealPlannerContext";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";


function formatDateKey(d: Date) {
  return d.toISOString().slice(0, 10);
}

function startOfWeek(d = new Date()) {
  const date = new Date(d);
  const day = (date.getDay() + 6) % 7; // Monday as 0
  date.setDate(date.getDate() - day);
  date.setHours(0, 0, 0, 0);
  return date;
}

const slots: ("breakfast" | "lunch" | "dinner")[] = ["breakfast", "lunch", "dinner"];

export default function PlansPage() {
  const { plans, setMeal, clearDays, saved } = useMealPlanner();
  const [selectedDays, setSelectedDays] = useState<string[]>([]);
  const [prompt, setPrompt] = useState("");
  const [diet, setDiet] = useState<string>("all");
  const [calories, setCalories] = useState<string>("2000");
  const [protein, setProtein] = useState<string>("120");
  const [selectorOpen, setSelectorOpen] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [shoppingOpen, setShoppingOpen] = useState(false);
  const [slotPicker, setSlotPicker] = useState<{ dateKey: string; slot: (typeof slots)[number] } | null>(null);
  const [slotSearch, setSlotSearch] = useState("");

  const [viewMode, setViewMode] = useState<"day" | "week" | "month">("week");
  const today = new Date();
  const days = useMemo(() => {
    if (viewMode === "day") {
      const d = new Date(today);
      const key = formatDateKey(d);
      return [{ date: d, key }];
    }
    if (viewMode === "week") {
      const weekStart = startOfWeek(today);
      return Array.from({ length: 7 }).map((_, i) => {
        const d = new Date(weekStart);
        d.setDate(weekStart.getDate() + i);
        const key = formatDateKey(d);
        return { date: d, key };
      });
    }
    // month view
    const start = new Date(today.getFullYear(), today.getMonth(), 1);
    const end = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    const total = end.getDate();
    return Array.from({ length: total }).map((_, i) => {
      const d = new Date(start);
      d.setDate(start.getDate() + i);
      const key = formatDateKey(d);
      return { date: d, key };
    });
  }, [viewMode]);


  const toggleDay = (key: string) => {
    setSelectedDays((prev) => (prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]));
  };

  function quickSuggest(text: string) {
    const t = text.toLowerCase();
    const pool = recipes.filter((r) => {
      if (t.includes("vegan")) return r.diet === "vegan";
      if (t.includes("keto")) return r.tags.includes("keto");
      if (t.includes("vegetarian")) return r.diet === "vegetarian";
      if (t.includes("fish") || t.includes("salmon")) return r.title.toLowerCase().includes("salmon") || r.diet === "pescatarian";
      if (t.includes("breakfast")) return r.tags.includes("breakfast");
      if (t.includes("high protein")) return r.tags.includes("high-protein") || r.macros.protein >= 25;
      if (t.includes("quick")) return r.timeMinutes <= 20;
      return true;
    });
    return pool.length ? pool : recipes;
  }

  function fillSelectedDaysWith(pool: typeof recipes, mealsPerDay = 3) {
    const pick = (i: number) => pool[i % pool.length];
    selectedDays.forEach((key, idx) => {
      const breakfast = pick(idx);
      const lunch = pick(idx + 1);
      const dinner = pick(idx + 2);
      if (mealsPerDay >= 1) setMeal(key, "breakfast", breakfast.id);
      if (mealsPerDay >= 2) setMeal(key, "lunch", lunch.id);
      if (mealsPerDay >= 3) setMeal(key, "dinner", dinner.id);
    });
  }

  function buildPool() {
    let pool = recipes;
    if (diet !== "all") {
      pool = pool.filter((r) => r.diet === diet || r.tags.includes(diet));
    }
    const targetCal = parseInt(calories) || 2000;
    const targetProtein = parseInt(protein) || 100;
    pool = pool.sort((a, b) => Math.abs(a.macros.protein - targetProtein / 3) - Math.abs(b.macros.protein - targetProtein / 3));
    return pool;
  }

  return (
    <main>
      <header className="px-4 pt-4 flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Meal Plans</h1>
          <p className="text-muted-foreground mt-1">Plan your meals with a calendar view.</p>
        </div>
        <div className="w-40">
          <Select value={viewMode} onValueChange={(v) => setViewMode(v as any)}>
            <SelectTrigger aria-label="Calendar view"><SelectValue placeholder="View" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="day">Day</SelectItem>
              <SelectItem value="week">Week</SelectItem>
              <SelectItem value="month">Month</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </header>

      <section className="px-4 mt-4">
        {selectedDays.length > 0 && (
          <div className="mb-4 flex flex-wrap gap-2 items-center">
            <Button variant="hero" onClick={() => setSelectorOpen(true)}>Select recipes</Button>
            <Button variant="secondary" onClick={() => setShoppingOpen(true)}>Shopping list</Button>
            <Button variant="outline" onClick={() => { clearDays(selectedDays); setSelectedDays([]); }}>Clear days</Button>
            <span className="text-sm text-muted-foreground">{selectedDays.length} day(s) selected</span>
          </div>
        )}
        <div className="grid gap-4 md:grid-cols-7">
          {days.map(({ date, key }) => {
            const dayPlan = plans[key] || {};
            const label = date.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
            const selected = selectedDays.includes(key);
            return (
              <article key={key} className={`rounded-lg border p-3 cursor-pointer transition-[transform,box-shadow] ${selected ? "ring-2 ring-primary shadow-lg" : "hover:shadow"}`} onClick={() => toggleDay(key)} aria-label={`Plan for ${label}`}>
                <header className="flex items-center justify-between mb-2">
                  <h3 className="font-medium text-sm">{label}</h3>
                </header>
                <div className="space-y-2 text-sm">
                  {slots.map((s) => {
                    const r = dayPlan[s] ? recipes.find((x) => x.id === dayPlan[s]) : undefined;
                    return (
                      <div key={s} className="flex items-center justify-between">
                        <div className="flex-1 min-w-0">
                          <span className="capitalize text-muted-foreground">{s}</span>
                          <span className="truncate ml-2 font-medium">{r ? r.title : "—"}</span>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={(e) => { e.stopPropagation(); setSlotPicker({ dateKey: key, slot: s }); }}
                          aria-label={`Select recipe for ${s}`}
                        >
                          {r ? "Change" : "Select"}
                        </Button>
                      </div>
                    );
                  })}
                </div>
              </article>
            );
          })}
        </div>
      </section>


      {/* Unified recipe selector */}
      <Dialog open={selectorOpen} onOpenChange={setSelectorOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Select recipes for selected days</DialogTitle>
          </DialogHeader>
          <div className="space-y-3">
            <Input placeholder="e.g. vegan high protein quick" value={prompt} onChange={(e) => setPrompt(e.target.value)} aria-label="Fill prompt" />
            <Button variant="outline" onClick={() => setShowDetails((v) => !v)} aria-expanded={showDetails} className="w-full justify-between">
              More details
              <span aria-hidden>{showDetails ? "−" : "+"}</span>
            </Button>
            {showDetails && (
              <div className="grid gap-3 md:grid-cols-2">
                <div>
                  <label className="text-sm">Diet</label>
                  <Select value={diet} onValueChange={setDiet}>
                    <SelectTrigger><SelectValue placeholder="Diet" /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All</SelectItem>
                      <SelectItem value="vegan">Vegan</SelectItem>
                      <SelectItem value="vegetarian">Vegetarian</SelectItem>
                      <SelectItem value="keto">Keto</SelectItem>
                      <SelectItem value="pescatarian">Pescatarian</SelectItem>
                      <SelectItem value="omnivore">Omnivore</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-sm">Daily calories</label>
                  <Input type="number" value={calories} onChange={(e) => setCalories(e.target.value)} />
                </div>
                <div>
                  <label className="text-sm">Daily protein (g)</label>
                  <Input type="number" value={protein} onChange={(e) => setProtein(e.target.value)} />
                </div>
              </div>
            )}
            <div className="flex gap-2">
              <Button onClick={() => { const pool = prompt.trim() ? quickSuggest(prompt) : buildPool(); fillSelectedDaysWith(pool, 3); setSelectorOpen(false); setPrompt(""); }}>Apply</Button>
              <Button variant="outline" onClick={() => setSelectorOpen(false)}>Cancel</Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>

      {/* Shopping list dialog */}
      <Dialog open={shoppingOpen} onOpenChange={setShoppingOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Shopping list</DialogTitle>
          </DialogHeader>
          <div className="space-y-3">
            {selectedDays.length === 0 ? (
              <p className="text-sm text-muted-foreground">Select days on the calendar to build a shopping list.</p>
            ) : (
              <ul className="list-disc pl-5 text-sm space-y-1 max-h-80 overflow-auto">
                {(() => {
                  const map = new Map<string, number>();
                  selectedDays.forEach((key) => {
                    const dayPlan = plans[key] || {};
                    (Object.values(dayPlan) as string[]).forEach((id) => {
                      const r = recipes.find((x) => x.id === id);
                      r?.ingredients.forEach((ing) => {
                        const k = ing.trim().toLowerCase();
                        map.set(k, (map.get(k) || 0) + 1);
                      });
                    });
                  });
                  return Array.from(map.entries()).sort().map(([name, count]) => (
                    <li key={name}><span className="font-medium">{count}×</span> {name}</li>
                  ));
                })()}
              </ul>
            )}
          </div>
        </DialogContent>
      </Dialog>

      {/* Saved recipe picker for a meal slot */}
      <Dialog open={!!slotPicker} onOpenChange={(o) => !o && setSlotPicker(null)}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Select a saved recipe</DialogTitle>
          </DialogHeader>
          <div className="space-y-3">
            <Input placeholder="Search saved recipes" value={slotSearch} onChange={(e) => setSlotSearch(e.target.value)} />
            <div className="max-h-80 overflow-auto divide-y">
              {recipes.filter((r) => saved.has(r.id)).filter((r) => r.title.toLowerCase().includes(slotSearch.toLowerCase())).map((r) => (
                <div key={r.id} className="py-2 flex items-center justify-between">
                  <div className="min-w-0">
                    <div className="font-medium truncate">{r.title}</div>
                    <div className="text-xs text-muted-foreground">{r.macros.calories} kcal • {r.timeMinutes}m</div>
                  </div>
                  <Button size="sm" onClick={() => { if (slotPicker) setMeal(slotPicker.dateKey, slotPicker.slot, r.id); setSlotPicker(null); }}>Set</Button>
                </div>
              ))}
              {Array.from(saved).length === 0 && (
                <p className="text-sm text-muted-foreground py-6 text-center">You have no saved recipes yet.</p>
              )}
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </main>
  );
}
