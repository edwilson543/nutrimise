import mediterraneanChicken from "@/assets/recipes/mediterranean-chicken-bowl.jpg";
import veganBuddha from "@/assets/recipes/vegan-buddha-bowl.jpg";
import ketoSalmon from "@/assets/recipes/keto-salmon-asparagus.jpg";
import proteinOmelette from "@/assets/recipes/protein-omelette.jpg";
import quinoaAvocado from "@/assets/recipes/quinoa-avocado-salad.jpg";
import spicyTofu from "@/assets/recipes/spicy-tofu-stirfry.jpg";
import pastaPrimavera from "@/assets/recipes/pasta-primavera.jpg";
import berryParfait from "@/assets/recipes/berry-yogurt-parfait.jpg";

export type Macros = {
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  fiber?: number;
};

export type Recipe = {
  id: string;
  title: string;
  description: string;
  image: string;
  diet: "vegan" | "vegetarian" | "keto" | "pescatarian" | "omnivore";
  cuisine: string;
  timeMinutes: number;
  tags: string[];
  macros: Macros;
  ingredients: string[];
  steps: string[];
};

export const recipes: Recipe[] = [
  {
    id: "med-chicken-bowl",
    title: "Mediterranean Chicken Bowl",
    description: "Grilled chicken with quinoa, crisp veggies, olives, and feta.",
    image: mediterraneanChicken,
    diet: "omnivore",
    cuisine: "Mediterranean",
    timeMinutes: 30,
    tags: ["gluten-free", "quick", "high-protein"],
    macros: { calories: 540, protein: 42, carbs: 48, fat: 20, fiber: 7 },
    ingredients: [
      "2 chicken breasts",
      "1 cup cooked quinoa",
      "1/2 cup cherry tomatoes",
      "1/2 cup cucumber",
      "1/4 cup olives",
      "2 tbsp feta",
      "1 tbsp olive oil",
      "Lemon, oregano, salt, pepper",
    ],
    steps: [
      "Season and grill chicken until cooked through.",
      "Assemble bowl with quinoa, chopped veggies, olives, and feta.",
      "Drizzle with olive oil and lemon, sprinkle oregano.",
    ],
  },
  {
    id: "vegan-buddha-bowl",
    title: "Vegan Buddha Bowl",
    description: "Roasted sweet potato, chickpeas, kale and avocado with tahini.",
    image: veganBuddha,
    diet: "vegan",
    cuisine: "Fusion",
    timeMinutes: 35,
    tags: ["vegan", "fiber-rich", "meal-prep"],
    macros: { calories: 520, protein: 17, carbs: 66, fat: 20, fiber: 12 },
    ingredients: [
      "1 sweet potato",
      "1 cup chickpeas",
      "2 cups kale",
      "1/2 avocado",
      "Tahini, lemon, garlic",
    ],
    steps: [
      "Roast cubed sweet potato and chickpeas.",
      "Massage kale with lemon.",
      "Assemble and drizzle tahini dressing.",
    ],
  },
  {
    id: "keto-salmon-asparagus",
    title: "Keto Salmon with Asparagus",
    description: "Pan-seared salmon with lemon butter asparagus.",
    image: ketoSalmon,
    diet: "pescatarian",
    cuisine: "American",
    timeMinutes: 20,
    tags: ["keto", "low-carb", "omega-3"],
    macros: { calories: 460, protein: 36, carbs: 8, fat: 30, fiber: 4 },
    ingredients: [
      "2 salmon fillets",
      "1 bunch asparagus",
      "Butter, lemon, garlic",
    ],
    steps: [
      "Sear salmon skin-side down, finish with butter.",
      "Sauté asparagus with garlic and lemon.",
    ],
  },
  {
    id: "protein-omelette",
    title: "Protein Omelette",
    description: "Fluffy omelette with spinach, mushrooms and tomatoes.",
    image: proteinOmelette,
    diet: "omnivore",
    cuisine: "Breakfast",
    timeMinutes: 15,
    tags: ["breakfast", "high-protein", "quick"],
    macros: { calories: 380, protein: 32, carbs: 8, fat: 24, fiber: 3 },
    ingredients: [
      "3 eggs",
      "Spinach, mushrooms, tomatoes",
      "Olive oil, salt, pepper",
    ],
    steps: [
      "Sauté vegetables.",
      "Whisk eggs and cook, fold in vegetables.",
    ],
  },
  {
    id: "quinoa-avocado-salad",
    title: "Quinoa Avocado Salad",
    description: "Refreshing salad with quinoa, avocado and lemon vinaigrette.",
    image: quinoaAvocado,
    diet: "vegetarian",
    cuisine: "Mediterranean",
    timeMinutes: 20,
    tags: ["vegetarian", "gluten-free", "light"],
    macros: { calories: 420, protein: 13, carbs: 54, fat: 16, fiber: 9 },
    ingredients: [
      "1 cup cooked quinoa",
      "1 avocado",
      "Cherry tomatoes, cucumber, parsley",
    ],
    steps: [
      "Toss all ingredients with lemon vinaigrette.",
    ],
  },
  {
    id: "spicy-tofu-stirfry",
    title: "Spicy Tofu Stir-fry",
    description: "Crispy tofu with bell peppers and snap peas in spicy sauce.",
    image: spicyTofu,
    diet: "vegan",
    cuisine: "Asian",
    timeMinutes: 25,
    tags: ["vegan", "high-protein", "stir-fry"],
    macros: { calories: 480, protein: 24, carbs: 48, fat: 20, fiber: 6 },
    ingredients: [
      "Firm tofu",
      "Bell peppers, snap peas",
      "Soy sauce, chili, garlic",
    ],
    steps: [
      "Crisp tofu, set aside.",
      "Stir-fry veggies, add sauce and tofu.",
    ],
  },
  {
    id: "pasta-primavera",
    title: "Pasta Primavera (Light)",
    description: "Light pasta with seasonal veggies and basil.",
    image: pastaPrimavera,
    diet: "vegetarian",
    cuisine: "Italian",
    timeMinutes: 22,
    tags: ["vegetarian", "comfort", "quick"],
    macros: { calories: 520, protein: 18, carbs: 78, fat: 14, fiber: 6 },
    ingredients: [
      "Pasta",
      "Zucchini, peas, tomatoes",
      "Olive oil, parmesan, basil",
    ],
    steps: [
      "Cook pasta al dente.",
      "Sauté veggies, toss with pasta and basil.",
    ],
  },
  {
    id: "berry-yogurt-parfait",
    title: "Berry Yogurt Parfait",
    description: "Greek yogurt layered with berries and granola.",
    image: berryParfait,
    diet: "vegetarian",
    cuisine: "Breakfast",
    timeMinutes: 5,
    tags: ["breakfast", "quick", "snack"],
    macros: { calories: 300, protein: 18, carbs: 42, fat: 8, fiber: 5 },
    ingredients: [
      "Greek yogurt",
      "Mixed berries",
      "Granola",
    ],
    steps: [
      "Layer yogurt, berries and granola in a glass.",
    ],
  },
];
