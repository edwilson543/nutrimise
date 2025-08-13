import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type {Recipe} from "@/lib/client/types.gen.ts";
import { RecipeCard } from "@/components/RecipeCard";
import {useRecipeList} from "@/hooks/queries/useRecipeList.ts";
import {RecipeDetails} from "@/components/RecipeDetails.tsx";

const diets = ["all", "vegan", "vegetarian", "keto", "pescatarian", "omnivore"] as const;

export default function RecipesPage() {
  const [search, setSearch] = useState("");
  const [diet, setDiet] = useState<(typeof diets)[number]>("all");
  const [maxTime, setMaxTime] = useState<string>("any");
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);

  const {data: recipes, isLoading} = useRecipeList();

  const onOpen = (recipe: Recipe) => {
    setSelectedRecipe(recipe);
  };

  const onBook = (recipe: Recipe) => {
    // TODO: Implement booking functionality
    console.log('Booking recipe:', recipe.name);
  };

  // If a recipe is selected, show full-screen view
  if (selectedRecipe) {
    return <RecipeDetails recipe={selectedRecipe} onBack={() => setSelectedRecipe(null)}/>
  }


  // Default list view
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
            {isLoading ? <div>Loading</div> : recipes?.map((r) => (
            <RecipeCard key={r.id} recipe={r} onOpen={onOpen} onBook={onBook} />
          ))}
        </div>
      </section>
    </main>
  );
}
