import { useState, useEffect, useCallback, useRef } from "react";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type {Recipe} from "@/lib/client/types.gen.ts";
import { RecipeCard } from "@/components/RecipeCard";
import {useRecipeList} from "@/hooks/queries/useRecipeList.ts";
import {RecipeDetails} from "@/components/RecipeDetails.tsx";
import {useKeyboardShortcuts} from "@/hooks/useKeyboardShortcuts.ts";

const diets = ["all", "vegan", "vegetarian", "keto", "pescatarian", "omnivore"] as const;

export default function RecipesPage() {
  const [search, setSearch] = useState("");
  const [selectedRecipe, setSelectedRecipe] = useState<Recipe | null>(null);
  const [focusedIndex, setFocusedIndex] = useState<number>(0);
  const cardRefs = useRef<(HTMLDivElement | null)[]>([]);
  const lastMousePosition = useRef<{ x: number; y: number } | null>(null);
  const hasMouseMoved = useRef<boolean>(false);

  // TODO -> unused state.
  const [diet, setDiet] = useState<(typeof diets)[number]>("all");
  const [maxTime, setMaxTime] = useState<string>("any");

  const {data: recipes, isLoading} = useRecipeList();

  const gridColumns = {
    sm: 2,
    lg: 3,
    xl: 4
  };

  const currentCols = window.innerWidth >= 1280 ? gridColumns.xl :
                       window.innerWidth >= 1024 ? gridColumns.lg : gridColumns.sm;

  const handleMouseMove = useCallback((e: MouseEvent) => {
    const currentPosition = { x: e.clientX, y: e.clientY };

    if (lastMousePosition.current) {
      const distance = Math.sqrt(
        Math.pow(currentPosition.x - lastMousePosition.current.x, 2) +
        Math.pow(currentPosition.y - lastMousePosition.current.y, 2)
      );

      if (distance > 5) { // Threshold to avoid tiny movements
        hasMouseMoved.current = true;
      }
    }

    lastMousePosition.current = currentPosition;
  }, []);

  const handleKeyNavigation = useCallback(() => {
    hasMouseMoved.current = false;
  }, []);

  const shortcuts = {
    'ArrowRight': () => {
      if (!recipes?.length) return;
      handleKeyNavigation();
      setFocusedIndex(prev => Math.min(prev + 1, recipes.length - 1));
    },
    'ArrowLeft': () => {
      if (!recipes?.length) return;
      handleKeyNavigation();
      setFocusedIndex(prev => Math.max(prev - 1, 0));
    },
    'ArrowDown': () => {
      if (!recipes?.length) return;
      handleKeyNavigation();
      setFocusedIndex(prev => Math.min(prev + currentCols, recipes.length - 1));
    },
    'ArrowUp': () => {
      if (!recipes?.length) return;
      handleKeyNavigation();
      setFocusedIndex(prev => Math.max(prev - currentCols, 0));
    },
    'Enter': () => {
      if (recipes?.[focusedIndex]) {
        onOpen(recipes[focusedIndex]);
      }
    },
  };

  useKeyboardShortcuts(shortcuts);

  useEffect(() => {
    document.addEventListener('mousemove', handleMouseMove);
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, [handleMouseMove]);

  useEffect(() => {
    setFocusedIndex(0);
    cardRefs.current = cardRefs.current.slice(0, recipes?.length || 0);
  }, [recipes]);

  useEffect(() => {
    if (cardRefs.current[focusedIndex]) {
      cardRefs.current[focusedIndex]?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
        inline: 'nearest'
      });
    }
  }, [focusedIndex]);

  const onOpen = (recipe: Recipe) => {
    setSelectedRecipe(recipe);
  };

  const onBook = (recipe: Recipe) => {
    // TODO: Implement booking functionality
    console.log('Booking recipe:', recipe.name);
  };

  const onHover = (index: number) => {
    if (hasMouseMoved.current) {
      setFocusedIndex(index);
    }
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
            {isLoading ? <div>Loading</div> : recipes.map((r, index) => (
            <div
              key={r.id}
              ref={(el) => cardRefs.current[index] = el}
            >
              <RecipeCard
                recipe={r}
                onOpen={onOpen}
                onBook={onBook}
                onHover={() => onHover(index)}
                isFocused={index === focusedIndex}
              />
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
