import {Heart, Clock} from "lucide-react";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import type {Recipe} from "@/lib/client/types.gen.ts";
import {useSaveRecipe, useUnsaveRecipe} from "@/hooks/mutations/useSaveRecipe.ts";
import {useKeyboardShortcuts} from "@/hooks/useKeyboardShortcuts.ts";

type Props = {
    recipe: Recipe;
    onOpen: (recipe: Recipe) => void;
    onBook: (recipe: Recipe) => void;
    onHover?: () => void;
    isFocused?: boolean;
};

/**
 * A recipe preview card, displayed in the recipe grid view.
 * */
export const RecipeCard = (props: Props) => {
    const {recipe, onOpen, onBook, onHover, isFocused = false} = props;

    const onSaveRecipe = useSaveRecipe(recipe.id);
    const onUnsaveRecipe = useUnsaveRecipe(recipe.id);
    const onToggleSaved = () => {
        return recipe.is_saved ? onUnsaveRecipe.mutate() : onSaveRecipe.mutate();
    }

    useKeyboardShortcuts({'s': () => isFocused ? onToggleSaved() : undefined})

    return (
        <Card
            className={`h-full flex flex-col overflow-hidden hover:shadow-lg transition-all duration-200 ${
                isFocused ? 'ring-2 ring-primary shadow-lg scale-105' : ''
            }`}
            role="article"
            aria-label={recipe.name}
            onMouseEnter={onHover}
        >
            <button className="w-full text-left" onClick={() => onOpen(recipe)} aria-label={`Open ${recipe.name}`}>
                <div className="aspect-[3/2] w-full overflow-hidden">
                    <img src={recipe.media_url} alt={`${recipe.name} healthy recipe`}
                         className="h-full w-full object-cover" loading="lazy"/>
                </div>
            </button>
            <CardHeader className="pb-2">
                <CardTitle className="text-lg">{recipe.name}</CardTitle>
            </CardHeader>
            <CardContent className="pt-0 flex-1 flex flex-col">
                <div className="h-10 mb-3">
                    <p className="text-sm text-muted-foreground line-clamp-2">{recipe.description || '\u00A0'}</p>
                </div>
                <div className="mt-auto">
                    <div className="flex items-center justify-between text-sm">
                        <span className="inline-flex items-center gap-1 text-muted-foreground"><Clock
                            className="h-4 w-4"/>30m</span>
                        <span className="font-medium">500 kcal</span>
                    </div>
                    <div className="mt-4 flex items-center justify-between">
                        <div className="text-xs text-muted-foreground capitalize">veggie • thai</div>
                        <div className="flex items-center gap-2">
                            <Button variant="outline" size="sm" onClick={() => onBook(recipe)}
                                    aria-label="Add to meal plan">
                                Book
                            </Button>
                            <Button variant={recipe.is_saved ? "secondary" : "outline"} size="sm"
                                    onClick={onToggleSaved} aria-pressed={recipe.is_saved}
                                    aria-label={recipe.is_saved ? "Unsave recipe" : "Save recipe"}>
                                <Heart className={`h-4 w-4 ${recipe.is_saved ? "fill-current" : ""}`}/>
                                {recipe.is_saved ? "Saved" : "Save"}
                            </Button>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};
