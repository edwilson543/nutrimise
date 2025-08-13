import {useQuery} from "@tanstack/react-query";

import {listRecipesRecipesGet} from "@/lib/client";

export const useRecipeList = () => useQuery(
    {
        queryFn: () => listRecipesRecipesGet().then((response) => response.data.recipes),
        queryKey: ['use-recipe-list'],
    }
)

