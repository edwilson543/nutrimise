import { useEffect, useMemo, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useMealPlanner } from "@/contexts/MealPlannerContext";
import { recipes } from "@/data/recipes";

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

const TARGETS_KEY = "nutrimise:targets";
const EXTRAS_KEY = "nutrimise:extras"; // Record<dateKey, {calories,protein,carbs,fat}[]>

type Macros = { calories: number; protein: number; carbs: number; fat: number };

type ExtraMeals = Record<string, Macros[]>;

export default function NutritionPage() {
  const { plans } = useMealPlanner();

  // Targets state
  const [targets, setTargets] = useState<Macros>({ calories: 2000, protein: 120, carbs: 220, fat: 70 });

  // Extras state (manual tracking)
  const [extras, setExtras] = useState<ExtraMeals>({});
  const [newExtra, setNewExtra] = useState<Macros>({ calories: 0, protein: 0, carbs: 0, fat: 0 });
  const [extraDate, setExtraDate] = useState<string>(formatDateKey(new Date()));

  useEffect(() => {
    try {
      const t = JSON.parse(localStorage.getItem(TARGETS_KEY) || "null");
      if (t) setTargets(t);
      const e = JSON.parse(localStorage.getItem(EXTRAS_KEY) || "{}");
      setExtras(e);
    } catch {}
  }, []);

  useEffect(() => {
    localStorage.setItem(TARGETS_KEY, JSON.stringify(targets));
  }, [targets]);

  useEffect(() => {
    localStorage.setItem(EXTRAS_KEY, JSON.stringify(extras));
  }, [extras]);

  // Weekly aggregation
  const weekStart = startOfWeek(new Date());
  const days = Array.from({ length: 7 }).map((_, i) => {
    const d = new Date(weekStart);
    d.setDate(weekStart.getDate() + i);
    const key = formatDateKey(d);
    return { date: d, key };
  });

  const weekData = useMemo(() => {
    return days.map(({ key }) => {
      const dayPlan = plans[key] || {};
      const meals = ["breakfast", "lunch", "dinner"].map((s) => recipes.find((r) => r.id === (dayPlan as any)[s]!)).filter(Boolean);
      const totals = meals.reduce(
        (acc, r) => ({
          calories: acc.calories + (r?.macros.calories || 0),
          protein: acc.protein + (r?.macros.protein || 0),
          carbs: acc.carbs + (r?.macros.carbs || 0),
          fat: acc.fat + (r?.macros.fat || 0),
        }),
        { calories: 0, protein: 0, carbs: 0, fat: 0 }
      );
      const extraMeals = (extras[key] || []).reduce(
        (acc, m) => ({
          calories: acc.calories + m.calories,
          protein: acc.protein + m.protein,
          carbs: acc.carbs + m.carbs,
          fat: acc.fat + m.fat,
        }),
        { calories: 0, protein: 0, carbs: 0, fat: 0 }
      );
      return { day: key.slice(5), ...Object.fromEntries(Object.entries(totals).map(([k, v]) => [k, (v as number) + (extraMeals as any)[k]])) } as any;
    });
  }, [plans, extras]);

  const preset = (type: "cut" | "maintain" | "bulk") => {
    // simple presets
    if (type === "cut") setTargets({ calories: 1800, protein: 140, carbs: 160, fat: 60 });
    if (type === "maintain") setTargets({ calories: 2200, protein: 130, carbs: 250, fat: 70 });
    if (type === "bulk") setTargets({ calories: 2600, protein: 150, carbs: 300, fat: 80 });
  };

  const addExtraMeal = () => {
    if (!extraDate) return;
    setExtras((prev) => ({ ...prev, [extraDate]: [...(prev[extraDate] || []), newExtra] }));
    setNewExtra({ calories: 0, protein: 0, carbs: 0, fat: 0 });
  };

  return (
    <main>
      <header className="px-4 pt-4">
        <h1 className="text-3xl font-bold tracking-tight">Nutrition</h1>
        <p className="text-muted-foreground mt-1">Set your macro targets and track your intake.</p>
      </header>

      <section className="px-4 mt-6">
        <h2 className="text-xl font-semibold mb-3">Targets</h2>
        <div className="grid gap-4 md:grid-cols-4">
          <div>
            <label className="text-sm">Calories</label>
            <Input type="number" value={targets.calories} onChange={(e) => setTargets({ ...targets, calories: Number(e.target.value) })} />
          </div>
          <div>
            <label className="text-sm">Protein (g)</label>
            <Input type="number" value={targets.protein} onChange={(e) => setTargets({ ...targets, protein: Number(e.target.value) })} />
          </div>
          <div>
            <label className="text-sm">Carbs (g)</label>
            <Input type="number" value={targets.carbs} onChange={(e) => setTargets({ ...targets, carbs: Number(e.target.value) })} />
          </div>
          <div>
            <label className="text-sm">Fat (g)</label>
            <Input type="number" value={targets.fat} onChange={(e) => setTargets({ ...targets, fat: Number(e.target.value) })} />
          </div>
        </div>
        <div className="flex gap-2 mt-3">
          <Button variant="secondary" onClick={() => preset("cut")}>Fat loss preset</Button>
          <Button variant="secondary" onClick={() => preset("maintain")}>Maintenance preset</Button>
          <Button variant="secondary" onClick={() => preset("bulk")}>Muscle gain preset</Button>
        </div>
      </section>

      <section className="px-4 mt-8 pb-10">
        <h2 className="text-xl font-semibold mb-3">Tracking (this week)</h2>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Day</TableHead>
              <TableHead>Calories</TableHead>
              <TableHead>Protein (g)</TableHead>
              <TableHead>Carbs (g)</TableHead>
              <TableHead>Fat (g)</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {weekData.map((d) => (
              <TableRow key={d.day}>
                <TableCell>{d.day}</TableCell>
                <TableCell>{d.calories}</TableCell>
                <TableCell>{d.protein}</TableCell>
                <TableCell>{d.carbs}</TableCell>
                <TableCell>{d.fat}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>

        <div className="mt-6">
          <h3 className="font-medium mb-2">Add additional meals</h3>
          <div className="grid gap-3 md:grid-cols-6">
            <div className="md:col-span-2">
              <label className="text-sm">Date</label>
              <Input type="date" value={extraDate} onChange={(e) => setExtraDate(e.target.value)} />
            </div>
            <div>
              <label className="text-sm">Calories</label>
              <Input type="number" value={newExtra.calories} onChange={(e) => setNewExtra({ ...newExtra, calories: Number(e.target.value) })} />
            </div>
            <div>
              <label className="text-sm">Protein</label>
              <Input type="number" value={newExtra.protein} onChange={(e) => setNewExtra({ ...newExtra, protein: Number(e.target.value) })} />
            </div>
            <div>
              <label className="text-sm">Carbs</label>
              <Input type="number" value={newExtra.carbs} onChange={(e) => setNewExtra({ ...newExtra, carbs: Number(e.target.value) })} />
            </div>
            <div>
              <label className="text-sm">Fat</label>
              <Input type="number" value={newExtra.fat} onChange={(e) => setNewExtra({ ...newExtra, fat: Number(e.target.value) })} />
            </div>
          </div>
          <div className="mt-3">
            <Button onClick={addExtraMeal}>Add meal</Button>
          </div>
        </div>
      </section>

      {/* Structured data */}
      <script type="application/ld+json" suppressHydrationWarning>
        {JSON.stringify({
          "@context": "https://schema.org",
          "@type": "WebPage",
          name: "Nutrition targets and tracking",
          description: "Set your macro targets and track your weekly intake with NutriMise.",
          potentialAction: {
            "@type": "Action",
            name: "Update nutrition targets"
          }
        })}
      </script>
    </main>
  );
}
