import { useState, useEffect, useRef } from "react";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import {Recipe} from "@/hooks/queries/types.ts";
import { RecipeCard } from "@/components/recipes/RecipeCard";
import {useRecipeList} from "@/hooks/queries/useRecipeList.ts";
import {RecipeDetails} from "@/components/recipes/RecipeDetails.tsx";
import {useKeyboardShortcuts} from "@/hooks/useKeyboardShortcuts.ts";

const diets = ["all", "vegan", "vegetarian", "keto", "pescatarian", "omnivore"] as const;
const savedFilters = ["all", "saved", "unsaved"] as const;

export default function RecipesPage() {
  const [search, setSearch] = useState("");
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [focusedIndex, setFocusedIndex] = useState<number>(0);
  const cardRefs = useRef<(HTMLDivElement | null)[]>([]);

  const [savedFilter, setSavedFilter] = useState<(typeof savedFilters)[number]>("all");

  // TODO -> unused state.
  const [diet, setDiet] = useState<(typeof diets)[number]>("all");
  const [maxTime, setMaxTime] = useState<string>("any");

  const {data: allRecipes, isLoading} = useRecipeList();
  
  const displayedRecipes = allRecipes?.filter((recipe) => {
    if (savedFilter === "saved") return recipe.isSaved;
    if (savedFilter === "unsaved") return !recipe.isSaved;
    return true;
  }) || undefined;

  const gridColumns = {
    sm: 2,
    lg: 3,
    xl: 4
  };

  const currentCols = window.innerWidth >= 1280 ? gridColumns.xl :
                       window.innerWidth >= 1024 ? gridColumns.lg : gridColumns.sm;


  const shortcuts = {
    'ArrowRight': () => {
      if (!displayedRecipes?.length) return;
      setFocusedIndex(prev => Math.min(prev + 1, displayedRecipes.length - 1));
    },
    'ArrowLeft': () => {
      if (!displayedRecipes?.length) return;
      setFocusedIndex(prev => Math.max(prev - 1, 0));
    },
    'ArrowDown': () => {
      if (!displayedRecipes?.length) return;
      setFocusedIndex(prev => Math.min(prev + currentCols, displayedRecipes.length - 1));
    },
    'ArrowUp': () => {
      if (!displayedRecipes?.length) return;
      setFocusedIndex(prev => Math.max(prev - currentCols, 0));
    },
    'Enter': () => {
      if (displayedRecipes?.[focusedIndex]) {
        onOpen(displayedRecipes[focusedIndex], focusedIndex);
      }
    },
  };

  useKeyboardShortcuts(shortcuts);

  useEffect(() => {
    if (cardRefs.current[focusedIndex]) {
      cardRefs.current[focusedIndex]?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
        inline: 'nearest'
      });
    }
  }, [focusedIndex, selectedRecipe]);

  const onOpen = (recipe: Recipe, index: number) => {
    setFocusedIndex(index);
    setSelectedRecipe(recipe);
  };

  const onBook = (recipe: Recipe) => {
    // TODO: Implement booking functionality
    console.log('Booking recipe:', recipe.name);
  };

  // If a recipe is selected, show full-screen view.
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
        <div className="grid grid-cols-1 md:grid-cols-6 gap-3">
          <div className="md:col-span-3">
            <Input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search recipes, cuisines, tags..." aria-label="Search recipes" />
          </div>
          <Select value={savedFilter} onValueChange={(v) => setSavedFilter(v as any)}>
            <SelectTrigger aria-label="Filter by saved status"><SelectValue placeholder="Saved" /></SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All recipes</SelectItem>
              <SelectItem value="saved">Saved only</SelectItem>
              <SelectItem value="unsaved">Unsaved only</SelectItem>
            </SelectContent>
          </Select>
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
            {isLoading ? <div>Loading</div> : displayedRecipes.map((recipe, index) => (
            <div
              key={recipe.id}
              ref={(el) => cardRefs.current[index] = el}
            >
              <RecipeCard
                recipe={recipe}
                onOpen={(recipe: Recipe) => onOpen(recipe, index)}
                onBook={onBook}
                isFocused={index === focusedIndex}
              />
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
