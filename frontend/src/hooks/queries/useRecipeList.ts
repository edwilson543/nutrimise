import {useQuery} from "@tanstack/react-query";

import {listRecipesRecipesGet} from "@/lib/client";
import * as queryKeys from "@/hooks/queries/query-keys.ts";

export const useRecipeList = () => useQuery(
    {
        queryFn: () => listRecipesRecipesGet().then((response) => response.data.recipes),
        queryKey: [queryKeys.RECIPE_LIST],
    }
)

