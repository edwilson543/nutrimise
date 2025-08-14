import {Clock} from "lucide-react";
import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {Recipe} from "@/hooks/queries/types.ts";
import {SaveRecipeButton} from "@/components/recipes/SaveRecipeButton.tsx";

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
                    <img src={recipe.mediaUrl} alt={`${recipe.name} healthy recipe`}
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
                            <SaveRecipeButton recipe={recipe} isFocused={isFocused}/>
                        </div>
                    </div>
                </div>
            </CardContent>
        </Card>
    );
};
