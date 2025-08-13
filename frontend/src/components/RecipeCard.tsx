import {Heart, Clock} from "lucide-react";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import type {Recipe} from "@/lib/client/types.gen.ts";
import {useMealPlanner} from "@/contexts/MealPlannerContext";

type Props = {
    recipe: Recipe;
    onOpen: (recipe: Recipe) => void;
    onBook: (recipe: Recipe) => void;
};

export const RecipeCard = ({recipe, onOpen, onBook}: Props) => {
    const {saved, toggleSave} = useMealPlanner();
    const isSaved = saved.has(recipe.id.toString());

    return (
        <Card className="overflow-hidden hover:shadow-lg transition-shadow" role="article" aria-label={recipe.name}>
            <button className="w-full text-left" onClick={() => onOpen(recipe)} aria-label={`Open ${recipe.name}`}>
                <div className="aspect-[3/2] w-full overflow-hidden">
                    <img src={recipe.media_url} alt={`${recipe.name} healthy recipe`}
                         className="h-full w-full object-cover" loading="lazy"/>
                </div>
            </button>
            <CardHeader className="pb-2">
                <CardTitle className="text-lg">{recipe.name}</CardTitle>
            </CardHeader>
            <CardContent className="pt-0">
                <p className="text-sm text-muted-foreground line-clamp-2">{recipe.description}</p>
                <div className="mt-3 flex items-center justify-between text-sm">
                    <span className="inline-flex items-center gap-1 text-muted-foreground"><Clock className="h-4 w-4"/>30m</span>
                    <span className="font-medium">500 kcal</span>
                </div>
                <div className="mt-4 flex items-center justify-between">
                    <div className="text-xs text-muted-foreground capitalize">veggie • thai</div>
                    <div className="flex items-center gap-2">
                        <Button variant="outline" size="sm" onClick={() => onBook(recipe)}
                                aria-label="Add to meal plan">
                            Book
                        </Button>
                        <Button variant={isSaved ? "secondary" : "outline"} size="sm"
                                onClick={() => toggleSave(recipe.id.toString())} aria-pressed={isSaved}
                                aria-label={isSaved ? "Unsave recipe" : "Save recipe"}>
                            <Heart className={`h-4 w-4 ${isSaved ? "fill-current" : ""}`}/>
                            {isSaved ? "Saved" : "Save"}
                        </Button>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};
