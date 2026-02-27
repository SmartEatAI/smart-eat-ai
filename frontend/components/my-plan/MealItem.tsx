import { useState } from "react";
import RecipeCard from "@/components/ui/cards/recipe-card";
import ProposalCard from "../chat/ProposalCard";
import Button from "../ui/Button";
import { RotateCw, Loader2 } from "lucide-react";
import { MealItemProps } from "@/types/my-plan";

export default function MealItem({ meal, onConfirm, onRequestSwap }: MealItemProps) {
  const [loading, setLoading] = useState(false);
  const [confirming, setConfirming] = useState(false);

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
        image={meal.swapSuggestion.image_url?.split(', ').map(img => img.trim())?.[0] ?? ""}
        badge="Suggestion"
        title={meal.recipe.name}
        description={`${meal.recipe.name} (${meal.recipe.calories} kcal) → ${meal.swapSuggestion.name} (${meal.swapSuggestion.calories} kcal)`}
        onConfirm={onConfirm}           // aceptar swap
        onCancel={handleSwapClick}      // pedir otra sugerencia
      />
    );
  }

  // Mostrar todos los meal_types de la receta
  const mealTypes = meal.recipe.meal_types;
  const fats = meal.recipe.fat;

  return (
    <RecipeCard
      {...meal.recipe}
      title={meal.recipe.name}
      images={meal.recipe.image_url}
      mealType={mealTypes}
      fats={fats}
    >
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