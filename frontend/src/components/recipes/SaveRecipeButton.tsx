import {Heart} from "lucide-react";
import {Button} from "@/components/ui/button";
import {Recipe} from "@/hooks/queries/types.ts";
import {useSaveRecipe, useUnsaveRecipe} from "@/hooks/mutations/useSaveRecipe.ts";
import {useKeyboardShortcuts} from "@/hooks/useKeyboardShortcuts.ts";

type Props = {
    recipe: Recipe;
    isFocused: boolean;
};

/**
 * A button for saving and unsaving a recipe.
 * */
export const SaveRecipeButton = (props: Props) => {
    const {recipe, isFocused} = props;

    const onSaveRecipe = useSaveRecipe(recipe.id);
    const onUnsaveRecipe = useUnsaveRecipe(recipe.id);
    const onToggleSaved = () => {
        return recipe.isSaved ? onUnsaveRecipe.mutate() : onSaveRecipe.mutate();
    }

    useKeyboardShortcuts({'s': () => isFocused ? onToggleSaved() : undefined})

    return (
        <Button variant={recipe.isSaved ? "secondary" : "outline"} size="sm"
                onClick={onToggleSaved} aria-pressed={recipe.isSaved}
                aria-label={recipe.isSaved ? "Unsave recipe" : "Save recipe"}>
            <Heart className={`h-4 w-4 ${recipe.isSaved ? "fill-current" : ""}`}/>
            {recipe.isSaved ? "Saved" : "Save"}
        </Button>
    );
};
