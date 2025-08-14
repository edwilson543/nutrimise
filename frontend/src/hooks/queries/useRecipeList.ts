import {useQuery} from "@tanstack/react-query";

import {listRecipesRecipesGet, listSavedRecipesRecipesSavedGet} from "@/lib/client";
import * as queryKeys from "@/hooks/queries/query-keys.ts";
import {Recipe} from "@/hooks/queries/types.ts";


/**
 * Get the filtered list of recipes.
 *
 * We fetch saved recipes separately, so that this query can be invalided independently.
 * */
export const useRecipeList = () => {
    const recipeList = useQuery(
        {
            queryFn: () => listRecipesRecipesGet().then((response) => response.data.recipes),
            queryKey: [queryKeys.RECIPE_LIST],
        }
    )

    const savedRecipes = useQuery(
        {
            queryFn: () => listSavedRecipesRecipesSavedGet().then((response) => response.data),
            queryKey: [queryKeys.SAVED_RECIPE_LIST],
        }
    )

    const data: Recipe[] | undefined = recipeList.data && savedRecipes.data 
        ? recipeList.data.map(recipe => ({
            ...recipe,
            mediaUrl: recipe.media_url,
            isSaved: savedRecipes.data.includes(recipe.id)
        }))
        : undefined;

    return {
        data,
        isLoading: recipeList.isLoading || savedRecipes.isLoading,
        error: recipeList.error || savedRecipes.error,
        isError: recipeList.isError || savedRecipes.isError,
    };
}

