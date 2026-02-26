import { useState } from "react";
import RecipeCard from "@/components/ui/cards/recipe-card";
import ProposalCard from "../chat/ProposalCard";
import Button from "../ui/Button";
import { RotateCw, Loader2 } from "lucide-react";

type Recipe = {
  recipe_id: number;
  name: string;
  image_url: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
  meal_types: string[];
  diet_types: string[];
  recipe_url: string;
};

type Meal = {
  recipe: Recipe;
  swapSuggestion?: Recipe;
  accepted?: boolean;
};

type Props = {
  meal: Meal;
  onConfirm?: () => void;       // aceptar swap
  onRequestSwap?: () => void;   // solicitar nueva sugerencia
};

export default function MealItem({ meal, onConfirm, onRequestSwap }: Props) {
  const [loading, setLoading] = useState(false);

  const handleSwapClick = async () => {
    if (!onRequestSwap) return;
    setLoading(true);
    try {
      await onRequestSwap(); // llama a la función del padre que hace fetch al backend
    } finally {
      setLoading(false);
    }
  };

  // Si hay sugerencia, mostrar ProposalCard
  if (meal.swapSuggestion) {
    return (
      <ProposalCard
        image={meal.swapSuggestion.image_url}
        badge="Suggestion"
        title={meal.recipe.name}
        description={`${meal.recipe.name} (${meal.recipe.calories} kcal) → ${meal.swapSuggestion.name} (${meal.swapSuggestion.calories} kcal)`}
        onConfirm={onConfirm}           // aceptar swap
        onCancel={handleSwapClick}      // pedir otra sugerencia
      />
    );
  }

  // Si no hay sugerencia, mostrar receta original con botón de swap
  return (
    <RecipeCard {...meal.recipe} title={meal.recipe.name} image={meal.recipe.image_url}>
      <Button
        variant="primary"
        onClick={handleSwapClick}
        disabled={loading}
        className="w-full flex items-center justify-center gap-2"
      >
        {loading ? <Loader2 className="size-4 animate-spin" /> : <RotateCw className="size-4" />}
        <span>{loading ? "Searching..." : "Change"}</span>
      </Button>
    </RecipeCard>
  );
}