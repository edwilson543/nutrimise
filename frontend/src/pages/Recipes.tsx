import { useMemo, useState } from "react";
import { recipes as allRecipes, type Recipe } from "@/data/recipes";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { RecipeCard } from "@/components/RecipeCard";

const diets = ["all", "vegan", "vegetarian", "keto", "pescatarian", "omnivore"] as const;

export default function RecipesPage() {
  const [search, setSearch] = useState("");
  const [diet, setDiet] = useState<(typeof diets)[number]>("all");
  const [maxTime, setMaxTime] = useState<string>("any");
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<Recipe | null>(null);

  const recipes = useMemo(() => {
    return allRecipes.filter((r) => {
      const matchesSearch = [r.title, r.description, r.tags.join(" "), r.cuisine, r.diet]
        .join(" ")
        .toLowerCase()
        .includes(search.toLowerCase());
      const matchesDiet = diet === "all" || r.diet === diet || (diet === "keto" && r.tags.includes("keto"));
      const matchesTime = maxTime === "any" || r.timeMinutes <= parseInt(maxTime);
      return matchesSearch && matchesDiet && matchesTime;
    });
  }, [search, diet, maxTime]);

  const onOpen = (recipe: Recipe) => {
    setSelected(recipe);
    setOpen(true);
  };

  return (
    <main>
      <header className="px-4 pt-4">
        <h1 className="text-3xl font-bold tracking-tight">Healthy Recipes</h1>
        <p className="text-muted-foreground mt-1">Search and filter to find the perfect meal.</p>
      </header>

      <section className="px-4 mt-6">
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
          <div className="md:col-span-3">
            <Input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search recipes, cuisines, tags..." aria-label="Search recipes" />
          </div>
          <Select value={diet} onValueChange={(v) => setDiet(v as any)}>
            <SelectTrigger aria-label="Filter by diet"><SelectValue placeholder="Diet" /></SelectTrigger>
            <SelectContent>
              {diets.map((d) => (
                <SelectItem key={d} value={d}>{d[0].toUpperCase() + d.slice(1)}</SelectItem>
              ))}
            </SelectContent>
          </Select>
          <Select value={maxTime} onValueChange={setMaxTime}>
            <SelectTrigger aria-label="Max cooking time"><SelectValue placeholder="Time" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="any">Any time</SelectItem>
              <SelectItem value="15">Under 15 min</SelectItem>
              <SelectItem value="20">Under 20 min</SelectItem>
              <SelectItem value="30">Under 30 min</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </section>

      <section className="px-4 mt-6 pb-10">
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {recipes.map((r) => (
            <RecipeCard key={r.id} recipe={r} onOpen={onOpen} />
          ))}
        </div>
      </section>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-2xl">
          {selected && (
            <>
              <DialogHeader>
                <DialogTitle>{selected.title}</DialogTitle>
              </DialogHeader>
              <article className="grid md:grid-cols-2 gap-4">
                <div className="rounded-md overflow-hidden">
                  <img src={selected.image} alt={`${selected.title} nutrition and ingredients`} className="w-full h-full object-cover" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground mb-3">{selected.description}</p>
                  <h3 className="font-medium mb-2">Macronutrients</h3>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Nutrient</TableHead>
                        <TableHead>Amount</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      <TableRow><TableCell>Calories</TableCell><TableCell>{selected.macros.calories} kcal</TableCell></TableRow>
                      <TableRow><TableCell>Protein</TableCell><TableCell>{selected.macros.protein} g</TableCell></TableRow>
                      <TableRow><TableCell>Carbs</TableCell><TableCell>{selected.macros.carbs} g</TableCell></TableRow>
                      <TableRow><TableCell>Fat</TableCell><TableCell>{selected.macros.fat} g</TableCell></TableRow>
                      {selected.macros.fiber !== undefined && (
                        <TableRow><TableCell>Fiber</TableCell><TableCell>{selected.macros.fiber} g</TableCell></TableRow>
                      )}
                    </TableBody>
                  </Table>

                  <h3 className="font-medium mt-4 mb-1">Ingredients</h3>
                  <ul className="list-disc pl-5 text-sm space-y-1">
                    {selected.ingredients.map((i, idx) => <li key={idx}>{i}</li>)}
                  </ul>
                </div>
              </article>

              {/* Structured data for the selected recipe */}
              <script type="application/ld+json" suppressHydrationWarning>
                {JSON.stringify({
                  "@context": "https://schema.org",
                  "@type": "Recipe",
                  name: selected.title,
                  description: selected.description,
                  image: selected.image,
                  recipeCuisine: selected.cuisine,
                  recipeCategory: selected.diet,
                  nutrition: {
                    "@type": "NutritionInformation",
                    calories: `${selected.macros.calories} calories`,
                    proteinContent: `${selected.macros.protein} g`,
                    carbohydrateContent: `${selected.macros.carbs} g`,
                    fatContent: `${selected.macros.fat} g`,
                    fiberContent: selected.macros.fiber ? `${selected.macros.fiber} g` : undefined,
                  },
                  recipeIngredient: selected.ingredients,
                  recipeInstructions: selected.steps,
                })}
              </script>
            </>
          )}
        </DialogContent>
      </Dialog>
    </main>
  );
}
