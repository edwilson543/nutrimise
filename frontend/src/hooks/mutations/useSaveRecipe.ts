import {useMutation, useQueryClient} from "@tanstack/react-query";

import {saveRecipeRecipesRecipeIdSavePut, unsaveRecipeRecipesRecipeIdUnsavePut} from "@/lib/client";
import * as queryKeys from "@/hooks/queries/query-keys.ts";

export const useSaveRecipe = (recipeId: number) => {
    const queryClient = useQueryClient()

    return useMutation(
        {
            mutationFn: () => saveRecipeRecipesRecipeIdSavePut({path: {recipe_id: recipeId}}),
            onSuccess: () => {
                queryClient.invalidateQueries({queryKey: [queryKeys.RECIPE_LIST]})
            }
        }
    )
}

export const useUnsaveRecipe = (recipeId: number) => {
    const queryClient = useQueryClient()

    return useMutation(
        {
            mutationFn: () => unsaveRecipeRecipesRecipeIdUnsavePut({path: {recipe_id: recipeId}}),
            onSuccess: () => {
                queryClient.invalidateQueries({queryKey: [queryKeys.RECIPE_LIST]})
            }
        }
    )
}
