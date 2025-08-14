import {Button} from "@/components/ui/button.tsx";
import {ArrowLeft} from "lucide-react";
import {Recipe} from "@/hooks/queries/types.ts";
import {useKeyboardShortcuts} from "@/hooks/useKeyboardShortcuts.ts";


type Props = {
    recipe: Recipe
    onBack: () => void
}

export const RecipeDetails = (props: Props) => {
    const {recipe, onBack} = props;

    useKeyboardShortcuts({'Escape': onBack})

    return (
        <main className="min-h-screen bg-background">
            <header
                className="sticky top-0 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b px-4 py-3 flex items-center gap-4">
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={onBack}
                    aria-label="Back to recipes list"
                    className="flex items-center gap-2"
                >
                    <ArrowLeft className="h-4 w-4"/>
                    Back
                </Button>
                <h1 className="text-xl font-semibold truncate">{recipe.name}</h1>
            </header>

            <div className="max-w-4xl mx-auto p-4">
                <div className="aspect-video w-full overflow-hidden rounded-lg mb-6">
                    <img
                        src={recipe.mediaUrl}
                        alt={`${recipe.name} recipe`}
                        className="w-full h-full object-cover"
                    />
                </div>

                <div className="grid md:grid-cols-2 gap-8">
                    <div>
                        <p className="text-muted-foreground mb-6 text-lg leading-relaxed">{recipe.description}</p>

                        <div className="space-y-6">
                            <div>
                                <h2 className="text-xl font-semibold mb-3">Preparation Time</h2>
                                <p className="text-lg">30 minutes</p>
                            </div>

                            <div>
                                <h2 className="text-xl font-semibold mb-3">Calories</h2>
                                <p className="text-lg">500 kcal</p>
                            </div>

                            <div>
                                <h2 className="text-xl font-semibold mb-3">Tags</h2>
                                <p className="text-lg capitalize">veggie • thai</p>
                            </div>
                        </div>
                    </div>

                    <div className="space-y-6">
                        <div>
                            <h2 className="text-xl font-semibold mb-3">Ingredients</h2>
                            <ul className="space-y-2">
                                {recipe.ingredients?.map((ingredient, idx) => (
                                    <li key={idx} className="flex items-start gap-2">
                                        <span className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></span>
                                        <span>{ingredient}</span>
                                    </li>
                                )) || <li>Ingredients not available</li>}
                            </ul>
                        </div>

                        <div>
                            <h2 className="text-xl font-semibold mb-3">Instructions</h2>
                            <ol className="space-y-3">
                                {recipe.instructions?.map((step, idx) => (
                                    <li key={idx} className="flex gap-3">
                      <span
                          className="bg-primary text-primary-foreground w-6 h-6 rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0 mt-0.5">
                        {idx + 1}
                      </span>
                                        <span>{step}</span>
                                    </li>
                                )) || <li>Instructions not available</li>}
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}